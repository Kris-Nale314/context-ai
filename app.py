# app.py
import streamlit as st
import os
from utils.theme import setup_page_config, apply_theme, COLORS
from utils.ui_components import header_with_logo, concept_card, layer_card
from utils.state import init_session_state

# Set up page config and theme
setup_page_config()
apply_theme()

# Initialize session state
init_session_state()

# Header
header_with_logo()

# Main content
st.markdown("""
# Context-AI: Adaptive Intelligence Through Evolving Knowledge Graphs

> *"Because your AI system should be as dynamic as the world it operates in."*
""")

# Introduction section
st.markdown("""
Context-AI is an experimental platform that creates digital twins of entities through evolving 
knowledge graphs. By combining temporal knowledge representation with contextual integration 
and adaptive guidance, it transforms how we process, analyze, and draw insights from complex, 
interconnected data.
""")

# Platform architecture image - use a container to constrain the width
image_container = st.container()
with image_container:
    # Create a column layout to center and constrain the image width
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Display image at 70% of the column width
        st.image("images/platformLayers.png", use_container_width=True)
st.caption("The four layers of the Context-AI platform work together to create a comprehensive, evolving understanding.")

# Core challenge section
st.markdown("## The Challenge: Static Analysis in a Dynamic World")

# Create two columns for challenges
col1, col2 = st.columns(2)

with col1:
    challenges = [
        "**Static Snapshots**: Missing the evolution and trends that provide early warning signals",
        "**Relational Blindness**: Failing to capture the complex web of relationships where insights hide",
        "**Disconnected Systems**: Critical context scattered across information silos"
    ]
    
    for challenge in challenges:
        st.markdown(f"- {challenge}")

with col2:
    challenges = [
        "**Binary Certainty**: Treating all information as equally reliable regardless of source",
        "**Expertise Bottlenecks**: Domain knowledge trapped in experts' minds that doesn't scale",
        "**Black Box Decisions**: Recommendations without explanation, forcing blind trust"
    ]
    
    for challenge in challenges:
        st.markdown(f"- {challenge}")

# Platform layer overview
st.markdown("## Platform Architecture: A Layered Approach")

# Layer explanations
layer_card(
    "Digital Twin Layer",
    "Creates a digital representation of each loan application as a knowledge graph, capturing not just the standard financial metrics but all relationships between the applicant, their industry, similar past cases, and relevant risk factors.",
    "For a small business loan application, this layer would connect the business's financial statements to its industry classification, ownership structure, credit history, collateral assets, and market position—building a complete picture rather than isolated data points.",
    "Traditional loan processing systems store data in flat database tables. Our knowledge graph approach reveals insights from these relationships, like how industry-specific factors affect this business model."
)

layer_card(
    "Temporal Intelligence Layer",
    "Tracks history of each loan, monitoring how key metrics, relationships, and risk factors evolve from pre-application through underwriting and beyond.",
    "When an applicant submits updated financial information, this layer doesn't just replace old data—it maintains the history of changes, analyzing trends like improving cash flow or deteriorating debt ratios over time, and flagging significant shifts that might indicate changing risk.",
    "Conventional systems capture application data at a single point in time or simply overwrite previous versions. Our temporal approach detects patterns in how applications evolve that often provide early warning signals of potential problems or opportunities that static snapshots would miss."
)

layer_card(
    "External Integration Layer",
    "Connects each digital twin to external context, e.g. market data, news events, industry trends, competitive intelligence, that impact risk assessment.",
    "In the case of a manufacturing loan, this layer continuously integrate earnings call intelligence, news event monitoring, and competitive landscape changes to provide a complete picture of the environment the applicant operates in.",
    "Traditional loan assessment systems considering only the information directly provided. Our platform creates an awareness that accounts for external factors often determining business success or failure."
)

layer_card(
    "Adaptive Guidance Layer",
    "Analyzes the knowledge graph to generate recommendations, explaining the reasoning and identifying what information would most reduce uncertainty.",
    "Rather than simply calculating a risk score, this layer may recommend requesting additional collateral based on specific industry volatility, suggest modified terms that would better match the applicant's cash flow patterns, or identify key questions about their supply chain that would clarify risk factors.",
    "Conventional systems typically provide simplistic risk scores without explanation. Our guidance system provides specific, actionable recommendations with transparent reasoning paths, and continuously updates these recommendations as new information becomes available."
)

# Footer
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #94A3B8; font-size: 0.8em;">
Building intelligence that understands not just entities, but the worlds they exist in and how they change over time.
</p>
""", unsafe_allow_html=True)

# Make sure necessary directories exist
os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)

if __name__ == "__main__":
    pass