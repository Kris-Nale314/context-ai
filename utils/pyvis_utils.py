# utils/pyvis_utils.py
import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
from utils.theme import COLORS

def interactive_knowledge_graph(G, height=500, width=None, physics=True, 
                              bgcolor=COLORS['bg_dark'], font_color=COLORS['text_primary'],
                              buttons=True):
    """
    Create an interactive PyVis graph visualization.
    
    Args:
        G: NetworkX graph object
        height: Height of the visualization in pixels
        width: Width of the visualization (or None for container width)
        physics: Whether to enable physics simulation
        bgcolor: Background color
        font_color: Font color for labels
        buttons: Whether to show physics control buttons
        
    Returns:
        HTML component with the interactive visualization
    """
    # Default width to 100% for responsive design
    if width is None:
        width = "100%"
    
    # Create PyVis network
    net = Network(height=f"{height}px", width=width, notebook=False, 
                 bgcolor=bgcolor, font_color=font_color)
    
    # Add nodes with properties
    for node, node_attrs in G.nodes(data=True):
        size = node_attrs.get('size', 25)
        title = node_attrs.get('title', str(node))
        color = node_attrs.get('color', COLORS['node_default'])
        shape = node_attrs.get('shape', 'dot')
        
        net.add_node(str(node), title=title, color=color, size=size, shape=shape, label=str(node))
    
    # Add edges with properties
    for source, target, edge_attrs in G.edges(data=True):
        width = edge_attrs.get('width', 1)
        color = edge_attrs.get('color', COLORS['edge_default'])
        title = edge_attrs.get('title', '')
        
        net.add_edge(str(source), str(target), width=width, color=color, title=title)
    
    # Configure physics
    if physics:
        net.force_atlas_2based(spring_length=200, spring_strength=0.05, damping=0.2)
        if buttons:
            net.show_buttons(['physics'])
    else:
        net.toggle_physics(False)
    
    # Set options for better interaction
    net.set_options("""
    const options = {
      "nodes": {
        "borderWidth": 1,
        "borderWidthSelected": 2,
        "font": {
          "size": 14,
          "face": "arial"
        }
      },
      "edges": {
        "smooth": {
          "type": "continuous",
          "forceDirection": "none"
        }
      },
      "interaction": {
        "navigationButtons": true,
        "hover": true,
        "multiselect": true,
        "dragNodes": true
      },
      "physics": {
        "stabilization": {
          "iterations": 100
        },
        "barnesHut": {
          "gravitationalConstant": -80000,
          "springConstant": 0.001,
          "springLength": 200
        }
      }
    }
    """)
    
    # Generate HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
        path = temp.name
        net.save_graph(path)
    
    # Read HTML content
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Clean up the temporary file
    try:
        os.unlink(path)
    except:
        pass
    
    # Display the interactive graph
    return components.html(html, height=height, width=width)

