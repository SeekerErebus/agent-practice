import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001'


def main():
    parser = argparse.ArgumentParser(description="Sends a prompt to Google Gemini and gives the response.")
    parser.add_argument('prompt', help="The prompt to ask Gemini.")
    parser.add_argument('--verbose', '-v', action='store_true', help="Use verbose output")
    args = parser.parse_args()
    user_prompt = args.prompt
    verbose_mode = args.verbose

    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    gemini_response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if verbose_mode:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {gemini_response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {gemini_response.usage_metadata.candidates_token_count}')
    print(gemini_response.text)


if __name__ == "__main__":
    main()
