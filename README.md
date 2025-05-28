# hack2future

[User's Web Browser]
      | (Upload Image, Fill Form)
      V
[Frontend Web App] (React/Vue/Svelte + App Service)
      | (API Calls)
      V
[Backend API] (Flask/FastAPI + App Service)
      |
      +----- (Image) ----> [Azure AI Vision]
      |                         |
      |                         V
      |                   (Detected Objects/Text)
      |                         |
      +----- (Text) ----> [Azure AI Language]
      |                         |
      |                         V
      |                   (Extracted Entities/Sentiment)
      |                         |
      V                         V
[Backend API] (Combines AI results + original form data)
      |
      +----- (Prompt for Tips) ---> [Azure OpenAI Service (GPT)]
      |                                  |
      |                                  V
      |                             (Actionable Tips)
      V
[Backend API] (Sends combined insights to frontend)
      |
      V
[Frontend Web App] (Displays Image, Form Data, AI Insights, Actionable Tips)

1. HuggingFace
2. 