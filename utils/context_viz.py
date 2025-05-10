# utils/context_viz.py
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from utils.theme import COLORS
from utils.graph_viz import create_pyvis_graph

def create_context_integration_graph(entity_name, context_sources=None, complexity=2):
    """Create a graph showing external context integration."""
    G = nx.Graph()
    
    # Add main entity node
    G.add_node(entity_name, size=30, color=COLORS['digital_twin'], 
               title=entity_name, shape='dot')
    
    # Default context sources if not provided
    if context_sources is None:
        context_sources = {
            "Industry Trends": {
                "active": True, 
                "color": COLORS['external'],
                "subnodes": ["Growth Rate", "Technology Adoption", "Market Size"]
            },
            "Competitive Landscape": {
                "active": True, 
                "color": COLORS['external'],
                "subnodes": ["Competitor A", "Competitor B", "Market Leader"]
            },
            "Economic Indicators": {
                "active": False, 
                "color": COLORS['external'],
                "subnodes": ["Interest Rates", "Inflation", "GDP Growth"]
            },
            "Regulatory Environment": {
                "active": False, 
                "color": COLORS['external'],
                "subnodes": ["Compliance Changes", "Industry Standards", "Tax Policy"]
            }
        }
    
    # Add context source nodes
    for source, attrs in context_sources.items():
        if attrs.get("active", False):
            G.add_node(source, size=20, color=attrs.get("color", COLORS['external']), 
                      title=source, shape='dot')
            G.add_edge(entity_name, source, width=2, color=COLORS['edge_default'])
            
            # Add subnodes for higher complexity
            if complexity >= 2 and "subnodes" in attrs:
                for subnode in attrs["subnodes"]:
                    G.add_node(subnode, size=10, color=attrs.get("color", COLORS['external']), 
                              title=subnode, shape='dot')
                    G.add_edge(source, subnode, width=1, color=COLORS['edge_default'])
    
    # Add cross-connections for highest complexity
    if complexity >= 3:
        # Connect some subnodes that would be related
        cross_connections = [
            ("Growth Rate", "Competitor A"),
            ("Technology Adoption", "Competitor B"),
            ("Compliance Changes", "Technology Adoption"),
            ("Interest Rates", "Market Size")
        ]
        
        for source, target in cross_connections:
            if source in G.nodes and target in G.nodes:
                G.add_edge(source, target, width=1, color=COLORS['edge_default'], 
                          style='dashed')
    
    return G

def context_impact_visualization(context_impacts, height=400):
    """Create a visualization of context impact on risk assessment."""
    # Create figure
    fig = go.Figure()
    
    # Add bars for impacts
    for context, impact in context_impacts.items():
        # Determine color based on impact
        if impact > 0:
            color = COLORS['high_confidence']  # Positive impact
        else:
            color = COLORS['low_confidence']   # Negative impact
        
        # Add bar
        fig.add_trace(go.Bar(
            x=[impact],
            y=[context],
            orientation='h',
            marker_color=color,
            name=context,
            hovertemplate='<b>%{y}</b><br>Impact: %{x:.2f}'
        ))
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="External Context Impact on Risk Assessment",
        xaxis_title="Impact (negative = higher risk)",
        yaxis_title="Context Source",
        height=height,
        xaxis=dict(
            gridcolor=COLORS['bg_light'],
            zeroline=True,
            zerolinecolor=COLORS['text_secondary']
        ),
        yaxis=dict(
            gridcolor=COLORS['bg_light']
        )
    )
    
    return fig

