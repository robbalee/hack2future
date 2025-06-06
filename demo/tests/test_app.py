"""
Flask application tests using pytest.
"""
import pytest
import json
from unittest.mock import patch, MagicMock


class TestFlaskApp:
    """Test cases for the Flask application endpoints"""
    
    def test_index_page(self, client):
        """Test the main index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Insurance Claims' in response.data or b'Fraud Detection' in response.data
    
    def test_list_claims_empty(self, client):
        """Test listing claims when no claims exist"""
        with patch.object(client.application.data_service, 'list_claims') as mock_list_claims:
            mock_list_claims.return_value = []
            
            response = client.get('/list_claims')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['claims'] == []
    
    def test_list_claims_with_data(self, client, sample_claim_data):
        """Test listing claims when claims exist"""
        with patch.object(client.application.data_service, 'list_claims') as mock_list_claims:
            mock_list_claims.return_value = [sample_claim_data]
            
            response = client.get('/list_claims')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['success'] is True
            assert len(data['claims']) == 1
            assert data['claims'][0]['claim_id'] == sample_claim_data['claim_id']
    
    def test_submit_claim_success(self, client, sample_claim_data):
        """Test successful claim submission"""
        with patch.object(client.application.data_service, 'save_claim') as mock_save_claim:
            mock_save_claim.return_value = sample_claim_data['claim_id']
            
            form_data = {
                'claimAmount': str(sample_claim_data['claim_amount']),
                'description': sample_claim_data['description']
            }
            
            response = client.post('/submit_claim', data=form_data)
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'claim_id' in data
    
    def test_submit_claim_missing_data(self, client):
        """Test claim submission with missing required data"""
        response = client.post('/submit_claim', data={})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_get_claim_exists(self, client, sample_claim_data):
        """Test retrieving an existing claim"""
        with patch.object(client.application.data_service, 'get_claim') as mock_get_claim:
            mock_get_claim.return_value = sample_claim_data
            
            claim_id = sample_claim_data['claim_id']
            response = client.get(f'/get_claim/{claim_id}')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['claim']['claim_id'] == claim_id
    
    def test_get_claim_not_found(self, client):
        """Test retrieving a non-existent claim"""
        with patch.object(client.application.data_service, 'get_claim') as mock_get_claim:
            mock_get_claim.return_value = None
            
            response = client.get('/get_claim/nonexistent-id')
            assert response.status_code == 404
            
            data = json.loads(response.data)
            assert data['success'] is False
            assert data['error'] == 'Claim not found'
    
    def test_update_claim_success(self, client, sample_claim_data):
        """Test successful claim update"""
        with patch.object(client.application.data_service, 'update_claim') as mock_update_claim:
            mock_update_claim.return_value = sample_claim_data
            
            update_data = {
                'status': 'reviewed',
                'fraud_score': 0.25
            }
            
            claim_id = sample_claim_data['claim_id']
            response = client.post(f'/update_claim/{claim_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_update_claim_not_found(self, client):
        """Test updating a non-existent claim"""
        with patch.object(client.application.data_service, 'update_claim') as mock_update_claim:
            mock_update_claim.return_value = None
            
            update_data = {'status': 'reviewed'}
            
            response = client.post('/update_claim/nonexistent-id',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
            assert response.status_code == 404
            
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'Claim not found' in data['error']


class TestFlaskAppIntegration:
    """Integration tests for Flask app (marked as integration tests)"""
    
    @pytest.mark.integration
    def test_submit_and_retrieve_claim_flow(self, client):
        """Test the full flow of submitting and retrieving a claim"""
        # Submit a claim
        form_data = {
            'claimAmount': '1500.00',
            'description': 'Integration test claim'
        }
        
        response = client.post('/submit_claim', data=form_data)
        assert response.status_code == 200
        
        submit_data = json.loads(response.data)
        assert submit_data['success'] is True
        claim_id = submit_data['claim_id']
        
        # Retrieve the claim
        response = client.get(f'/get_claim/{claim_id}')
        assert response.status_code == 200
        
        get_data = json.loads(response.data)
        assert get_data['success'] is True
        assert get_data['claim']['claim_id'] == claim_id
        assert float(get_data['claim']['claim_amount']) == 1500.00
