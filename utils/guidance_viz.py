# utils/guidance_viz.py
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from utils.theme import COLORS
from utils.graph_viz import create_pyvis_graph

def create_reasoning_path_graph(reasoning_steps, conclusion):
    """Create a graph showing the reasoning path to a recommendation."""
    G = nx.DiGraph()
    
    # Add conclusion node
    G.add_node(conclusion, size=25, color=COLORS['guidance'], title=conclusion, shape='star')
    
    # Track previous level nodes for connections
    previous_level = [conclusion]
    
    # Add reasoning steps in reverse (working backwards from conclusion)
    for i, level in enumerate(reversed(reasoning_steps)):
        current_level = []
        
        # Process each item at this level
        for j, item in enumerate(level):
            # Create node name
            node_name = f"{item} (L{len(reasoning_steps)-i})"
            
            # Add node
            G.add_node(node_name, size=15, color=COLORS['primary'], title=item, shape='dot')
            current_level.append(node_name)
            
            # Connect to all nodes in the previous level
            for prev_node in previous_level:
                G.add_edge(node_name, prev_node, width=2, color=COLORS['edge_default'])
        
        # Update previous level
        previous_level = current_level
    
    return G

def information_value_visualization(info_values, height=400):
    """Create a visualization of information value calculation."""
    # Create figure
    fig = go.Figure()
    
    # Sort by value for better visualization
    sorted_items = sorted(info_values.items(), key=lambda x: x[1], reverse=True)
    
    # Add bars for information value
    for info, value in sorted_items:
        # Determine color based on value
        if value >= 0.8:
            color = COLORS['high_confidence']
        elif value >= 0.5:
            color = COLORS['medium_confidence']
        else:
            color = COLORS['low_confidence']
        
        # Add bar
        fig.add_trace(go.Bar(
            x=[value],
            y=[info],
            orientation='h',
            marker_color=color,
            name=info,
            hovertemplate='<b>%{y}</b><br>Value: %{x:.2f}'
        ))
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="Information Value Analysis",
        xaxis_title="Expected Value of Information",
        yaxis_title="Information Type",
        height=height,
        xaxis=dict(
            gridcolor=COLORS['bg_light'],
            range=[0, 1]
        ),
        yaxis=dict(
            gridcolor=COLORS['bg_light']
        )
    )
    
    return fig

def confidence_breakdown_radar(confidence_components, height=400):
    """Create a radar chart showing confidence breakdown."""
    # Create figure
    fig = go.Figure()
    
    # Add radar chart
    fig.add_trace(go.Scatterpolar(
        r=list(confidence_components.values()),
        theta=list(confidence_components.keys()),
        fill='toself',
        name='Confidence Components',
        line_color=COLORS['primary']
    ))
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="Confidence Component Analysis",
        height=height,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor=COLORS['bg_light']
            ),
            angularaxis=dict(
                gridcolor=COLORS['bg_light']
            ),
            bgcolor=COLORS['bg_dark']
        )
    )
    
    return fig

