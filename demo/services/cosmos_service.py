"""
Cosmos DB Service for the insurance fraud detection system.
This service provides methods to interact with Azure Cosmos DB.
"""
import os
from typing import Dict, List, Any, Optional, Union
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from utils.config import Config
from models.claim import Claim
from models.event import Event


class CosmosDBService:
    """Service for interacting with Azure Cosmos DB"""
    
    def __init__(self):
        """Initialize the Cosmos DB service"""
        config = Config()
        self.endpoint = config.get('database.cosmos_endpoint', os.environ.get('COSMOS_ENDPOINT', ''))
        self.key = config.get('database.cosmos_key', os.environ.get('COSMOS_KEY', ''))
        self.database_name = config.get('database.cosmos_database', 'insurance-claims-db')
        self.claims_container_name = config.get('database.cosmos_claims_container', 'claims')
        self.events_container_name = config.get('database.cosmos_events_container', 'events')
        
        # Check if we have the necessary configuration
        if not self.endpoint or not self.key:
            self.client = None
            self.database = None
            self.claims_container = None
            self.events_container = None
            print("Cosmos DB connection not configured. Missing endpoint or key.")
            return
            
        try:
            # Initialize the Cosmos client
            print(f"Connecting to Cosmos DB at {self.endpoint[:30]}...")
            self.client = CosmosClient(self.endpoint, self.key)
            
            # Get database
            self.database = self.client.get_database_client(self.database_name)
            
            # Get containers
            self.claims_container = self.database.get_container_client(self.claims_container_name)
            self.events_container = self.database.get_container_client(self.events_container_name)
            
            # Verify connection with a simple operation
            database_properties = self.database.read()
            print(f"Connected to Cosmos DB: {self.database_name} (RU/s: {database_properties.get('offer_throughput', 'autoscale')})")
        except exceptions.CosmosResourceNotFoundError as e:
            print(f"Cosmos DB resource not found: {str(e)}")
            self.client = None
            self.database = None
            self.claims_container = None
            self.events_container = None
        except Exception as e:
            print(f"Error connecting to Cosmos DB: {str(e)}")
            self.client = None
            self.database = None
            self.claims_container = None
            self.events_container = None
    
    def is_connected(self) -> bool:
        """Check if connected to Cosmos DB"""
        return self.client is not None and self.claims_container is not None
    
    def save_claim(self, claim: Union[Claim, Dict[str, Any]]) -> bool:
        """Save a claim to Cosmos DB"""
        if not self.is_connected():
            return False
            
        try:
            # Convert to dict if it's a Claim object
            claim_data = claim.to_dict() if isinstance(claim, Claim) else claim
            
            # Save to Cosmos DB
            self.claims_container.upsert_item(claim_data)
            print(f"Claim {claim_data.get('claim_id')} saved to Cosmos DB")
            return True
        except Exception as e:
            print(f"Error saving claim to Cosmos DB: {str(e)}")
            return False
    
    def get_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Get a claim from Cosmos DB by ID"""
        if not self.is_connected():
            return None
            
        try:
            # Use the claim_id as the partition key
            claim = self.claims_container.read_item(item=claim_id, partition_key=claim_id)
            return claim
        except exceptions.CosmosResourceNotFoundError:
            print(f"Claim {claim_id} not found in Cosmos DB")
            return None
        except Exception as e:
            print(f"Error getting claim from Cosmos DB: {str(e)}")
            return None
    
    def list_claims(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List claims from Cosmos DB"""
        if not self.is_connected():
            return []
            
        try:
            # Query all claims with a limit
            query = f"SELECT * FROM c ORDER BY c.submission_time DESC OFFSET 0 LIMIT {limit}"
            items = list(self.claims_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return items
        except Exception as e:
            print(f"Error listing claims from Cosmos DB: {str(e)}")
            return []
    
    def delete_claim(self, claim_id: str) -> bool:
        """Delete a claim from Cosmos DB"""
        if not self.is_connected():
            return False
            
        try:
            self.claims_container.delete_item(item=claim_id, partition_key=claim_id)
            print(f"Claim {claim_id} deleted from Cosmos DB")
            return True
        except exceptions.CosmosResourceNotFoundError:
            print(f"Claim {claim_id} not found in Cosmos DB")
            return False
        except Exception as e:
            print(f"Error deleting claim from Cosmos DB: {str(e)}")
            return False
    
    def save_event(self, event: Union[Event, Dict[str, Any]]) -> bool:
        """Save an event to Cosmos DB"""
        if not self.is_connected():
            return False
            
        try:
            # Convert to dict if it's an Event object
            event_data = event.to_dict() if isinstance(event, Event) else event
            
            # Save to Cosmos DB
            self.events_container.upsert_item(event_data)
            print(f"Event {event_data.get('event_id')} saved to Cosmos DB")
            return True
        except Exception as e:
            print(f"Error saving event to Cosmos DB: {str(e)}")
            return False
    
    def list_events(self, entity_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List events from Cosmos DB, optionally filtered by entity_id"""
        if not self.is_connected():
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
            return items
        except Exception as e:
            print(f"Error listing events from Cosmos DB: {str(e)}")
            return []
