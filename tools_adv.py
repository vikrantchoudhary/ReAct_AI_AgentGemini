# parallel actions and safety gate

import subprocess

def get_weather(city : str) :
    return f"The weather in {city} is sunny , 22 degree."

def write_to_file(filename: str, content: str):
    with open(filename,"w") as f:
        f.write(content)
    return f"Successfully written to the file {filename}"

SENSITIVE_TOOLS=["write_to_file"]