def create_comparison_graph():
    """
    Create a simple comparison graph showing traditional vs knowledge graph data models.
    
    Returns:
        Two NetworkX graphs: traditional model and knowledge graph model
    """
    # Traditional data model (simplified relational model)
    traditional_G = nx.DiGraph()
    
    # Create tables
    traditional_G.add_node("Companies Table", size=30, color=COLORS['primary'], 
                         title="Companies Table (Records)")
    traditional_G.add_node("Financials Table", size=30, color=COLORS['primary'], 
                         title="Financials Table (Records)")
    traditional_G.add_node("Industries Table", size=30, color=COLORS['primary'], 
                         title="Industries Table (Records)")
    traditional_G.add_node("Loans Table", size=30, color=COLORS['primary'], 
                         title="Loans Table (Records)")
    
    # Create table fields
    fields = [
        ("Companies Table", "CompanyID"),
        ("Companies Table", "Name"),
        ("Companies Table", "IndustryID"),
        ("Companies Table", "YearsInBusiness"),
        ("Financials Table", "FinancialID"),
        ("Financials Table", "CompanyID"),
        ("Financials Table", "Revenue"),
        ("Financials Table", "ProfitMargin"),
        ("Industries Table", "IndustryID"),
        ("Industries Table", "IndustryName"),
        ("Industries Table", "RiskFactor"),
        ("Loans Table", "LoanID"),
        ("Loans Table", "CompanyID"),
        ("Loans Table", "Amount"),
        ("Loans Table", "Purpose")
    ]
    
    # Add fields as nodes
    for table, field in fields:
        traditional_G.add_node(f"{field}", size=15, color=COLORS['primary'], title=f"{field} (Column)")
        traditional_G.add_edge(table, f"{field}", width=1)
    
    # Add foreign key relationships (dotted lines)
    traditional_G.add_edge("Financials Table", "Companies Table", width=1, style="dashed", 
                         title="Foreign Key Relationship")
    traditional_G.add_edge("Loans Table", "Companies Table", width=1, style="dashed", 
                         title="Foreign Key Relationship")
    traditional_G.add_edge("Companies Table", "Industries Table", width=1, style="dashed", 
                         title="Foreign Key Relationship")
    
    # Knowledge graph model
    kg_G = nx.Graph()
    
    # Create main entity
    kg_G.add_node("TechInnovate", size=30, color=COLORS['digital_twin'], 
                title="Company Entity: TechInnovate")
    
    # Create key nodes
    kg_G.add_node("Software Industry", size=20, color=COLORS['external'], 
                title="Industry: Software Development")
    kg_G.add_node("Financial Metrics", size=20, color=COLORS['primary'], 
                title="Financial Information")
    kg_G.add_node("Loan Request", size=20, color=COLORS['primary'], 
                title="Loan Request Details")
    kg_G.add_node("Market Context", size=20, color=COLORS['external'], 
                title="External Market Context")
    
    # Connect main nodes to entity
    kg_G.add_edge("TechInnovate", "Software Industry", width=2, title="operates in")
    kg_G.add_edge("TechInnovate", "Financial Metrics", width=2, title="has financials")
    kg_G.add_edge("TechInnovate", "Loan Request", width=2, title="requests")
    kg_G.add_edge("TechInnovate", "Market Context", width=2, title="exists in")
    
    # Add detailed nodes
    detail_nodes = [
        ("Financial Metrics", "Revenue: $2.4M", COLORS['primary']),
        ("Financial Metrics", "Profit Margin: 18%", COLORS['primary']),
        ("Loan Request", "Amount: $500K", COLORS['primary']),
        ("Loan Request", "Purpose: Expansion", COLORS['primary']),
        ("Software Industry", "Growth Rate: 12%", COLORS['external']),
        ("Software Industry", "Competition: High", COLORS['external']),
        ("Market Context", "Tech Investment Trend", COLORS['external'])
    ]
    
    # Add detailed nodes
    for parent, node_name, color in detail_nodes:
        kg_G.add_node(node_name, size=15, color=color, title=node_name)
        kg_G.add_edge(parent, node_name, width=1)
    
    # Add cross-connections that show the power of knowledge graphs
    kg_G.add_edge("Software Industry", "Revenue: $2.4M", width=1, color=COLORS['edge_default'], 
                title="influences")
    kg_G.add_edge("Tech Investment Trend", "Software Industry", width=1, color=COLORS['edge_default'], 
                title="affects")
    kg_G.add_edge("Purpose: Expansion", "Revenue: $2.4M", width=1, color=COLORS['edge_default'], 
                title="aims to increase")
    
    return traditional_G, kg_G

