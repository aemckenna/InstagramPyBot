# Imports
import openai

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
        stop=None  # You can specify custom stop words/phrases
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
    # HERE: Add code for creating reel content
    pass
elif post_type == "image":
    # HERE: Add code for creating image content
    pass
else:
    print("Something is not right... Try again.")
    exit()

# Connect with ChatGPT AI to get a summary of that country
# HERE: Add code to interact with ChatGPT for country summary

# Pass summary to ElevenLabs
# HERE: Add code to pass summary to ElevenLabs

# Pass the country name to AI Image generator
# HERE: Add code to pass the country name to AI Image generator

# Store images in the directory
# HERE: Add code to store images in the directory

# Use MoviePy to create a video and render
# HERE: Add code to use MoviePy to create a video and render

# Login to Instagram
# HERE: Add code to login to Instagram

# Use ChatGPT to write a caption and generate hashtags
# HERE: Add code to use ChatGPT for writing a caption and generating hashtags

# Post video to Instagram
# HERE: Add code to post the video to Instagram
