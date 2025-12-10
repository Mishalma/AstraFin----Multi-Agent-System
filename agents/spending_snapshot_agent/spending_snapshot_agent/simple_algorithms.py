"""
Simple Deterministic Financial Algorithms
Easy to explain and write during interviews
"""

def categorize_transaction(merchant_name, description):
    """
    Simple rule-based categorization you can write in 30 seconds
    """
    text = (merchant_name + " " + description).lower()
    
    if any(word in text for word in ["restaurant", "cafe", "pizza", "burger"]):
        return "dining"
    elif any(word in text for word in ["grocery", "supermarket", "walmart"]):
        return "groceries"
    elif any(word in text for word in ["gas", "uber", "taxi"]):
        return "transportation"
    else:
        return "other"


def calculate_budget_variance(actual, budget):
    """
    Basic percentage calculation - interview friendly
    """
    if budget == 0:
        return {"status": "no_budget", "percentage": 0}
    
    variance = ((actual - budget) / budget) * 100
    
    if variance > 10:
        status = "over_budget"
    elif variance < -10:
        status = "under_budget"
    else:
        status = "on_track"
    
    return {
        "percentage": round(variance, 1),
        "amount": round(actual - budget, 2),
        "status": status
    }


def detect_spending_trend(monthly_amounts):
    """
    Simple trend detection - compare first half vs second half
    """
    if len(monthly_amounts) < 2:
        return "insufficient_data"
    
    mid = len(monthly_amounts) // 2
    first_half_avg = sum(monthly_amounts[:mid]) / mid
    second_half_avg = sum(monthly_amounts[mid:]) / (len(monthly_amounts) - mid)
    
    change_percent = ((second_half_avg - first_half_avg) / first_half_avg) * 100
    
    if change_percent > 5:
        return "increasing"
    elif change_percent < -5:
        return "decreasing"
    else:
        return "stable"


def calculate_savings_timeline(target_amount, monthly_income, monthly_expenses):
    """
    Basic savings calculation - easy to explain
    """
    monthly_available = monthly_income - monthly_expenses
    
    if monthly_available <= 0:
        return {"feasible": False, "reason": "no_surplus"}
    
    months_needed = target_amount / monthly_available
    
    return {
        "feasible": True,
        "months": round(months_needed, 1),
        "monthly_savings": round(monthly_available, 2)
    }


def optimize_dining_budget(current_dining, total_budget, savings_goal):
    """
    Simple optimization - reduce dining to meet savings goal
    """
    available_for_expenses = total_budget - savings_goal
    max_dining_budget = available_for_expenses * 0.15  # 15% rule for dining
    
    if current_dining <= max_dining_budget:
        return {"needs_reduction": False, "current_dining": current_dining}
    
    suggested_reduction = current_dining - max_dining_budget
    
    return {
        "needs_reduction": True,
        "current_dining": current_dining,
        "suggested_dining": round(max_dining_budget, 2),
        "reduction_needed": round(suggested_reduction, 2)
    }


# Example usage for interview demonstration
def demo_algorithms():
    """
    Simple demo you can run through in an interview
    """
    print("=== SIMPLE FINANCIAL ALGORITHMS DEMO ===\n")
    
    # 1. Transaction Categorization
    print("1. Transaction Categorization:")
    print(f"   'Starbucks Coffee' -> {categorize_transaction('Starbucks', 'Coffee')}")
    print(f"   'Walmart Groceries' -> {categorize_transaction('Walmart', 'Groceries')}")
    print(f"   'Shell Gas Station' -> {categorize_transaction('Shell', 'Gas Station')}")
    
    # 2. Budget Variance
    print("\n2. Budget Variance Analysis:")
    variance = calculate_budget_variance(actual=250, budget=200)
    print(f"   Spent $250 vs $200 budget -> {variance}")
    
    # 3. Trend Detection
    print("\n3. Spending Trend:")
    monthly_spending = [180, 190, 220, 240, 260]
    trend = detect_spending_trend(monthly_spending)
    print(f"   Monthly spending {monthly_spending} -> Trend: {trend}")
    
    # 4. Savings Timeline
    print("\n4. Savings Timeline:")
    timeline = calculate_savings_timeline(target_amount=5000, monthly_income=4000, monthly_expenses=3200)
    print(f"   Save $5000 with $800/month surplus -> {timeline}")
    
    # 5. Budget Optimization
    print("\n5. Dining Budget Optimization:")
    optimization = optimize_dining_budget(current_dining=300, total_budget=3000, savings_goal=500)
    print(f"   Current dining $300, need $500 savings -> {optimization}")


if __name__ == "__main__":
    demo_algorithms()