def create_kg_growth_sequence():
    """
    Create a sequence of knowledge graphs showing how they grow over time.
    
    Returns:
        List of NetworkX graphs at different stages of development
    """
    # Stage 1: Basic application data
    G1 = nx.Graph()
    G1.add_node("TechInnovate", size=30, color=COLORS['digital_twin'], title="Company Entity")
    
    G1.add_node("Basic Info", size=20, color=COLORS['primary'], title="Basic Information")
    G1.add_edge("TechInnovate", "Basic Info", width=2)
    
    basic_details = [
        "Software Industry",
        "7 Years in Business",
        "48 Employees"
    ]
    
    for detail in basic_details:
        G1.add_node(detail, size=15, color=COLORS['primary'], title=detail)
        G1.add_edge("Basic Info", detail, width=1)
    
    G1.add_node("Loan Request", size=20, color=COLORS['primary'], title="Loan Request")
    G1.add_edge("TechInnovate", "Loan Request", width=2)
    
    loan_details = [
        "Amount: $500K",
        "Purpose: Expansion",
        "Term: 5 years"
    ]
    
    for detail in loan_details:
        G1.add_node(detail, size=15, color=COLORS['primary'], title=detail)
        G1.add_edge("Loan Request", detail, width=1)
    
    # Stage 2: Add financial data
    G2 = G1.copy()
    
    G2.add_node("Financial Metrics", size=20, color=COLORS['primary'], title="Financial Information")
    G2.add_edge("TechInnovate", "Financial Metrics", width=2)
    
    financial_details = [
        "Revenue: $2.4M",
        "Profit Margin: 18%",
        "Cash Balance: $750K",
        "Debt Ratio: 0.3"
    ]
    
    for detail in financial_details:
        G2.add_node(detail, size=15, color=COLORS['primary'], title=detail)
        G2.add_edge("Financial Metrics", detail, width=1)
    
    G2.add_node("SaaS Metrics", size=20, color=COLORS['primary'], title="SaaS Business Metrics")
    G2.add_edge("TechInnovate", "SaaS Metrics", width=2)
    
    saas_details = [
        "CAC: $1,200",
        "LTV: $6,500",
        "MRR: $200K"
    ]
    
    for detail in saas_details:
        G2.add_node(detail, size=15, color=COLORS['primary'], title=detail)
        G2.add_edge("SaaS Metrics", detail, width=1)
    
    # Connect software industry to SaaS metrics
    G2.add_edge("Software Industry", "SaaS Metrics", width=1, color=COLORS['edge_default'])
    
    # Stage 3: Add external context
    G3 = G2.copy()
    
    G3.add_node("External Context", size=20, color=COLORS['external'], title="External Context")
    G3.add_edge("TechInnovate", "External Context", width=2)
    
    external_factors = [
        "Market Growth: 15%",
        "Tech Investment Trends",
        "Competitive Landscape",
        "Regulatory Environment"
    ]
    
    for factor in external_factors:
        G3.add_node(factor, size=15, color=COLORS['external'], title=factor)
        G3.add_edge("External Context", factor, width=1)
    
    # Add cross-connections to show context integration
    G3.add_edge("Market Growth: 15%", "Revenue: $2.4M", width=1, color=COLORS['edge_default'])
    G3.add_edge("Tech Investment Trends", "LTV: $6,500", width=1, color=COLORS['edge_default'])
    G3.add_edge("Competitive Landscape", "CAC: $1,200", width=1, color=COLORS['edge_default'])
    
    # Stage 4: Add risk assessment and recommendations
    G4 = G3.copy()
    
    G4.add_node("Risk Assessment", size=20, color=COLORS['guidance'], title="Risk Analysis")
    G4.add_edge("TechInnovate", "Risk Assessment", width=2)
    
    risk_factors = [
        "Financial Health: Strong",
        "Market Position: Growing",
        "Overall Risk: Low"
    ]
    
    for factor in risk_factors:
        G4.add_node(factor, size=15, color=COLORS['guidance'], title=factor)
        G4.add_edge("Risk Assessment", factor, width=1)
    
    G4.add_node("Recommendations", size=20, color=COLORS['guidance'], title="Adaptive Guidance")
    G4.add_edge("TechInnovate", "Recommendations", width=2)
    
    recommendations = [
        "Approve Standard Terms",
        "Quarterly Monitoring",
        "Upsell Opportunity"
    ]
    
    for rec in recommendations:
        G4.add_node(rec, size=15, color=COLORS['guidance'], title=rec)
        G4.add_edge("Recommendations", rec, width=1)
    
    # Connect assessment to relevant factors
    G4.add_edge("Financial Health: Strong", "Financial Metrics", width=1, color=COLORS['edge_default'])
    G4.add_edge("Market Position: Growing", "External Context", width=1, color=COLORS['edge_default'])
    G4.add_edge("Approve Standard Terms", "Overall Risk: Low", width=1, color=COLORS['edge_default'])
    
    return [G1, G2, G3, G4]

