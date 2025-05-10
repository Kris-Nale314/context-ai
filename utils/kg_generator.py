# utils/kg_generator.py
import networkx as nx
import pandas as pd
from utils.theme import COLORS

def create_initial_knowledge_graph(company_profile):
    """
    Create the initial knowledge graph for a loan application with basic information.
    
    Args:
        company_profile: Dictionary containing company profile information
        
    Returns:
        NetworkX graph object representing the initial knowledge graph
    """
    G = nx.Graph()
    
    # Add main company node
    G.add_node(company_profile['name'], 
               size=30, 
               color=COLORS['digital_twin'], 
               title=company_profile['name'])
    
    # Add basic info group
    G.add_node("Basic Information", 
               size=20, 
               color=COLORS['primary'], 
               title="Basic Company Information")
    G.add_edge(company_profile['name'], "Basic Information", width=2)
    
    # Add basic company info nodes
    basic_info = [
        {"name": f"Industry: {company_profile['industry']}", 
         "title": f"Industry: {company_profile['industry']}"},
        {"name": f"Business Type: {company_profile['business_type']}", 
         "title": f"Business Type: {company_profile['business_type']}"},
        {"name": f"Years in Business: {company_profile['years_in_business']}", 
         "title": f"Years in Business: {company_profile['years_in_business']}"},
        {"name": f"Employees: {company_profile['employees']}", 
         "title": f"Employees: {company_profile['employees']}"},
        {"name": f"Location: {company_profile['location']}", 
         "title": f"Location: {company_profile['location']}"}
    ]
    
    for info in basic_info:
        G.add_node(info["name"], size=15, color=COLORS['primary'], title=info["title"])
        G.add_edge("Basic Information", info["name"], width=1)
    
    # Add loan request group
    G.add_node("Loan Request", 
               size=20, 
               color=COLORS['primary'], 
               title="Loan Request Details")
    G.add_edge(company_profile['name'], "Loan Request", width=2)
    
    # Add loan request details
    loan_info = [
        {"name": f"Amount: ${company_profile['loan_amount_requested']:,}", 
         "title": f"Loan Amount: ${company_profile['loan_amount_requested']:,}"},
        {"name": f"Purpose: {company_profile['loan_purpose']}", 
         "title": f"Loan Purpose: {company_profile['loan_purpose']}"},
        {"name": f"Term: {company_profile['loan_term_requested']} years", 
         "title": f"Loan Term: {company_profile['loan_term_requested']} years"},
        {"name": f"Collateral: {company_profile['collateral_offered']}", 
         "title": f"Collateral: {company_profile['collateral_offered']}"}
    ]
    
    for info in loan_info:
        G.add_node(info["name"], size=15, color=COLORS['primary'], title=info["title"])
        G.add_edge("Loan Request", info["name"], width=1)
    
    # Add credit history group
    G.add_node("Credit History", 
               size=20, 
               color=COLORS['primary'], 
               title="Credit History")
    G.add_edge(company_profile['name'], "Credit History", width=2)
    
    # Add credit history details
    credit_info = [
        {"name": f"Credit Score: {company_profile['credit_score']}", 
         "title": f"Credit Score: {company_profile['credit_score']}"},
        {"name": f"Previous Loans: {company_profile['previous_loans']}", 
         "title": f"Previous Loans: {company_profile['previous_loans']}"},
        {"name": f"Loans Repaid: {company_profile['previous_loans_repaid']}", 
         "title": f"Loans Repaid: {company_profile['previous_loans_repaid']}"}
    ]
    
    for info in credit_info:
        G.add_node(info["name"], size=15, color=COLORS['primary'], title=info["title"])
        G.add_edge("Credit History", info["name"], width=1)
    
    return G

