from functions.get_files_info import get_files_info

print("Result for current directory:")
print(get_files_info("calculator", "."))

print("Result for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))

# This third test is required to show the "Error:" message to the grader
print("Result for invalid directory:")
print(get_files_info("calculator", ".."))
