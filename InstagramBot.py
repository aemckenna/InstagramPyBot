# Imports
import openai

# Function to interact with GPT-3
openai.api_key = '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'
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        stop=None  # You can specify custom stop words/phrases
    )
    return response.choices[0].text.strip()

# Interact with user to request country to make content from
print("Would you like to make an image post or a reel?")
post_type = input()

if post_type == reel



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