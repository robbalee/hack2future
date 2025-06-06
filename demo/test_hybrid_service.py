#!/usr/bin/env python3
"""
Test utility for the hybrid data service integration.
This script tests the connection to Cosmos DB and performs basic operations.
"""
import os
import sys
import json
from datetime import datetime
import uuid

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import our modules
try:
    from services.hybrid_service import HybridDataService
    from models.claim import Claim
    from models.event import Event
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure you are running this script from the correct directory")
    print("Current directory:", os.getcwd())
    print("Current PYTHONPATH:", sys.path)
    sys.exit(1)

def test_hybrid_service():
    """Test the hybrid data service"""
    print("Testing HybridDataService integration...")
    
    try:
        # Create service instance
        service = HybridDataService()
        
        # Check if Cosmos DB is available
        print(f"Using Cosmos DB: {service.use_cosmos}")
        
        # Create a test claim
        test_claim_id = f"test-{uuid.uuid4()}"
        test_claim = {
            "claim_id": test_claim_id,
            "claim_amount": 1000.0,
            "description": "Test claim for hybrid service",
            "submission_time": datetime.now().isoformat(),
            "status": "pending",
            "fraud_score": None,
            "uploaded_files": []
        }
        
        # Save the claim
        print(f"Saving test claim {test_claim_id}...")
        saved_id = service.save_claim(test_claim)
        print(f"Saved claim with ID: {saved_id}")
        
        # Retrieve the claim
        print("Retrieving claim...")
        retrieved_claim = service.get_claim(test_claim_id)
        if retrieved_claim:
            print("Claim retrieved successfully!")
            if isinstance(retrieved_claim, dict):
                print(f"Claim amount: {retrieved_claim.get('claim_amount')}")
            else:
                print(f"Claim amount: {retrieved_claim.claim_amount}")
        else:
            print("Failed to retrieve claim!")
        
        # Create a test event
        test_event_id = str(uuid.uuid4())
        test_event = {
            "event_id": test_event_id,
            "entity_id": test_claim_id,
            "entity_type": "claim",
            "event_type": "test",
            "timestamp": datetime.now().isoformat(),
            "data": {"test": True}
        }
        
        # Save the event
        print(f"Saving test event {test_event_id}...")
        saved_event_id = service.save_event(test_event)
        print(f"Saved event with ID: {saved_event_id}")
        
        # List events for the claim
        print("Listing events for claim...")
        events = service.list_events(test_claim_id)
        print(f"Found {len(events)} events")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    print("Test completed successfully!")
    return True

if __name__ == "__main__":
    # Change to the demo directory to ensure correct path resolution
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Current directory:", os.getcwd())
    print("Python path:", sys.path)
    
    # Display environment variables related to Cosmos DB
    print("COSMOS_ENDPOINT:", os.environ.get('COSMOS_ENDPOINT', 'Not set'))
    print("COSMOS_KEY:", "****" + os.environ.get('COSMOS_KEY', 'Not set')[-4:] if os.environ.get('COSMOS_KEY') else 'Not set')
    
    # Run the test
    success = test_hybrid_service()
    sys.exit(0 if success else 1)
