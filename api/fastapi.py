# api/fastapi.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import re

app = FastAPI()

# Enable CORS to allow any origin to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Example FastAPI endpoints (same as previous ones)
def get_ticket_status(ticket_id: int):
    return {"ticket_id": ticket_id, "status": "In Progress"}

def schedule_meeting(date: str, time: str, meeting_room: str):
    return {"date": date, "time": time, "meeting_room": meeting_room, "status": "Scheduled"}

def get_expense_balance(employee_id: int):
    return {"employee_id": employee_id, "balance": 1500.75}

def calculate_performance_bonus(employee_id: int, current_year: int):
    return {"employee_id": employee_id, "year": current_year, "bonus": 5000.00}

def report_office_issue(issue_code: int, department: str):
    return {"issue_code": issue_code, "department": department, "status": "Reported"}

# Query parsers (same as before)
def parse_ticket_status(query: str):
    match = re.match(r"^What is the status of ticket (\d+)\?$", query)
    if match:
        return {"name": "get_ticket_status", "arguments": json.dumps({"ticket_id": int(match.group(1))})}
    return None

def parse_schedule_meeting(query: str):
    match = re.match(r"^Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.$", query)
    if match:
        return {"name": "schedule_meeting", "arguments": json.dumps({
            "date": match.group(1),
            "time": match.group(2),
            "meeting_room": match.group(3)
        })}
    return None

def parse_expense_balance(query: str):
    match = re.match(r"^Show my expense balance for employee (\d+)\.$", query)
    if match:
        return {"name": "get_expense_balance", "arguments": json.dumps({"employee_id": int(match.group(1))})}
    return None

def parse_performance_bonus(query: str):
    match = re.match(r"^Calculate performance bonus for employee (\d+) for (\d{4})\.$", query)
    if match:
        return {"name": "calculate_performance_bonus", "arguments": json.dumps({
            "employee_id": int(match.group(1)),
            "current_year": int(match.group(2))
        })}
    return None

def parse_office_issue(query: str):
    match = re.match(r"^Report office issue (\d+) for the (.+) department\.$", query)
    if match:
        return {"name": "report_office_issue", "arguments": json.dumps({
            "issue_code": int(match.group(1)),
            "department": match.group(2)
        })}
    return None

# Main route
@app.get("/execute")
async def execute(q: str):
    # Try each query parser and return the matching response
    for parser in [parse_ticket_status, parse_schedule_meeting, parse_expense_balance, parse_performance_bonus, parse_office_issue]:
        result = parser(q)
        if result:
            return result

    return {"error": "Invalid query format"}

