import sys, subprocess
from functions.file_access_confirmation import confirm_python_execute
#from file_access_confirmation import confirm_python_execute


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_file_path, abs_working = confirm_python_execute(working_directory, file_path)
    except Exception as e:
        return(f'    Error: {e}')
    
    try:
        cmd = [sys.executable, '-u', abs_file_path] + args
        result = subprocess.run(
            cmd,
            cwd=abs_working,
            capture_output=True,
            text=True,
            timeout=30
        )
    except Exception as e:
        return(f"    Error: executing Python file: {e}")
    
    try:
        output = ''
        if result.stdout == '':
            output += f'No output produced.\n'
        else:
            output += f'STDOUT: {result.stdout}\n'
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}\n'
        if result.stderr != '':
            output += f'STDERR: {result.stderr}\n'
        return output
    except Exception as e:
        return(f'    Error: {e}')


def main():
    output = run_python_file("calculator", "lorem.txt")
    print(f'output: {output}')

if __name__ == "__main__":
    main()