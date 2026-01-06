import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import date

def forecast_next_month(expenses):
    """
    expenses: list of dicts with keys {date, amount}
    """

    if len(expenses) < 3:
        return None  # not enough data

    # Convert to month index
    months = []
    totals = {}

    for e in expenses:
        key = (e["date"].year, e["date"].month)
        totals[key] = totals.get(key, 0) + e["amount"]

    for i, ((year, month), total) in enumerate(sorted(totals.items())):
        months.append([i])
        totals[(year, month)] = total

    X = np.array(months)
    y = np.array(list(totals.values()))

    model = LinearRegression()
    model.fit(X, y)

    next_month_index = [[len(X)]]
    prediction = model.predict(next_month_index)

    return round(float(prediction[0]), 2)