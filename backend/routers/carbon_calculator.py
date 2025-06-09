from fastapi import APIRouter, Body

router = APIRouter()

emission_factors = {
    "Fuel": 0.0033,
    "Flight": 0.0025,
    "Food Delivery": 0.002,
    "Fashion": 0.004,
    "Grocery": 0.0012,
    "Electronics": 0.006,
    "Transport": 0.0028,
    "Streaming": 0.001
}

base_suggestions = {
    "Fuel": "Use public transport or carpool more often.",
    "Fashion": "Try thrift stores or eco-friendly brands.",
    "Food Delivery": "Reduce ordering frequency or batch orders.",
    "Flight": "Opt for trains or combine trips.",
    "Grocery": "Buy local and seasonal produce.",
    "Electronics": "Delay gadget upgrades, recycle devices.",
    "Streaming": "Lower resolution when possible.",
    "Transport": "Walk or bike for short distances."
}

def calculate_emission_and_suggestions(categories: list[str], total_amount: list[float]) -> dict:
    total_emission = 0.0
    per_category = {}
    suggestions = {}

    for category, amount in zip(categories, total_amount):
        factor = emission_factors.get(category, 0)
        emission = round(amount * factor, 2)

        per_category[category] = emission
        total_emission += emission

        if category in base_suggestions:
            optimal_amount = round(amount * 0.5)
            suggestions[category] = (
                f"{base_suggestions[category]} Try limiting to ₹{optimal_amount} to cut carbon impact by ~50%."
            )

    return {
        "total_emission": round(total_emission, 2),
        "per_category": per_category,
        "suggestions": suggestions
    }

@router.post("/carbon-calculator")
async def carbon_calculator_endpoint(
    body: dict = Body(...)
):
    categories = body.get("categories", [])
    total_amount = body.get("totalAmount", [])
    return calculate_emission_and_suggestions(categories, total_amount)