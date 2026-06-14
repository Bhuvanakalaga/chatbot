

import os
import pandas as pd

#Path
CSV_PATH = os.path.join("data", "employees.csv")

_df: pd.DataFrame | None = None


def _get_df() -> pd.DataFrame:
    """Load the CSV once and cache it. Return the cached DataFrame."""
    global _df
    if _df is None:
        _df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
        # Normalise emp_id to uppercase for case-insensitive lookups
        _df["emp_id"] = _df["emp_id"].str.upper().str.strip()
        print(f"[EmployeeDB] Loaded {len(_df)} employees from {CSV_PATH}")
    return _df


def validate_employee(emp_id: str) -> dict:
    """
    Check whether an employee ID exists.
    Returns {"valid": True/False, "message": str}
    """
    df = _get_df()
    emp_id = emp_id.upper().strip()
    row = df[df["emp_id"] == emp_id]
    if row.empty:
        return {"valid": False, "message": f"Employee {emp_id} not found in the system."}
    status = row.iloc[0]["employment_status"]
    return {"valid": True, "message": f"Employee {emp_id} is a valid employee. Status: {status}"}


def get_employee_profile(emp_id: str) -> dict:
    """
    Return profile fields for a given employee ID.
    Returns a dict with employee details, or an error message.
    """
    df = _get_df()
    emp_id = emp_id.upper().strip()
    row = df[df["emp_id"] == emp_id]
    if row.empty:
        return {"error": f"Employee {emp_id} not found."}
    r = row.iloc[0]
    return {
        "Employee ID":    r["emp_id"],
        "Name":           r["full_name"],
        "Department":     r["department"],
        "Designation":    r["designation"],
        "Email":          r["email"],
        "Manager":        r["manager_name"],
        "Joining Date":   r["joining_date"],
        "Work Location":  r["work_location"],
        "Status":         r["employment_status"],
    }


def get_leave_balance(emp_id: str) -> dict:
    """
    Return leave balance for a given employee ID.
    """
    df = _get_df()
    emp_id = emp_id.upper().strip()
    row = df[df["emp_id"] == emp_id]
    if row.empty:
        return {"error": f"Employee {emp_id} not found."}
    r = row.iloc[0]
    return {
        "Employee ID":   r["emp_id"],
        "Name":          r["full_name"],
        "Leave Balance": r["leave_balance"] + " days",
        "Status":        r["employment_status"],
    }