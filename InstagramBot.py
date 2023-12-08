# Imports
import openai
from pathlib import Path
import requests
import os
from google.cloud import texttospeech

# Determined Topic (change this value to set Instagram bot to post differently)
topic_mode = "country"

# Function to interact with GPT-3
openai.api_key = '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'

def ChatGPT(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        stop=None
    )
    return response.choices[0].text.strip()

# Function that returns true if the word is found
def WordFinder(sentence, word):
    
    # Breaking the sentence into words
    s = sentence.split(" ")

    for i in s:
        if i == word:
            return True
    return False

# Interacting with the user to determine post type
print("Would you like to make an \"image\" post or a \"reel\"?")
post_type = input().lower()

# Checking to confirm the user entered a valid option
if not (WordFinder(post_type, "reel") or WordFinder(post_type, "image")):
    print(f'You entered {post_type} which is not a valid post type. Please try again.')
    exit()

# Requesting post type
print(f'What country would you like to make a {post_type} on?')
content_topic = input()

# Checking to confirm that it matches post topic mode
topic_mode_check = f'Answer only "yes" or "no". Is {content_topic} a {topic_mode}?'
topic_check_response = ChatGPT(topic_mode_check)
print(topic_check_response)

if topic_check_response.lower() == "yes" or "yes.":
    pass
elif topic_check_response.lower() == "no" or "no.":
    print(f'Your chosen {topic_mode} is not a valid {topic_mode} for this bot. Please use a different one next time.')
    exit()
else:
    print(f'{content_topic} is not a valid {topic_mode}. Please choose a different one next time.')
    exit()

if post_type == "reel":
    # Set the environment variable to the path of your service account key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ashermckenna/Documents/InstagraPy/InstagramPyBot/rapid-pivot-407416-88aae5fe7262.json"

    # Create a Text-to-Speech client
    client_tts = texttospeech.TextToSpeechClient()

    # Set the text to be synthesized
    text_to_speak = f"Write a script for a 30 second reel on {content_topic} the {topic_mode}."
    script = ChatGPT(text_to_speak)

    # Select the voice and other parameters
    voice_tts = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config_tts = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Synthesize the speech
    response_tts = client_tts.synthesize_speech(
        input=texttospeech.SynthesisInput(text=script),
        voice=voice_tts,
        audio_config=audio_config_tts
    )

    # Save the audio to a file
    audio_file_path = Path(__file__).parent / (f"{content_topic}_audio.mp3")
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(response_tts.audio_content)

    # Generating prompts to pass on to Dall-E-3
    video_script = f'Write a script for a 30 second reel on {content_topic} the {topic_mode}.'
    topic_check_response = ChatGPT(video_script)

    # Creating a new folder to save the images
    os.makedirs(content_topic, exist_ok=True)

    # Generating images that will then be animated for the reel
    dalle3_image = openai.Image.create(
        prompt=content_topic, 
        n=4, 
        size="1024x1024")

    # Getting URL and downloading image
    image_url = dalle3_image.data[0].url
    image_data = requests.get(image_url).content
    image_name = f"{content_topic}_image1.png"

    # Saving the image to a file in the new folder
    image_path = os.path.join(content_topic, image_name)
    with open(image_path, "wb") as f:
        f.write(image_data)

elif post_type == "image":
    pass

else:
    print("Something is not right... Try again.")
    exit()

# Use MoviePy to create a video and render
# Add your MoviePy code here

# Login to Instagram
# Add your Instagram login code here

# Use ChatGPT to write a caption and generate hashtags
caption_prompt = f"Write a caption and generate hashtags for a {post_type} post on {content_topic}."
caption_response = ChatGPT(caption_prompt)

# Post video to Instagram
# Add your Instagram post code here

# End of the script