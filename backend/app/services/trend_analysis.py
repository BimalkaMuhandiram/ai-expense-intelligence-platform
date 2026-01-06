from datetime import datetime, timedelta
from collections import defaultdict

def analyze_trends(expenses):
    if not expenses:
        return {"message": "No expense data available."}

    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp.category] += exp.amount

    alerts = []
    total_spent = sum(category_totals.values())

    for category, amount in category_totals.items():
        percent = (amount / total_spent) * 100

        if percent > 40:
            alerts.append(
                f"High spending detected in {category} "
                f"({percent:.1f}% of total expenses)."
            )

    return {
        "total_spent": total_spent,
        "alerts": alerts
    }

def overspending_alert(total, limit=10000):
    if total > limit:
        return f"Alert: You exceeded your monthly limit of {limit}."
    return None