def create_expanded_knowledge_graph(company_profile, financial_data):
    """
    Create an expanded knowledge graph with financial and management data.
    
    Args:
        company_profile: Dictionary containing company profile information
        financial_data: DataFrame or dictionary containing financial metrics
        
    Returns:
        NetworkX graph object representing the expanded knowledge graph
    """
    # Start with initial graph
    G = create_initial_knowledge_graph(company_profile)
    
    # If financial_data is a DataFrame, convert relevant row to dict
    if isinstance(financial_data, pd.DataFrame):
        if len(financial_data) > 0:
            financial_data = financial_data.iloc[0].to_dict()
    
    # Add financial metrics group
    G.add_node("Financial Metrics", 
               size=20, 
               color=COLORS['primary'], 
               title="Financial Metrics")
    G.add_edge(company_profile['name'], "Financial Metrics", width=2)
    
    # Add financial metrics
    financial_metrics = [
        {"name": f"Revenue: ${financial_data.get('revenue', 0):,.0f}", 
         "title": f"Revenue: ${financial_data.get('revenue', 0):,.0f}"},
        {"name": f"Profit Margin: {financial_data.get('profit_margin', 0)*100:.1f}%", 
         "title": f"Profit Margin: {financial_data.get('profit_margin', 0)*100:.1f}%"},
        {"name": f"Cash Balance: ${financial_data.get('cash_balance', 0):,.0f}", 
         "title": f"Cash Balance: ${financial_data.get('cash_balance', 0):,.0f}"},
        {"name": f"Debt Ratio: {financial_data.get('debt_ratio', 0):.2f}", 
         "title": f"Debt Ratio: {financial_data.get('debt_ratio', 0):.2f}"}
    ]
    
    for metric in financial_metrics:
        G.add_node(metric["name"], size=15, color=COLORS['primary'], title=metric["title"])
        G.add_edge("Financial Metrics", metric["name"], width=1)
    
    # Add industry-specific metrics if available
    if company_profile['industry'] == "Software Development" and 'customer_acquisition_cost' in financial_data:
        G.add_node("SaaS Metrics", 
                   size=20, 
                   color=COLORS['primary'], 
                   title="SaaS Business Metrics")
        G.add_edge(company_profile['name'], "SaaS Metrics", width=2)
        
        saas_metrics = [
            {"name": f"CAC: ${financial_data.get('customer_acquisition_cost', 0):.0f}", 
             "title": f"Customer Acquisition Cost: ${financial_data.get('customer_acquisition_cost', 0):.0f}"},
            {"name": f"MRR: ${financial_data.get('monthly_recurring_revenue', 0):,.0f}", 
             "title": f"Monthly Recurring Revenue: ${financial_data.get('monthly_recurring_revenue', 0):,.0f}"},
            {"name": f"LTV: ${financial_data.get('customer_lifetime_value', 0):,.0f}", 
             "title": f"Customer Lifetime Value: ${financial_data.get('customer_lifetime_value', 0):,.0f}"}
        ]
        
        for metric in saas_metrics:
            G.add_node(metric["name"], size=15, color=COLORS['primary'], title=metric["title"])
            G.add_edge("SaaS Metrics", metric["name"], width=1)
    
    elif company_profile['industry'] == "Manufacturing" and 'raw_material_costs' in financial_data:
        G.add_node("Manufacturing Metrics", 
                   size=20, 
                   color=COLORS['primary'], 
                   title="Manufacturing Metrics")
        G.add_edge(company_profile['name'], "Manufacturing Metrics", width=2)
        
        mfg_metrics = [
            {"name": f"Material Costs: ${financial_data.get('raw_material_costs', 0):,.0f}", 
             "title": f"Raw Material Costs: ${financial_data.get('raw_material_costs', 0):,.0f}"},
            {"name": f"Capacity Utilization: {financial_data.get('capacity_utilization', 0)*100:.1f}%", 
             "title": f"Capacity Utilization: {financial_data.get('capacity_utilization', 0)*100:.1f}%"},
            {"name": f"Order Backlog: ${financial_data.get('order_backlog', 0):,.0f}", 
             "title": f"Order Backlog: ${financial_data.get('order_backlog', 0):,.0f}"}
        ]
        
        for metric in mfg_metrics:
            G.add_node(metric["name"], size=15, color=COLORS['primary'], title=metric["title"])
            G.add_edge("Manufacturing Metrics", metric["name"], width=1)
    
    elif company_profile['industry'] == "Retail" and 'same_store_sales_growth' in financial_data:
        G.add_node("Retail Metrics", 
                   size=20, 
                   color=COLORS['primary'], 
                   title="Retail Metrics")
        G.add_edge(company_profile['name'], "Retail Metrics", width=2)
        
        retail_metrics = [
            {"name": f"Same Store Sales Growth: {financial_data.get('same_store_sales_growth', 0)*100:.1f}%", 
             "title": f"Same Store Sales Growth: {financial_data.get('same_store_sales_growth', 0)*100:.1f}%"},
            {"name": f"Inventory Turnover: {financial_data.get('inventory_turnover', 0):.1f}x", 
             "title": f"Inventory Turnover: {financial_data.get('inventory_turnover', 0):.1f}x"},
            {"name": f"Customer Traffic: {financial_data.get('customer_traffic', 0):,.0f}", 
             "title": f"Monthly Customer Traffic: {financial_data.get('customer_traffic', 0):,.0f}"}
        ]
        
        for metric in retail_metrics:
            G.add_node(metric["name"], size=15, color=COLORS['primary'], title=metric["title"])
            G.add_edge("Retail Metrics", metric["name"], width=1)
    
    # Add management information
    G.add_node("Management", 
               size=20, 
               color=COLORS['primary'], 
               title="Management Information")
    G.add_edge(company_profile['name'], "Management", width=2)
    
    management_info = [
        {"name": f"Team Size: {company_profile.get('management_team_size', 'Unknown')}", 
         "title": f"Management Team Size: {company_profile.get('management_team_size', 'Unknown')}"},
        {"name": f"Experience: {company_profile.get('management_experience_years', 'Unknown')} years", 
         "title": f"Average Experience: {company_profile.get('management_experience_years', 'Unknown')} years"}
    ]
    
    for info in management_info:
        G.add_node(info["name"], size=15, color=COLORS['primary'], title=info["title"])
        G.add_edge("Management", info["name"], width=1)
    
    # Add customer information if available
    if 'customer_count' in company_profile and company_profile['customer_count'] != "General public":
        G.add_node("Customers", 
                  size=20, 
                  color=COLORS['primary'], 
                  title="Customer Information")
        G.add_edge(company_profile['name'], "Customers", width=2)
        
        customer_info = [
            {"name": f"Count: {company_profile.get('customer_count', 'Unknown')}", 
             "title": f"Customer Count: {company_profile.get('customer_count', 'Unknown')}"},
            {"name": f"Concentration: {company_profile.get('largest_customer_percentage', 'Unknown')}%", 
             "title": f"Largest Customer: {company_profile.get('largest_customer_percentage', 'Unknown')}% of revenue"}
        ]
        
        for info in customer_info:
            G.add_node(info["name"], size=15, color=COLORS['primary'], title=info["title"])
            G.add_edge("Customers", info["name"], width=1)
    
    return G

