#Imports
import litellm
import json
import os

from weather import get_current_weather

#Api key

os.environ['GROQ_API_KEY'] = "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"


#JSON schema for the function call
tools =[
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    },
]

# Function call

messages = [{"role": "user", "content": "whats the weather in chennai"}]

response = litellm.completion(
    model="groq/llama3-70b-8192",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
print("\nLLM Response1:\n", response.choices[0].message.content)
response_message = response.choices[0].message
tool_calls = response.choices[0].message.tool_calls

# Extract the tool call

print("\nTool call:\n", tool_calls)

# Extract the function call


available_functions = {
    "get_current_weather": get_current_weather
}


if tool_calls:
    messages.append(response_message)

    for tool_call in tool_calls:
        print(f"\nExecuting tool call\n{tool_call}")
        function_name = tool_call.function.name

        if function_name in available_functions:
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            # Call the appropriate function
            function_response = function_to_call(**function_args)

            # Display result
            print(f"Result from tool call\n{function_response}\n")

            # Extend conversation with function response
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),  # Ensure response is a string
                }
            )
        else:
            print(f"Function name '{function_name}' not found")

    # Get the final response
    
    
second_response = litellm.completion(
    model="groq/llama3-70b-8192",
    messages=messages,
    tools = tools
)
print("Second Response\n", second_response.choices[0].message.content)
