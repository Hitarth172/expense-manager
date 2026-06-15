def budget_status(
    spent,
    limit
):

    if spent > limit:

        return {
            "status": "OVER_LIMIT",
            "over_by": spent - limit
        }

    return {
        "status": "SAFE",
        "remaining": limit - spent
    }