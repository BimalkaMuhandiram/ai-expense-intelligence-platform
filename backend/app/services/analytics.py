from datetime import datetime
from collections import defaultdict

def monthly_comparison(expenses):
    current_month = datetime.utcnow().month
    last_month = current_month - 1 or 12

    current = defaultdict(float)
    previous = defaultdict(float)

    for exp in expenses:
        month = exp.created_at.month
        if month == current_month:
            current[exp.category] += exp.amount
        elif month == last_month:
            previous[exp.category] += exp.amount

    comparison = []

    categories = set(current) | set(previous)

    for cat in categories:
        comparison.append({
            "category": cat,
            "current_month": current.get(cat, 0),
            "last_month": previous.get(cat, 0),
            "difference": current.get(cat, 0) - previous.get(cat, 0)
        })

    return comparison