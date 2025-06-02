import os
import google.generativeai as genai
from typing import List, Dict, Tuple, Optional

# Configure Gemini API key
try:
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=GOOGLE_API_KEY)
except ValueError as e:
    print(f"Error configuring Gemini: {e}")
    # You might want to handle this more gracefully, e.g., by disabling LLM features
    # or raising an exception that the main app can catch.
    # For now, we'll let it proceed, and API calls will fail if key is not set.


# Configuration for the generative model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", # Using flash for speed and cost-effectiveness
    safety_settings=safety_settings,
    generation_config=generation_config,
)

BASE_SYSTEM_PROMPT = """You are a creative and engaging storyteller for young children aged 4 to 8.
Your stories are always positive, simple to understand, and encourage curiosity. Avoid scary or complex themes.
Each turn, write one short paragraph of the story (3-5 sentences).
Then, provide a visual description for an image related to this scene, enclosed in square brackets like this: [IMAGE: A vibrant, sunlit meadow with a small, smiling blue bunny holding a red flower.]
Finally, offer 2-3 simple choices for the child to make. Each choice must be on a new line and start with 'CHOICE: '.
Example of a choice:
CHOICE: Pet the bunny.
CHOICE: Ask the bunny its name.
Ensure choices are distinct and lead to different story paths."""

def parse_llm_response(llm_text: str) -> Tuple[str, str, List[str]]:
    story_text = ""
    image_prompt = "A delightful scene." # Default image prompt
    choices = []

    # Extract image prompt
    image_prompt_start = llm_text.find("[IMAGE:")
    if image_prompt_start != -1:
        image_prompt_end = llm_text.find("]", image_prompt_start)
        if image_prompt_end != -1:
            image_prompt = llm_text[image_prompt_start + len("[IMAGE:"):image_prompt_end].strip()
            # Story text is before [IMAGE:]
            story_text_part = llm_text[:image_prompt_start].strip()
            remaining_text_after_image = llm_text[image_prompt_end + 1:].strip()
        else: # Malformed image prompt
            story_text_part = llm_text.strip()
            remaining_text_after_image = ""
    else: # No image prompt found
        story_text_part = llm_text.strip()
        remaining_text_after_image = ""


    # Extract choices and potentially more story text
    lines = remaining_text_after_image.split('\n')
    potential_story_continuation = []
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith("CHOICE:"):
            choice_text = line_stripped[len("CHOICE:"):].strip()
            if choice_text: # Ensure choice is not empty
                choices.append(choice_text)
        elif choices: # if we already found choices, subsequent non-choice lines are ignored for story
            pass
        elif line_stripped: # Lines after image prompt but before first choice can be part of story
            potential_story_continuation.append(line_stripped)

    if story_text_part:
        story_text = story_text_part
    if potential_story_continuation and not choices: # If no choices found, these lines are story
        story_text += ("\n" + "\n".join(potential_story_continuation)).strip()
    elif potential_story_continuation and choices: # If choices found, these lines before choices are story
         story_text += ("\n" + "\n".join(potential_story_continuation)).strip()


    # Fallback if parsing failed to get choices, try to find choices anywhere in the original text
    if not choices:
        all_lines = llm_text.split('\n')
        for line in all_lines:
            line_stripped = line.strip()
            if line_stripped.startswith("CHOICE:"):
                choice_text = line_stripped[len("CHOICE:"):].strip()
                if choice_text:
                    choices.append(choice_text)
        # If choices were found this way, the story text is everything before the first choice
        if choices:
            first_choice_marker = llm_text.find("CHOICE:")
            if first_choice_marker != -1:
                story_text_candidate = llm_text[:first_choice_marker].strip()
                # Refine story text to exclude image prompt if it's within this candidate
                img_prompt_idx = story_text_candidate.find("[IMAGE:")
                if img_prompt_idx != -1:
                    img_prompt_end_idx = story_text_candidate.find("]", img_prompt_idx)
                    if img_prompt_end_idx != -1:
                        story_text = (story_text_candidate[:img_prompt_idx] + story_text_candidate[img_prompt_end_idx+1:]).strip()
                    else:
                        story_text = story_text_candidate[:img_prompt_idx].strip() # remove incomplete image tag
                else:
                    story_text = story_text_candidate


    # If still no story text, use a default
    if not story_text.strip() and choices: # If there are choices, but no story text was parsed before them
        story_text = "The story continues..."
    elif not story_text.strip() and not choices: # Total failure
        story_text = "Oh no! The storyteller seems to be taking a nap. Let's try again."
        image_prompt = "A sleeping storyteller."
        choices = ["Try again?"]


    # Ensure at least one choice, even in error/fallback
    if not choices:
        choices = ["What happens next?"]
        if not story_text.strip(): # If really nothing came back
            story_text = "It's a mysterious silence... what could be happening?"
            image_prompt = "A mysterious, empty scene."

    return story_text, image_prompt, choices


