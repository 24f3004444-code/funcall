from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import re
from typing import Dict

# Create FastAPI instance
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Function definitions (these are just placeholders for now)
def get_ticket_status(ticket_id: int):
    return f"Ticket {ticket_id} status: Open"

def schedule_meeting(date: str, time: str, meeting_room: str):
    return f"Meeting scheduled on {date} at {time} in {meeting_room}"

def get_expense_balance(employee_id: int):
    return f"Employee {employee_id} expense balance: $500"

def calculate_performance_bonus(employee_id: int, current_year: int):
    return f"Employee {employee_id} performance bonus for {current_year}: $2000"

def report_office_issue(issue_code: int, department: str):
    return f"Office issue {issue_code} reported for {department} department"

# Helper function to extract parameters from queries
def parse_query(q: str) -> Dict[str, str]:
    # Ticket status: "What is the status of ticket 83742?"
    ticket_match = re.match(r"What is the status of ticket (\d+)\?", q)
    if ticket_match:
        return {"name": "get_ticket_status", "arguments": {"ticket_id": int(ticket_match.group(1))}}

    # Meeting scheduling: "Schedule a meeting on 2025-02-15 at 14:00 in Room A."
    meeting_match = re.match(r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q)
    if meeting_match:
        return {
            "name": "schedule_meeting",
            "arguments": {
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3)
            }
        }

    # Expense balance: "Show my expense balance for employee 10056."
    expense_match = re.match(r"Show my expense balance for employee (\d+)\.", q)
    if expense_match:
        return {"name": "get_expense_balance", "arguments": {"employee_id": int(expense_match.group(1))}}

    # Performance bonus: "Calculate performance bonus for employee 10056 for 2025."
    bonus_match = re.match(r"Calculate performance bonus for employee (\d+) for (\d{4})\.", q)
    if bonus_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": {
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            }
        }

    # Office issue: "Report office issue 45321 for the Facilities department."
    issue_match = re.match(r"Report office issue (\d+) for the (\w+) department\.", q)
    if issue_match:
        return {
            "name": "report_office_issue",
            "arguments": {
                "issue_code": int(issue_match.group(1)),
                "department": issue_match.group(2)
            }
        }

    # If no match found
    return None

# Endpoint to process the query
@app.get("/execute")
async def execute_query(q: str):
    # Parse the query to find the appropriate function and arguments
    result = parse_query(q)
    
    if result is None:
        return JSONResponse(status_code=400, content={"error": "Unable to parse query."})

    # Return the function name and arguments in the specified format
    return result
