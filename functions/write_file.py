import os, sys
from functions.file_access_confirmation import confirm_file_write
#from file_access_confirmation import confirm_file_write


def write_file(working_directory, file_path, content):
    try:
        abs_file_path = confirm_file_write(working_directory, file_path)

        with open(abs_file_path, "w") as f:
            written_count = f.write(content)
        return f'Successfully wrote to "{file_path}" ({written_count} characters written)'
    except Exception as e:
        return(f'    Error: {e}')


def main():
    output = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(output)

if __name__ == "__main__":
    main()