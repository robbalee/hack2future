"""
Validation utilities for the insurance fraud detection system.
"""
import json
import os
import jsonschema
from typing import Dict, Any, List


class ValidationError(Exception):
    """Exception raised for validation errors"""
    def __init__(self, message: str, errors: List[str] = None):
        self.message = message
        self.errors = errors or []
        super().__init__(self.message)


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema from the claims_data directory"""
    schema_path = os.path.join('claims_data', f"{schema_name}.json")
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValidationError(f"Schema {schema_name} not found")
    except json.JSONDecodeError:
        raise ValidationError(f"Schema {schema_name} is not valid JSON")


def validate_data(data: Dict[str, Any], schema_name: str) -> None:
    """Validate data against a JSON schema"""
    schema = load_schema(schema_name)
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(f"Validation error: {e.message}", [e.message])
    

def validate_claim(claim_data: Dict[str, Any]) -> None:
    """Basic validation for claim data"""
    required_fields = ['claim_amount', 'description']
    errors = []
    
    for field in required_fields:
        if field not in claim_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        raise ValidationError("Claim data validation failed", errors)
    
    # Type validation
    if not isinstance(claim_data.get('claim_amount'), (int, float)):
        errors.append("claim_amount must be a number")
    
    if not isinstance(claim_data.get('description'), str):
        errors.append("description must be a string")
    
    if errors:
        raise ValidationError("Claim data validation failed", errors)
