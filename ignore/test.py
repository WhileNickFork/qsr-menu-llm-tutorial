from openai import OpenAI
# client = OpenAI(
#     base_url='http://192.168.1.23:11434/v1/',
#     api_key='ollama', # required but ignored
# )
# chat_completion = client.chat.completions.create(
#     model="gemini3:27b",
#     messages=[{"role": "user", "content": "Hello!"}],
# )
# print(chat_completion.choices[0].message.content)

from openai import OpenAI
import base64
import os

# Helper function to encode the image
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to the image file
image_path = "./data/competitor_menu.png"

# Check if file exists
if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' not found.")
    exit(1)

# Get the base64 encoding of the image
base64_image = encode_image_to_base64(image_path)

client = OpenAI(
    base_url='http://192.168.1.23:11434/v1/',
    api_key='ollama', # required but ignored
)

chat_completion = client.chat.completions.create(
    model="gemma3:27b",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please describe this image in detail:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ],
)

print(chat_completion.choices[0].message.content)