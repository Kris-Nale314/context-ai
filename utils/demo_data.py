# utils/demo_data.py
import pandas as pd
import numpy as np
import networkx as nx
import random
from datetime import datetime, timedelta
from utils.theme import COLORS

def generate_company_timeline_data(num_months=12):
    """Generate sample timeline data for a company."""
    # Start date
    start_date = datetime(2023, 1, 1)
    
    # Create dates
    dates = [start_date + timedelta(days=30*i) for i in range(num_months)]
    
    # Base values
    base_revenue = 1000000
    base_profit_margin = 0.15
    base_cash_flow = 120000
    base_debt_ratio = 0.35
    base_risk_score = 0.30
    
    # Generate data with trends and noise
    data = {
        'date': dates,
        'revenue': [base_revenue * (1 + 0.02*i + random.uniform(-0.05, 0.05)) 
                   for i in range(num_months)],
        'profit_margin': [max(0.01, base_profit_margin * (1 - 0.01*i + random.uniform(-0.05, 0.05)))
                         for i in range(num_months)],
        'cash_flow': [base_cash_flow * (1 + 0.01*i + random.uniform(-0.1, 0.1)) 
                     for i in range(num_months)],
        'debt_ratio': [min(0.9, base_debt_ratio * (1 + 0.02*i + random.uniform(-0.05, 0.05)))
                      for i in range(num_months)],
        'risk_score': [min(0.9, max(0.1, base_risk_score * (1 + 0.05*i + random.uniform(-0.1, 0.1))))
                      for i in range(num_months)]
    }
    
    # Create events
    events = [
        {
            'date': dates[1],
            'event': 'Loan application submitted',
            'category': 'application',
            'type': 'info'
        },
        {
            'date': dates[2],
            'event': 'Initial approval with conditions',
            'category': 'approval',
            'type': 'positive'
        },
        {
            'date': dates[4],
            'event': 'Industry slowdown reported',
            'category': 'external',
            'type': 'warning'
        },
        {
            'date': dates[6],
            'event': 'Q2 financial results below projections',
            'category': 'financial',
            'type': 'negative'
        },
        {
            'date': dates[8],
            'event': 'Cost-cutting measures implemented',
            'category': 'company',
            'type': 'info'
        },
        {
            'date': dates[10],
            'event': 'New major customer contract signed',
            'category': 'company',
            'type': 'positive'
        }
    ]
    
    # Return as DataFrame
    return pd.DataFrame(data), events

def generate_loan_journey_data():
    """Generate sample data for a loan journey demonstration."""
    # Journey stages
    stages = [
        "Initial Application",
        "Information Gathering",
        "Risk Assessment",
        "Decision Point",
        "Monitoring Phase"
    ]
    
    # Risk scores for each stage
    risk_scores = [0.45, 0.52, 0.38, 0.35, 0.41]
    
    # Confidence scores for each stage
    confidence_scores = [0.52, 0.68, 0.75, 0.82, 0.78]
    
    # Key factors at each stage
    key_factors = [
        ["Basic application data", "Industry classification", "Credit history"],
        ["Financial statements", "Customer relationships", "Market position", "Management team"],
        ["Financial ratios", "Industry trends", "Competitor performance", "Economic indicators"],
        ["Risk level", "Confidence assessment", "Decision reasoning", "Terms and conditions"],
        ["Payment performance", "Financial updates", "Market changes", "Risk trend"]
    ]
    
    # Next best information at each stage
    next_info = [
        ["Complete financial statements", "Customer concentration details", "Collateral documentation"],
        ["Industry forecast", "Competitive positioning details", "Cash flow projections"],
        ["Market share trend", "Supply chain stability", "Customer contract renewals"],
        ["Stress test scenarios", "Risk mitigation options", "Monitoring plan"],
        ["Updated financial statements", "Industry news updates", "Payment pattern analysis"]
    ]
    
    # Return as dictionary
    return {
        "stages": stages,
        "risk_scores": risk_scores,
        "confidence_scores": confidence_scores,
        "key_factors": key_factors,
        "next_info": next_info
    }

def generate_kg_evolution(stage_idx):
    """Generate knowledge graph at different stages of the loan journey."""
    G = nx.Graph()
    
    # Core entity
    G.add_node("ACME Corp", size=30, color=COLORS['digital_twin'], title="ACME Corporation")
    
    # Basic data always present
    G.add_node("Industry: Manufacturing", size=15, color=COLORS['primary'], 
              title="Industry Classification")
    G.add_edge("ACME Corp", "Industry: Manufacturing", width=2)
    
    G.add_node("Business Age: 7 years", size=15, color=COLORS['primary'], 
              title="Years in Business")
    G.add_edge("ACME Corp", "Business Age: 7 years", width=2)
    
    G.add_node("Loan Request: $500K", size=15, color=COLORS['primary'], 
              title="Requested Loan Amount")
    G.add_edge("ACME Corp", "Loan Request: $500K", width=2)
    
    # Add nodes based on stage
    if stage_idx >= 1:  # Information Gathering or beyond
        # Financial data
        G.add_node("Financials", size=20, color=COLORS['primary'], title="Financial Information")
        G.add_edge("ACME Corp", "Financials", width=2)
        
        financial_nodes = [
            "Revenue: $2.4M",
            "Profit Margin: 12%",
            "Cash Balance: $320K"
        ]
        
        for node in financial_nodes:
            G.add_node(node, size=10, color=COLORS['primary'], title=node)
            G.add_edge("Financials", node, width=1)
    
    if stage_idx >= 2:  # Risk Assessment or beyond
        # External context
        G.add_node("Market Context", size=20, color=COLORS['external'], 
                  title="External Market Context")
        G.add_edge("ACME Corp", "Market Context", width=2)
        
        market_nodes = [
            "Industry Growth: 3.2%",
            "Competitor Trends",
            "Economic Indicators"
        ]
        
        for node in market_nodes:
            G.add_node(node, size=10, color=COLORS['external'], title=node)
            G.add_edge("Market Context", node, width=1)
    
    if stage_idx >= 3:  # Decision Point or beyond
        # Risk assessment
        G.add_node("Risk Assessment", size=20, color=COLORS['guidance'], 
                  title="Risk Assessment")
        G.add_edge("ACME Corp", "Risk Assessment", width=2)
        
        risk_nodes = [
            "Credit Score: B+",
            "Debt Service: 1.4x",
            "Risk Level: Medium-Low"
        ]
        
        for node in risk_nodes:
            G.add_node(node, size=10, color=COLORS['guidance'], title=node)
            G.add_edge("Risk Assessment", node, width=1)
    
    if stage_idx >= 4:  # Monitoring Phase
        # Temporal intelligence
        G.add_node("Historical Trends", size=20, color=COLORS['temporal'], 
                  title="Temporal Intelligence")
        G.add_edge("ACME Corp", "Historical Trends", width=2)
        
        temporal_nodes = [
            "Payment History: Strong",
            "Growth Trend: Steady",
            "Risk Evolution: Stable"
        ]
        
        for node in temporal_nodes:
            G.add_node(node, size=10, color=COLORS['temporal'], title=node)
            G.add_edge("Historical Trends", node, width=1)
        
        # Add some cross-connections to show relationships
        G.add_edge("Payment History: Strong", "Risk Level: Medium-Low", width=1, color=COLORS['edge_default'])
        G.add_edge("Industry Growth: 3.2%", "Growth Trend: Steady", width=1, color=COLORS['edge_default'])
    
    return G

def generate_signal_library():
    """Generate a library of signals for the signal amplification demo."""
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