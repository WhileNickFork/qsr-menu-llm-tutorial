# describe_image.py
import base64
import os, json
import traceback
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

# --- Configuration ---
OLLAMA_BASE_URL = "http://192.168.1.23:11434/v1" # Replace with your Ollama IP if not localhost
# IMPORTANT: Choose a multimodal model served by your Ollama instance
OLLAMA_VISION_MODEL = "gemma3:27b"
# Provide the path to the image you want to describe
IMAGE_PATH = "./data/competitor_menu.png" # <<< CHANGE THIS TO YOUR IMAGE PATH

# --- Helper Function ---
def encode_image(image_path):
    """Encodes an image file into a base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error encoding image {image_path}: {repr(e)}")
        return None


class CompetitorMenuItem(BaseModel):
    item_name: str = Field(...)
    price: Optional[float] = None

class CompetitorMenu(BaseModel):
    items: List[CompetitorMenuItem]


schema_desc = json.dumps(CompetitorMenu.model_json_schema())
prompt_text = (
    "Analyze the menu in the provided image. Extract all distinct menu items and their corresponding prices. "
    "Format the output strictly as a JSON string representing a list of objects. "
    "Each object must have keys 'item_name' (string) and 'price' (float or null if price is missing or unreadable). "
    "Ignore headers, descriptions, or non-item text. Consolidate slightly different phrasings of the same item if possible. "
    "Only output the valid JSON string, with no surrounding text, explanations, or markdown fences.\n"
    # f"The required JSON structure is described by this schema: {schema_desc}\n"
    "Example: '[{\"item_name\": \"Classic Burger\", \"price\": 6.50}, {\"item_name\": \"Fries\", \"price\": 2.50}, {\"item_name\": \"Soda\", \"price\": null}]'"
)







# --- Main Execution ---
if __name__ == "__main__":
    print(f"Attempting to describe image: {IMAGE_PATH}")
    print(f"Using Ollama model: {OLLAMA_VISION_MODEL} at {OLLAMA_BASE_URL}")
    print(prompt_text)
    print("-----------------\n\n")
    print(f"The required JSON structure is described by this schema: {schema_desc}\n")

    # 1. Check if image exists
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Cannot find image file at '{IMAGE_PATH}'. Please check the path.")
        exit()

    # 2. Encode the image
    base64_image = encode_image(IMAGE_PATH)
    if not base64_image:
        print("Exiting due to image encoding error.")
        exit()

    print("Image encoded successfully.")

    # 3. Initialize ChatOpenAI client for Ollama
    try:
        llm = ChatOpenAI(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_VISION_MODEL,
            api_key="ollama",  # Required by ChatOpenAI, but value ignored by Ollama
            temperature=0.1    # Lower temperature for more factual description
        )
        print("ChatOpenAI client initialized.")
    except Exception as e:
        print(f"Error initializing ChatOpenAI: {repr(e)}")
        print(traceback.format_exc())
        exit()

    # 4. Prepare the prompt message
    # The message content needs to be a list containing text and image data
    # Assuming JPEG/PNG works with this data URI format, adjust mime type if needed (e.g., image/png)
    prompt_message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"{prompt_text}"
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"} # Adjust mime type if necessary
            },
        ]
    )
    print("Prompt message constructed.")

    # 5. Invoke the LLM and print the response
    try:
        print("\n--- Calling Vision LLM ---")
        response = llm.invoke([prompt_message]) # Pass messages as a list
        print("--- LLM Call Complete ---")
        print("\n--- Image Description ---")
        print(response.content)
        print("-------------------------\n")

    except Exception as e:
        print(f"\n--- Error during LLM invocation ---")
        print(f"An error occurred: {repr(e)}")
        print("Check if:")
        print(f" - Ollama is running at {OLLAMA_BASE_URL}")
        print(f" - The model '{OLLAMA_VISION_MODEL}' is downloaded and available in Ollama (`ollama list`)")
        print(" - Ollama service logs show any specific errors (memory, etc.)")
        print(traceback.format_exc())
        print("----------------------------------\n")

    print("Script finished.")