"""
Cosmos DB Service for the insurance fraud detection system.
This service provides methods to interact with Azure Cosmos DB with proper
authentication, error handling, and health monitoring.
"""
import os
import logging
from typing import Dict, List, Any, Optional, Union
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from services.cosmos_client_factory import CosmosClientFactory
from models.claim import Claim
from models.event import Event


logger = logging.getLogger(__name__)


class CosmosDBService:
    """Service for interacting with Azure Cosmos DB with proper health monitoring"""
    
    def __init__(self, config):
        """Initialize the Cosmos DB service with configuration"""
        self.config = config
        self.client = None
        self.database = None
        self.claims_container = None
        self.events_container = None
        self._connection_healthy = False
        self._last_health_check = None
        
        # Initialize if configuration allows
        if config.USE_COSMOS:
            self.initialize()
    
    def initialize(self) -> bool:
        """
        Initialize Cosmos DB connection and containers.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing Cosmos DB service...")
            
            # Create client using factory
            self.client = CosmosClientFactory.create_client(self.config)
            
            if not self.client:
                logger.warning("No Cosmos client created, service will not be available")
                return False
            
            # Get database and containers
            self.database = self.client.get_database_client(self.config.COSMOS_DATABASE)
            self.claims_container = self.database.get_container_client(self.config.COSMOS_CLAIMS_CONTAINER)
            self.events_container = self.database.get_container_client(self.config.COSMOS_EVENTS_CONTAINER)
            
            # Perform health check
            if self._perform_health_check():
                self._connection_healthy = True
                logger.info("Cosmos DB service initialized successfully")
                return True
            else:
                logger.error("Cosmos DB health check failed during initialization")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize Cosmos DB service: {e}")
            self._connection_healthy = False
            
            if not self.config.FALLBACK_TO_LOCAL:
                raise
            
            return False
    
    def _perform_health_check(self) -> bool:
        """
        Perform health check on Cosmos DB connection.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            if not self.client or not self.database:
                return False
            
            # Test connection with lightweight operation
            is_healthy = CosmosClientFactory.test_connection(self.client, self.config.COSMOS_DATABASE)
            
            if is_healthy:
                # Test container access
                self.claims_container.read()
                self.events_container.read()
                logger.debug("Cosmos DB health check passed")
            
            return is_healthy
            
        except Exception as e:
            logger.error(f"Cosmos DB health check failed: {e}")
            return False
    
    def is_healthy(self) -> bool:
        """
        Check if Cosmos DB service is healthy.
        
        Returns:
            True if service is healthy and connected
        """
        return self._connection_healthy and self.client is not None
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get detailed health status information.
        
        Returns:
            Dictionary with health status details
        """
        return {
            'service': 'cosmos_db',
            'healthy': self.is_healthy(),
            'client_available': self.client is not None,
            'database_name': self.config.COSMOS_DATABASE,
            'endpoint': self.config.COSMOS_ENDPOINT[:50] + '...' if self.config.COSMOS_ENDPOINT else None,
            'auth_method': 'managed_identity' if self.config.USE_MANAGED_IDENTITY else 'key_based',
            'fallback_enabled': self.config.FALLBACK_TO_LOCAL
        }
    
    def is_connected(self) -> bool:
        """Check if connected to Cosmos DB (backwards compatibility)"""
        return self.is_healthy()
    
    def save_claim(self, claim: Union[Claim, Dict[str, Any]]) -> bool:
        """
        Save a claim to Cosmos DB.
        
        Args:
            claim: Claim object or dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_healthy():
            logger.warning("Cannot save claim: Cosmos DB service not healthy")
            return False
            
        try:
            # Convert to dict if it's a Claim object
            claim_data = claim.to_dict() if isinstance(claim, Claim) else claim
            
            # Ensure we have required fields
            if 'claim_id' not in claim_data:
                logger.error("Cannot save claim: missing claim_id")
                return False
            
            # Save to Cosmos DB
            self.claims_container.upsert_item(claim_data)
            logger.info(f"Claim {claim_data.get('claim_id')} saved to Cosmos DB successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving claim to Cosmos DB: {e}")
            return False
    
    def get_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a claim from Cosmos DB by ID.
        
        Args:
            claim_id: ID of the claim to retrieve
            
        Returns:
            Claim data as dictionary or None if not found
        """
        if not self.is_healthy():
            logger.warning("Cannot get claim: Cosmos DB service not healthy")
            return None
            
        try:
            # Use the claim_id as the partition key
            claim = self.claims_container.read_item(item=claim_id, partition_key=claim_id)
            logger.debug(f"Successfully retrieved claim {claim_id} from Cosmos DB")
            return claim
            
        except exceptions.CosmosResourceNotFoundError:
            logger.info(f"Claim {claim_id} not found in Cosmos DB")
            return None
        except Exception as e:
            logger.error(f"Error getting claim from Cosmos DB: {e}")
            return None
    
    def list_claims(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List claims from Cosmos DB.
        
        Args:
            limit: Maximum number of claims to return
            
        Returns:
            List of claim dictionaries
        """
        if not self.is_healthy():
            logger.warning("Cannot list claims: Cosmos DB service not healthy")
            return []
            
        try:
            # Query all claims with a limit, ordered by submission time
            query = f"SELECT * FROM c ORDER BY c.submission_time DESC OFFSET 0 LIMIT {limit}"
            items = list(self.claims_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            logger.debug(f"Successfully retrieved {len(items)} claims from Cosmos DB")
            return items
            
        except Exception as e:
            logger.error(f"Error listing claims from Cosmos DB: {e}")
            return []
    
    def delete_claim(self, claim_id: str) -> bool:
        """
        Delete a claim from Cosmos DB.
        
        Args:
            claim_id: ID of the claim to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_healthy():
            logger.warning("Cannot delete claim: Cosmos DB service not healthy")
            return False
            
        try:
            self.claims_container.delete_item(item=claim_id, partition_key=claim_id)
            logger.info(f"Claim {claim_id} deleted from Cosmos DB successfully")
            return True
            
        except exceptions.CosmosResourceNotFoundError:
            logger.info(f"Claim {claim_id} not found in Cosmos DB for deletion")
            return False
        except Exception as e:
            logger.error(f"Error deleting claim from Cosmos DB: {e}")
            return False
    
    def save_event(self, event: Union[Event, Dict[str, Any]]) -> bool:
        """
        Save an event to Cosmos DB.
        
        Args:
            event: Event object or dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_healthy():
            logger.warning("Cannot save event: Cosmos DB service not healthy")
            return False
            
        try:
            # Convert to dict if it's an Event object
            event_data = event.to_dict() if isinstance(event, Event) else event
            
            # Ensure we have required fields
            if 'event_id' not in event_data:
                logger.error("Cannot save event: missing event_id")
                return False
            
            # Save to Cosmos DB
            self.events_container.upsert_item(event_data)
            logger.info(f"Event {event_data.get('event_id')} saved to Cosmos DB successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving event to Cosmos DB: {e}")
            return False
    
    def list_events(self, entity_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List events from Cosmos DB, optionally filtered by entity_id.
        
        Args:
            entity_id: Optional entity ID to filter events
            limit: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        if not self.is_healthy():
            logger.warning("Cannot list events: Cosmos DB service not healthy")
            return []
            
        try:
            # Query events with optional entity_id filter
            if entity_id:
                query = f"SELECT * FROM c WHERE c.entity_id = '{entity_id}' ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}"
            else:
                query = f"SELECT * FROM c ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}"
                
            items = list(self.events_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            logger.debug(f"Successfully retrieved {len(items)} events from Cosmos DB")
            return items
            
        except Exception as e:
            logger.error(f"Error listing events from Cosmos DB: {e}")
            return []
