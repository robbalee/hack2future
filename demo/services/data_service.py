"""
Local data service for the insurance fraud detection system.
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging

from models import Claim, Event
from utils import validate_claim, ValidationError, Config

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LocalDataService:
    """Service for managing local data storage"""
    
    def __init__(self):
        """Initialize the data service"""
        self.config = Config()
        self.claims_dir = self.config.get('storage.claims_dir', 'claims_data')
        self.events_dir = self.config.get('storage.events_dir', 'events_data')
        self.backup_dir = self.config.get('storage.backup_dir', 'backups')
        
        # Ensure directories exist
        for directory in [self.claims_dir, self.events_dir, self.backup_dir]:
            os.makedirs(directory, exist_ok=True)
        
        logger.info(f"LocalDataService initialized with claims directory: {self.claims_dir}")
    
    def save_claim(self, claim: Union[Claim, Dict[str, Any]]) -> str:
        """
        Save a claim to the local storage
        
        Args:
            claim: The claim object or dictionary to save
            
        Returns:
            str: The claim ID
            
        Raises:
            ValidationError: If the claim data is invalid
        """
        try:
            # Convert to Claim object if it's a dictionary
            if isinstance(claim, dict):
                # Validate the claim data
                validate_claim(claim)
                claim_obj = Claim.from_dict(claim)
            else:
                claim_obj = claim
            
            # Set updated time
            claim_obj.updated_time = datetime.now().isoformat()
            
            # Convert to dictionary for storage
            claim_data = claim_obj.to_dict()
            
            # Create backup if file exists
            claim_file_path = os.path.join(self.claims_dir, f"{claim_obj.claim_id}.json")
            if os.path.exists(claim_file_path):
                self._backup_file(claim_file_path)
            
            # Save to file atomically
            temp_file_path = f"{claim_file_path}.tmp"
            with open(temp_file_path, 'w') as f:
                json.dump(claim_data, f, indent=2)
            
            # Atomically replace the file
            os.replace(temp_file_path, claim_file_path)
            
            # Log event
            self.save_event(Event(
                event_type="claim_saved",
                entity_id=claim_obj.claim_id,
                data={"action": "save"}
            ))
            
            logger.info(f"Claim {claim_obj.claim_id} saved successfully")
            return claim_obj.claim_id
            
        except ValidationError as e:
            logger.error(f"Validation error saving claim: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error saving claim: {str(e)}")
            raise RuntimeError(f"Failed to save claim: {str(e)}")
    
    def get_claim(self, claim_id: str) -> Optional[Claim]:
        """
        Retrieve a claim by ID
        
        Args:
            claim_id: The ID of the claim to retrieve
            
        Returns:
            Optional[Claim]: The claim object if found, None otherwise
        """
        try:
            claim_file_path = os.path.join(self.claims_dir, f"{claim_id}.json")
            if not os.path.exists(claim_file_path):
                logger.warning(f"Claim {claim_id} not found")
                return None
            
            with open(claim_file_path, 'r') as f:
                claim_data = json.load(f)
            
            # Log event
            self.save_event(Event(
                event_type="claim_accessed",
                entity_id=claim_id,
                data={"action": "get"}
            ))
            
            logger.info(f"Claim {claim_id} retrieved successfully")
            return Claim.from_dict(claim_data)
            
        except Exception as e:
            logger.error(f"Error retrieving claim {claim_id}: {str(e)}")
            return None
    
    def list_claims(self, limit: int = 100, offset: int = 0) -> List[Claim]:
        """
        List all claims, paginated
        
        Args:
            limit: Maximum number of claims to return
            offset: Number of claims to skip
            
        Returns:
            List[Claim]: List of claim objects
        """
        try:
            claims = []
            
            # Get all claim files
            claim_files = [f for f in os.listdir(self.claims_dir) 
                         if f.endswith('.json') and not f.startswith('.')]
            
            # Sort by modification time (newest first)
            claim_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.claims_dir, x)), 
                           reverse=True)
            
            # Apply pagination
            paginated_files = claim_files[offset:offset+limit]
            
            for file_name in paginated_files:
                try:
                    with open(os.path.join(self.claims_dir, file_name), 'r') as f:
                        claim_data = json.load(f)
                        claims.append(Claim.from_dict(claim_data))
                except Exception as e:
                    logger.error(f"Error loading claim from {file_name}: {str(e)}")
            
            logger.info(f"Retrieved {len(claims)} claims")
            return claims
            
        except Exception as e:
            logger.error(f"Error listing claims: {str(e)}")
            return []
    
    def update_claim(self, claim_id: str, updates: Dict[str, Any]) -> Optional[Claim]:
        """
        Update a claim with new data
        
        Args:
            claim_id: The ID of the claim to update
            updates: Dictionary of fields to update
            
        Returns:
            Optional[Claim]: The updated claim if successful, None otherwise
        """
        try:
            claim = self.get_claim(claim_id)
            if not claim:
                logger.warning(f"Claim {claim_id} not found for update")
                return None
            
            # Update the claim object
            claim_dict = claim.to_dict()
            claim_dict.update(updates)
            claim_dict['updated_time'] = datetime.now().isoformat()
            
            # Save the updated claim
            updated_claim = Claim.from_dict(claim_dict)
            self.save_claim(updated_claim)
            
            # Log event
            self.save_event(Event(
                event_type="claim_updated",
                entity_id=claim_id,
                data={"fields_updated": list(updates.keys())}
            ))
            
            logger.info(f"Claim {claim_id} updated successfully")
            return updated_claim
            
        except Exception as e:
            logger.error(f"Error updating claim {claim_id}: {str(e)}")
            return None
    
    def delete_claim(self, claim_id: str) -> bool:
        """
        Delete a claim
        
        Args:
            claim_id: The ID of the claim to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            claim_file_path = os.path.join(self.claims_dir, f"{claim_id}.json")
            if not os.path.exists(claim_file_path):
                logger.warning(f"Claim {claim_id} not found for deletion")
                return False
            
            # Backup before deletion
            self._backup_file(claim_file_path)
            
            # Delete the file
            os.remove(claim_file_path)
            
            # Log event
            self.save_event(Event(
                event_type="claim_deleted",
                entity_id=claim_id,
                data={"action": "delete"}
            ))
            
            logger.info(f"Claim {claim_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting claim {claim_id}: {str(e)}")
            return False
    
    def save_event(self, event: Union[Event, Dict[str, Any]]) -> str:
        """
        Save an event to the local storage
        
        Args:
            event: The event object or dictionary to save
            
        Returns:
            str: The event ID
        """
        try:
            # Convert to Event object if it's a dictionary
            if isinstance(event, dict):
                event_obj = Event.from_dict(event)
            else:
                event_obj = event
            
            # Convert to dictionary for storage
            event_data = event_obj.to_dict()
            
            # Save to file
            event_file_path = os.path.join(self.events_dir, f"{event_obj.event_id}.json")
            with open(event_file_path, 'w') as f:
                json.dump(event_data, f, indent=2)
            
            return event_obj.event_id
            
        except Exception as e:
            logger.error(f"Error saving event: {str(e)}")
            # Don't raise here, events are secondary
            return ""
    
    def _backup_file(self, file_path: str) -> None:
        """Create a backup of a file"""
        try:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"{filename}_{timestamp}.bak"
                backup_path = os.path.join(self.backup_dir, backup_filename)
                shutil.copy2(file_path, backup_path)
                logger.info(f"Created backup of {file_path} at {backup_path}")
        except Exception as e:
            logger.error(f"Error creating backup of {file_path}: {str(e)}")
    
    def list_events(self, entity_id: Optional[str] = None, limit: int = 100) -> List[Event]:
        """
        List events, optionally filtered by entity_id
        
        Args:
            entity_id: Optional entity ID to filter events by
            limit: Maximum number of events to return
            
        Returns:
            List[Event]: List of event objects
        """
        try:
            events = []
            
            # Get all event files
            event_files = [f for f in os.listdir(self.events_dir) 
                         if f.endswith('.json') and not f.startswith('.')]
            
            # Sort by modification time (newest first)
            event_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.events_dir, x)), 
                           reverse=True)
            
            count = 0
            for file_name in event_files:
                if count >= limit:
                    break
                    
                try:
                    with open(os.path.join(self.events_dir, file_name), 'r') as f:
                        event_data = json.load(f)
                        
                        # Filter by entity_id if provided
                        if entity_id is None or event_data.get('entity_id') == entity_id:
                            events.append(Event.from_dict(event_data))
                            count += 1
                            
                except Exception as e:
                    logger.error(f"Error loading event from {file_name}: {str(e)}")
            
            logger.info(f"Retrieved {len(events)} events")
            return events
            
        except Exception as e:
            logger.error(f"Error listing events: {str(e)}")
            return []
