"""
Example: Mathematical Integration Workflow
Demonstrates how "Am I overspending on dining?" query flows through the system
"""

from datetime import datetime, timedelta
from .financial_algorithms import (
    SpendingAnalyzer, 
    BudgetCalculator, 
    TrendPredictor, 
    RecommendationEngine,
    Transaction
)


def demonstrate_dining_overspending_analysis():
    """
    Complete workflow example for "Am I overspending on dining?" query
    Shows integration of LLM agents with mathematical algorithms
    """
    
    # STEP 1: Simulated data from cymbal_agent (what LLM retriever gets)
    raw_transactions = [
        {'date': '2024-10-01', 'merchant': 'Starbucks', 'amount': 15.50, 'description': 'Coffee and pastry'},
        {'date': '2024-10-02', 'merchant': 'Pizza Palace', 'amount': 28.75, 'description': 'Dinner pizza'},
        {'date': '2024-10-03', 'merchant': 'Whole Foods', 'amount': 85.20, 'description': 'Grocery shopping'},
        {'date': '2024-10-05', 'merchant': 'Burger King', 'amount': 12.30, 'description': 'Fast food lunch'},
        {'date': '2024-10-07', 'merchant': 'Fine Dining Restaurant', 'amount': 95.00, 'description': 'Date night dinner'},
        {'date': '2024-10-10', 'merchant': 'Cafe Mocha', 'amount': 8.75, 'description': 'Morning coffee'},
        {'date': '2024-10-12', 'merchant': 'Taco Bell', 'amount': 18.50, 'description': 'Quick lunch'},
        {'date': '2024-10-15', 'merchant': 'Sushi Bar', 'amount': 65.00, 'description': 'Sushi dinner'},
    ]
    
    user_budget = {
        'dining': 200.00,  # Monthly dining budget
        'groceries': 400.00,
        'total_monthly': 3000.00
    }
    
    # STEP 2: Mathematical Analysis (what mathematical_analyzer agent does)
    
    # 2a. Transaction Categorization
    categorized_transactions = SpendingAnalyzer.categorize_transactions(raw_transactions)
    
    # 2b. Calculate dining spending
    dining_transactions = [t for t in categorized_transactions if t.category == 'dining']
    total_dining_spending = sum(t.amount for t in dining_transactions)
    
    print(f"=== MATHEMATICAL ANALYSIS RESULTS ===")
    print(f"Total Dining Spending: ${total_dining_spending:.2f}")
    print(f"Dining Budget: ${user_budget['dining']:.2f}")
    
    # 2c. Budget Variance Analysis
    variance_analysis = BudgetCalculator.calculate_variance(
        actual_spending=total_dining_spending,
        budgeted_amount=user_budget['dining']
    )
    
    print(f"\n=== BUDGET VARIANCE ANALYSIS ===")
    print(f"Variance Percentage: {variance_analysis['variance_percentage']}%")
    print(f"Variance Amount: ${variance_analysis['variance_amount']:.2f}")
    print(f"Status: {variance_analysis['status']}")
    print(f"Significance: {variance_analysis['significance']}")
    
    # 2d. Trend Analysis (simulate 3 months of data)
    monthly_dining_spending = [180.50, 195.75, total_dining_spending]  # Simulated historical data
    trend_direction = SpendingAnalyzer.detect_trend_direction(monthly_dining_spending)
    
    print(f"\n=== TREND ANALYSIS ===")
    print(f"Monthly Spending History: {monthly_dining_spending}")
    print(f"Trend Direction: {trend_direction}")
    
    # 2e. Predictive Modeling
    forecast_result = TrendPredictor.forecast_spending(monthly_dining_spending, periods_ahead=1)
    
    print(f"\n=== PREDICTIVE MODELING ===")
    print(f"Next Month Forecast: ${forecast_result['forecast']:.2f}")
    print(f"Confidence Interval: ${forecast_result['confidence_interval'][0]:.2f} - ${forecast_result['confidence_interval'][1]:.2f}")
    print(f"Trend: {forecast_result['trend']}")
    
    # 2f. Recommendation Engine
    current_spending = {'dining': total_dining_spending, 'groceries': 85.20, 'other': 500.00}
    financial_goals = {'monthly_savings': 500.00}
    
    recommendations = RecommendationEngine.optimize_budget_allocation(
        current_spending=current_spending,
        financial_goals=financial_goals,
        total_income=3000.00
    )
    
    print(f"\n=== OPTIMIZATION RECOMMENDATIONS ===")
    print(f"Status: {recommendations['status']}")
    if recommendations['recommendations']:
        for rec in recommendations['recommendations']:
            print(f"Category: {rec['category']}")
            print(f"  Current: ${rec['current_spending']:.2f}")
            print(f"  Suggested Reduction: ${rec['suggested_reduction']:.2f}")
            print(f"  New Budget: ${rec['new_budget']:.2f}")
    
    # STEP 3: LLM Response Generation (what formatting_agent does)
    mathematical_insights = {
        'overspending_confirmed': variance_analysis['status'] == 'over_budget',
        'overspending_percentage': variance_analysis['variance_percentage'],
        'trend': trend_direction,
        'forecast_next_month': forecast_result['forecast'],
        'recommended_reduction': recommendations.get('potential_savings', 0)
    }
    
    # This is what the LLM would use to generate natural language response
    llm_response_data = f"""
    Based on mathematical analysis of your dining spending:
    
    **Overspending Analysis:**
    - You spent ${total_dining_spending:.2f} on dining this month
    - Your dining budget is ${user_budget['dining']:.2f}
    - You are {variance_analysis['variance_percentage']:.1f}% over budget (${variance_analysis['variance_amount']:.2f} excess)
    - This overspending is mathematically {variance_analysis['significance']}
    
    **Trend Analysis:**
    - Your dining spending trend is: {trend_direction}
    - Mathematical forecast for next month: ${forecast_result['forecast']:.2f}
    - Confidence range: ${forecast_result['confidence_interval'][0]:.2f} - ${forecast_result['confidence_interval'][1]:.2f}
    
    **Mathematical Recommendations:**
    - Reduce dining spending by ${recommendations.get('potential_savings', 0):.2f} to meet your savings goals
    - Focus on discretionary dining (restaurants vs. necessary meals)
    - Set a strict weekly dining limit of ${user_budget['dining']/4:.2f}
    """
    
    print(f"\n=== LLM RESPONSE (Natural Language) ===")
    print(llm_response_data)
    
    return mathematical_insights


