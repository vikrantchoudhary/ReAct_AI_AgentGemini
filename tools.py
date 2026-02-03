import datetime

def get_current_time(location: str = "local"):
    now = datetime.datetime.now()
    return f"The currrent time in {location} is {now.strftime('%H:%M:%S')}"

def mock_search_tool(query : str):
    database = {
        "Gemini 2.5 features": "Gemini 2.5 Flash introduced native thinking and adaptive reasoning levels.",
        "Nvidia stock": "NVDA is currently trading at $1,250.00 (Mock Data)."
    }
    return database.gry(query, "No specific info available, try broder search")