import os
import json

class LLMClient:
    def complete_json(self, system_prompt: str, user_prompt: str, schema: dict) -> dict:
        raise NotImplementedError

    def complete_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError

class MockLLMClient(LLMClient):
    def complete_json(self, system_prompt: str, user_prompt: str, schema: dict) -> dict:
        # Provide a mock response based on the system prompt context
        if "structured facts" in system_prompt.lower():
            # mock extraction
            return {
                "fields": [
                    {
                        "field_name": "mock_field",
                        "field_type": "string",
                        "value": "Mock Value",
                        "raw_text": "Mock text passage",
                        "confidence": 0.9,
                        "chunk_id": "mock_chk_1",
                        "page_number": 1,
                        "uncertainty_reason": None
                    }
                ]
            }
        return {}
        
    def complete_text(self, system_prompt: str, user_prompt: str) -> str:
        if "Template:" in user_prompt:
            # Generate the 8 required sections with mock citation chips
            return """# Case Fact Summary and Internal Memo

## 1. Matter Overview
This matter involves a synthetic request for review based on provided documents [E1]. The current status is preliminary review [E2].

## 2. Parties Involved
- **Northbridge Estates LLP**: Sender of notice [E1].
- **Riya Malhotra**: Recipient of notice [E1].
- **Arjun Mehta**: Affiant [E2].

## 3. Key Dates and Events
- **March 12, 2024**: Date of the notice [E1].
- **February 6, 2024**: Date the affidavit was notarized [E2].
- **January 21, 2024**: Property record updated [E3].

## 4. Documents Reviewed
- Notice of Document Request
- Affidavit (Noisy scan)
- Property Record Extract

## 5. Core Facts
Northbridge Estates requested documents within 15 days of notice receipt [E1]. Arjun Mehta states the payment receipt of Rs. 75,000 relates to Unit 4B [E2]. Riya Malhotra is the recorded occupant of Unit 4B [E3].

## 6. Open Issues and Missing Information
- The date of receipt for the notice is missing [E1].
- The occupancy certificate number is not visible in the extract [E3].
- The payment amount in the affidavit needs verification due to an unclear scan [E2].

## 7. Evidence Table
See citations referenced in the text.

## 8. Suggested Next Steps
- Verify the receipt date.
- Obtain a clear copy of the affidavit.
- Request the occupancy certificate number.
"""
        return f"Mock response. System: {system_prompt[:20]}... User: {user_prompt[:20]}..."

# In future, implement OpenAILLMClient here

def get_llm_client() -> LLMClient:
    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "mock":
        return MockLLMClient()
    # Add real LLM client initialization here
    return MockLLMClient()
