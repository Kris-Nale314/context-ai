# utils/demo_data.py
import pandas as pd
import numpy as np
import networkx as nx
import random
import json
import os
from datetime import datetime, timedelta
from utils.theme import COLORS

# Constants for data generation
DATA_DIR = "data"
MONTHS = 12
START_DATE = datetime(2023, 1, 1)

def ensure_data_directories():
    """Ensure all necessary data directories exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "strong_applicant"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "unclear_applicant"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "challenged_applicant"), exist_ok=True)

def save_data(data, filename, applicant_type="strong_applicant"):
    """Save data to JSON or CSV file in appropriate directory."""
    dir_path = os.path.join(DATA_DIR, applicant_type)
    
    if isinstance(data, pd.DataFrame):
        # Save as CSV
        data.to_csv(os.path.join(dir_path, f"{filename}.csv"), index=False)
    else:
        # Save as JSON
        with open(os.path.join(dir_path, f"{filename}.json"), 'w') as f:
            json.dump(data, f, indent=2, default=str)

def load_data(filename, applicant_type="strong_applicant", format="json"):
    """Load data from file in appropriate directory."""
    dir_path = os.path.join(DATA_DIR, applicant_type)
    
    if format == "csv":
        return pd.read_csv(os.path.join(dir_path, f"{filename}.csv"))
    else:
        with open(os.path.join(dir_path, f"{filename}.json"), 'r') as f:
            return json.load(f)

def check_data_exists(applicant_type="strong_applicant"):
    """Check if data files exist for this applicant type."""
    dir_path = os.path.join(DATA_DIR, applicant_type)
    
    # Check for basic files
    basic_files = [
        "company_profile.json", 
        "financial_data.csv", 
        "risk_scores.csv",
        "events.json",
        "external_context.json"
    ]
    
    return all(os.path.exists(os.path.join(dir_path, f)) for f in basic_files)

def generate_company_profile(applicant_type="strong_applicant"):
    """Generate a detailed company profile based on applicant type."""
    
    # Base profiles for each applicant type
    profiles = {
        "strong_applicant": {
            "name": "TechInnovate Solutions",
            "industry": "Software Development",
            "business_type": "B2B SaaS Platform",
            "years_in_business": 7,
            "employees": 48,
            "location": "Austin, TX",
            "ownership_structure": "LLC",
            "management_team_size": 5,
            "management_experience_years": 15,
            "customer_count": 120,
            "largest_customer_percentage": 12,
            "loan_amount_requested": 500000,
            "loan_purpose": "Expansion into new markets",
            "loan_term_requested": 5,
            "collateral_offered": "Intellectual property and equipment",
            "previous_loans": 1,
            "previous_loans_repaid": 1,
            "credit_score": "A",
            "description": "TechInnovate Solutions provides cloud-based workflow automation software for professional services firms. With a stable customer base and strong management team, they're seeking funding to expand into healthcare and financial services verticals."
        },
        "unclear_applicant": {
            "name": "ManufacturePro Inc.",
            "industry": "Manufacturing",
            "business_type": "Custom Metal Fabrication",
            "years_in_business": 12,
            "employees": 73,
            "location": "Detroit, MI",
            "ownership_structure": "S-Corp",
            "management_team_size": 4,
            "management_experience_years": 20,
            "customer_count": 45,
            "largest_customer_percentage": 28,
            "loan_amount_requested": 750000,
            "loan_purpose": "Equipment modernization",
            "loan_term_requested": 7,
            "collateral_offered": "Equipment and property",
            "previous_loans": 3,
            "previous_loans_repaid": 3,
            "credit_score": "B+",
            "description": "ManufacturePro specializes in custom metal fabrication for automotive and aerospace industries. While they have a strong history, they face increasing competition from overseas and need to modernize equipment to remain competitive."
        },
        "challenged_applicant": {
            "name": "RetailGiant Stores",
            "industry": "Retail",
            "business_type": "Multi-location Retail Chain",
            "years_in_business": 15,
            "employees": 95,
            "location": "Phoenix, AZ",
            "ownership_structure": "C-Corp",
            "management_team_size": 6,
            "management_experience_years": 8,
            "customer_count": "General public",
            "largest_customer_percentage": "N/A",
            "loan_amount_requested": 1200000,
            "loan_purpose": "Debt consolidation and store renovations",
            "loan_term_requested": 10,
            "collateral_offered": "Real estate and inventory",
            "previous_loans": 5,
            "previous_loans_repaid": 4,
            "credit_score": "C+",
            "description": "RetailGiant operates a chain of general merchandise stores across Arizona. They face significant challenges from e-commerce disruption, have experienced recent management turnover, and need funding to consolidate existing debt and renovate stores to remain viable."
        }
    }
    
    # Return the appropriate profile
    return profiles[applicant_type]

def generate_financial_data(applicant_type="strong_applicant"):
    """Generate financial time series data based on applicant type."""
    
    # Create dates array
    dates = [START_DATE + timedelta(days=30*i) for i in range(MONTHS)]
    dates_str = [d.strftime("%Y-%m-%d") for d in dates]
    
    # Set base values and trends based on applicant type
    if applicant_type == "strong_applicant":
        base_revenue = 250000
        revenue_trend = 0.03  # 3% monthly growth
        base_profit_margin = 0.18
        margin_trend = 0.001  # Slight improvement
        base_cash_balance = 180000
        cash_trend = 0.02
        base_debt_ratio = 0.25
        debt_trend = -0.005  # Decreasing debt
        volatility = 0.05  # Low volatility
    
    elif applicant_type == "unclear_applicant":
        base_revenue = 420000
        revenue_trend = 0.01  # 1% monthly growth
        base_profit_margin = 0.12
        margin_trend = -0.002  # Slight decline
        base_cash_balance = 210000
        cash_trend = 0.005
        base_debt_ratio = 0.38
        debt_trend = 0.001  # Slight increase
        volatility = 0.08  # Medium volatility
    
    elif applicant_type == "challenged_applicant":
        base_revenue = 580000
        revenue_trend = -0.02  # 2% monthly decline
        base_profit_margin = 0.08
        margin_trend = -0.004  # Declining
        base_cash_balance = 150000
        cash_trend = -0.03
        base_debt_ratio = 0.45
        debt_trend = 0.01  # Increasing debt
        volatility = 0.12  # High volatility
    
    # Generate data with trends and noise
    data = {
        'date': dates_str,
        'revenue': [base_revenue * (1 + revenue_trend*i + random.uniform(-volatility, volatility)) 
                   for i in range(MONTHS)],
        'profit_margin': [max(0.01, base_profit_margin * (1 + margin_trend*i + random.uniform(-volatility, volatility)))
                         for i in range(MONTHS)],
        'cash_balance': [base_cash_balance * (1 + cash_trend*i + random.uniform(-volatility, volatility)) 
                        for i in range(MONTHS)],
        'debt_ratio': [min(0.9, max(0.1, base_debt_ratio * (1 + debt_trend*i + random.uniform(-volatility/2, volatility/2))))
                      for i in range(MONTHS)],
        'accounts_receivable': [base_revenue * 0.3 * (1 + random.uniform(-volatility, volatility))
                               for i in range(MONTHS)],
        'inventory': [base_revenue * 0.25 * (1 + random.uniform(-volatility, volatility))
                     for i in range(MONTHS)]
    }
    
    # Add industry-specific metrics
    if applicant_type == "strong_applicant":
        data['customer_acquisition_cost'] = [350 * (1 + random.uniform(-volatility, volatility))
                                           for i in range(MONTHS)]
        data['monthly_recurring_revenue'] = [base_revenue * 0.7 * (1 + revenue_trend*i + random.uniform(-volatility, volatility))
                                           for i in range(MONTHS)]
        data['customer_lifetime_value'] = [2100 * (1 + 0.01*i + random.uniform(-volatility, volatility))
                                         for i in range(MONTHS)]
    
    elif applicant_type == "unclear_applicant":
        data['raw_material_costs'] = [base_revenue * 0.4 * (1 + 0.015*i + random.uniform(-volatility, volatility))
                                    for i in range(MONTHS)]
        data['capacity_utilization'] = [0.72 * (1 + -0.005*i + random.uniform(-volatility, volatility))
                                       for i in range(MONTHS)]
        data['order_backlog'] = [base_revenue * 1.2 * (1 + -0.01*i + random.uniform(-volatility, volatility))
                               for i in range(MONTHS)]
    
    elif applicant_type == "challenged_applicant":
        data['same_store_sales_growth'] = [-0.03 * (1 - 0.1*i + random.uniform(-volatility, volatility))
                                         for i in range(MONTHS)]
        data['inventory_turnover'] = [4.2 * (1 + -0.02*i + random.uniform(-volatility, volatility))
                                     for i in range(MONTHS)]
        data['customer_traffic'] = [8500 * (1 + -0.025*i + random.uniform(-volatility, volatility))
                                   for i in range(MONTHS)]
    
    # Convert to DataFrame
    return pd.DataFrame(data)

def generate_events(applicant_type="strong_applicant"):
    """Generate timeline events based on applicant type."""
    
    # Create base events common to all applicants
    events = [
        {
            'date': (START_DATE + timedelta(days=0)).strftime("%Y-%m-%d"),
            'event': 'Initial loan application submitted',
            'category': 'application',
            'type': 'info',
            'description': 'Company submitted loan application with basic business information.'
        },
        {
            'date': (START_DATE + timedelta(days=14)).strftime("%Y-%m-%d"),
            'event': 'Financial statements requested',
            'category': 'information',
            'type': 'info',
            'description': 'Underwriter requested detailed financial statements for the past 12 months.'
        },
        {
            'date': (START_DATE + timedelta(days=21)).strftime("%Y-%m-%d"),
            'event': 'Financial statements received',
            'category': 'information',
            'type': 'info',
            'description': 'Company provided required financial statements showing operational history.'
        }
    ]
    
    # Add applicant-specific events
    if applicant_type == "strong_applicant":
        events.extend([
            {
                'date': (START_DATE + timedelta(days=35)).strftime("%Y-%m-%d"),
                'event': 'New customer contract signed',
                'category': 'company',
                'type': 'positive',
                'description': 'Company secured a significant new customer contract increasing projected revenue by 15%.'
            },
            {
                'date': (START_DATE + timedelta(days=60)).strftime("%Y-%m-%d"),
                'event': 'Industry growth report published',
                'category': 'external',
                'type': 'positive',
                'description': 'Industry report shows 18% growth projection for SaaS sector over next 24 months.'
            },
            {
                'date': (START_DATE + timedelta(days=75)).strftime("%Y-%m-%d"),
                'event': 'Preliminary approval issued',
                'category': 'approval',
                'type': 'positive',
                'description': 'Based on strong financials and industry outlook, preliminary approval issued.'
            },
            {
                'date': (START_DATE + timedelta(days=90)).strftime("%Y-%m-%d"),
                'event': 'Final terms accepted',
                'category': 'approval',
                'type': 'positive',
                'description': 'Company accepted final loan terms with favorable interest rate.'
            }
        ])
    
    elif applicant_type == "unclear_applicant":
        events.extend([
            {
                'date': (START_DATE + timedelta(days=30)).strftime("%Y-%m-%d"),
                'event': 'Customer concentration clarification requested',
                'category': 'information',
                'type': 'warning',
                'description': 'Underwriter requested clarification about 28% revenue from single customer.'
            },
            {
                'date': (START_DATE + timedelta(days=45)).strftime("%Y-%m-%d"),
                'event': 'Supply chain disruption reported',
                'category': 'external',
                'type': 'warning',
                'description': 'Industry news reported potential supply chain disruptions affecting raw material costs.'
            },
            {
                'date': (START_DATE + timedelta(days=65)).strftime("%Y-%m-%d"),
                'event': 'Updated business plan requested',
                'category': 'information',
                'type': 'info',
                'description': 'Detailed modernization plan and competitive analysis requested to clarify growth strategy.'
            },
            {
                'date': (START_DATE + timedelta(days=85)).strftime("%Y-%m-%d"),
                'event': 'Conditional approval issued',
                'category': 'approval',
                'type': 'info',
                'description': 'Conditional approval with additional reporting requirements and slightly higher interest rate.'
            }
        ])
    
    elif applicant_type == "challenged_applicant":
        events.extend([
            {
                'date': (START_DATE + timedelta(days=28)).strftime("%Y-%m-%d"),
                'event': 'Management changes disclosed',
                'category': 'company',
                'type': 'negative',
                'description': 'Disclosed that CFO and Operations Director left the company within past 90 days.'
            },
            {
                'date': (START_DATE + timedelta(days=42)).strftime("%Y-%m-%d"),
                'event': 'E-commerce impact report published',
                'category': 'external',
                'type': 'negative',
                'description': 'Industry analysis shows physical retailers in sector losing 12% market share annually to e-commerce.'
            },
            {
                'date': (START_DATE + timedelta(days=50)).strftime("%Y-%m-%d"),
                'event': 'Late payment on existing loan',
                'category': 'financial',
                'type': 'negative',
                'description': 'Company made 15-day late payment on existing equipment loan.'
            },
            {
                'date': (START_DATE + timedelta(days=70)).strftime("%Y-%m-%d"),
                'event': 'Restructuring plan requested',
                'category': 'information',
                'type': 'warning',
                'description': 'Detailed debt restructuring and business turnaround plan requested.'
            },
            {
                'date': (START_DATE + timedelta(days=95)).strftime("%Y-%m-%d"),
                'event': 'Application declined',
                'category': 'decision',
                'type': 'negative',
                'description': 'Loan application declined due to declining financial performance and industry outlook.'
            }
        ])
    
    return events

def generate_risk_scores(applicant_type="strong_applicant"):
    """Generate risk assessment scores over time based on applicant type."""
    
    # Create dates array
    dates = [START_DATE + timedelta(days=30*i) for i in range(MONTHS)]
    dates_str = [d.strftime("%Y-%m-%d") for d in dates]
    
    # Set base values and trends based on applicant type
    if applicant_type == "strong_applicant":
        base_risk = 0.25
        risk_trend = -0.01  # Decreasing risk
        base_confidence = 0.75
        confidence_trend = 0.02  # Increasing confidence
        volatility = 0.05
    
    elif applicant_type == "unclear_applicant":
        base_risk = 0.45
        risk_trend = 0.005  # Slightly increasing risk
        base_confidence = 0.60
        confidence_trend = 0.01  # Slightly increasing confidence
        volatility = 0.08
    
    elif applicant_type == "challenged_applicant":
        base_risk = 0.65
        risk_trend = 0.02  # Increasing risk
        base_confidence = 0.55
        confidence_trend = 0.005  # Barely increasing confidence
        volatility = 0.10
    
    # Generate data with trends and noise
    data = {
        'date': dates_str,
        'risk_score': [min(0.95, max(0.05, base_risk + risk_trend*i + random.uniform(-volatility, volatility))) 
                      for i in range(MONTHS)],
        'confidence_score': [min(0.95, max(0.30, base_confidence + confidence_trend*i + random.uniform(-volatility, volatility))) 
                            for i in range(MONTHS)]
    }
    
    # Add component scores
    data['financial_health_score'] = [min(0.95, max(0.05, 1 - (data['risk_score'][i] * 0.8 + random.uniform(-volatility, volatility))))
                                     for i in range(MONTHS)]
    
    data['management_risk_score'] = [min(0.95, max(0.05, data['risk_score'][i] * 0.9 + random.uniform(-volatility, volatility)))
                                    for i in range(MONTHS)]
    
    data['industry_risk_score'] = [min(0.95, max(0.05, data['risk_score'][i] * 1.1 + random.uniform(-volatility, volatility)))
                                  for i in range(MONTHS)]
    
    data['external_context_score'] = [min(0.95, max(0.05, data['risk_score'][i] * 0.95 + random.uniform(-volatility, volatility)))
                                     for i in range(MONTHS)]
    
    # Convert to DataFrame
    return pd.DataFrame(data)

def generate_external_context(applicant_type="strong_applicant"):
    """Generate external context data based on applicant type."""
    
    # Base context sources common to all applicants
    context = {
        "industry_trends": {
            "active": True,
            "reliability": 0.85,
            "sources": [
                {
                    "name": "Industry Growth Forecast",
                    "type": "report",
                    "reliability": 0.88,
                    "date": (START_DATE + timedelta(days=45)).strftime("%Y-%m-%d")
                },
                {
                    "name": "Market Size Analysis",
                    "type": "market_research",
                    "reliability": 0.82,
                    "date": (START_DATE + timedelta(days=60)).strftime("%Y-%m-%d")
                }
            ]
        },
        "economic_indicators": {
            "active": True,
            "reliability": 0.92,
            "sources": [
                {
                    "name": "Federal Reserve Interest Rate Guidance",
                    "type": "official",
                    "reliability": 0.95,
                    "date": (START_DATE + timedelta(days=30)).strftime("%Y-%m-%d")
                },
                {
                    "name": "Quarterly GDP Report",
                    "type": "official",
                    "reliability": 0.90,
                    "date": (START_DATE + timedelta(days=50)).strftime("%Y-%m-%d")
                }
            ]
        }
    }
    
    # Add applicant-specific context
    if applicant_type == "strong_applicant":
        # Tech company context
        context["technology_adoption"] = {
            "active": True,
            "reliability": 0.82,
            "impact": 0.12,  # Positive impact
            "sources": [
                {
                    "name": "SaaS Adoption Survey",
                    "type": "market_research",
                    "reliability": 0.78,
                    "date": (START_DATE + timedelta(days=55)).strftime("%Y-%m-%d"),
                    "content": "Survey shows 42% increase in SaaS adoption among mid-sized businesses."
                },
                {
                    "name": "Cloud Technology Forecast",
                    "type": "analyst_report",
                    "reliability": 0.85,
                    "date": (START_DATE + timedelta(days=70)).strftime("%Y-%m-%d"),
                    "content": "Projected 22% CAGR for cloud workflow solutions over next 5 years."
                }
            ]
        }
        
        context["competitive_landscape"] = {
            "active": True,
            "reliability": 0.75,
            "impact": 0.08,  # Positive impact
            "sources": [
                {
                    "name": "Competitor Funding News",
                    "type": "news",
                    "reliability": 0.70,
                    "date": (START_DATE + timedelta(days=40)).strftime("%Y-%m-%d"),
                    "content": "Two competitors secured Series B funding, validating market potential."
                },
                {
                    "name": "Market Share Analysis",
                    "type": "market_research",
                    "reliability": 0.80,
                    "date": (START_DATE + timedelta(days=65)).strftime("%Y-%m-%d"),
                    "content": "Company has gained 2.5% market share in the past year."
                }
            ]
        }
    
    elif applicant_type == "unclear_applicant":
        # Manufacturing company context
        context["supply_chain_issues"] = {
            "active": True,
            "reliability": 0.78,
            "impact": -0.10,  # Negative impact
            "sources": [
                {
                    "name": "Materials Cost Index",
                    "type": "industry_data",
                    "reliability": 0.85,
                    "date": (START_DATE + timedelta(days=35)).strftime("%Y-%m-%d"),
                    "content": "Raw material costs increased 15% over past quarter."
                },
                {
                    "name": "Supply Chain Disruption Report",
                    "type": "news",
                    "reliability": 0.72,
                    "date": (START_DATE + timedelta(days=55)).strftime("%Y-%m-%d"),
                    "content": "Transportation delays affecting 40% of manufacturers in the sector."
                }
            ]
        }
        
        context["automation_trends"] = {
            "active": True,
            "reliability": 0.80,
            "impact": 0.15,  # Positive impact
            "sources": [
                {
                    "name": "Manufacturing Automation Report",
                    "type": "industry_report",
                    "reliability": 0.82,
                    "date": (START_DATE + timedelta(days=60)).strftime("%Y-%m-%d"),
                    "content": "Companies investing in automation seeing 28% efficiency improvements."
                },
                {
                    "name": "Industry 4.0 Adoption Study",
                    "type": "academic_research",
                    "reliability": 0.88,
                    "date": (START_DATE + timedelta(days=75)).strftime("%Y-%m-%d"),
                    "content": "Early adopters of smart manufacturing technologies showing 22% cost advantage."
                }
            ]
        }
    
    elif applicant_type == "challenged_applicant":
        # Retail company context
        context["retail_disruption"] = {
            "active": True,
            "reliability": 0.90,
            "impact": -0.25,  # Strong negative impact
            "sources": [
                {
                    "name": "Retail Sector Analysis",
                    "type": "industry_report",
                    "reliability": 0.92,
                    "date": (START_DATE + timedelta(days=30)).strftime("%Y-%m-%d"),
                    "content": "Physical retail locations decreasing at 8% annually in this segment."
                },
                {
                    "name": "E-commerce Impact Study",
                    "type": "market_research",
                    "reliability": 0.88,
                    "date": (START_DATE + timedelta(days=50)).strftime("%Y-%m-%d"),
                    "content": "E-commerce now accounts for 35% of sales in this category, up from 22% last year."
                }
            ]
        }
        
        context["consumer_behavior"] = {
            "active": True,
            "reliability": 0.75,
            "impact": -0.18,  # Negative impact
            "sources": [
                {
                    "name": "Consumer Spending Trends",
                    "type": "market_research",
                    "reliability": 0.78,
                    "date": (START_DATE + timedelta(days=40)).strftime("%Y-%m-%d"),
                    "content": "In-store visits down 22% year-over-year for this retail category."
                },
                {
                    "name": "Shopping Pattern Analysis",
                    "type": "behavioral_research",
                    "reliability": 0.72,
                    "date": (START_DATE + timedelta(days=65)).strftime("%Y-%m-%d"),
                    "content": "Consumers increasingly research online before making purchases, with 62% comparing prices digitally."
                }
            ]
        }
    
    return context

def generate_knowledge_graphs(applicant_type="strong_applicant"):
    """Generate knowledge graph evolution data based on applicant type."""
    # This is a placeholder for the structure - actual graph data would be created
    # at runtime based on this metadata when visualizing
    
    # Journey stages
    stages = [
        "Initial Application",
        "Information Gathering",
        "Risk Assessment",
        "Decision Point",
        "Monitoring Phase"
    ]
    
    # Graph complexity at each stage
    stage_complexity = {
        "Initial Application": {
            "node_count": 10,
            "relationship_types": ["basic_info", "industry", "loan_request"],
            "confidence": 0.45
        },
        "Information Gathering": {
            "node_count": 25,
            "relationship_types": ["basic_info", "industry", "loan_request", "financials", "management", "ownership"],
            "confidence": 0.65
        },
        "Risk Assessment": {
            "node_count": 40,
            "relationship_types": ["basic_info", "industry", "loan_request", "financials", "management", "ownership", "external_context", "market_position"],
            "confidence": 0.75
        },
        "Decision Point": {
            "node_count": 45,
            "relationship_types": ["basic_info", "industry", "loan_request", "financials", "management", "ownership", "external_context", "market_position", "risk_factors"],
            "confidence": 0.85
        },
        "Monitoring Phase": {
            "node_count": 55,
            "relationship_types": ["basic_info", "industry", "loan_request", "financials", "management", "ownership", "external_context", "market_position", "risk_factors", "temporal_patterns"],
            "confidence": 0.88
        }
    }
    
    return {
        "stages": stages,
        "complexity": stage_complexity
    }

def generate_next_best_information(applicant_type="strong_applicant"):
    """Generate next best information recommendations based on applicant type."""
    
    # Common information value categories
    base_info_value = {
        "Initial Application": {
            "Financial Statements": 0.85,
            "Management Background": 0.65,
            "Customer Contracts": 0.60,
            "Existing Debt Details": 0.72,
            "Business Plan": 0.58
        },
        "Information Gathering": {
            "Industry Forecast": 0.70,
            "Competitive Analysis": 0.65,
            "Detailed Cash Flow Projections": 0.82,
            "Customer Concentration Details": 0.75,
            "Collateral Valuation": 0.68
        },
        "Risk Assessment": {
            "Supply Chain Stability": 0.60,
            "Key Personnel Background": 0.55,
            "Technology Infrastructure": 0.50,
            "Regulatory Compliance Status": 0.58,
            "Market Share Trend": 0.65
        },
        "Decision Point": {
            "Stress Test Scenarios": 0.72,
            "Risk Mitigation Options": 0.68,
            "Additional Collateral Options": 0.60,
            "Reference Checks": 0.52,
            "Monitoring Plan": 0.75
        },
        "Monitoring Phase": {
            "Updated Financial Statements": 0.88,
            "Industry News Updates": 0.70,
            "Payment Pattern Analysis": 0.82,
            "Management Changes": 0.65,
            "Customer Relationship Status": 0.75
        }
    }
    
    # Adjust based on applicant type
    if applicant_type == "strong_applicant":
        # Minimal adjustments - already strong candidate
        pass
    
    elif applicant_type == "unclear_applicant":
        # Adjust to focus on clarifying uncertainties
        base_info_value["Information Gathering"]["Customer Concentration Details"] = 0.90
        base_info_value["Information Gathering"]["Industry Forecast"] = 0.85
        base_info_value["Risk Assessment"]["Supply Chain Stability"] = 0.82
        base_info_value["Risk Assessment"]["Competitive Positioning"] = 0.78
        base_info_value["Decision Point"]["Stress Test Scenarios"] = 0.85
    
    elif applicant_type == "challenged_applicant":
        # Adjust to focus on turnaround potential
        base_info_value["Information Gathering"]["Turnaround Plan"] = 0.92
        base_info_value["Information Gathering"]["Updated Management Structure"] = 0.88
        base_info_value["Risk Assessment"]["Cost Reduction Opportunities"] = 0.85
        base_info_value["Risk Assessment"]["Alternative Business Models"] = 0.80
        base_info_value["Decision Point"]["Additional Collateral Options"] = 0.88
    
    return base_info_value

def generate_reasoning_paths(applicant_type="strong_applicant"):
    """Generate reasoning paths for recommendations based on applicant type."""
    
    if applicant_type == "strong_applicant":
        reasoning = {
            "conclusion": "Approve with standard terms",
            "confidence": 0.85,
            "reasoning_steps": [
                ["Strong financial metrics", "Positive industry outlook", "Experienced management team"],
                ["Growth trend confirmed", "Debt service capacity validated", "Market position verified"]
            ],
            "counterfactuals": [
                "Would change to 'Approve with modified terms' if cash flow decreased by 20%",
                "Would change to 'Decline' if management team experienced significant turnover",
                "Would change to 'Request more information' if customer concentration exceeded 25%"
            ]
        }
    
    elif applicant_type == "unclear_applicant":
        reasoning = {
            "conclusion": "Approve with additional conditions",
            "confidence": 0.68,
            "reasoning_steps": [
                ["Mixed financial signals", "Industry transition period", "Strong management experience"],
                ["Modernization plan validated", "Customer concentration risk mitigated", "Collateral value sufficient"]
            ],
            "counterfactuals": [
                "Would change to 'Approve with standard terms' if equipment modernization plan showed 30%+ efficiency gain",
                "Would change to 'Decline' if raw material costs increased another 20%",
                "Would change to 'Decline' if largest customer contract was not renewed"
            ]
        }
    
    elif applicant_type == "challenged_applicant":
        reasoning = {
            "conclusion": "Decline application",
            "confidence": 0.82,
            "reasoning_steps": [
                ["Declining financial performance", "Industry disruption accelerating", "Recent management turnover"],
                ["Cash flow insufficient for debt service", "Business model viability concerns", "Insufficient turnaround evidence"]
            ],
            "counterfactuals": [
                "Would change to 'Approve with modified terms' if significant additional collateral was provided",
                "Would change to 'Approve with conditions' if comprehensive turnaround plan demonstrated viability",
                "Would change to 'Request more information' if new management team showed successful retail turnarounds"
            ]
        }
    
    return reasoning

def generate_confidence_components(applicant_type="strong_applicant"):
    """Generate confidence component breakdown based on applicant type."""
    
    if applicant_type == "strong_applicant":
        components = {
            "Financial Data Quality": 0.92,
            "Management Assessment": 0.88,
            "Industry Trend Clarity": 0.85,
            "Market Position Certainty": 0.78,
            "Temporal Pattern Consistency": 0.90
        }
    
    elif applicant_type == "unclear_applicant":
        components = {
            "Financial Data Quality": 0.85,
            "Management Assessment": 0.80,
            "Industry Trend Clarity": 0.62,
            "Market Position Certainty": 0.70,
            "Temporal Pattern Consistency": 0.75
        }
    
    elif applicant_type == "challenged_applicant":
        components = {
            "Financial Data Quality": 0.78,
            "Management Assessment": 0.55,
            "Industry Trend Clarity": 0.88,  # High certainty about negative trends
            "Market Position Certainty": 0.82,
            "Temporal Pattern Consistency": 0.85
        }
    
    return components

def generate_all_data():
    """Generate and save all data files for all applicant types."""
    ensure_data_directories()
    
    applicant_types = ["strong_applicant", "unclear_applicant", "challenged_applicant"]
    
    for applicant_type in applicant_types:
        # Check if data already exists
        if check_data_exists(applicant_type):
            print(f"Data for {applicant_type} already exists. Skipping generation.")
            continue
        
        print(f"Generating data for {applicant_type}...")
        
        # Generate and save all data
        company_profile = generate_company_profile(applicant_type)
        save_data(company_profile, "company_profile", applicant_type)
        
        financial_data = generate_financial_data(applicant_type)
        save_data(financial_data, "financial_data", applicant_type)
        
        events = generate_events(applicant_type)
        save_data(events, "events", applicant_type)
        
        risk_scores = generate_risk_scores(applicant_type)
        save_data(risk_scores, "risk_scores", applicant_type)
        
        external_context = generate_external_context(applicant_type)
        save_data(external_context, "external_context", applicant_type)
        
        knowledge_graphs = generate_knowledge_graphs(applicant_type)
        save_data(knowledge_graphs, "knowledge_graphs", applicant_type)
        
        next_best_info = generate_next_best_information(applicant_type)
        save_data(next_best_info, "next_best_information", applicant_type)
        
        reasoning_paths = generate_reasoning_paths(applicant_type)
        save_data(reasoning_paths, "reasoning_paths", applicant_type)
        
        confidence_components = generate_confidence_components(applicant_type)
        save_data(confidence_components, "confidence_components", applicant_type)
        
        print(f"Data generation complete for {applicant_type}.")
    
    print("All data generation complete.")

# Functions to load data at runtime
def load_applicant_data(applicant_type="strong_applicant"):
    """Load all data for a specific applicant type."""
    data = {}
    
    try:
        data["company_profile"] = load_data("company_profile", applicant_type)
        data["financial_data"] = load_data("financial_data", applicant_type, "csv")
        data["events"] = load_data("events", applicant_type)
        data["risk_scores"] = load_data("risk_scores", applicant_type, "csv")
        data["external_context"] = load_data("external_context", applicant_type)
        data["knowledge_graphs"] = load_data("knowledge_graphs", applicant_type)
        data["next_best_information"] = load_data("next_best_information", applicant_type)
        data["reasoning_paths"] = load_data("reasoning_paths", applicant_type)
        data["confidence_components"] = load_data("confidence_components", applicant_type)
        
        return data
    except Exception as e:
        print(f"Error loading data for {applicant_type}: {e}")
        return None

def get_signal_library():
    """Return the signal library for signal amplification demo."""
    return {
        "Company Signals": [
            "Revenue Decline",
            "Margin Pressure",
            "Cash Flow Reduction",
            "Management Turnover",
            "Inventory Buildup",
            "Delayed Financial Filing"
        ],
        "Industry Signals": [
            "Industry Slowdown",
            "Competitor Struggles",
            "Supply Chain Disruption",
            "Technology Shift",
            "Regulatory Changes",
            "Market Saturation"
        ],
        "Economic Signals": [
            "Interest Rate Increase",
            "Consumer Confidence Drop",
            "Credit Market Tightening",
            "Currency Fluctuations",
            "Inflation Acceleration",
            "Employment Trend Change"
        ]
    }

# If this module is run directly, generate all data
if __name__ == "__main__":
    generate_all_data()