def create_customer_concentration_graph():
    """
    Create a graph showing customer concentration risk detection.
    
    Returns:
        NetworkX graph showing customer concentration analysis
    """
    G = nx.Graph()
    
    # Create company node
    G.add_node("ManufacturePro", size=30, color=COLORS['digital_twin'], 
             title="Manufacturing Company")
    
    # Add customers group
    G.add_node("Customer Base", size=25, color=COLORS['primary'], 
             title="Company's Customers")
    G.add_edge("ManufacturePro", "Customer Base", width=3)
    
    # Add individual customers with concentration
    customers = [
        {"name": "Customer A", "revenue": "$210K", "percentage": 42, "color": COLORS['low_confidence']},
        {"name": "Customer B", "revenue": "$84K", "percentage": 17, "color": COLORS['medium_confidence']},
        {"name": "Customer C", "revenue": "$63K", "percentage": 13, "color": COLORS['primary']},
        {"name": "Customer D", "revenue": "$42K", "percentage": 8, "color": COLORS['primary']},
        {"name": "Customer E", "revenue": "$21K", "percentage": 4, "color": COLORS['primary']},
        {"name": "Others", "revenue": "$80K", "percentage": 16, "color": COLORS['primary']}
    ]
    
    # Add customer nodes
    for customer in customers:
        node_name = f"{customer['name']}: {customer['percentage']}%"
        node_size = 10 + (customer['percentage'] * 0.5)
        
        G.add_node(node_name, size=node_size, color=customer['color'], 
                 title=f"{customer['name']}: {customer['revenue']} ({customer['percentage']}%)")
        
        # Edge width based on percentage
        edge_width = max(1, customer['percentage'] / 10)
        G.add_edge("Customer Base", node_name, width=edge_width)
    
    # Add risk assessment
    G.add_node("Risk Assessment", size=25, color=COLORS['guidance'], 
             title="Risk Analysis")
    G.add_edge("ManufacturePro", "Risk Assessment", width=3)
    
    # Add risk nodes
    G.add_node("Customer Concentration Risk", size=20, color=COLORS['low_confidence'], 
             title="High concentration risk with Customer A")
    G.add_edge("Risk Assessment", "Customer Concentration Risk", width=2)
    
    # Connect high-concentration customer to risk
    G.add_edge("Customer A: 42%", "Customer Concentration Risk", width=2, 
             color=COLORS['low_confidence'])
    
    # Add industry context
    G.add_node("Industry Context", size=25, color=COLORS['external'], 
             title="Manufacturing Industry Context")
    G.add_edge("ManufacturePro", "Industry Context", width=3)
    
    # Add industry standard
    G.add_node("Industry Standard: 20% Max", size=15, color=COLORS['external'], 
             title="Industry recommendation: maximum 20% from single customer")
    G.add_edge("Industry Context", "Industry Standard: 20% Max", width=1)
    
    # Connect industry standard to risk
    G.add_edge("Industry Standard: 20% Max", "Customer Concentration Risk", width=1, 
             color=COLORS['edge_default'])
    
    # Add recommendation
    G.add_node("Recommendations", size=25, color=COLORS['guidance'], 
             title="Adaptive Guidance")
    G.add_edge("ManufacturePro", "Recommendations", width=3)
    
    G.add_node("Customer Diversification Plan", size=15, color=COLORS['guidance'], 
             title="Develop plan to reduce Customer A concentration")
    G.add_edge("Recommendations", "Customer Diversification Plan", width=2)
    
    G.add_node("Modified Loan Terms", size=15, color=COLORS['guidance'], 
             title="Adjust terms to account for concentration risk")
    G.add_edge("Recommendations", "Modified Loan Terms", width=2)
    
    # Connect risk to recommendations
    G.add_edge("Customer Concentration Risk", "Customer Diversification Plan", width=1, 
             color=COLORS['edge_default'])
    G.add_edge("Customer Concentration Risk", "Modified Loan Terms", width=1, 
             color=COLORS['edge_default'])
    
    return G