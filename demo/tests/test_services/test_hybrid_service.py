"""
Tests for the HybridDataService integration.
"""
import pytest
import uuid
from datetime import datetime
from unittest.mock import patch, MagicMock

from services.hybrid_service import HybridDataService
from models.claim import Claim
from models.event import Event


class TestHybridDataService:
    """Test cases for HybridDataService"""
    
    def test_initialization_with_cosmos(self):
        """Test service initialization when Cosmos DB is available"""
        mock_env = {
            'COSMOS_ENDPOINT': 'https://test.documents.azure.com:443/',
            'COSMOS_KEY': 'test-key'
        }
        
        with patch.dict('os.environ', mock_env):
            with patch('services.hybrid_service.CosmosDBService') as mock_cosmos:
                mock_cosmos.return_value.is_connected.return_value = True
                
                service = HybridDataService()
                assert service.use_cosmos is True
                assert service.local_service is not None
                assert service.cosmos_service is not None
    
    def test_save_claim_local_only(self, sample_claim_data):
        """Test saving claim with local storage only"""
        with patch('services.hybrid_service.LocalDataService') as mock_local:
            mock_local.return_value.save_claim.return_value = sample_claim_data['claim_id']
            
            service = HybridDataService()
            service.use_cosmos = False
            service.cosmos_service = None
            
            result = service.save_claim(sample_claim_data)
            assert result == sample_claim_data['claim_id']
            mock_local.return_value.save_claim.assert_called_once()
    
    def test_save_claim_hybrid_success(self, sample_claim_data):
        """Test saving claim to both local and Cosmos DB successfully"""
        with patch('services.hybrid_service.LocalDataService') as mock_local, \
             patch('services.hybrid_service.CosmosDBService') as mock_cosmos:
            
            mock_local.return_value.save_claim.return_value = sample_claim_data['claim_id']
            mock_cosmos.return_value.save_claim.return_value = sample_claim_data['claim_id']
            mock_cosmos.return_value.test_connection.return_value = True
            
            service = HybridDataService()
            service.use_cosmos = True
            service.cosmos_service = mock_cosmos.return_value
            
            result = service.save_claim(sample_claim_data)
            assert result == sample_claim_data['claim_id']
            mock_local.return_value.save_claim.assert_called_once()
            mock_cosmos.return_value.save_claim.assert_called_once()
    
    def test_save_claim_cosmos_fallback(self, sample_claim_data):
        """Test fallback to local when Cosmos DB fails"""
        with patch('services.hybrid_service.LocalDataService') as mock_local, \
             patch('services.hybrid_service.CosmosDBService') as mock_cosmos:
            
            mock_local.return_value.save_claim.return_value = sample_claim_data['claim_id']
            mock_cosmos.return_value.save_claim.side_effect = Exception("Cosmos DB error")
            mock_cosmos.return_value.is_connected.return_value = True
            
            service = HybridDataService()
            service.use_cosmos = True
            service.cosmos_service = mock_cosmos.return_value
            
            result = service.save_claim(sample_claim_data)
            assert result == sample_claim_data['claim_id']
            mock_local.return_value.save_claim.assert_called_once()
            mock_cosmos.return_value.save_claim.assert_called_once()
    
    def test_get_claim_local_only(self, sample_claim_data):
        """Test retrieving claim from local storage only"""
        with patch('services.hybrid_service.LocalDataService') as mock_local:
            mock_local.return_value.get_claim.return_value = sample_claim_data
            
            service = HybridDataService()
            service.use_cosmos = False
            service.cosmos_service = None
            
            result = service.get_claim(sample_claim_data['claim_id'])
            assert result == sample_claim_data
            mock_local.return_value.get_claim.assert_called_once()
    
    def test_get_claim_cosmos_primary(self, sample_claim_data):
        """Test retrieving claim from Cosmos DB as primary source"""
        with patch('services.hybrid_service.LocalDataService') as mock_local, \
             patch('services.hybrid_service.CosmosDBService') as mock_cosmos:
            
            mock_cosmos.return_value.get_claim.return_value = sample_claim_data
            mock_cosmos.return_value.test_connection.return_value = True
            
            service = HybridDataService()
            service.use_cosmos = True
            service.cosmos_service = mock_cosmos.return_value
            
            result = service.get_claim(sample_claim_data['claim_id'])
            assert result == sample_claim_data
            mock_cosmos.return_value.get_claim.assert_called_once()
            # Local should not be called if Cosmos succeeds
            mock_local.return_value.get_claim.assert_not_called()
    
    def test_list_claims_hybrid(self, sample_claim_data):
        """Test listing claims from both sources"""
        claims_list = [sample_claim_data]
        
        with patch('services.hybrid_service.LocalDataService') as mock_local, \
             patch('services.hybrid_service.CosmosDBService') as mock_cosmos:
            
            mock_local.return_value.list_claims.return_value = claims_list
            mock_cosmos.return_value.list_claims.return_value = claims_list
            mock_cosmos.return_value.test_connection.return_value = True
            
            service = HybridDataService()
            service.use_cosmos = True
            service.cosmos_service = mock_cosmos.return_value
            
            result = service.list_claims()
            assert len(result) == 1
            assert result[0] == sample_claim_data


@pytest.mark.integration
class TestHybridDataServiceIntegration:
    """Integration tests for HybridDataService (require actual services)"""
    
    def test_real_hybrid_service_creation(self):
        """Test creating a real HybridDataService instance"""
        service = HybridDataService()
        assert service.local_service is not None
        # Cosmos service may or may not be available depending on environment
        
    @pytest.mark.cosmos
    def test_cosmos_connection_if_available(self):
        """Test Cosmos DB connection if credentials are available"""
        import os
        
        # Only run if Cosmos DB credentials are available
        if not (os.getenv('COSMOS_ENDPOINT') and os.getenv('COSMOS_KEY')):
            pytest.skip("Cosmos DB credentials not available")
        
        service = HybridDataService()
        # This test verifies the service can be created with real credentials
        # The actual connection test is done during initialization
        
    def test_save_and_retrieve_claim_flow(self, sample_claim_data):
        """Test the complete save and retrieve flow"""
        service = HybridDataService()
        
        # Save a claim
        claim_id = service.save_claim(sample_claim_data)
        assert claim_id == sample_claim_data['claim_id']
        
        # Retrieve the claim
        retrieved_claim = service.get_claim(claim_id)
        assert retrieved_claim is not None
        
        # Verify claim data (handle both dict and object returns)
        if isinstance(retrieved_claim, dict):
            assert retrieved_claim['claim_id'] == claim_id
            assert retrieved_claim['claim_amount'] == sample_claim_data['claim_amount']
        else:
            assert retrieved_claim.claim_id == claim_id
            assert retrieved_claim.claim_amount == sample_claim_data['claim_amount']
    
    def test_save_and_list_events_flow(self, sample_event_data):
        """Test the complete event save and list flow"""
        service = HybridDataService()
        
        # Save an event
        event_id = service.save_event(sample_event_data)
        assert event_id == sample_event_data['event_id']
        
        # List events for the entity
        events = service.list_events(sample_event_data['entity_id'])
        assert len(events) >= 1
        
        # Find our event in the list
        found_event = None
        for event in events:
            event_id_field = event.get('event_id') if isinstance(event, dict) else getattr(event, 'event_id', None)
            if event_id_field == sample_event_data['event_id']:
                found_event = event
                break
        
        assert found_event is not None
