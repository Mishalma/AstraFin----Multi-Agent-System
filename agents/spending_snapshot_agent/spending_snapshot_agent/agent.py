from typing import List, Dict, Any

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field

from .cymbal_agent_wrapper import bank_agent_wrapper
from .financial_algorithms import (
    SpendingAnalyzer, 
    BudgetCalculator, 
    TrendPredictor, 
    RecommendationEngine
)


class SpendingSummary(BaseModel):
    """Enhanced structured output for spending analysis with mathematical insights"""

    activities: List[str] = Field(description="List of 5 most recent transactions")
    income: float = Field(description="Total income amount from transactions")
    expenses: float = Field(description="Total expenses amount from transactions")
    category_breakdown: Dict[str, float] = Field(description="Spending by category with mathematical analysis")
    budget_variance: Dict[str, Any] = Field(description="Mathematical budget variance analysis")
    trend_analysis: Dict[str, Any] = Field(description="Statistical trend analysis and forecasting")
    recommendations: Dict[str, Any] = Field(description="Mathematical optimization recommendations")
    insights: str = Field(
        description="Financial insights based on mathematical analysis and user goals"
    )


retriever_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="spending_retriever",
    description="An agent that retrieves user transaction data and profile information for the requested period. ",
    instruction="""
    You are a helpful financial assistant. Your goal is to gather comprehensive spending and profile data.
    
    **Phase 1: Get Transaction Data**
    Call the cymbal_agent tool with the query "List my recent transactions." to get the user's transaction history.
    
    **Phase 2: Get User Profile**
    Call the cymbal_agent tool with the query "Get my user profile" to get the user's profile information including their financial goals.
    
    Combine both the transaction data and user profile information in your response for the next agent to use.
    """,
    tools=[AgentTool(bank_agent_wrapper)],
    output_key="spending_data",
)

mathematical_analyzer = LlmAgent(
    model="gemini-2.5-flash",
    name="mathematical_analyzer",
    description="Applies mathematical algorithms to spending data for precise financial analysis",
    instruction="""
    You are a mathematical financial analyst. Using the spending data from 'spending_data', apply deterministic 
    mathematical algorithms to ensure calculation accuracy.

    **Your Mathematical Analysis Process:**
    1. **Transaction Categorization**: Use SpendingAnalyzer.categorize_transactions() for rule-based categorization
    2. **Trend Analysis**: Apply SpendingAnalyzer.calculate_moving_average() and detect_trend_direction()
    3. **Budget Variance**: Use BudgetCalculator.calculate_variance() for statistical analysis
    4. **Forecasting**: Apply TrendPredictor.forecast_spending() for predictive modeling
    5. **Optimization**: Use RecommendationEngine for mathematical budget optimization

    **CRITICAL MATHEMATICAL CONSTRAINTS:**
    - All calculations must be deterministic and reproducible
    - Use the imported financial algorithms for mathematical precision
    - Validate all inputs before mathematical operations
    - Handle edge cases (zero values, insufficient data) gracefully
    - Ensure mathematical consistency across all metrics

    **Output Requirements:**
    - Return structured data with mathematical precision
    - Include confidence intervals and statistical significance
    - Provide mathematically-backed recommendations
    """,
    output_key="mathematical_analysis",
)

formatting_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="spending_formatter",
    description="Combines mathematical analysis with user-friendly insights generation",
    instruction="""
    You are an expert financial analyst. Using both the raw spending data from 'spending_data' and the 
    mathematical analysis from 'mathematical_analysis', create comprehensive structured insights.

    **Your Task:**
    1. **Activities**: List the 5 most recent transactions (format: "Date - Merchant - Amount")
    2. **Income**: Calculate total income from transactions (payrolls, salary deposits, refunds, etc.)
    3. **Expenses**: Calculate total expenses from transactions (purchases, bills, rent, groceries, etc.)
    4. **Category Breakdown**: Use mathematical categorization results with spending amounts per category
    5. **Budget Variance**: Include mathematical variance analysis with percentages and significance
    6. **Trend Analysis**: Incorporate statistical trend analysis, forecasts, and confidence intervals
    7. **Recommendations**: Use mathematical optimization results for actionable budget advice
    8. **Insights**: Synthesize mathematical results into user-friendly financial insights

    **CRITICAL CONSTRAINTS:**
    - You must return a structured JSON response that matches the SpendingSummary schema exactly
    - Combine mathematical precision with clear explanations
    - Base all financial advice on mathematical analysis results
    - Make insights specific and actionable based on mathematical optimization
    - Ensure all numerical values are mathematically validated
    """,
    output_schema=SpendingSummary,
    output_key="spending_summary",
)


spending_snapshot_workflow = SequentialAgent(
    name="spending_snapshot_pipeline",
    description="Executes a mathematical financial analysis pipeline: data retrieval → mathematical computation → structured insights generation.",
    sub_agents=[
        retriever_agent,
        mathematical_analyzer,
        formatting_agent,
    ],
)

root_agent = spending_snapshot_workflow