def recommendation_card(title, content, confidence=0.5):
    """Create a styled recommendation card."""
    # Determine color based on confidence
    if confidence >= 0.8:
        border_color = COLORS['high_confidence']
        confidence_text = "High Confidence"
    elif confidence >= 0.5:
        border_color = COLORS['medium_confidence']
        confidence_text = "Medium Confidence"
    else:
        border_color = COLORS['low_confidence']
        confidence_text = "Low Confidence"
    
    # Create HTML for the card
    st.markdown(f"""
    <div style="border-left: 4px solid {border_color}; 
                background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px;">
        <h4 style="color: {COLORS['text_primary']}; margin-top: 0;">{title}</h4>
        <p style="color: {COLORS['text_primary']};">{content}</p>
        <div style="display: flex; align-items: center;">
            <div style="background: linear-gradient(to right, {border_color} {confidence*100}%, {COLORS['bg_light']} {confidence*100}%); 
                        height: 8px; 
                        width: 100px; 
                        border-radius: 4px; 
                        margin-right: 10px;"></div>
            <span style="color: {COLORS['text_secondary']}; font-size: 0.8em;">{confidence_text} ({confidence:.2f})</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def adaptive_guidance_demo():
    """Create a complete adaptive guidance demonstration."""
    st.write("### Adaptive Guidance System")
    
    st.write("""
    The Adaptive Guidance layer analyzes all available information to provide specific,
    actionable recommendations with transparent reasoning paths. Unlike black-box systems
    that provide only risk scores, Context-AI explains its thinking and adapts
    recommendations as new information becomes available.
    """)
    
    # Decision context selection
    decision_context = st.selectbox(
        "Select a decision context:",
        ["Loan Application Assessment", "Monitoring Phase Alert", "Term Modification Request"]
    )
    
    # Information value calculation
    st.write("#### Next Best Information")
    
    if decision_context == "Loan Application Assessment":
        info_values = {
            "Industry Growth Forecast": 0.78,
            "Customer Concentration Details": 0.65,
            "Management Team Background": 0.52,
            "Detailed Cash Flow Projections": 0.87,
            "Competitor Performance Data": 0.41
        }
    elif decision_context == "Monitoring Phase Alert":
        info_values = {
            "Updated Financial Statements": 0.92,
            "Recent Management Changes": 0.44,
            "Industry News Events": 0.62,
            "Customer Payment Patterns": 0.75,
            "Market Share Trends": 0.38
        }
    else:  # Term Modification
        info_values = {
            "Cash Flow Timing Analysis": 0.85,
            "Industry Seasonality Data": 0.73,
            "Supply Chain Disruption Impact": 0.68,
            "Updated Collateral Valuation": 0.47,
            "Customer Contract Renewal Rates": 0.56
        }
    
    # Display information value visualization
    info_value_fig = information_value_visualization(info_values)
    st.plotly_chart(info_value_fig, use_container_width=True)
    
    st.write("The system calculates which information would most reduce uncertainty, focusing the process on high-value information rather than following a generic checklist.")
    
    # Reasoning path visualization
    st.write("#### Decision Reasoning Path")
    
    if decision_context == "Loan Application Assessment":
        reasoning_steps = [
            ["Strong financial metrics", "Positive industry outlook", "Acceptable collateral value"],
            ["Profitability meets threshold", "Debt service capacity confirmed", "Market position validation"]
        ]
        conclusion = "Approve with standard terms"
        confidence = 0.76
    elif decision_context == "Monitoring Phase Alert":
        reasoning_steps = [
            ["Delayed payments detected", "Industry downturn signals", "Competitive pressure increasing"],
            ["Cash flow deterioration trend", "Risk level increasing"]
        ]
        conclusion = "Increase monitoring frequency"
        confidence = 0.82
    else:  # Term Modification
        reasoning_steps = [
            ["Seasonal cash flow pattern confirmed", "Strong historical payment performance", "Industry-wide timing shift"],
            ["Payment timing misalignment", "Underlying business remains sound"]
        ]
        conclusion = "Approve payment schedule adjustment"
        confidence = 0.68
    
    # Create and display reasoning path graph
    G = create_reasoning_path_graph(reasoning_steps, conclusion)
    create_pyvis_graph(G, height=400)
    
    st.write("""
    The reasoning path shows how the system arrived at its recommendation,
    building trust through transparency rather than asking users to trust a black box score.
    """)
    
    # Confidence components
    st.write("#### Recommendation Confidence Analysis")
    
    if decision_context == "Loan Application Assessment":
        confidence_components = {
            "Financial Data Quality": 0.88,
            "Industry Trend Clarity": 0.72,
            "Market Position Certainty": 0.65,
            "Management Assessment": 0.81,
            "Collateral Valuation": 0.79
        }
    elif decision_context == "Monitoring Phase Alert":
        confidence_components = {
            "Payment Data Reliability": 0.95,
            "Industry Trend Clarity": 0.82,
            "Competitive Intelligence": 0.71,
            "Financial Statement Recency": 0.88,
            "Historical Pattern Matching": 0.75
        }
    else:  # Term Modification
        confidence_components = {
            "Cash Flow Analysis Quality": 0.84,
            "Seasonality Pattern Clarity": 0.92,
            "Payment History Completeness": 0.76,
            "Market Condition Assessment": 0.62,
            "Customer Relationship Stability": 0.69
        }
    
    # Display confidence component visualization
    confidence_fig = confidence_breakdown_radar(confidence_components)
    st.plotly_chart(confidence_fig, use_container_width=True)
    
    # Final recommendation
    st.write("#### Final Recommendation")
    
    if decision_context == "Loan Application Assessment":
        recommendation_title = "Approve the loan application with standard terms"
        recommendation_content = "Based on strong financial metrics, positive industry outlook, and acceptable collateral value, we recommend approving this loan with our standard terms and monitoring frequency."
    elif decision_context == "Monitoring Phase Alert":
        recommendation_title = "Increase monitoring frequency and request updated financials"
        recommendation_content = "Recent payment delays combined with industry downturn signals suggest increased risk. We recommend increasing monitoring frequency from quarterly to monthly and requesting updated financial statements immediately."
    else:  # Term Modification
        recommendation_title = "Approve payment schedule adjustment"
        recommendation_content = "The analysis confirms seasonal cash flow patterns typical for this industry. With the strong historical payment performance, we recommend approving the requested payment schedule adjustment to align with their business cycle."
    
    recommendation_card(recommendation_title, recommendation_content, confidence)
    
    # Counterfactual analysis
    st.write("#### What Would Change This Recommendation?")
    
    if decision_context == "Loan Application Assessment":
        st.write("""
        The recommendation would change to "Approve with modified terms" if:
        - Debt service coverage ratio fell below 1.2
        - Industry outlook showed increased volatility
        - Customer concentration exceeded 30% with a single client
        
        The recommendation would change to "Decline" if:
        - Cash flow projections showed insufficient coverage
        - Management team had recent significant turnover
        - Collateral valuation decreased by more than 15%
        """)
    elif decision_context == "Monitoring Phase Alert":
        st.write("""
        The recommendation would change to "Initiate loss mitigation" if:
        - Payment delays exceeded 60 days
        - Updated financials showed negative EBITDA
        - Major customer loss was reported
        
        The recommendation would change to "Return to normal monitoring" if:
        - Payment pattern returned to consistent on-time payments
        - Industry indicators stabilized
        - Updated financials showed strong liquidity position
        """)
    else:  # Term Modification
        st.write("""
        The recommendation would change to "Approve with additional conditions" if:
        - Seasonal pattern was less pronounced than reported
        - Recent payment history showed occasional delays
        - Industry peers were not experiencing similar timing issues
        
        The recommendation would change to "Decline modification" if:
        - Cash flow analysis revealed fundamental shortfalls
        - Customer concentration had increased significantly
        - Management provided inconsistent explanation for timing issues
        """)
    
    return decision_context