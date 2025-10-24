from google.genai import types
from functions.schema import available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part: types.FunctionCall, working_directory, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args or {}
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    result = ''
    match function_name:
        case 'get_files_info':
            result = get_files_info(working_directory=working_directory, **function_args)
        case 'get_file_content':
            result = get_file_content(working_directory=working_directory, **function_args)
        case 'write_file':
            result = write_file(working_directory=working_directory, **function_args)
        case 'run_python_file':
            result = run_python_file(working_directory=working_directory, **function_args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={'error': f'Unknown function: {function_name}'},
                    )
                ]
            )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={'output': result}
            )
        ]
    )
    


def main():
    function_call_part = types.FunctionCall(name='get_files_info')
    
    output = call_function(function_call_part=function_call_part, working_directory='./calculator', verbose=True)
    print(output)

if __name__ == "__main__":
    main()
