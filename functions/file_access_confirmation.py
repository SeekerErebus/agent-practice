import os
from enum import Enum


class Error_Forms(Enum):
    READ_DIR = 1
    READ_FILE = 2
    WRITE_DIR = 3
    WRITE_FILE = 4
    NOT_DIR = 5
    NOT_FILE = 6
    EXEC_PYTHON = 7
    NOT_PYTHON = 8

def viable_directory(working_directory: str, file_path = ''):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    is_not_valid_path = not os.path.commonpath([abs_file_path, abs_working]) == abs_working
    return abs_file_path, is_not_valid_path, abs_working

def confirm_directory(working_directory: str, directory="."):
    abs_directory, is_not_valid_path, _ = viable_directory(working_directory, directory)
    if is_not_valid_path:
        raise ValueError(error_text(Error_Forms.READ_DIR, directory))
    if not os.path.isdir(abs_directory):
        raise ValueError(error_text(Error_Forms.NOT_DIR, directory))
    return abs_directory

def confirm_file_read(working_directory: str, file_path = ''):
    abs_file_path, is_not_valid_path, _ = viable_directory(working_directory, file_path)
    if is_not_valid_path:
        raise ValueError(error_text(Error_Forms.READ_FILE, file_path))
    if not os.path.isfile(abs_file_path):
        raise ValueError(error_text(Error_Forms.NOT_FILE, file_path))
    return abs_file_path

def confirm_file_write(working_directory: str, file_path = ''):
    abs_file_path, is_not_valid_path, _ = viable_directory(working_directory, file_path)
    if is_not_valid_path:
        raise ValueError(error_text(Error_Forms.WRITE_FILE, file_path))
    return abs_file_path

def confirm_python_execute(working_directory: str, file_path = ''):
    abs_file_path, is_not_valid_path, abs_working = viable_directory(working_directory, file_path)
    if is_not_valid_path:
        raise ValueError(error_text(Error_Forms.EXEC_PYTHON, file_path))
    if not os.path.isfile(abs_file_path):
        raise ValueError(error_text(Error_Forms.NOT_FILE, file_path))
    if not abs_file_path.endswith('.py'):
        raise ValueError(error_text(Error_Forms.NOT_PYTHON, file_path))
    return abs_file_path, abs_working


def error_text(format: Error_Forms, file_path: str):
    match format:
        case Error_Forms.READ_DIR:
            return f'Cannot list "{file_path}" as it is outside the permitted working directory'
        case Error_Forms.WRITE_DIR:
            return f'Cannot make directory "{file_path}" as it is outside the permitted working directory'
        case Error_Forms.READ_FILE:
            return f'Cannot read "{file_path}" as it is outside the permitted working directory'
        case Error_Forms.WRITE_FILE:
            return f'Cannot write to "{file_path}" as it is outside the permitted working directory'
        case Error_Forms.NOT_DIR:
            return f'"{file_path}" is not a directory'
        case Error_Forms.NOT_FILE:
            return f'File "{file_path}" not found.'
        case Error_Forms.EXEC_PYTHON:
            return f'Cannot execute "{file_path}" as it is outside the permitted working directory'
        case Error_Forms.NOT_PYTHON:
            return f'"{file_path}" is not a Python file.'
        case _:
            raise Exception("Unknown Format.")
