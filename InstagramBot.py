# Imports
import openai

# Interact with user to request country to make content from

# Set your OpenAI API key here
openai.api_key = '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'

# Function to interact with GPT-3
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose a different engine if needed
        prompt=prompt,
        max_tokens=150,  # Adjust max_tokens as needed
        temperature=0.7,  # Adjust temperature as needed
        stop=None  # You can specify custom stop words/phrases
    )
    return response.choices[0].text.strip()

# Example usage
user_input = "Tell me a joke."
response = chat_with_gpt(user_input)
print(response)


# Check to confirm that it is a country


# Connect with ChatGPT AI to get summary of that country


# Pass summary to ElevenLabs


# Pass country name to AI Image generator


# Store images in directory


# Use MoviePy to create video and render


# Login to Instagram


# Use ChatGPT to write a caption and generate hastags


# Post video to instagram