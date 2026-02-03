import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import get_current_time,mock_search_tool
from tools_adv import get_weather,write_to_file,SENSITIVE_TOOLS
from memory import MemoryManager

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#memory added: 
memory = MemoryManager()
#tools = [get_current_time,mock_search_tool]
function_availables = {"get_weather" : get_weather,
                        "write_to_file" : write_to_file}
model_id = "gemini-2.5-flash"

def run_advance_agent_with_memory(prompt:str) :
    history = memory.get_full_history()
    chat = client.chats.create(
        model = model_id,
        config=types.GenerateContentConfig(tools=list(function_availables.values())),
        history=history
    )
    response = chat.send_message(prompt)

    #Handle parallel calls
    while any(part.function_call for part in response.candidates[0].content.parts):
        tools_result = []
        for part in response.candidates[0].content.parts:
            if fn := part.function_call:
                if fn.name is SENSITIVE_TOOLS:
                    confirm = input(f" ALLOW AGENT to run '{fn.name}' with {fn.args} ? (y/n):")
                    if confirm.lower() != 'y':
                        print( f"Permission denined for the user{fn.name}")
                        return
            print(f"Executing tool; {fn.name}")
            result = function_availables[fn.name](**fn.args)

            # result
            tools_result.append(type.Part.from_function_response(
                name=fn.name, response={"result" : result}
            ))
        memory.save_message("user", prompt)
        memory.save_message("model" ,response.text)
        print(f"\n[Agent] {response.text}")
def run_agent_cycle(user_prompt : str) :
    print(f"\n [USER] : {user_prompt}")
    chat = client.chats.create(
        model = model_id,
        config=types.GenerateContentConfig(
            tools = tools,
            system_instruction="You are helpful AI agent. use tools when necessarey to provide accurate info"
        )
    )
    response = chat.send_message(user_prompt)

    while response.candidates[0].content.parts[0].function_call:
        fc = response.candidates[0].content.parts[0].function_call
        print(f"--- 💡 Agent Reasoning: Needs to call {fc.name} with {fc.args}")
        available_functions = {
            "get_current_time": get_current_time,
            "mock_search_tool": mock_search_tool
        }
        
        tool_to_call = available_functions[fc.name]
        observation = tool_to_call(**fc.args)
        print(f"--- 🛠️ Action Output (Observation): {observation}")
        response = chat.send_message(
            types.Part.from_function_response(
                name=fc.name,
                response={"result": observation}
            )
        )

    
    print(f"\n[AGENT]: {response.text}")
def main():
    print("Hello from reactagentgemini!")


if __name__ == "__main__":
    run_advance_agent_with_memory("Check the weather in Paris and then save a summary to 'report.txt'.")
    #run_agent_cycle("What time is it and what are the new features of Gemini 2.5?")
