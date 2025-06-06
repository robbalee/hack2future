"""
Hybrid Data Service for the insurance fraud detection system.
This service provides a unified interface for both local and cloud storage.
"""
from typing import Dict, List, Any, Optional, Union
import os
from models.claim import Claim
from models.event import Event
from .data_service import LocalDataService
from .cosmos_service import CosmosDBService


class HybridDataService:
    """Service that combines local and cloud storage for data persistence"""
    
    def __init__(self):
        """Initialize the hybrid data service"""
        self.local_service = LocalDataService()
        
        # Only create Cosmos service if properly configured
        self.cosmos_service = CosmosDBService()
        if self.cosmos_service.is_connected():
            self.use_cosmos = True
        else:
            self.use_cosmos = False
            self.cosmos_service = None
        
        print(f"Hybrid Data Service initialized. Using Cosmos DB: {self.use_cosmos}")
    
    def save_claim(self, claim: Union[Claim, Dict[str, Any]]) -> str:
        """Save a claim to both local and cloud storage"""
        # Always save locally first
        if isinstance(claim, Dict):
            claim_obj = Claim.from_dict(claim)
            claim_id = self.local_service.save_claim(claim_obj)
        else:
            claim_id = self.local_service.save_claim(claim)
        
        # Try to save to Cosmos DB if available
        if self.use_cosmos and self.cosmos_service:
            try:
                if isinstance(claim, Claim):
                    claim_dict = claim.to_dict()
                else:
                    claim_dict = claim
                
                cosmos_success = self.cosmos_service.save_claim(claim_dict)
                
                if cosmos_success:
                    print(f"Claim {claim_id} saved to both local and cloud storage")
                else:
                    print(f"Claim {claim_id} saved locally only (cloud failed)")
            except Exception as e:
                print(f"Claim {claim_id} saved locally only (cloud error: {str(e)})")
        
        return claim_id
    
    def get_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Get a claim, trying cloud first then local fallback"""
        if self.use_cosmos and self.cosmos_service:
            # Try to get from Cosmos DB first
            claim = self.cosmos_service.get_claim(claim_id)
            if claim:
                return claim
        
        # Fallback to local
        claim = self.local_service.get_claim(claim_id)
        if claim:
            return claim.to_dict() if isinstance(claim, Claim) else claim
            
        return None
    
    def list_claims(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List claims from primary storage"""
        if self.use_cosmos and self.cosmos_service:
            # Try to list from Cosmos DB first
            claims = self.cosmos_service.list_claims(limit)
            if claims:
                return claims
        
        # Fallback to local
        claims = self.local_service.list_claims()
        return [claim.to_dict() if isinstance(claim, Claim) else claim for claim in claims]
    
    def delete_claim(self, claim_id: str) -> bool:
        """Delete a claim from both storages"""
        local_success = self.local_service.delete_claim(claim_id)
        
        if self.use_cosmos and self.cosmos_service:
            cosmos_success = self.cosmos_service.delete_claim(claim_id)
            return local_success and cosmos_success
        
        return local_success
    
    def update_claim(self, claim_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing claim in both storages"""
        # First get the existing claim
        existing_claim = self.get_claim(claim_id)
        if not existing_claim:
            return None
        
        # Merge the update data with existing claim
        updated_claim_data = existing_claim.copy()
        updated_claim_data.update(update_data)
        
        try:
            # Create a Claim object to validate the updated data
            updated_claim = Claim.from_dict(updated_claim_data)
            
            # Save the updated claim using existing save_claim method
            saved_claim_id = self.save_claim(updated_claim)
            
            # Return the updated claim data
            return updated_claim.to_dict()
            
        except Exception as e:
            print(f"Failed to update claim {claim_id}: {str(e)}")
            return None
    
    def save_event(self, event: Union[Event, Dict[str, Any]]) -> str:
        """Save an event to both local and cloud storage"""
        # Always save locally first
        if isinstance(event, Dict):
            event_obj = Event.from_dict(event)
            event_id = self.local_service.save_event(event_obj)
        else:
            event_id = self.local_service.save_event(event)
        
        # Try to save to Cosmos DB if available
        if self.use_cosmos and self.cosmos_service:
            try:
                if isinstance(event, Event):
                    event_dict = event.to_dict()
                else:
                    event_dict = event
                    
                cosmos_success = self.cosmos_service.save_event(event_dict)
                
                if cosmos_success:
                    print(f"Event {event_id} saved to both local and cloud storage")
                else:
                    print(f"Event {event_id} saved locally only (cloud failed)")
            except Exception as e:
                print(f"Event {event_id} saved locally only (cloud error: {str(e)})")
        
        return event_id
    
    def list_events(self, entity_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List events, optionally filtered by entity_id"""
        if self.use_cosmos and self.cosmos_service:
            # Try to list from Cosmos DB first
            events = self.cosmos_service.list_events(entity_id, limit)
            if events:
                return events
        
        # Fallback to local
        events = self.local_service.list_events(entity_id)
        return [event.to_dict() if isinstance(event, Event) else event for event in events]
