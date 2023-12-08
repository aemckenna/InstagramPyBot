# Imports
import openai
from openai import OpenAI
from pathlib import Path
import requests
import os

# Determined Topic (change this value to set Instagram bot to post differently)
topic_mode = "country"
client = OpenAI()

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

# Requesting post topic
print(f'What country would you like to make a {post_type} on?')
content_topic = input()

# Checking to confirm that it matches post topic mode
topic_mode_check = f'Answer only "yes" or "no". Is {content_topic} a {topic_mode}?'
topic_check_response = ChatGPT(topic_mode_check)

if topic_check_response.lower() == "yes":
    pass
elif topic_check_response.lower() == "no":
    print(f'Your chosen {topic_mode} is not a valid {topic_mode} for this bot. Please use a different one next time.')
    exit()
else:
    print(f'{content_topic} is not a valid {topic_mode}. Please choose a different one next time.')
    exit()

# Creating content based on user input
if post_type == "reel":

    # Generating script to pass on to ElevenLabs
    video_script = f'Write a script for a 30 second reel on {content_topic} the {topic_mode}.'
    topic_check_response = ChatGPT(video_script)
    
    # Using ChatGPT text to speech to download audio for reel
    speech_file_path = Path(__file__).parent / (f"{content_topic}.mp3")
    response = client.audio.speech.create(
    model = "tts-1-hd",
    voice = "onyx",
    input = video_script
    )

    response.stream_to_file(speech_file_path)

    # Generating prompts to pass on to Dall-E-3
    video_script = f'Write a script for a 30 second reel on {content_topic} the {topic_mode}.'
    topic_check_response = ChatGPT(video_script)

    # Creating a new folder to save the images
    os.makedirs(content_topic, exist_ok=True)

    # Generating images that will then be animated for the reel
    response = client.images.generate(
    model = "dall-e-3",
    prompt = "a white siamese cat",
    size = "1080x1920",
    qualit = "hd",
    n = 1,
    )

    # Getting URL and downloading image
    image_url = response.data[0].url
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

# Login to Instagram

# Use ChatGPT to write a caption and generate hashtags

# Post video to Instagram