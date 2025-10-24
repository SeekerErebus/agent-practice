import os, sys, importlib.util
from functions.file_access_confirmation import confirm_file_read


constants_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'constants.py'
)
spec = importlib.util.spec_from_file_location("constants", constants_path)
constants = importlib.util.module_from_spec(spec)
sys.modules["constants"] = constants
spec.loader.exec_module(constants)


def get_file_content(working_directory, file_path):
    try:
        abs_file_path = confirm_file_read(working_directory, file_path)

        with open(abs_file_path) as f:
            file_content_string = f.read(constants.MAX_API_CHARACTERS)
            exceeds_limit = len(file_content_string) == constants.MAX_API_CHARACTERS and bool(f.read(1))
        if exceeds_limit:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return(f'    Error: {e}')
