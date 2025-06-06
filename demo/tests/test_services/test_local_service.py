"""
Tests for the LocalDataService.
"""
import pytest
import os
import tempfile
import json
import shutil
from unittest.mock import patch, MagicMock
from services.data_service import LocalDataService


class TestLocalDataService:
    """Test cases for LocalDataService"""
    
    def test_service_initialization(self):
        """Test service initialization"""
        service = LocalDataService()
        
        assert hasattr(service, 'claims_dir')
        assert hasattr(service, 'events_dir')
        
        # Directories should exist after initialization
        assert os.path.exists(service.claims_dir)
        assert os.path.exists(service.events_dir)
    
    def test_save_and_get_claim(self, sample_claim_data):
        """Test saving and retrieving a claim"""
        service = LocalDataService()
        
        # Save claim
        saved_id = service.save_claim(sample_claim_data)
        assert saved_id == sample_claim_data['claim_id']
        
        # Verify file exists
        claim_file = os.path.join(service.claims_dir, f"{sample_claim_data['claim_id']}.json")
        assert os.path.exists(claim_file)
        
        # Retrieve claim
        retrieved_claim = service.get_claim(sample_claim_data['claim_id'])
        assert retrieved_claim is not None
        assert retrieved_claim.claim_id == sample_claim_data['claim_id']
        assert retrieved_claim.claim_amount == sample_claim_data['claim_amount']
        
        # Cleanup
        try:
            os.remove(claim_file)
        except FileNotFoundError:
            pass
    
    def test_get_nonexistent_claim(self):
        """Test retrieving a claim that doesn't exist"""
        service = LocalDataService()
        
        retrieved_claim = service.get_claim('nonexistent-id')
        assert retrieved_claim is None
    
    def test_list_claims_empty_vs_with_data(self, sample_claim_data):
        """Test listing claims when empty and with data"""
        service = LocalDataService()
        
        # Get initial count
        initial_claims = service.list_claims()
        initial_count = len(initial_claims)
        
        # Save a claim
        service.save_claim(sample_claim_data)
        
        # List claims
        claims = service.list_claims()
        assert len(claims) == initial_count + 1
         # Find our claim
        found_claim = None
        for claim in claims:
            if claim.claim_id == sample_claim_data['claim_id']:
                found_claim = claim
                break

        assert found_claim is not None
        assert found_claim.claim_id == sample_claim_data['claim_id']
        
        # Cleanup
        try:
            claim_file = os.path.join(service.claims_dir, f"{sample_claim_data['claim_id']}.json")
            os.remove(claim_file)
        except FileNotFoundError:
            pass
    
    def test_save_and_list_events(self, sample_event_data):
        """Test saving and listing events"""
        service = LocalDataService()
        
        # Save event
        saved_id = service.save_event(sample_event_data)
        assert saved_id == sample_event_data['event_id']
        
        # Verify file exists
        event_file = os.path.join(service.events_dir, f"{sample_event_data['event_id']}.json")
        assert os.path.exists(event_file)
        
        # List events for entity
        events = service.list_events(sample_event_data['entity_id'])
         # Find our event
        found_event = None
        for event in events:
            if event.event_id == sample_event_data['event_id']:
                found_event = event
                break

        assert found_event is not None
        assert found_event.event_id == sample_event_data['event_id']
        assert found_event.entity_id == sample_event_data['entity_id']
        
        # Cleanup
        try:
            os.remove(event_file)
        except FileNotFoundError:
            pass
    
    def test_list_events_empty(self):
        """Test listing events when no events exist for entity"""
        service = LocalDataService()
        
        events = service.list_events('nonexistent-entity')
        # Should return empty list, not error
        assert isinstance(events, list)
    
    def test_multiple_events_same_entity(self, sample_event_data):
        """Test multiple events for the same entity"""
        service = LocalDataService()
        
        # Create multiple events for the same entity
        entity_id = sample_event_data['entity_id']
        
        event1 = sample_event_data.copy()
        event1['event_id'] = 'test-event-1'
        event1['event_type'] = 'submitted'
        
        event2 = sample_event_data.copy()
        event2['event_id'] = 'test-event-2'
        event2['event_type'] = 'reviewed'
        
        # Save both events
        service.save_event(event1)
        service.save_event(event2)
        
        # List events for the entity
        events = service.list_events(entity_id)
        
        # Find our events
        our_events = [e for e in events if e.event_id in ['test-event-1', 'test-event-2']]
        assert len(our_events) >= 2
        
        # Cleanup
        try:
            event1_file = os.path.join(service.events_dir, f"{event1['event_id']}.json")
            event2_file = os.path.join(service.events_dir, f"{event2['event_id']}.json")
            os.remove(event1_file)
            os.remove(event2_file)
        except FileNotFoundError:
            pass
    
    def test_update_existing_claim(self, sample_claim_data):
        """Test updating an existing claim"""
        service = LocalDataService()
        
        # Save initial claim
        service.save_claim(sample_claim_data)
        
        # Update the claim
        updated_claim = sample_claim_data.copy()
        updated_claim['status'] = 'reviewed'
        updated_claim['fraud_score'] = 0.25
        
        # Save updated claim
        saved_id = service.save_claim(updated_claim)
        assert saved_id == sample_claim_data['claim_id']
        
        # Retrieve and verify update
        retrieved_claim = service.get_claim(sample_claim_data['claim_id'])
        assert retrieved_claim.status == 'reviewed'
        assert retrieved_claim.fraud_score == 0.25
        
        # Cleanup
        try:
            claim_file = os.path.join(service.claims_dir, f"{sample_claim_data['claim_id']}.json")
            os.remove(claim_file)
        except FileNotFoundError:
            pass
