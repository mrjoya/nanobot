"""
Cost control safeguards for fal.ai API calls.

This module provides cost control mechanisms to prevent accidental
excessive API usage and unexpected charges.

IMPORTANT: These safeguards should be used with ALL API calls!
"""

import os
import sys
from datetime import datetime
from pathlib import Path


# Cost tracking log file
COST_LOG_PATH = Path(__file__).parent.parent / "cost_log.json"

# Maximum default daily spend
DEFAULT_DAILY_LIMIT = 5.0  # $5.00 maximum per day

# Global tracking
_SESSION_COST = 0.0


def cost_confirmation(cost, description="API call"):
    """
    Show cost confirmation dialog for potentially expensive operations.
    
    Args:
        cost: Estimated cost in USD
        description: Description of the operation
    
    Returns:
        True if confirmed, False if rejected
    
    This should be used before any real API call that costs money.
    """
    # Always show the warning
    print(f"\n⚠️ COST WARNING: This {description} will cost ${cost:.2f}")
    
    # Skip in CI/CD environments or if explicitly disabled
    if os.environ.get("NANOBOT_SKIP_CONFIRM") == "1":
        print("Automatic confirmation (NANOBOT_SKIP_CONFIRM=1)")
        return True
    
    # Check for dry run mode
    if os.environ.get("NANOBOT_DRY_RUN") == "1":
        print("Skipping API call (NANOBOT_DRY_RUN=1)")
        return False
    
    # Check for daily limit
    if _would_exceed_daily_limit(cost):
        print(f"❌ This would exceed your daily limit of ${_get_daily_limit():.2f}")
        override = input("Override daily limit? (yes/no): ").lower() == "yes"
        if not override:
            return False
    
    # Interactive confirmation
    try:
        confirm = input(f"Proceed with this ${cost:.2f} operation? (y/n): ")
        return confirm.lower() in ('y', 'yes')
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled by user.")
        return False


def track_cost(cost, operation_type, details=None):
    """
    Track API call costs in the cost log.
    
    Args:
        cost: Cost in USD
        operation_type: Type of operation (e.g., "generate", "edit")
        details: Additional details (e.g., resolution, num_images)
    
    This helps monitor and audit API usage over time.
    """
    global _SESSION_COST
    _SESSION_COST += cost
    
    import json
    from datetime import datetime
    
    # Create log entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "cost": cost,
        "operation": operation_type,
        "details": details or {},
        "cumulative_session": _SESSION_COST,
    }
    
    # Load existing log
    try:
        if COST_LOG_PATH.exists():
            with open(COST_LOG_PATH, 'r') as f:
                log = json.load(f)
        else:
            log = {"entries": [], "total_cost": 0.0}
    except Exception as e:
        print(f"Error loading cost log: {e}")
        log = {"entries": [], "total_cost": 0.0}
    
    # Update log
    log["entries"].append(entry)
    log["total_cost"] = sum(e["cost"] for e in log["entries"])
    log["last_updated"] = datetime.now().isoformat()
    
    # Save log
    COST_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(COST_LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)
    
    # Print confirmation
    print(f"💰 Cost tracked: ${cost:.2f} for {operation_type}")
    print(f"   Session total: ${_SESSION_COST:.2f}")


def get_cost_report(days=7):
    """
    Generate a cost usage report for the specified period.
    
    Args:
        days: Number of days to include in the report
        
    Returns:
        Formatted cost report as string
    """
    import json
    from datetime import datetime, timedelta
    
    try:
        if not COST_LOG_PATH.exists():
            return "No cost log found."
        
        with open(COST_LOG_PATH, 'r') as f:
            log = json.load(f)
        
        if not log.get("entries"):
            return "No cost entries found."
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter entries by date
        filtered_entries = []
        for entry in log["entries"]:
            try:
                entry_date = datetime.fromisoformat(entry["timestamp"])
                if start_date <= entry_date <= end_date:
                    filtered_entries.append(entry)
            except (ValueError, KeyError):
                continue
        
        if not filtered_entries:
            return f"No cost entries found in the last {days} days."
        
        # Calculate totals
        total_cost = sum(entry["cost"] for entry in filtered_entries)
        by_operation = {}
        for entry in filtered_entries:
            op = entry.get("operation", "unknown")
            by_operation[op] = by_operation.get(op, 0) + entry["cost"]
        
        # Build report
        report = [
            f"Cost Report (Last {days} days)",
            f"=============================",
            f"Total cost: ${total_cost:.2f}",
            f"Number of operations: {len(filtered_entries)}",
            f"Average cost per operation: ${total_cost/len(filtered_entries):.2f}",
            f"",
            f"Breakdown by operation type:",
        ]
        
        for op, cost in sorted(by_operation.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {op}: ${cost:.2f} ({cost/total_cost*100:.1f}%)")
        
        return "\n".join(report)
    except Exception as e:
        return f"Error generating cost report: {e}"


def _get_daily_limit():
    """Get the configured daily spending limit."""
    limit = os.environ.get("NANOBOT_DAILY_LIMIT")
    try:
        return float(limit) if limit else DEFAULT_DAILY_LIMIT
    except ValueError:
        return DEFAULT_DAILY_LIMIT


def _get_todays_spend():
    """Calculate how much has been spent today."""
    import json
    from datetime import datetime
    
    today = datetime.now().date()
    
    try:
        if not COST_LOG_PATH.exists():
            return 0.0
        
        with open(COST_LOG_PATH, 'r') as f:
            log = json.load(f)
        
        # Sum up today's entries
        total = 0.0
        for entry in log.get("entries", []):
            try:
                entry_date = datetime.fromisoformat(entry["timestamp"]).date()
                if entry_date == today:
                    total += entry.get("cost", 0.0)
            except (ValueError, KeyError):
                continue
        
        return total
    except Exception:
        return 0.0


def _would_exceed_daily_limit(additional_cost):
    """Check if an additional cost would exceed the daily limit."""
    current_spend = _get_todays_spend()
    daily_limit = _get_daily_limit()
    
    return (current_spend + additional_cost) > daily_limit


# Safe wrapper for API calls that cost money
def safe_api_call(api_func, cost_estimate, description, *args, **kwargs):
    """
    Safely call an API function with cost control.
    
    Args:
        api_func: The API function to call
        cost_estimate: Estimated cost of the call
        description: Description of the operation
        *args, **kwargs: Arguments to pass to the API function
        
    Returns:
        API response if confirmed, None if rejected
        
    This wraps API calls with cost confirmation and tracking.
    """
    # Check if dry run mode is enabled
    if os.environ.get("NANOBOT_DRY_RUN") == "1":
        print(f"DRY RUN: Would call {api_func.__name__} (${cost_estimate:.2f})")
        return {"dry_run": True, "cost_estimate": cost_estimate}
    
    # Get confirmation
    if not cost_confirmation(cost_estimate, description):
        print("Operation cancelled by user.")
        return None
    
    # Call API and track cost
    try:
        result = api_func(*args, **kwargs)
        track_cost(cost_estimate, api_func.__name__, kwargs)
        return result
    except Exception as e:
        print(f"API call failed: {e}")
        # Don't track cost for failed calls
        return {"error": str(e)}