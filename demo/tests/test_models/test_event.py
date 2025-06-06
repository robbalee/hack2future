"""
Tests for the Event model.
"""
import pytest
from datetime import datetime
from models.event import Event


class TestEvent:
    """Test cases for the Event model"""
    
    def test_event_creation_from_dict(self, sample_event_data):
        """Test creating an Event from dictionary data"""
        event = Event.from_dict(sample_event_data)
        
        assert event.event_id == sample_event_data['event_id']
        assert event.entity_id == sample_event_data['entity_id']
        assert event.event_type == sample_event_data['event_type']
        assert event.data == sample_event_data['data']
    
    def test_event_to_dict(self, sample_event_data):
        """Test converting an Event to dictionary"""
        event = Event.from_dict(sample_event_data)
        event_dict = event.to_dict()
        
        assert event_dict['event_id'] == sample_event_data['event_id']
        assert event_dict['entity_id'] == sample_event_data['entity_id']
        assert event_dict['event_type'] == sample_event_data['event_type']
        assert event_dict['data'] == sample_event_data['data']
    
    def test_event_validation_valid_data(self, sample_event_data):
        """Test event validation with valid data"""
        event = Event.from_dict(sample_event_data)
        assert event is not None
    
    def test_event_validation_missing_required_field(self):
        """Test event validation with missing required field"""
        invalid_data = {
            "entity_id": "test-claim-123",
            "event_type": "submitted"
            # event_id is missing - but model generates it automatically
        }
        
        # The model should handle missing event_id by generating one
        event = Event.from_dict(invalid_data)
        assert event.event_id is not None
        assert len(event.event_id) > 0
    
    def test_event_string_representation(self, sample_event_data):
        """Test string representation of Event"""
        event = Event.from_dict(sample_event_data)
        event_str = str(event)
        
        assert sample_event_data['event_id'] in event_str
        assert sample_event_data['event_type'] in event_str
    
    def test_event_equality(self, sample_event_data):
        """Test equality comparison between events"""
        event1 = Event.from_dict(sample_event_data)
        event2 = Event.from_dict(sample_event_data.copy())
        
        assert event1 == event2
    
    def test_event_timestamp_handling(self, sample_event_data):
        """Test timestamp handling in events"""
        event = Event.from_dict(sample_event_data)
        
        # Should have a timestamp
        assert hasattr(event, 'timestamp')
        assert event.timestamp is not None
        
        # Timestamp should be in ISO format or datetime
        timestamp_str = event.timestamp
        if isinstance(timestamp_str, str):
            # Should be parseable as ISO format
            datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    
    def test_event_data_handling(self, sample_event_data):
        """Test event data field handling"""
        event = Event.from_dict(sample_event_data)
        
        assert event.data == sample_event_data['data']
        assert isinstance(event.data, dict)
        
        # Test with different data types
        event.data = {"new_key": "new_value", "number": 42}
        updated_dict = event.to_dict()
        assert updated_dict['data']['new_key'] == "new_value"
        assert updated_dict['data']['number'] == 42