def workflow_integration_explanation():
    """
    Explains how this integrates with your existing agent workflow
    """
    
    workflow_steps = """
    
    === COMPLETE INTEGRATION WORKFLOW ===
    
    1. USER QUERY: "Am I overspending on dining?"
    
    2. CHAT ORCHESTRATOR (Port 8090):
       - Classifies query as "spending" topic
       - Routes to spending_specialist agent
    
    3. SPENDING SPECIALIST AGENT:
       - Uses cymbal_agent tool to fetch transaction data
       - Gets user profile and budget information
       - Passes data to mathematical analysis layer
    
    4. MATHEMATICAL ANALYSIS LAYER:
       - SpendingAnalyzer.categorize_transactions() → Rule-based categorization
       - BudgetCalculator.calculate_variance() → Statistical variance analysis  
       - TrendPredictor.forecast_spending() → Linear regression forecasting
       - RecommendationEngine.optimize_budget_allocation() → Mathematical optimization
    
    5. LLM RESPONSE GENERATION:
       - Takes mathematical results as structured data
       - Generates natural language explanation
       - Provides actionable recommendations based on math
    
    6. USER RECEIVES:
       - Precise percentage overspending (e.g., "23.7% over budget")
       - Statistical significance ("mathematically significant overspending")
       - Trend analysis ("increasing trend detected")
       - Forecast with confidence ("next month: $245 ± $30")
       - Optimized recommendations ("reduce by $47.50 to meet savings goals")
    
    === KEY BENEFITS ===
    
    ✓ Eliminates LLM hallucination in financial calculations
    ✓ Provides deterministic, auditable results
    ✓ Maintains conversational AI experience
    ✓ Enables regulatory compliance through mathematical transparency
    ✓ Builds user trust through precision and consistency
    
    """
    
    print(workflow_steps)


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_dining_overspending_analysis()
    workflow_integration_explanation()