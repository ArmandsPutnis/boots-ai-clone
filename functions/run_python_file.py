import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout.strip() and not result.stderr.strip():
            output_parts.append("No output produced")
        else:
            if result.stdout.strip():
                output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
            if result.stderr.strip():
                output_parts.append(f"STDERR:\n{result.stderr.strip()}")
        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"


from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the permitted working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script.",
            ),
        },
        required=["file_path"],
    ),
)
