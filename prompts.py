SYSTEM_PROMPT = """
You are a personal finance advisor.

Analyze spending habits.

Your tasks:

1. Identify top spending categories.
2. Identify budget overruns.
3. Give 3 actionable recommendations.
4. Give overall assessment.

Be concise and data-driven.
"""


def build_spending_context(
    expenses,
    cat_totals,
    alerts,
    month,
    year
):

    context = f"""
Month: {month}
Year: {year}

Expenses:
"""

    total = sum(
        expense.amount
        for expense in expenses
    )

    context += f"\nTotal Spend: ${total}\n"

    context += "\nCategory Totals:\n"

    for row in cat_totals:

        context += (
            f"{row.name}: "
            f"${row.total}\n"
        )

    context += "\nAlerts:\n"

    for alert in alerts:

        context += (
            f"{alert['category']} "
            f"over by "
            f"${alert['over_by']}\n"
        )

    return context