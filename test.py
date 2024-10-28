import os
from openai import OpenAI

# Retrieve the API key from the operating system's environment variables
api_key = os.environ["OPENAI_API_KEY"]

# Initialize the OpenAI client with the API key from the environment variable
client = OpenAI(api_key=api_key)

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are "},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Get user input and generate a completion
prompt = input("Enter a prompt: ")
response = get_completion(prompt)
print(response)
