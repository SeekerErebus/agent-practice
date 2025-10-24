import os
from functions.file_access_confirmation import confirm_directory


def get_files_info(working_directory, directory="."):
    try:
        abs_directory = confirm_directory(working_directory, directory)

#'result_string' formatting
#Result for current directory:
# - main.py: file_size=719 bytes, is_dir=False
# - tests.py: file_size=1331 bytes, is_dir=False
# - pkg: file_size=44 bytes, is_dir=True
        result_string = ''
        dir_contents = os.listdir(abs_directory)

        for content in dir_contents:
            file_path = os.path.join(abs_directory,content)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            result_string += f' - {content}: '
            result_string += f'file_size={file_size} bytes, is_dir={is_dir}'
            result_string += '\n'

        return result_string
    except Exception as e:
        return(f'    Error: {e}')
