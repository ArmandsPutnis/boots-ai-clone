import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Api Key not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Initialize conversation history with the user's prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)

    # The Agent Loop: limit to 20 iterations to prevent infinite loops
    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("Failed to retrieve usage data")

        if args.verbose:
            print(f"--- Iteration {i + 1} ---")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Add the model's response (candidates) to history so it remembers its own thoughts/calls
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Check if the model wants to call any functions
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                # Execute the function call
                result_content = call_function(function_call, verbose=args.verbose)

                if not result_content.parts:
                    raise RuntimeError("Function call result has no parts")

                part = result_content.parts[0]
                if (
                    part.function_response is None
                    or part.function_response.response is None
                ):
                    raise RuntimeError("Invalid function response structure")

                # Collect the result part
                function_responses.append(part)

                if args.verbose:
                    print(f"-> {part.function_response.response}")

            # Add the function results back to history as a 'user' role
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            # If no function calls are requested, the agent has its final answer
            print("\nFinal response:")
            print(response.text)
            return

    # If we reach here, the loop finished without a final response
    print("\nError: Maximum iterations (20) reached without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
