from groq import Groq
from dotenv import load_dotenv
from app.prompts import (
    SYSTEM_PROMPT,
    build_spending_context
)

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyse_spending(
    expenses,
    cat_totals,
    alerts,
    month,
    year
):

    if not expenses:

        return (
            "No expenses found "
            "for this month."
        )

    context = build_spending_context(
        expenses,
        cat_totals,
        alerts,
        month,
        year
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": context
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content