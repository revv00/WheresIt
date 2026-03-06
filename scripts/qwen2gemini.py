import json
import uuid
import argparse
import os
import sys
from datetime import datetime

# Default settings based on the Gemini AI Studio example provided
DEFAULT_RUN_SETTINGS = {
    "temperature": 1.0,
    "model": "models/gemini-1.5-pro-latest", # Defaulting to a generally available model
    "topP": 0.95,
    "topK": 64,
    "maxOutputTokens": 8192,
    "safetySettings": [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "OFF"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "OFF"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "OFF"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "OFF"}
    ],
    "enableCodeExecution": False,
    "enableSearchAsATool": False,
    "enableBrowseAsATool": False,
    "enableAutoFunctionResponse": False,
    "thinkingBudget": -1
}

def extract_text_from_qwen_msg(msg):
    """Extracts text content from various Qwen message formats."""
    text_content = ""
    
    # Direct content string
    if msg.get("content") and isinstance(msg.get("content"), str):
        text_content = msg.get("content")
    # Content list (common in multimodal messages)
    elif msg.get("content_list"):
        for item in msg.get("content_list", []):
            if item.get("content"):
                text_content += item.get("content")
    
    # Handle files/images by appending a reference (AI Studio prompt text format)
    if "files" in msg and msg["files"]:
        for file_item in msg["files"]:
            url = file_item.get("url", "")
            name = file_item.get("name", "file")
            if url:
                text_content += f"\n\n[Attached File: {name} - {url}]"

    # Append reasoning content if it exists (DeepSeek/Qwen-Reasoning style)
    if msg.get("reasoning_content"):
        text_content = f"**Reasoning Process:**\n{msg['reasoning_content']}\n\n**Response:**\n{text_content}"

    return text_content

def convert_qwen_to_gemini(qwen_data):
    converted_files = []

    # Handle both wrapped "data" dict and raw list formats
    chat_list = qwen_data.get("data", [])
    if not chat_list and isinstance(qwen_data, list):
        chat_list = qwen_data

    for chat_session in chat_list:
        # --- 1. Flatten the Qwen Tree ---
        history = chat_session.get("chat", {}).get("history", {})
        messages_lst = chat_session.get("chat", {}).get("messages", {})
        messages_map = history.get("messages", {})
        
        if not messages_map:
            continue

        # Find root
        root_msg = None
        for msg_id, msg_data in messages_map.items():
            if msg_data.get("parentId") is None:
                root_msg = msg_data
                break
        
        if not root_msg:
            continue

        # Trace timeline
        linear_messages = []
        current_msg = root_msg
        
        while current_msg:
            linear_messages.append(current_msg)
            children = current_msg.get("childrenIds", [])
            if children:
                # Follow the first child (main path)
                next_id = children[0] 
                current_msg = messages_map.get(next_id)
            else:
                current_msg = None

        # --- 2. Build Gemini Structure ---
        
        gemini_chunks = []
        system_instruction_parts = []

        for msg in linear_messages:
            role = msg.get("role", "user")
            text = extract_text_from_qwen_msg(msg)

            if not text.strip():
                continue

            # Map Qwen roles to Gemini roles
            if role == "system":
                # System prompts go into a specific 'systemInstruction' block in AI Studio
                system_instruction_parts.append(text)
                continue
            elif role == "assistant":
                gemini_role = "model"
            else:
                gemini_role = "user"

            chunk = {
                "text": text,
                "role": gemini_role
            }
            # Optional: Add token count if available/estimated, otherwise AI Studio calculates it
            # chunk["tokenCount"] = 0 
            
            gemini_chunks.append(chunk)

        # Construct final object
        gemini_file_structure = {
            "runSettings": DEFAULT_RUN_SETTINGS.copy(),
            "systemInstruction": {}, # Default empty
            "chunkedPrompt": {
                "chunks": gemini_chunks
            }
        }

        # Populate system instruction if we found system messages
        if system_instruction_parts:
            # AI Studio system instruction format is often parts-based or simple text
            # We'll use the 'parts' format which is robust
            gemini_file_structure["systemInstruction"] = {
                "parts": [{"text": "\n".join(system_instruction_parts)}]
            }

        # Metadata for filename generation
        title = chat_session.get("title", "untitled").replace("/", "_").replace("\\", "_")
        chat_id = chat_session.get("id", str(uuid.uuid4()))
        date_str = datetime.fromtimestamp(messages_lst[0]['timestamp']).strftime("%Y%m%d")
        converted_files.append({
            "filename": f"{date_str}_{title[:50]}.json",
            "content": gemini_file_structure
        })

    return converted_files

def main():
    parser = argparse.ArgumentParser(description="Convert Qwen Chat export JSON to Gemini AI Studio format.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input Qwen JSON file.")
    parser.add_argument("--output", "-o", required=True, help="Path to the output directory.")
    
    args = parser.parse_args()

    # Input Validation
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    # Output Directory Creation
    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
            print(f"Created output directory: {args.output}")
        except OSError as e:
            print(f"Error creating directory {args.output}: {e}")
            sys.exit(1)

    # Processing
    print(f"Reading {args.input}...")
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            qwen_source = json.load(f)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        sys.exit(1)

    results = convert_qwen_to_gemini(qwen_source)
    print(f"Found {len(results)} conversations to convert.")

    # Writing Files
    for item in results:
        out_path = os.path.join(args.output, item["filename"].replace(' ', '_'))
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(item["content"], f, indent=2, ensure_ascii=False)
            # print(f"Saved: {item['filename']}")
        except IOError as e:
            print(f"Error writing {item['filename']}: {e}")

    print(f"Conversion complete. Files saved to '{args.output}'")

if __name__ == "__main__":
    main()
