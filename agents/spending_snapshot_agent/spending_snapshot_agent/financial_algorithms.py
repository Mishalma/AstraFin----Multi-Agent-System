"""
Financial Mathematical Algorithms for Spending Analysis
Provides deterministic calculations to complement LLM agents
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import statistics
import math


@dataclass
class Transaction:
    """Transaction data structure"""
    date: datetime
    amount: float
    merchant: str
    category: str
    description: str


@dataclass
class SpendingMetrics:
    """Structured spending analysis results"""
    total_spending: float
    category_breakdown: Dict[str, float]
    monthly_average: float
    trend_direction: str
    variance_percentage: float
    seasonal_factor: float


class SpendingAnalyzer:
    """Rule-based transaction analysis with mathematical precision"""
    
    CATEGORY_RULES = {
        'dining': ['restaurant', 'cafe', 'food', 'pizza', 'burger', 'starbucks', 'mcdonald'],
        'groceries': ['grocery', 'supermarket', 'walmart', 'target', 'costco', 'whole foods'],
        'transportation': ['gas', 'uber', 'lyft', 'taxi', 'parking', 'metro', 'bus'],
        'entertainment': ['movie', 'netflix', 'spotify', 'game', 'theater', 'concert'],
        'shopping': ['amazon', 'mall', 'store', 'shop', 'retail', 'clothing'],
        'utilities': ['electric', 'water', 'internet', 'phone', 'cable', 'utility'],
        'healthcare': ['doctor', 'pharmacy', 'hospital', 'medical', 'dental'],
        'other': []  # Default category
    }
    
    @staticmethod
    def categorize_transactions(transactions: List[Dict]) -> List[Transaction]:
        """
        Rule-based transaction categorization
        Returns structured Transaction objects with categories
        """
        categorized = []
        
        for txn in transactions:
            # Extract transaction details
            merchant = txn.get('merchant', '').lower()
            description = txn.get('description', '').lower()
            amount = abs(float(txn.get('amount', 0)))
            
            # Determine category using rule-based matching
            category = 'other'
            for cat, keywords in SpendingAnalyzer.CATEGORY_RULES.items():
                if any(keyword in merchant or keyword in description for keyword in keywords):
                    category = cat
                    break
            
            # Parse date
            date_str = txn.get('date', '')
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                date = datetime.now()
            
            categorized.append(Transaction(
                date=date,
                amount=amount,
                merchant=txn.get('merchant', ''),
                category=category,
                description=txn.get('description', '')
            ))
        
        return categorized
    
    @staticmethod
    def calculate_monthly_spending(transactions: List[Transaction]) -> Dict[str, Dict[str, float]]:
        """
        Calculate monthly spending by category
        Returns: {month: {category: amount}}
        """
        monthly_data = {}
        
        for txn in transactions:
            month_key = txn.date.strftime('%Y-%m')
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {}
            
            if txn.category not in monthly_data[month_key]:
                monthly_data[month_key][txn.category] = 0
            
            monthly_data[month_key][txn.category] += txn.amount
        
        return monthly_data
    
    @staticmethod
    def calculate_moving_average(values: List[float], window: int = 3) -> List[float]:
        """
        Calculate moving average for trend analysis
        """
        if len(values) < window:
            return values
        
        moving_averages = []
        for i in range(len(values) - window + 1):
            avg = sum(values[i:i + window]) / window
            moving_averages.append(avg)
        
        return moving_averages
    
    @staticmethod
    def detect_trend_direction(values: List[float]) -> str:
        """
        Detect spending trend using linear regression slope
        """
        if len(values) < 2:
            return "insufficient_data"
        
        n = len(values)
        x_values = list(range(n))
        
        # Calculate linear regression slope
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if slope > 0.05:  # 5% threshold
            return "increasing"
        elif slope < -0.05:
            return "decreasing"
        else:
            return "stable"


class BudgetCalculator:
    """Budget variance analysis with statistical methods"""
    
    @staticmethod
    def calculate_variance(actual_spending: float, budgeted_amount: float) -> Dict[str, Any]:
        """
        Calculate budget variance with statistical significance
        """
        if budgeted_amount == 0:
            return {
                'variance_percentage': 0,
                'variance_amount': actual_spending,
                'status': 'no_budget_set',
                'significance': 'unknown'
            }
        
        variance_amount = actual_spending - budgeted_amount
        variance_percentage = (variance_amount / budgeted_amount) * 100
        
        # Determine status
        if variance_percentage > 10:
            status = 'over_budget'
        elif variance_percentage < -10:
            status = 'under_budget'
        else:
            status = 'on_track'
        
        # Statistical significance (simplified)
        significance = 'significant' if abs(variance_percentage) > 15 else 'minor'
        
        return {
            'variance_percentage': round(variance_percentage, 2),
            'variance_amount': round(variance_amount, 2),
            'status': status,
            'significance': significance
        }
    
    @staticmethod
    def analyze_category_variance(monthly_data: Dict[str, Dict[str, float]], 
                                budget_by_category: Dict[str, float]) -> Dict[str, Dict]:
        """
        Analyze variance for each spending category
        """
        category_analysis = {}
        
        # Calculate average spending per category
        category_totals = {}
        for month_data in monthly_data.values():
            for category, amount in month_data.items():
                if category not in category_totals:
                    category_totals[category] = []
                category_totals[category].append(amount)
        
        # Calculate variance for each category
        for category, amounts in category_totals.items():
            avg_spending = sum(amounts) / len(amounts)
            budgeted = budget_by_category.get(category, 0)
            
            category_analysis[category] = BudgetCalculator.calculate_variance(
                avg_spending, budgeted
            )
            category_analysis[category]['average_spending'] = round(avg_spending, 2)
        
        return category_analysis


class TrendPredictor:
    """Predictive modeling for spending forecasts"""
    
    @staticmethod
    def forecast_spending(historical_data: List[float], periods_ahead: int = 3) -> Dict[str, Any]:
        """
        Linear regression forecast with confidence intervals
        """
        if len(historical_data) < 3:
            return {
                'forecast': historical_data[-1] if historical_data else 0,
                'confidence_interval': (0, 0),
                'trend': 'insufficient_data'
            }
        
        n = len(historical_data)
        x_values = list(range(n))
        
        # Linear regression calculation
        x_mean = sum(x_values) / n
        y_mean = sum(historical_data) / n
        
        numerator = sum((x_values[i] - x_mean) * (historical_data[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        
        # Forecast next period
        forecast_x = n + periods_ahead - 1
        forecast = slope * forecast_x + intercept
        
        # Calculate standard error for confidence interval
        residuals = [historical_data[i] - (slope * x_values[i] + intercept) for i in range(n)]
        mse = sum(r ** 2 for r in residuals) / (n - 2) if n > 2 else 0
        std_error = math.sqrt(mse)
        
        # 95% confidence interval (approximate)
        margin_of_error = 1.96 * std_error
        confidence_interval = (
            max(0, forecast - margin_of_error),
            forecast + margin_of_error
        )
        
        return {
            'forecast': round(max(0, forecast), 2),
            'confidence_interval': (round(confidence_interval[0], 2), round(confidence_interval[1], 2)),
            'trend': SpendingAnalyzer.detect_trend_direction(historical_data),
            'slope': round(slope, 4)
        }
    
    @staticmethod
    def seasonal_adjustment(monthly_data: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate seasonal factors for spending patterns
        """
        if len(monthly_data) < 12:
            return {month: 1.0 for month in monthly_data.keys()}
        
        # Calculate overall average
        total_avg = sum(monthly_data.values()) / len(monthly_data)
        
        # Calculate seasonal factors
        seasonal_factors = {}
        for month, amount in monthly_data.items():
            seasonal_factors[month] = amount / total_avg if total_avg > 0 else 1.0
        
        return seasonal_factors


