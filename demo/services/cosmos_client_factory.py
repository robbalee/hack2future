"""
Cosmos DB Client Factory with proper authentication strategies.
Handles both key-based authentication (development) and managed identity (production).
"""
import logging
from typing import Optional
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.core.exceptions import ClientAuthenticationError


logger = logging.getLogger(__name__)


class CosmosClientFactory:
    """Factory for creating properly authenticated Cosmos DB clients"""
    
    @staticmethod
    def create_client(config) -> Optional[CosmosClient]:
        """
        Create a Cosmos DB client with appropriate authentication strategy.
        
        Args:
            config: Configuration object with Cosmos DB settings
            
        Returns:
            CosmosClient instance or None if configuration is invalid
            
        Raises:
            ValueError: If required configuration is missing
            ClientAuthenticationError: If authentication fails
        """
        if not config.COSMOS_ENDPOINT:
            if config.FALLBACK_TO_LOCAL:
                logger.warning("No Cosmos endpoint configured, will use local storage only")
                return None
            else:
                raise ValueError("COSMOS_ENDPOINT is required but not configured")
        
        try:
            if config.USE_MANAGED_IDENTITY:
                return CosmosClientFactory._create_managed_identity_client(config)
            else:
                return CosmosClientFactory._create_key_based_client(config)
                
        except Exception as e:
            logger.error(f"Failed to create Cosmos client: {e}")
            if config.FALLBACK_TO_LOCAL:
                logger.warning("Falling back to local storage due to Cosmos client creation failure")
                return None
            raise
    
    @staticmethod
    def _create_managed_identity_client(config) -> CosmosClient:
        """Create client using Azure Managed Identity"""
        logger.info("Creating Cosmos client with Managed Identity authentication")
        
        # Use DefaultAzureCredential which tries multiple auth methods
        credential = DefaultAzureCredential()
        
        try:
            client = CosmosClient(
                url=config.COSMOS_ENDPOINT,
                credential=credential,
                consistency_level='Session'  # Good balance of performance and consistency
            )
            
            logger.info("Successfully created Cosmos client with Managed Identity")
            return client
            
        except ClientAuthenticationError as e:
            logger.error(f"Managed Identity authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create Cosmos client with Managed Identity: {e}")
            raise
    
    @staticmethod
    def _create_key_based_client(config) -> CosmosClient:
        """Create client using access key authentication"""
        if not config.COSMOS_KEY:
            raise ValueError("COSMOS_KEY is required for key-based authentication")
        
        logger.info("Creating Cosmos client with key-based authentication")
        
        try:
            client = CosmosClient(
                url=config.COSMOS_ENDPOINT,
                credential=config.COSMOS_KEY,
                consistency_level='Session'
            )
            
            logger.info("Successfully created Cosmos client with key-based authentication")
            return client
            
        except ClientAuthenticationError as e:
            logger.error(f"Key-based authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create Cosmos client with key authentication: {e}")
            raise
    
    @staticmethod
    def test_connection(client: CosmosClient, database_name: str) -> bool:
        """
        Test Cosmos DB connection with lightweight operation.
        
        Args:
            client: CosmosClient instance
            database_name: Name of the database to test
            
        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            if not client:
                return False
                
            # Try to read database properties (lightweight operation)
            database = client.get_database_client(database_name)
            database.read()
            
            logger.info(f"Cosmos DB connection test successful for database: {database_name}")
            return True
            
        except Exception as e:
            logger.error(f"Cosmos DB connection test failed: {e}")
            return False
