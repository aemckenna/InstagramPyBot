# Imports
import openai
from pathlib import Path
import requests
import os
from google.cloud import texttospeech
from moviepy.editor import VideoClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import time
from instagrapi import Client
from datetime import datetime, timezone
from urllib.parse import urljoin
from instagrapi.types import User


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
    audio_file_path = Path(__file__).parent / f"{content_topic}_audio.mp3"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(response_tts.audio_content)

    # Create the audio file variable
    audio_file = str(audio_file_path)

    # Generate prompts to pass on to DALL-E-3
    image_prompt = f'Give me a list of five things about {content_topic} with no descriptions.'
    image_prompt_output = ChatGPT(image_prompt)

    # Formatting and stripping to not include numbers or punctuation
    image_prompt_list = image_prompt_output.split('\n')
    image_prompt_list = [item.strip('1-5, .') for item in image_prompt_list if item]

    # Convert the list to a dictionary without index formatting
    image_prompts_dictionary = {f"Item {index + 1}": item for index, item in enumerate(image_prompt_list)}

    # Creating a new folder to save the images
    os.makedirs(content_topic, exist_ok=True)

    # Generating images that will then be animated for the reel
    for index, prompt in image_prompts_dictionary.items():
        image = openai.Image.create(prompt=f"{content_topic}'s {prompt}", n=1, size="1024x1024")
        image_url = image['data'][0]['url']
        
        # Downloading the image
        image_data = requests.get(image_url).content

        # Saving each image to a separate file in the new folder
        image_path = os.path.join(content_topic, f"{content_topic}_{index}.png")
        with open(image_path, "wb") as f:
            f.write(image_data)

    time.sleep(30)

    # Generate the image list from the folder
    image_folder_path = content_topic
    image_list = [os.path.join(image_folder_path, file) for file in os.listdir(image_folder_path) if file.lower().endswith(('.png'))]

    # Using MoviePy to create a video and render
    def create_video(image_list, audio_file):
        # Calculate the duration of the audio file
        audio_duration = AudioFileClip(audio_file).duration

        # Load images dynamically from the folder with equal spacing
        clips = [ImageSequenceClip([image], fps=1).set_duration(audio_duration / len(image_list)) for image in image_list]

        audio_file = f"{content_topic}_audio.mp3"
        # Load audio
        audio = AudioFileClip(audio_file)

        # Set audio for each clip
        clips_with_audio = [clip.set_audio(audio) for clip in clips]

        # Concatenate video clips
        final_clip = concatenate_videoclips(clips_with_audio, method="compose")
        final_clip = final_clip.set_audio(audio)

        # Write the final video file
        final_clip.write_videofile(f'{content_topic}_{topic_mode}_FINAL.mp4', fps=24, codec='libx264', audio=True, audio_codec="aac")

    video = f'{content_topic}_{topic_mode}_FINAL.mp4'
    # Create the video with images and audio
    create_video(image_list, audio_file)

    # Use ChatGPT to write a caption and generate hashtags
    caption_prompt = f"Write a caption and generate hashtags for a {post_type} post on {content_topic}."
    ig_caption = ChatGPT(caption_prompt)
    
    class CustomInstagrapiException(Exception):
        pass

    username = "intrepidlearning"
    password = "censak-cakWo6-niwsec"

    # Video file path as a string
    video_path = f'{content_topic}_{topic_mode}_FINAL.mp4'

    try:
        # Initialize the instagrapi client
        cl = Client()
        cl.login(username, password)

        # Upload video to Instagram
        cl.video_upload(
            path=video_path,
            caption=ig_caption,
            thumbnail=None,
            usertags=[],
            location=None,
            extra_data={}
        )

        # Logout after uploading
        cl.logout()

    except CustomInstagrapiException as e:
        print("Video uploaded")
    except Exception as e:
        print("Video Uploaded")


elif post_type == "image":
    pass

else:
    print("Something is not right... Try again.")
    exit()