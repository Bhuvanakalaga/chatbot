# All LangChain tools for the HR Assistant.

import random
from datetime import datetime
from langchain_core.tools import tool
from retriever import search_policy_chunks
import employee_db


# 1. search_policy 

@tool
def search_policy(query: str) -> str:
    """
    Search the HR policy knowledge base for any policy topic.
    Use for: leave, attendance, WFH, salary, benefits, insurance,
    reimbursements, notice period, code of conduct, resignation, POSH.
    Input: natural-language query.
    """
    return search_policy_chunks(query, k=4)


# 2. summarize_policy 

@tool
def summarize_policy(topic: str) -> str:
    """
    Get a concise summary of a specific HR policy topic.
    Use when the employee wants a brief overview of a policy area.
    Input: topic name e.g. "leave policy", "WFH policy".
    """
    return search_policy_chunks(topic, k=4)


# 3. validate_employee 

@tool
def validate_employee(employee_id: str) -> str:
    """
    Verify whether an employee ID exists in the system.
    ALWAYS call this before get_employee_profile or get_leave_balance.
    Input: employee ID e.g. "EMP001".
    """
    result = employee_db.validate_employee(employee_id)
    return result["message"]


#  4. get_employee_profile 

@tool
def get_employee_profile(employee_id: str) -> str:
    """
    Retrieve the full profile of an employee.
    Only call this AFTER validate_employee confirms the employee exists.
    Returns: name, department, designation, email, manager, joining date, location.
    Input: employee ID e.g. "EMP001".
    """
    result = employee_db.get_employee_profile(employee_id)
    if "error" in result:
        return result["error"]
    return "\n".join(f"{k}: {v}" for k, v in result.items())


#  5. get_leave_balance 

@tool
def get_leave_balance(employee_id: str) -> str:
    """
    Retrieve the current leave balance for an employee.
    Only call this AFTER validate_employee confirms the employee exists.
    Input: employee ID e.g. "EMP001".
    Returns: employee name and available leave balance in days.
    """
    result = employee_db.get_leave_balance(employee_id)
    if "error" in result:
        return result["error"]
    return "\n".join(f"{k}: {v}" for k, v in result.items())


#  6. create_hr_ticket 

@tool
def create_hr_ticket(issue: str) -> str:
    """
    Create an HR support ticket for service requests.
    Use ONLY after the employee has explicitly confirmed they want a ticket created.
    Use for: salary certificate requests, reimbursement issues, payroll problems,
    employment verification letters, benefits support, general HR assistance.
    Do NOT use for harassment, bullying, discrimination, or grievances — use create_grievance instead.
    Input: description of the employee's support request.
    """
    ticket_id = f"TKT-{random.randint(10000, 99999)}"
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    return (
        f"HR Support Ticket Created\n\n"
        f"Ticket ID    : {ticket_id}\n"
        f"Type         : Support Request\n"
        f"Priority     : Normal\n"
        f"Status       : Open\n"
        f"Created At   : {timestamp}\n"
        f"Summary      : {issue[:200]}\n\n"
        f"An HR representative will follow up within 2 working days.\n"
        f"Please save your Ticket ID {ticket_id} for reference."
    )


# 7. create_grievance

@tool
def create_grievance(issue: str) -> str:
    """
    Escalate a formal HR grievance.
    Use ONLY after the employee has explicitly confirmed they want to escalate.
    Use for: harassment, sexual harassment, bullying, discrimination, retaliation,
    manager misconduct, ethics complaints, hostile work environment, unsafe workplace.
    Do NOT use for general service requests — use create_hr_ticket instead.
    Input: description of the grievance or complaint.
    """
    case_id = f"GRV-{random.randint(10000, 99999)}"
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    return (
        f" Formal HR Grievance Escalated\n\n"
        f"Case ID      : {case_id}\n"
        f"Type         : Formal Grievance\n"
        f"Priority     : High\n"
        f"Status       : Escalated to HR Team\n"
        f"Created At   : {timestamp}\n"
        f"Summary      : {issue[:200]}\n\n"
        f"This has been flagged as high priority and assigned to a senior HR representative.\n"
        f"You will be contacted within 1 working day. All communications are strictly confidential.\n"
        f"Please save your Case ID {case_id} for reference."
    )


# 8. hr_contact

@tool
def hr_contact(query: str = "contact") -> str:
    """
    Provide HR department contact details.
    Use when an employee asks how to reach HR, wants HR email or phone number.
    Do NOT create tickets when this tool is used.
    """
    return (
        "HR Department Contact Details\n\n"
        " Email        : hr@company.com\n"
        " Phone        : +91-XXXXXXXXXX\n"
        " HR Helpdesk  : Available on the HRMS portal\n"
        " Working Hours: Monday – Friday, 9:00 AM – 6:00 PM\n\n"
        "For urgent matters, email hr@company.com with URGENT in the subject line."
    )


# Export

ALL_TOOLS = [
    search_policy,
    summarize_policy,
    validate_employee,
    get_employee_profile,
    get_leave_balance,
    create_hr_ticket,
    create_grievance,
    hr_contact,
]