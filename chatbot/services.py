import requests
from decouple import config

def get_ai_response(user_question, retrieved_data):
    """
    Sends user input and relevant knowledge base data to Gemini API
    and returns a concise, relevant AI-generated response.
    """
    api_key = config('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Construct prompt clearly
    prompt = (
        "You are a helpful assistant. Use ONLY the following data to answer the question. "
        "Focus on content that directly relates to the question's keywords or intent. "
        "If no relevant data exists, respond exactly with: 'Sorry, I don’t have relevant information for that.' "
        "Do not invent information.\n\n"
        f"Data:\n{retrieved_data}\n\n"
        f"Question:\n{user_question}"
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        print("Full API Response:", result)  # Debugging log

        # Extract AI text safely
        content = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No response content.")
        )

        print("AI Response Content:", content)
        return content

    except requests.RequestException as e:
        error_msg = f"Error: Could not connect to Gemini API ({e})"
        print(error_msg)
        return "⚠️ AI service error. Please try again."

    except ValueError as e:
        error_msg = f"Error: Invalid JSON response ({e})"
        print(error_msg)
        return "⚠️ Received invalid response from AI service."