def context_source_reliability(sources, height=300):
    """Create a visualization of source reliability."""
    # Create figure
    fig = go.Figure()
    
    # Add bars for source reliability
    for source, reliability in sources.items():
        # Determine color based on reliability
        if reliability >= 0.8:
            color = COLORS['high_confidence']
        elif reliability >= 0.5:
            color = COLORS['medium_confidence']
        else:
            color = COLORS['low_confidence']
        
        # Add bar
        fig.add_trace(go.Bar(
            x=[reliability],
            y=[source],
            orientation='h',
            marker_color=color,
            name=source,
            hovertemplate='<b>%{y}</b><br>Reliability: %{x:.2f}'
        ))
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="Source Reliability Assessment",
        xaxis_title="Reliability Score",
        yaxis_title="Information Source",
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

def context_integration_demo():
    """Create a complete context integration demonstration."""
    st.write("### External Context Integration")
    
    st.write("""
    Traditional systems consider only internal data about an entity. Context-AI connects
    entities to the broader world they operate in, integrating relevant external factors
    that often determine success or failure.
    """)
    
    # Entity selection
    entity = st.selectbox(
        "Select an entity to analyze:",
        ["TechStart Inc (Software)", "ManufacturePro (Industrial)", "RetailGiant (Retail)"]
    )
    
    # Context source selection
    st.write("#### Toggle External Context Sources")
    
    col1, col2 = st.columns(2)
    
    context_sources = {}
    
    with col1:
        context_sources["Industry Trends"] = {
            "active": st.checkbox("Industry Trends", value=True),
            "color": COLORS['external'],
            "subnodes": ["Growth Rate", "Technology Adoption", "Market Size"],
            "reliability": 0.85,
            "impact": 0.15
        }
        
        context_sources["Competitive Landscape"] = {
            "active": st.checkbox("Competitive Landscape", value=True),
            "color": COLORS['external'],
            "subnodes": ["Competitor A", "Competitor B", "Market Leader"],
            "reliability": 0.78,
            "impact": -0.12
        }
    
    with col2:
        context_sources["Economic Indicators"] = {
            "active": st.checkbox("Economic Indicators", value=False),
            "color": COLORS['external'],
            "subnodes": ["Interest Rates", "Inflation", "GDP Growth"],
            "reliability": 0.92,
            "impact": -0.08
        }
        
        context_sources["Regulatory Environment"] = {
            "active": st.checkbox("Regulatory Environment", value=False),
            "color": COLORS['external'],
            "subnodes": ["Compliance Changes", "Industry Standards", "Tax Policy"],
            "reliability": 0.81,
            "impact": -0.05
        }
    
    # Create and display knowledge graph
    st.write("#### External Context Network")
    G = create_context_integration_graph(entity, context_sources)
    create_pyvis_graph(G, height=400)
    
    # Only show impact analysis if there are active sources
    active_sources = {k: v for k, v in context_sources.items() if v.get("active", False)}
    
    if active_sources:
        # Source reliability visualization
        st.write("#### Source Reliability")
        source_reliability = {k: v.get("reliability", 0.5) for k, v in active_sources.items()}
        reliability_fig = context_source_reliability(source_reliability)
        st.plotly_chart(reliability_fig, use_container_width=True)
        
        # Context impact visualization
        st.write("#### Impact on Risk Assessment")
        context_impacts = {k: v.get("impact", 0) for k, v in active_sources.items()}
        impact_fig = context_impact_visualization(context_impacts)
        st.plotly_chart(impact_fig, use_container_width=True)
        
        # Show risk adjustment
        st.write("#### Risk Assessment Adjustment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Risk Score Without Context", "Medium (0.45)")
        
        with col2:
            # Calculate adjusted score based on active sources
            adjustment = sum(v.get("impact", 0) for v in active_sources.values())
            new_score = max(0.05, min(0.95, 0.45 + adjustment))
            
            risk_level = "Medium"
            if new_score > 0.7:
                risk_level = "High"
            elif new_score > 0.4:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            # Display with positive/negative delta
            delta_text = f"{adjustment:+.2f}"
            st.metric("Risk Score With Context", f"{risk_level} ({new_score:.2f})", delta_text)
    else:
        st.info("Select context sources above to see how they impact risk assessment.")
    
    return active_sources