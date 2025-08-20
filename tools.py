from datetime import datetime

# Simple in-memory notes
NOTES = []

def get_time():
    """Return current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calc(expression: str):
    """Evaluate math expression safely"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {e}"

def notes_tool(action: str, note: str = ""):
    """Add or list notes"""
    global NOTES
    if action == "add" and note:
        NOTES.append(note)
        return f"Note added: {note}"
    elif action == "list":
        if not NOTES:
            return "No notes saved."
        return "\n".join([f"{i+1}. {n}" for i, n in enumerate(NOTES)])
    else:
        return "Invalid notes command."
