import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schema import available_functions
from functions.call_function import call_function


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

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    model_config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
    working_directory = './calculator'
    output_string = ''
    verbose_string = f'\n\nUser prompt: {user_prompt}\n'

    llm_agent_iteration_count = 20
    did_complete = False
    try:
        for iter in range(llm_agent_iteration_count):

            gemini_response = client.models.generate_content(
                model=model_name, 
                contents=messages,
                config=model_config,
            )
            verbose_string += f'Iteration count: {iter+1}'
            verbose_string += f'  Prompt tokens: {gemini_response.usage_metadata.prompt_token_count}\n'
            verbose_string += f'  Response tokens: {gemini_response.usage_metadata.candidates_token_count}\n'
            candidate = gemini_response.candidates[0]
            messages.append(candidate.content)
            function_calls = [part.function_call for part in candidate.content.parts if part.function_call]
            if not function_calls:
                output_string += gemini_response.text
                did_complete = True
                break
            for function_call_part in function_calls:
                tool_content = call_function(function_call_part=function_call_part, working_directory=working_directory, verbose=verbose_mode)
                call_result = tool_content.parts[0].function_response
                if call_result.response == None:
                    raise SystemExit(1, "Fatal Exception: API didn't return a function response.")
                verbose_string += f'  -> {call_result.response}\n'
                user_part = types.Part(function_response=call_result)
                messages.append(types.Content(role="user", parts=[user_part]))
            
            if verbose_mode:
                #verbose_string += f'Full response object:\n{gemini_response}\n'
                print(verbose_string)
            verbose_string = ''
        if verbose_mode: print(verbose_string)
        if not did_complete:
            print("Gemini has failed to answer in a reasonable number of toolcalls.")
            sys.exit(1)
        print(output_string)
    except Exception as e:
        print(f'Error: {e}')
    

if __name__ == "__main__":
    main()