def create_comprehensive_knowledge_graph(company_profile, financial_data, risk_data, external_context=None):
    """
    Create a comprehensive knowledge graph with all layers integrated.
    
    Args:
        company_profile: Dictionary containing company profile information
        financial_data: DataFrame or dictionary containing financial metrics
        risk_data: DataFrame or dictionary containing risk assessment data
        external_context: Dictionary containing external context data (optional)
        
    Returns:
        NetworkX graph object representing the comprehensive knowledge graph
    """
    # Start with expanded graph
    G = create_expanded_knowledge_graph(company_profile, financial_data)
    
    # Convert DataFrame rows to dict if needed
    if isinstance(risk_data, pd.DataFrame) and len(risk_data) > 0:
        risk_data = risk_data.iloc[0].to_dict()
    
    # Add risk assessment group
    G.add_node("Risk Assessment", 
               size=20, 
               color=COLORS['guidance'], 
               title="Risk Assessment")
    G.add_edge(company_profile['name'], "Risk Assessment", width=2)
    
    # Add risk metrics
    risk_metrics = [
        {"name": f"Risk Score: {risk_data.get('risk_score', 0):.2f}", 
         "title": f"Overall Risk Score: {risk_data.get('risk_score', 0):.2f}"},
        {"name": f"Confidence: {risk_data.get('confidence_score', 0):.2f}", 
         "title": f"Confidence Score: {risk_data.get('confidence_score', 0):.2f}"}
    ]
    
    # Add component scores if available
    if 'financial_health_score' in risk_data:
        risk_metrics.append({
            "name": f"Financial Health: {risk_data.get('financial_health_score', 0):.2f}", 
            "title": f"Financial Health Score: {risk_data.get('financial_health_score', 0):.2f}"
        })
    
    if 'management_risk_score' in risk_data:
        risk_metrics.append({
            "name": f"Management Risk: {risk_data.get('management_risk_score', 0):.2f}", 
            "title": f"Management Risk Score: {risk_data.get('management_risk_score', 0):.2f}"
        })
    
    if 'industry_risk_score' in risk_data:
        risk_metrics.append({
            "name": f"Industry Risk: {risk_data.get('industry_risk_score', 0):.2f}", 
            "title": f"Industry Risk Score: {risk_data.get('industry_risk_score', 0):.2f}"
        })
    
    if 'external_context_score' in risk_data:
        risk_metrics.append({
            "name": f"External Risk: {risk_data.get('external_context_score', 0):.2f}", 
            "title": f"External Context Risk Score: {risk_data.get('external_context_score', 0):.2f}"
        })
    
    for metric in risk_metrics:
        G.add_node(metric["name"], size=15, color=COLORS['guidance'], title=metric["title"])
        G.add_edge("Risk Assessment", metric["name"], width=1)
    
    # Add external context if provided
    if external_context:
        G.add_node("External Context", 
                   size=20, 
                   color=COLORS['external'], 
                   title="External Context")
        G.add_edge(company_profile['name'], "External Context", width=2)
        
        # Add active context sources
        for source_name, source_data in external_context.items():
            if source_data.get("active", False):
                # Add the context source node
                source_node_name = f"{source_name}"
                G.add_node(source_node_name, 
                           size=15, 
                           color=COLORS['external'], 
                           title=f"{source_name} (Reliability: {source_data.get('reliability', 0):.2f})")
                G.add_edge("External Context", source_node_name, width=1)
                
                # Add source details if sources are available
                if "sources" in source_data:
                    for i, src in enumerate(source_data["sources"]):
                        if i < 2:  # Limit to 2 sources per category to avoid overloading
                            source_detail_name = f"{src.get('name', 'Source')}"
                            G.add_node(source_detail_name, 
                                       size=10, 
                                       color=COLORS['external'], 
                                       title=f"{src.get('content', src.get('name', 'Source'))}")
                            G.add_edge(source_node_name, source_detail_name, width=1)
    
    # Add temporal intelligence layer if we have multiple time points of data
    if isinstance(financial_data, pd.DataFrame) and len(financial_data) > 1:
        G.add_node("Temporal Intelligence", 
                   size=20, 
                   color=COLORS['temporal'], 
                   title="Temporal Intelligence")
        G.add_edge(company_profile['name'], "Temporal Intelligence", width=2)
        
        # Add trend nodes based on industry
        if company_profile['industry'] == "Software Development":
            trends = [
                {"name": "Growth Trend", 
                 "title": "Consistent revenue growth pattern"},
                {"name": "Margin Stability", 
                 "title": "Stable profit margins over time"},
                {"name": "Increasing LTV/CAC Ratio", 
                 "title": "Improving unit economics"}
            ]
        elif company_profile['industry'] == "Manufacturing":
            trends = [
                {"name": "Capacity Utilization Trend", 
                 "title": "Changing factory utilization over time"},
                {"name": "Material Cost Pressure", 
                 "title": "Rising raw material costs"},
                {"name": "Order Backlog Evolution", 
                 "title": "Changing order pipeline"}
            ]
        elif company_profile['industry'] == "Retail":
            trends = [
                {"name": "Store Traffic Decline", 
                 "title": "Decreasing customer visits over time"},
                {"name": "Margin Compression", 
                 "title": "Decreasing profit margins"},
                {"name": "Inventory Turnover Slowdown", 
                 "title": "Slowing inventory movement"}
            ]
        else:
            trends = [
                {"name": "Revenue Trend", 
                 "title": "Revenue change over time"},
                {"name": "Margin Trend", 
                 "title": "Profit margin evolution"},
                {"name": "Cash Flow Pattern", 
                 "title": "Cash flow stability over time"}
            ]
        
        for trend in trends:
            G.add_node(trend["name"], size=15, color=COLORS['temporal'], title=trend["title"])
            G.add_edge("Temporal Intelligence", trend["name"], width=1)
    
    # Add cross-connections to show relationships between nodes
    # Connect risk scores to relevant data
    if "Financial Health: " in G.nodes:
        relevant_nodes = [n for n in G.nodes if "Financial Metrics" in n]
        if relevant_nodes:
            G.add_edge("Financial Health: " + str(risk_data.get('financial_health_score', 0)), 
                      "Financial Metrics", width=1, color=COLORS['edge_default'])
    
    if "Industry Risk: " in G.nodes and "External Context" in G.nodes:
        G.add_edge("Industry Risk: " + str(risk_data.get('industry_risk_score', 0)), 
                  "External Context", width=1, color=COLORS['edge_default'])
    
    if "Management Risk: " in G.nodes and "Management" in G.nodes:
        G.add_edge("Management Risk: " + str(risk_data.get('management_risk_score', 0)), 
                  "Management", width=1, color=COLORS['edge_default'])
    
    # Connect relevant external context to financial metrics
    if "External Context" in G.nodes and "Financial Metrics" in G.nodes:
        G.add_edge("External Context", "Financial Metrics", width=1, color=COLORS['edge_default'])
    
    # Connect temporal intelligence to financial metrics
    if "Temporal Intelligence" in G.nodes and "Financial Metrics" in G.nodes:
        G.add_edge("Temporal Intelligence", "Financial Metrics", width=1, color=COLORS['edge_default'])
    
    return G

