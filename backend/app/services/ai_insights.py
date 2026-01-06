def generate_insight(summary: dict) -> str:
    total = summary["total"]
    categories = summary["by_category"]

    if total == 0:
        return "No expenses recorded yet."

    insights = []

    # Find highest spending category
    max_category = max(categories, key=categories.get)
    max_amount = categories[max_category]
    percentage = (max_amount / total) * 100

    insights.append(
        f"You spend most on {max_category} "
        f"({percentage:.1f}% of total expenses)."
    )

    # Rule-based suggestions
    if percentage > 40:
        insights.append(
            f"Your spending on {max_category} is relatively high. "
            f"Consider reducing unnecessary costs in this category."
        )

    if "Food" in categories and categories["Food"] > 0.3 * total:
        insights.append(
            "Food expenses are significant. Cooking at home may help save money."
        )

    if "Transport" in categories and categories["Transport"] > 0.25 * total:
        insights.append(
            "Transport costs are high. Consider using public transport or carpooling."
        )

    return " ".join(insights)