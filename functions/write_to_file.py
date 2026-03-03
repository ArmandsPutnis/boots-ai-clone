import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
        is_safe = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not is_safe:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the permitted working directory, creating or overwriting it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path where the file will be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
