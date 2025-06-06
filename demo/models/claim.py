"""
Claim data models for the insurance fraud detection system.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class FileInfo:
    """Represents an uploaded file in the system"""
    original_name: str
    saved_name: str
    file_path: str
    file_type: str
    file_size: int


@dataclass
class Claim:
    """Represents an insurance claim in the system"""
    claim_amount: float
    description: str
    uploaded_files: List[FileInfo] = field(default_factory=list)
    claim_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    submission_time: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_time: Optional[str] = None
    fraud_score: Optional[float] = None
    status: str = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the claim to a dictionary"""
        return {
            "claim_id": self.claim_id,
            "claim_amount": self.claim_amount,
            "description": self.description,
            "uploaded_files": [vars(file) for file in self.uploaded_files],
            "submission_time": self.submission_time,
            "updated_time": self.updated_time,
            "fraud_score": self.fraud_score,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Claim':
        """Create a claim from a dictionary"""
        files = [FileInfo(**file_data) for file_data in data.get('uploaded_files', [])]
        return cls(
            claim_id=data.get('claim_id', str(uuid.uuid4())),
            claim_amount=data.get('claim_amount', 0.0),
            description=data.get('description', ''),
            uploaded_files=files,
            submission_time=data.get('submission_time', datetime.now().isoformat()),
            updated_time=data.get('updated_time'),
            fraud_score=data.get('fraud_score'),
            status=data.get('status', 'pending')
        )