def get_graph_for_stage(applicant_data, journey_stage, stage_to_index=None):
    """
    Get the appropriate knowledge graph for a specific journey stage.
    
    Args:
        applicant_data: Dictionary containing all applicant data
        journey_stage: String indicating the current journey stage
        stage_to_index: Dictionary mapping stages to data indices (optional)
        
    Returns:
        NetworkX graph object for the specified stage
    """
    company_profile = applicant_data["company_profile"]
    financial_data = applicant_data["financial_data"]
    risk_scores = applicant_data["risk_scores"]
    external_context = applicant_data.get("external_context", None)
    
    # Default stage to index mapping if not provided
    if stage_to_index is None:
        stage_to_index = {
            "Initial Application": 0,
            "Information Gathering": 2,
            "Risk Assessment": 5,
            "Decision Point": 8,
            "Monitoring Phase": 11
        }
    
    # Get the appropriate index for the current stage
    current_index = stage_to_index.get(journey_stage, 0)
    
    # Create graph based on journey stage
    if journey_stage == "Initial Application":
        return create_initial_knowledge_graph(company_profile)
    
    elif journey_stage == "Information Gathering":
        return create_expanded_knowledge_graph(company_profile, financial_data.iloc[current_index])
    
    else:  # Risk Assessment, Decision Point, or Monitoring
        return create_comprehensive_knowledge_graph(
            company_profile, 
            financial_data.iloc[current_index], 
            risk_scores.iloc[current_index], 
            external_context
        )

