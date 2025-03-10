import litellm
import os
import subprocess

def get_current_weather(location, unit="celsius"):
    os.environ['GROQ_API_KEY'] = "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"

    messages = [{"role": "system", "content": """Generate a Python script that fetches the current weather for a given location using the OpenWeatherMap API. The script should:
    - the script be function ask for the location and the unit of temperature (eg.def func(location, unit))
    - Use the `requests` library to make an API call.
    - Use the OpenWeatherMap API key `c59414a31d0342f7b8799b2a07440798`.
    - Accept a location (city, state, country) from user input.
    - The code must give temperature in asked unit.
    - Return the location,temperature and weather description in JSON format.
    - Use  errors handling where ever needed.
    - the script must contain the only the weather fetching function.
    Respond with only python code donot generate additional texts
    """},
         {"role": "user", "content": f"location {location}, unit : {unit}"}       
        ]

    try:
        response = litellm.completion(
            model="groq/llama3-70b-8192",
            messages=messages,
        )

        generated_code = response.choices[0].message.content.strip('```')

        # Saving the generated code to a Python file
        file_name = "weather_fetcher.py"
        with open(file_name, "w") as f:
            f.write(generated_code)

        #print(f"Generated Python script saved as {file_name}")

        # Run the generated script and capture output
        result = subprocess.run(["python", "weather_fetcher.py"], capture_output=True, text=True)
        
        # Write both stdout and stderr to a file
        with open("output.txt", "w") as output_file:
            #output_file.write("Standard Output:\n")
            output_file.write(result.stdout)
            #output_file.write("\nStandard Error:\n")
            output_file.write(result.stderr)
            
        #print("Output and errors from weather_fetcher.py have been saved to output.txt")

        # Read and return the output file content
        with open("output.txt", "r") as file:
            output_content = file.read()
        
        return output_content

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return error_message