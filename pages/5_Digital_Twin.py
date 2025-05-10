# pages/digital_twin.py
import streamlit as st
from utils.theme import apply_theme, COLORS
from utils.ui_components import header_with_logo, concept_card, comparison_card
from utils.graph_viz import create_pyvis_graph
from utils.state import init_session_state, get_state, set_state
import networkx as nx

# Set up page
st.set_page_config(
    page_title="Digital Twin Layer - Context-AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_theme()

# Header
header_with_logo()

# Page content
st.title("🔄 Digital Twin Layer")

st.markdown("""
## Knowledge Graph Representation of Entities

The Digital Twin Layer is the foundation of the Context-AI platform, creating a comprehensive 
knowledge graph representation of each entity that captures not just attributes, but all 
relevant relationships and context.
""")

# Explanation of concept
concept_card(
    "What is a Digital Twin?",
    """
    In Context-AI, a Digital Twin is a knowledge graph that represents an entity (like a 
    loan application) with all its attributes, relationships, and connections to relevant 
    context. This goes beyond traditional database records by modeling the entity within its 
    complete network of relationships.
    """,
    layer="digital_twin"
)

# Comparison with traditional approach
comparison_card(
    "Traditional Records vs. Knowledge Graphs",
    """
    Stores data in flat database tables with fixed schemas. Relationships between entities 
    exist only as foreign keys, and the focus is on efficient storage and retrieval of 
    individual records.
    """,
    """
    Represents data as a network of interconnected nodes and relationships, preserving the 
    context around each entity. The focus is on understanding the connections between data 
    points where valuable insights often hide.
    """
)

# Interactive knowledge graph demo
st.markdown("## Interactive Knowledge Graph Explorer")

st.markdown("""
Use this interactive knowledge graph to explore how a loan application is represented as a 
digital twin. The graph shows the connections between the business, its financial metrics, 
ownership structure, industry context, and other relevant factors.
""")

# Create a sample knowledge graph
G = nx.Graph()

# Add main entity node
G.add_node("ACME Corp", 
           size=30, 
           color=COLORS['digital_twin'], 
           title="ACME Corporation")

# Add relationship groups
relationship_groups = {
    "Financial Data": {
        "color": COLORS['primary'],
        "nodes": [
            "Revenue: $2.4M",
            "Profit Margin: 12%",
            "Cash Flow: $320K",
            "Debt Ratio: 0.34"
        ]
    },
    "Ownership": {
        "color": COLORS['primary'],
        "nodes": [
            "Owner: Jane Smith",
            "Years in Business: 7",
            "Management Team: 5 people"
        ]
    },
    "Industry": {
        "color": COLORS['external'],
        "nodes": [
            "Sector: Manufacturing",
            "Market Share: 3.2%",
            "Competitors: 12"
        ]
    },
    "Loan Details": {
        "color": COLORS['primary'],
        "nodes": [
            "Amount: $500K",
            "Purpose: Expansion",
            "Term: 5 years"
        ]
    }
}

# Add group nodes
for group, attrs in relationship_groups.items():
    # Add group node
    G.add_node(group, 
               size=20, 
               color=attrs["color"], 
               title=group)
    
    # Connect to main entity
    G.add_edge("ACME Corp", group, width=2)
    
    # Add detail nodes
    for node in attrs["nodes"]:
        G.add_node(node, 
                   size=12, 
                   color=attrs["color"], 
                   title=node)
        G.add_edge(group, node, width=1)

# Add some cross-connections to show relationship power
G.add_edge("Sector: Manufacturing", "Profit Margin: 12%", width=1, color=COLORS['edge_default'])
G.add_edge("Owner: Jane Smith", "Management Team: 5 people", width=1, color=COLORS['edge_default'])
G.add_edge("Purpose: Expansion", "Cash Flow: $320K", width=1, color=COLORS['edge_default'])

# Display the graph
create_pyvis_graph(G, height=600)

st.markdown("""
### Key Insights from the Knowledge Graph

The power of the digital twin representation comes from the ability to see connections that 
would be invisible in traditional data models:

- **Industry-Specific Context**: Understanding how this company performs relative to industry benchmarks
- **Financial Health Relationships**: Seeing how different financial metrics relate to each other
- **Ownership Structure Impact**: Recognizing how management experience connects to business performance
- **Loan Purpose Alignment**: Evaluating how the loan purpose aligns with business financials
""")

# Show how this fits into the larger platform
st.markdown("## How the Digital Twin Layer Fits in the Platform")

st.markdown("""
The Digital Twin Layer serves as the foundation for the entire Context-AI platform:

1. It provides the base representation that the **Temporal Intelligence Layer** tracks over time
2. It connects to external context through the **External Integration Layer**
3. It supplies the comprehensive view that the **Adaptive Guidance Layer** analyzes for recommendations

By starting with a rich, relationship-first representation, we enable all the other capabilities 
of the platform.
""")

# Next steps
st.markdown("## Next Steps")

col1, col2 = st.columns(2)

with col1:
    if st.button("Learn About Temporal Intelligence", key="btn_temporal"):
        st.switch_page("pages/temporal_intelligence_layer.py")

with col2:
    if st.button("Experience the Loan Journey Demo", key="btn_journey"):
        st.switch_page("pages/loan_journey_demo.py")