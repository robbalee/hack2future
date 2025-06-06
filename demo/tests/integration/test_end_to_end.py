"""
End-to-end integration tests for the insurance fraud detection system.
These tests verify the complete system functionality.
"""
import pytest
import os
import uuid
from datetime import datetime

from services.hybrid_service import HybridDataService
from models.claim import Claim
from models.event import Event


@pytest.mark.integration
class TestEndToEndIntegration:
    """End-to-end integration tests"""
    
    def test_complete_claim_lifecycle(self):
        """Test the complete lifecycle of a claim through the system"""
        service = HybridDataService()
        
        # 1. Create a new claim
        claim_id = f"e2e-test-{uuid.uuid4()}"
        claim_data = {
            "claim_id": claim_id,
            "claim_amount": 5000.0,
            "description": "End-to-end test claim - vehicle damage",
            "submission_time": datetime.now().isoformat(),
            "status": "submitted",
            "fraud_score": None,
            "uploaded_files": []
        }
        
        # 2. Save the claim
        saved_id = service.save_claim(claim_data)
        assert saved_id == claim_id
        
        # 3. Create submission event
        submission_event = {
            "event_id": str(uuid.uuid4()),
            "entity_id": claim_id,
            "entity_type": "claim",
            "event_type": "submitted",
            "timestamp": datetime.now().isoformat(),
            "data": {"source": "e2e_test", "ip_address": "127.0.0.1"}
        }
        
        submission_event_id = service.save_event(submission_event)
        assert submission_event_id == submission_event['event_id']
        
        # 4. Retrieve and verify the claim
        retrieved_claim = service.get_claim(claim_id)
        assert retrieved_claim is not None
        
        if isinstance(retrieved_claim, dict):
            assert retrieved_claim['claim_id'] == claim_id
            assert retrieved_claim['claim_amount'] == 5000.0
            assert retrieved_claim['status'] == "submitted"
        else:
            assert retrieved_claim.claim_id == claim_id
            assert retrieved_claim.claim_amount == 5000.0
            assert retrieved_claim.status == "submitted"
        
        # 5. Update claim status (processing)
        if isinstance(retrieved_claim, dict):
            retrieved_claim['status'] = 'processing'
            retrieved_claim['fraud_score'] = 0.15
        else:
            retrieved_claim.status = 'processing'
            retrieved_claim.fraud_score = 0.15
            retrieved_claim = retrieved_claim.to_dict()
        
        service.save_claim(retrieved_claim)
        
        # 6. Add processing event
        processing_event = {
            "event_id": str(uuid.uuid4()),
            "entity_id": claim_id,
            "entity_type": "claim",
            "event_type": "processing_started",
            "timestamp": datetime.now().isoformat(),
            "data": {"processor": "automated_system", "estimated_completion": "2h"}
        }
        
        service.save_event(processing_event)
        
        # 7. Add fraud check event
        fraud_event = {
            "event_id": str(uuid.uuid4()),
            "entity_id": claim_id,
            "entity_type": "claim",
            "event_type": "fraud_check_completed",
            "timestamp": datetime.now().isoformat(),
            "data": {"score": 0.15, "risk_level": "low", "factors": ["normal_amount", "verified_policy"]}
        }
        
        service.save_event(fraud_event)
        
        # 8. Final status update
        final_claim = service.get_claim(claim_id)
        if isinstance(final_claim, dict):
            final_claim['status'] = 'approved'
        else:
            final_claim.status = 'approved'
            final_claim = final_claim.to_dict()
        
        service.save_claim(final_claim)
        
        # 9. Add approval event
        approval_event = {
            "event_id": str(uuid.uuid4()),
            "entity_id": claim_id,
            "entity_type": "claim",
            "event_type": "approved",
            "timestamp": datetime.now().isoformat(),
            "data": {"approved_by": "system", "approved_amount": 5000.0}
        }
        
        service.save_event(approval_event)
        
        # 10. Verify final state
        final_retrieved_claim = service.get_claim(claim_id)
        if isinstance(final_retrieved_claim, dict):
            assert final_retrieved_claim['status'] == 'approved'
            assert final_retrieved_claim['fraud_score'] == 0.15
        else:
            assert final_retrieved_claim.status == 'approved'
            assert final_retrieved_claim.fraud_score == 0.15
        
        # 11. Verify all events were recorded
        events = service.list_events(claim_id)
        assert len(events) >= 4  # submitted, processing, fraud_check, approved
        
        # Verify event types
        event_types = []
        for event in events:
            if isinstance(event, dict):
                event_types.append(event['event_type'])
            else:
                event_types.append(event.event_type)
        
        assert 'submitted' in event_types
        assert 'processing_started' in event_types
        assert 'fraud_check_completed' in event_types
        assert 'approved' in event_types
        
        print(f"✅ End-to-end test completed successfully for claim {claim_id}")
        print(f"   Final status: approved")
        print(f"   Fraud score: 0.15")
        print(f"   Events recorded: {len(events)}")
    
    def test_high_risk_claim_workflow(self):
        """Test workflow for a high-risk claim"""
        service = HybridDataService()
        
        # Create a high-risk claim
        claim_id = f"high-risk-{uuid.uuid4()}"
        high_risk_claim = {
            "claim_id": claim_id,
            "claim_amount": 50000.0,  # High amount
            "description": "Total loss - suspicious circumstances",
            "submission_time": datetime.now().isoformat(),
            "status": "submitted",
            "fraud_score": None,
            "uploaded_files": []
        }
        
        # Save claim
        service.save_claim(high_risk_claim)
        
        # Add high-risk fraud score
        high_risk_claim['fraud_score'] = 0.85
        high_risk_claim['status'] = 'under_investigation'
        service.save_claim(high_risk_claim)
        
        # Add investigation event
        investigation_event = {
            "event_id": str(uuid.uuid4()),
            "entity_id": claim_id,
            "entity_type": "claim",
            "event_type": "investigation_started",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "reason": "high_fraud_score",
                "assigned_investigator": "detective_smith",
                "priority": "high"
            }
        }
        
        service.save_event(investigation_event)
        
        # Verify the claim is marked for investigation
        retrieved_claim = service.get_claim(claim_id)
        if isinstance(retrieved_claim, dict):
            assert retrieved_claim['status'] == 'under_investigation'
            assert retrieved_claim['fraud_score'] == 0.85
        else:
            assert retrieved_claim.status == 'under_investigation'
            assert retrieved_claim.fraud_score == 0.85
        
        # Verify investigation event was recorded
        events = service.list_events(claim_id)
        investigation_events = [
            e for e in events 
            if (e.get('event_type') if isinstance(e, dict) else e.event_type) == 'investigation_started'
        ]
        assert len(investigation_events) == 1
        
        print(f"✅ High-risk claim workflow test completed for claim {claim_id}")
    
    @pytest.mark.cosmos
    def test_hybrid_storage_consistency(self):
        """Test that data is consistent between local and cloud storage"""
        # Only run if Cosmos DB is available
        if not (os.getenv('COSMOS_ENDPOINT') and os.getenv('COSMOS_KEY')):
            pytest.skip("Cosmos DB credentials not available")
        
        service = HybridDataService()
        
        if not service.use_cosmos:
            pytest.skip("Cosmos DB not available for hybrid testing")
        
        # Create test claim
        claim_id = f"hybrid-test-{uuid.uuid4()}"
        test_claim = {
            "claim_id": claim_id,
            "claim_amount": 1500.0,
            "description": "Hybrid storage consistency test",
            "submission_time": datetime.now().isoformat(),
            "status": "pending",
            "fraud_score": None,
            "uploaded_files": []
        }
        
        # Save to hybrid storage
        saved_id = service.save_claim(test_claim)
        assert saved_id == claim_id
        
        # Retrieve from hybrid storage
        retrieved_claim = service.get_claim(claim_id)
        assert retrieved_claim is not None
        
        # Verify data consistency
        if isinstance(retrieved_claim, dict):
            assert retrieved_claim['claim_id'] == claim_id
            assert retrieved_claim['claim_amount'] == 1500.0
        else:
            assert retrieved_claim.claim_id == claim_id
            assert retrieved_claim.claim_amount == 1500.0
        
        # Verify the claim appears in listings
        all_claims = service.list_claims()
        claim_ids = [
            c.get('claim_id') if isinstance(c, dict) else c.claim_id
            for c in all_claims
        ]
        assert claim_id in claim_ids
        
        print(f"✅ Hybrid storage consistency test completed for claim {claim_id}")


if __name__ == "__main__":
    # This allows running the integration tests directly
    pytest.main([__file__, "-v", "-m", "integration"])
