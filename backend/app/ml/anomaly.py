import statistics

def detect_anomalies(expenses, threshold=2):
    """
    expenses: list of dicts with key {amount}
    threshold: how many std deviations is considered anomaly
    """

    if len(expenses) < 5:
        return []

    amounts = [e["amount"] for e in expenses]

    mean = statistics.mean(amounts)
    std = statistics.stdev(amounts)

    anomalies = []

    for e in expenses:
        if abs(e["amount"] - mean) > threshold * std:
            anomalies.append(e)

    return anomalies