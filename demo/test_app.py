import requests

# Test list_claims endpoint
response = requests.get("http://localhost:5000/list_claims")
print("List Claims Response:", response.status_code)
print(response.json())

# Test submitting a claim
test_claim = {
    "claimAmount": "1000",
    "description": "Test claim from enhanced data service"
}
files = {}

response = requests.post("http://localhost:5000/submit_claim", data=test_claim, files=files)
print("\nSubmit Claim Response:", response.status_code)
print(response.json())

if response.status_code == 200 and response.json().get('success'):
    # Test getting the claim
    claim_id = response.json().get('claim_id')
    response = requests.get(f"http://localhost:5000/get_claim/{claim_id}")
    print("\nGet Claim Response:", response.status_code)
    print(response.json())
    
    # Test updating the claim
    update_data = {
        "status": "reviewed",
        "fraud_score": 0.25
    }
    response = requests.post(f"http://localhost:5000/update_claim/{claim_id}", json=update_data)
    print("\nUpdate Claim Response:", response.status_code)
    print(response.json())
    
    # Test listing claims again to see the updated claim
    response = requests.get("http://localhost:5000/list_claims")
    print("\nList Claims After Update:", response.status_code)
    print(response.json())
