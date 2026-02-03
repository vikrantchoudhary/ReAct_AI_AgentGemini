import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import get_current_time,mock_search_tool

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

tools = [get_current_time,mock_search_tool]
model_id = "gemini-2.5-flash"

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
    run_agent_cycle("What time is it and what are the new features of Gemini 2.5?")
