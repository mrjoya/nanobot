#!/usr/bin/env python3
"""
Cost Monitor for NanoBot API Usage

This script helps track and monitor API costs, set limits,
and provides reporting on usage patterns.

Usage:
  python cost_monitor.py report [--days=7]
  python cost_monitor.py limit [--set=5.00]
  python cost_monitor.py reset

IMPORTANT: Always run this before using API features to check your spending.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.api import estimate_cost

# Cost log file
COST_LOG_PATH = Path(__file__).parent.parent / "cost_log.json"
LIMITS_PATH = Path(__file__).parent.parent / "cost_limits.json"

# Default limits
DEFAULT_LIMITS = {
    "daily": 5.00,   # $5.00 per day
    "session": 2.00, # $2.00 per session
    "monthly": 30.00 # $30.00 per month
}


def initialize_cost_log():
    """Create or initialize the cost log file."""
    if not COST_LOG_PATH.exists():
        log = {
            "entries": [],
            "total_cost": 0.0,
            "last_updated": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        with open(COST_LOG_PATH, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"✅ Created new cost log at {COST_LOG_PATH}")
    
    if not LIMITS_PATH.exists():
        with open(LIMITS_PATH, 'w') as f:
            json.dump(DEFAULT_LIMITS, f, indent=2)
        print(f"✅ Created default cost limits at {LIMITS_PATH}")


def load_cost_log():
    """Load the cost log, creating it if it doesn't exist."""
    initialize_cost_log()
    
    try:
        with open(COST_LOG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading cost log: {e}")
        return {"entries": [], "total_cost": 0.0}


def load_limits():
    """Load cost limits, creating defaults if they don't exist."""
    if not LIMITS_PATH.exists():
        with open(LIMITS_PATH, 'w') as f:
            json.dump(DEFAULT_LIMITS, f, indent=2)
    
    try:
        with open(LIMITS_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_LIMITS


def save_limits(limits):
    """Save cost limits to file."""
    with open(LIMITS_PATH, 'w') as f:
        json.dump(limits, f, indent=2)


def generate_report(days=7):
    """Generate a cost report for the specified period."""
    log = load_cost_log()
    limits = load_limits()
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Filter entries by date
    filtered_entries = []
    for entry in log.get("entries", []):
        try:
            entry_date = datetime.fromisoformat(entry["timestamp"])
            if start_date <= entry_date <= end_date:
                filtered_entries.append(entry)
        except (ValueError, KeyError):
            continue
    
    # Calculate totals
    total_cost = sum(entry.get("cost", 0) for entry in filtered_entries)
    by_operation = {}
    by_date = {}
    
    for entry in filtered_entries:
        # By operation
        op = entry.get("operation", "unknown")
        by_operation[op] = by_operation.get(op, 0) + entry.get("cost", 0)
        
        # By date
        try:
            date_str = datetime.fromisoformat(entry["timestamp"]).date().isoformat()
            by_date[date_str] = by_date.get(date_str, 0) + entry.get("cost", 0)
        except (ValueError, KeyError):
            continue
    
    # Calculate daily average
    daily_avg = total_cost / days if days > 0 else 0
    
    # Calculate today's spend
    today = datetime.now().date().isoformat()
    today_spend = by_date.get(today, 0)
    
    # Format the report
    report = [
        f"\n📊 NanoBot API Cost Report ({days} days)",
        f"======================================",
        f"",
        f"📅 Period: {start_date.date()} to {end_date.date()}",
        f"💰 Total cost: ${total_cost:.2f}",
        f"📈 Daily average: ${daily_avg:.2f}",
        f"🔄 Operations: {len(filtered_entries)}",
        f"",
        f"⚠️ Limits:",
        f"  Daily limit: ${limits.get('daily', DEFAULT_LIMITS['daily']):.2f}",
        f"  Today's usage: ${today_spend:.2f} ({today_spend/limits.get('daily', DEFAULT_LIMITS['daily'])*100:.1f}% of limit)",
        f"",
    ]
    
    if by_operation:
        report.append(f"🔍 Cost breakdown by operation:")
        for op, cost in sorted(by_operation.items(), key=lambda x: x[1], reverse=True):
            pct = cost/total_cost*100 if total_cost > 0 else 0
            report.append(f"  {op}: ${cost:.2f} ({pct:.1f}%)")
        report.append("")
    
    if by_date:
        report.append(f"📆 Cost breakdown by date:")
        for date_str, cost in sorted(by_date.items(), reverse=True):
            pct = cost/total_cost*100 if total_cost > 0 else 0
            report.append(f"  {date_str}: ${cost:.2f} ({pct:.1f}%)")
    
    return "\n".join(report)


def estimate_image_cost():
    """Calculate cost for different image generation scenarios."""
    scenarios = [
        {"desc": "Single draft image (1K)", "images": 1, "res": "1K"},
        {"desc": "Single high-res image (4K)", "images": 1, "res": "4K"},
        {"desc": "Four variations (1K)", "images": 4, "res": "1K"},
        {"desc": "Four high-res variations (4K)", "images": 4, "res": "4K"},
    ]
    
    report = [
        "\n💵 Cost Estimates for Common Scenarios",
        "=====================================",
    ]
    
    for s in scenarios:
        cost = estimate_cost(s["images"], s["res"])
        report.append(f"{s['desc']}: ${cost:.2f}")
    
    return "\n".join(report)


def set_limit(limit_type, value):
    """Set a spending limit."""
    if limit_type not in ["daily", "session", "monthly"]:
        print(f"❌ Invalid limit type: {limit_type}")
        return
    
    try:
        value = float(value)
        if value <= 0:
            print("❌ Limit must be greater than zero")
            return
            
        limits = load_limits()
        old_value = limits.get(limit_type, DEFAULT_LIMITS[limit_type])
        limits[limit_type] = value
        save_limits(limits)
        
        print(f"✅ {limit_type.capitalize()} limit updated: ${old_value:.2f} → ${value:.2f}")
        
    except ValueError:
        print("❌ Invalid limit value. Must be a number.")


def reset_cost_log():
    """Reset the cost log (with confirmation)."""
    if not COST_LOG_PATH.exists():
        print("No cost log exists yet.")
        return
    
    confirm = input("⚠️ This will delete ALL cost history. Continue? (yes/no): ")
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return
    
    log = load_cost_log()
    total = log.get("total_cost", 0)
    entries = len(log.get("entries", []))
    
    # Create backup
    backup_path = COST_LOG_PATH.with_suffix(".backup.json")
    with open(backup_path, 'w') as f:
        json.dump(log, f, indent=2)
    
    # Reset log
    new_log = {
        "entries": [],
        "total_cost": 0.0,
        "last_updated": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "reset_from": {
            "timestamp": datetime.now().isoformat(),
            "previous_total": total,
            "previous_entries": entries
        }
    }
    
    with open(COST_LOG_PATH, 'w') as f:
        json.dump(new_log, f, indent=2)
    
    print(f"✅ Cost log reset. Previous data (${ total:.2f}, {entries} entries) backed up to {backup_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor and manage NanoBot API costs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cost_monitor.py report
  python cost_monitor.py report --days=30
  python cost_monitor.py limit --daily=10
  python cost_monitor.py reset
        """
    )
    
    # Commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Show cost report")
    report_parser.add_argument("--days", type=int, default=7, help="Number of days to include (default: 7)")
    
    # Limit command
    limit_parser = subparsers.add_parser("limit", help="Set spending limits")
    limit_parser.add_argument("--daily", type=float, help="Set daily spending limit")
    limit_parser.add_argument("--session", type=float, help="Set per-session limit")
    limit_parser.add_argument("--monthly", type=float, help="Set monthly limit")
    
    # Reset command
    subparsers.add_parser("reset", help="Reset cost log (with backup)")
    
    # Initialize command
    subparsers.add_parser("init", help="Initialize cost tracking files")
    
    args = parser.parse_args()
    
    # Initialize cost log if needed
    initialize_cost_log()
    
    if args.command == "report":
        print(generate_report(args.days))
        print("\n" + estimate_image_cost())
    elif args.command == "limit":
        if args.daily is not None:
            set_limit("daily", args.daily)
        if args.session is not None:
            set_limit("session", args.session)
        if args.monthly is not None:
            set_limit("monthly", args.monthly)
        
        # Show current limits if no specific limit was set
        if args.daily is None and args.session is None and args.monthly is None:
            limits = load_limits()
            print("\n⚠️ Current spending limits:")
            for limit_type, value in limits.items():
                print(f"  {limit_type.capitalize()}: ${value:.2f}")
    elif args.command == "reset":
        reset_cost_log()
    elif args.command == "init":
        initialize_cost_log()
        print("✅ Cost tracking initialized.")
    else:
        # Default to report if no command provided
        print(generate_report(7))
        print("\n" + estimate_image_cost())
        
        limits = load_limits()
        print("\n⚠️ Current spending limits:")
        for limit_type, value in limits.items():
            print(f"  {limit_type.capitalize()}: ${value:.2f}")


if __name__ == "__main__":
    main()