# In utils/kg_generator.py

def get_graph_for_stage(applicant_data, journey_stage, stage_to_index=None):
    """
    Get the appropriate knowledge graph for a specific journey stage.
    
    Args:
        applicant_data: Dictionary containing all applicant data
        journey_stage: String indicating the current journey stage
        stage_to_index: Dictionary mapping stages to data indices (optional)
        
    Returns:
        NetworkX graph object for the specified stage
    """
    try:
        company_profile = applicant_data["company_profile"]
        financial_data = applicant_data["financial_data"]
        risk_scores = applicant_data["risk_scores"]
        external_context = applicant_data.get("external_context", None)
        
        # Default stage to index mapping if not provided
        if stage_to_index is None:
            stage_to_index = {
                "Initial Application": 0,
                "Information Gathering": 2,
                "Risk Assessment": 5,
                "Decision Point": 8,
                "Monitoring Phase": 11
            }
        
        # Get the appropriate index for the current stage
        current_index = stage_to_index.get(journey_stage, 0)
        
        # Make sure current_index is valid
        if current_index >= len(financial_data):
            current_index = len(financial_data) - 1
            print(f"Warning: Adjusted current_index to {current_index}")
        
        # Create graph based on journey stage
        if journey_stage == "Initial Application":
            return create_initial_knowledge_graph(company_profile)
        
        elif journey_stage == "Information Gathering":
            return create_expanded_knowledge_graph(company_profile, financial_data.iloc[current_index])
        
        else:  # Risk Assessment, Decision Point, or Monitoring
            return create_comprehensive_knowledge_graph(
                company_profile, 
                financial_data.iloc[current_index], 
                risk_scores.iloc[current_index], 
                external_context
            )
    except Exception as e:
        import traceback
        print(f"Error generating graph: {e}")
        print(traceback.format_exc())
        
        # Return a simple fallback graph
        G = nx.Graph()
        G.add_node("Error", size=25, color=COLORS['low_confidence'], 
                   title=f"Error generating graph: {str(e)}")
        return G