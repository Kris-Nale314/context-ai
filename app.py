# app.py
import streamlit as st
from utils.theme import setup_page_config, apply_theme
from utils.ui_components import header_with_logo, concept_card, comparison_card, layer_card
from utils.state import init_session_state
import os

# Set up page config and theme
setup_page_config()
apply_theme()

# Initialize session state
init_session_state({
    'page': 'home',
    'show_intro': True
})

# Header
header_with_logo()

# Introduction section
if st.session_state.show_intro:
    st.markdown("""
    # Context-AI: Adaptive Intelligence Through Evolving Knowledge Graphs
    
    > *"Because your AI system should be as dynamic as the world it operates in."*
    
    Welcome to the Context-AI interactive platform! This experience will guide you through 
    the core concepts of our approach to decision intelligence using evolving knowledge graphs.
    
    Unlike a traditional slideshow, this platform allows you to explore concepts interactively, 
    see the system in action, and understand both how it works and why it matters.
    """)
    
    if st.button("Skip Introduction", key="skip_intro"):
        st.session_state.show_intro = False
        st.rerun()
else:
    # Main navigation
    st.sidebar.title("Navigation")
    
    pages = [
        "Home",
        "Architecture Overview",
        "Digital Twin Layer",
        "Temporal Intelligence Layer",
        "External Integration Layer",
        "Adaptive Guidance Layer",
        "Loan Journey Demo",
        "Beyond Finance"
    ]
    
    selected_page = st.sidebar.radio("Go to", pages)
    
    # Set page in session state
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page.lower().replace(" ", "_")
        st.rerun()
    
    # Display selected page
    if st.session_state.page == "home":
        show_home_page()
    elif st.session_state.page == "architecture_overview":
        show_architecture_page()
    elif st.session_state.page == "digital_twin_layer":
        show_digital_twin_page()
    elif st.session_state.page == "temporal_intelligence_layer":
        show_temporal_intelligence_page()
    elif st.session_state.page == "external_integration_layer":
        show_external_integration_page()
    elif st.session_state.page == "adaptive_guidance_layer":
        show_adaptive_guidance_page()
    elif st.session_state.page == "loan_journey_demo":
        show_loan_journey_page()
    elif st.session_state.page == "beyond_finance":
        show_beyond_finance_page()

# Home page function
def show_home_page():
    st.title("Context-AI: The Basics")
    
    st.markdown("""
    ## The Challenge: Static Analysis in a Dynamic World
    
    Traditional decision support systems fail to capture the dynamic, interconnected nature of the real world:
    """)
    
    # Display challenges
    challenges = [
        "**Static Snapshots**: They miss the critical evolution and trends that provide early warning signals",
        "**Relational Blindness**: They fail to capture the complex web of relationships where valuable insights hide",
        "**Disconnected Systems**: Critical context remains scattered across multiple information silos",
        "**Binary Certainty**: They treat all information as equally reliable regardless of source or recency",
        "**Expertise Bottlenecks**: Domain knowledge remains trapped in experts' minds and doesn't scale",
        "**Black Box Decisions**: Recommendations come without explanation, forcing blind trust or rejection"
    ]
    
    for challenge in challenges:
        st.markdown(f"- {challenge}")
    
    st.markdown("## Platform Architecture: A Layered Approach")
    
    # Display architecture image
    st.image("images/platformLayers.png", width=700)
    
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
    
    # Call to action
    st.markdown("## Explore the Concepts")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Digital Twin Layer", key="btn_digital"):
            st.session_state.page = "digital_twin_layer"
            st.rerun()
    
    with col2:
        if st.button("Temporal Intelligence", key="btn_temporal"):
            st.session_state.page = "temporal_intelligence_layer"
            st.rerun()
    
    with col3:
        if st.button("External Integration", key="btn_external"):
            st.session_state.page = "external_integration_layer"
            st.rerun()
    
    with col4:
        if st.button("Adaptive Guidance", key="btn_guidance"):
            st.session_state.page = "adaptive_guidance_layer"
            st.rerun()
    
    st.markdown("## Or Experience the Complete System")
    
    if st.button("Loan Journey Demo", key="btn_loan_journey"):
        st.session_state.page = "loan_journey_demo"
        st.rerun()

# Make sure necessary directories exist
os.makedirs("images", exist_ok=True)

if __name__ == "__main__":
    pass