class RecommendationEngine:
    """Mathematical optimization for budget recommendations"""
    
    @staticmethod
    def optimize_budget_allocation(current_spending: Dict[str, float], 
                                 financial_goals: Dict[str, float],
                                 total_income: float) -> Dict[str, Any]:
        """
        Mathematical optimization for budget reallocation
        """
        total_spending = sum(current_spending.values())
        savings_target = financial_goals.get('monthly_savings', 0)
        
        # Calculate required reduction
        required_reduction = max(0, total_spending + savings_target - total_income)
        
        if required_reduction == 0:
            return {
                'status': 'budget_balanced',
                'recommendations': [],
                'potential_savings': 0
            }
        
        # Identify categories for reduction (prioritize discretionary spending)
        discretionary_categories = ['dining', 'entertainment', 'shopping']
        recommendations = []
        
        for category in discretionary_categories:
            if category in current_spending and current_spending[category] > 0:
                # Suggest 10-20% reduction in discretionary categories
                suggested_reduction = min(
                    current_spending[category] * 0.15,  # 15% reduction
                    required_reduction * 0.4  # Don't exceed 40% of total needed reduction
                )
                
                recommendations.append({
                    'category': category,
                    'current_spending': current_spending[category],
                    'suggested_reduction': round(suggested_reduction, 2),
                    'new_budget': round(current_spending[category] - suggested_reduction, 2)
                })
        
        total_potential_savings = sum(rec['suggested_reduction'] for rec in recommendations)
        
        return {
            'status': 'optimization_needed',
            'required_reduction': round(required_reduction, 2),
            'recommendations': recommendations,
            'potential_savings': round(total_potential_savings, 2)
        }
    
    @staticmethod
    def goal_based_adjustments(current_spending: Dict[str, float],
                             savings_goal: float,
                             timeline_months: int) -> Dict[str, Any]:
        """
        Calculate spending adjustments needed to meet savings goals
        """
        monthly_savings_needed = savings_goal / timeline_months
        total_current_spending = sum(current_spending.values())
        
        # Calculate percentage reduction needed
        if total_current_spending == 0:
            return {'feasible': False, 'reason': 'no_spending_data'}
        
        reduction_percentage = (monthly_savings_needed / total_current_spending) * 100
        
        feasible = reduction_percentage <= 30  # Max 30% reduction considered feasible
        
        return {
            'feasible': feasible,
            'monthly_savings_needed': round(monthly_savings_needed, 2),
            'reduction_percentage': round(reduction_percentage, 2),
            'timeline_months': timeline_months,
            'total_goal': savings_goal
        }