async def generate_story_segment(
    theme: Optional[str] = None,
    story_history: Optional[List[Dict[str, any]]] = None, # Using 'any' for parts content
    user_choice: Optional[str] = None
) -> Tuple[str, str, List[str], List[Dict[str, any]]]:

    if not GOOGLE_API_KEY:
        # Simulate LLM response if API key is not available
        error_story = "The magic storybook needs a special key to open! Please tell a grown-up to check the settings."
        error_image = "A locked storybook with a keyhole."
        error_choices = ["Try again later"]
        
        # Construct a minimal history to send back
        updated_history = story_history.copy() if story_history else []
        if user_choice:
             updated_history.append({"role": "user", "parts": [{"text": user_choice}]})
        updated_history.append({"role": "model", "parts": [{"text": f"{error_story} [IMAGE: {error_image}] CHOICE: {error_choices[0]}"}]})
        return error_story, error_image, error_choices, updated_history

    current_conversation_history = []
    if story_history:
        # Convert parts to simple text for Gemini if they are not already
        # The SDK expects a list of Content objects or dicts with role & parts (list of Part/dict)
        current_conversation_history = []
        for entry in story_history:
            # Ensure parts are in the correct format. The SDK is flexible but explicit is good.
            parts_processed = []
            if "parts" in entry and isinstance(entry["parts"], list):
                for part_item in entry["parts"]:
                    if isinstance(part_item, str): # if part is just a string
                        parts_processed.append({"text": part_item})
                    elif isinstance(part_item, dict) and "text" in part_item:
                        parts_processed.append(part_item)
                    # else, skip malformed part
            current_conversation_history.append({
                "role": entry["role"],
                "parts": parts_processed
            })


    if theme:
        # Start of a new story
        prompt = f"{BASE_SYSTEM_PROMPT}\n\nStart a new adventure story about: {theme}"
        current_conversation_history.append({"role": "user", "parts": [{"text": prompt}]})
    elif user_choice and current_conversation_history:
        # Continuing an existing story
        # The system prompt is implicitly part of the model's configuration or first user turn
        # For chat models, the history carries the context.
        # The last message in history should be from 'model'. We add the user's choice.
        prompt_text = f"The child chose: \"{user_choice}\". Continue the story."
        current_conversation_history.append({"role": "user", "parts": [{"text": prompt_text}]})
    else:
        # Should not happen with proper frontend logic
        return "Error: Invalid request to generate story.", "Error sign.", ["Start over"], []

    try:
        chat_session = model.start_chat(history=current_conversation_history[:-1]) # History up to the last user message
        last_user_message_parts = current_conversation_history[-1]['parts']
        
        # The send_message method expects a simple string or list of parts, not a full content dict
        message_to_send = ""
        if last_user_message_parts and isinstance(last_user_message_parts, list) and \
           isinstance(last_user_message_parts[0], dict) and "text" in last_user_message_parts[0]:
            message_to_send = last_user_message_parts[0]["text"]
        elif last_user_message_parts and isinstance(last_user_message_parts, list) and \
             isinstance(last_user_message_parts[0], str): # if parts is list of str
             message_to_send = last_user_message_parts[0]

        if not message_to_send:
            raise ValueError("Could not extract text from last user message parts.")

        response = await chat_session.send_message_async(message_to_send)
        llm_text_response = response.text
        
        story_text, image_prompt, choices = parse_llm_response(llm_text_response)
        
        # Update history with the model's response
        # The chat_session.history is automatically updated by the SDK
        updated_history = []
        for content in chat_session.history:
            parts_data = []
            for part in content.parts:
                 # Assuming part.text is available. For other data types, adjust accordingly.
                if hasattr(part, 'text'):
                    parts_data.append({"text": part.text})
                # else: handle other part types if necessary
            updated_history.append({"role": content.role, "parts": parts_data})
            
        return story_text, image_prompt, choices, updated_history

    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}")
        # Fallback response
        story_text = "The storyteller seems to have wandered off! Let's try to find them."
        image_prompt = "A 'missing storyteller' sign on a path in a forest."
        choices = ["Try to continue?", "Start a new story?"]
        # Return original history if call failed, or a modified one if it partially succeeded
        failed_history = current_conversation_history
        failed_history.append({"role": "model", "parts": [{"text": f"{story_text} [IMAGE: {image_prompt}] CHOICE: {choices[0]}"}]})

        return story_text, image_prompt, choices, failed_history 