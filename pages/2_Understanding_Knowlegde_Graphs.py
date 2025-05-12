import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

# Page setup for dark theme
st.set_page_config(page_title="Understanding Knowledge Graphs", layout="wide")

# Apply custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    h1, h2, h3 {
        color: #FAFAFA;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .highlight {
        background-color: #1E88E5;
        padding: 0.4rem;
        border-radius: 0.4rem;
    }
    .container {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("Understanding Knowledge Graphs")
st.markdown("### The Building Blocks of Context-AI")

# Introduction with GIF
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ## What is a Knowledge Graph?
    
    A knowledge graph connects information through **relationships**, creating a network of knowledge that reveals insights hidden in isolated data.
    
    Think of it like the difference between:
    - A list of contacts in your phone
    - Your entire social network showing who knows whom and how
    
    In Context-AI, knowledge graphs serve as the foundation for understanding complex, interconnected information.
    """)

with col2:
    # Display the KG basics animation
    st.markdown("""
    <div style="text-align: center; padding-top: 2rem;">
        <img src="https://raw.githubusercontent.com/Kris-Nale314/context-ai/main/images/sillyKgExample.gif" width="100%">
    </div>
    """, unsafe_allow_html=True)

# Interactive section
st.markdown("""
<div class="container">
    <h2>Explore Knowledge Graphs Interactively</h2>
    <p>See how knowledge graphs build understanding by connecting information across domains. Use the buttons below to add different types of information to the graph.</p>
</div>
""", unsafe_allow_html=True)

# Create state to track which elements are shown
if 'show_basic' not in st.session_state:
    st.session_state.show_basic = True
    st.session_state.show_financial = False
    st.session_state.show_external = False

# Buttons to control what's displayed
col1, col2, col3 = st.columns(3)

with col1:
    basic_button = st.button("Basic Company Info", 
                          type="primary" if st.session_state.show_basic else "secondary")
    if basic_button:
        st.session_state.show_basic = True
        st.session_state.show_financial = False
        st.session_state.show_external = False

with col2:
    financial_button = st.button("Add Financial Data", 
                              type="primary" if st.session_state.show_financial else "secondary")
    if financial_button:
        st.session_state.show_basic = True
        st.session_state.show_financial = True
        st.session_state.show_external = False

with col3:
    external_button = st.button("Add External Context", 
                             type="primary" if st.session_state.show_external else "secondary")
    if external_button:
        st.session_state.show_basic = True
        st.session_state.show_financial = True
        st.session_state.show_external = True

# Start building nodes and edges with basic company info
nodes = [
    Node(id="TechInnovate", label="TechInnovate", size=30, color="#4CAF50")
]

edges = []

# Description area that changes based on what's shown
description_container = st.container()

# Always show these if basic info is enabled
if st.session_state.show_basic:
    # Add basic company info nodes
    nodes.extend([
        Node(id="Software", label="Software Industry", size=25, color="#2196F3"),
        Node(id="Founded", label="Founded: 2016", size=20, color="#9C27B0"),
        Node(id="Location", label="Austin, TX", size=20, color="#9C27B0"),
        Node(id="Team", label="48 Employees", size=20, color="#9C27B0")
    ])
    
    # Add basic relationships
    edges.extend([
        Edge(source="TechInnovate", target="Software", label="operates in", color="#FFFFFF"),
        Edge(source="TechInnovate", target="Founded", label="was", color="#FFFFFF"),
        Edge(source="TechInnovate", target="Location", label="based in", color="#FFFFFF"),
        Edge(source="TechInnovate", target="Team", label="has", color="#FFFFFF")
    ])
    
    with description_container:
        st.markdown("""
        <div class="container">
            <h3>Basic Information</h3>
            <p>The knowledge graph starts with basic information about the company. Even at this simple stage, relationships are made explicit - we don't just know facts about TechInnovate, we understand how these facts relate to the company.</p>
        </div>
        """, unsafe_allow_html=True)

# Add financial data if enabled
if st.session_state.show_financial:
    # Add financial nodes
    nodes.extend([
        Node(id="Financials", label="Financial Data", size=25, color="#FFC107"),
        Node(id="Revenue", label="Revenue: $2.4M", size=20, color="#FFC107"),
        Node(id="Margin", label="Profit: 18%", size=20, color="#FFC107"),
        Node(id="CAC", label="Customer Acq. Cost", size=20, color="#FFC107"),
        Node(id="LTV", label="Customer Lifetime Value", size=20, color="#FFC107")
    ])
    
    # Add financial relationships
    edges.extend([
        Edge(source="TechInnovate", target="Financials", label="has", color="#FFFFFF"),
        Edge(source="Financials", target="Revenue", label="includes", color="#FFFFFF"),
        Edge(source="Financials", target="Margin", label="includes", color="#FFFFFF"),
        Edge(source="Financials", target="CAC", label="includes", color="#FFFFFF"),
        Edge(source="Financials", target="LTV", label="includes", color="#FFFFFF"),
        # Cross-domain relationship
        Edge(source="Software", target="CAC", label="influences", color="#FFC107")
    ])
    
    with description_container:
        st.markdown("""
        <div class="container">
            <h3>Financial Context Added</h3>
            <p>As financial data is added, the knowledge graph expands to include detailed metrics. Notice the yellow relationship connecting the Software Industry to Customer Acquisition Cost - this is a <b>cross-domain relationship</b> that shows how industry context influences financial metrics.</p>
            <p>This type of insight would be difficult to capture in traditional databases.</p>
        </div>
        """, unsafe_allow_html=True)

# Add external context if enabled
if st.session_state.show_external:
    # Add external context nodes
    nodes.extend([
        Node(id="External", label="External Context", size=25, color="#E91E63"),
        Node(id="Market", label="Market Growth: 15%", size=20, color="#E91E63"),
        Node(id="Trend", label="Tech Investment Trend", size=20, color="#E91E63"),
        Node(id="Competitor", label="Competitor Funding", size=20, color="#E91E63"),
        Node(id="Risk", label="Risk Assessment", size=25, color="#673AB7"),
        Node(id="Recommend", label="Recommendation", size=25, color="#673AB7"),
        Node(id="Approve", label="Approve Loan", size=20, color="#673AB7")
    ])
    
    # Add external relationships
    edges.extend([
        Edge(source="Software", target="External", label="has", color="#FFFFFF"),
        Edge(source="External", target="Market", label="includes", color="#FFFFFF"),
        Edge(source="External", target="Trend", label="includes", color="#FFFFFF"),
        Edge(source="External", target="Competitor", label="includes", color="#FFFFFF"),
        # Strategic cross-connections
        Edge(source="Market", target="Revenue", label="positively impacts", color="#E91E63"),
        Edge(source="Trend", target="LTV", label="increases", color="#E91E63"),
        Edge(source="TechInnovate", target="Risk", label="has", color="#FFFFFF"),
        Edge(source="Risk", target="Recommend", label="leads to", color="#FFFFFF"),
        Edge(source="Recommend", target="Approve", label="suggests", color="#FFFFFF"),
        # Evidence paths
        Edge(source="Financials", target="Risk", label="informs", color="#673AB7"),
        Edge(source="External", target="Risk", label="influences", color="#673AB7")
    ])
    
    with description_container:
        st.markdown("""
        <div class="container">
            <h3>Complete Picture with External Context</h3>
            <p>With external context integrated, the knowledge graph now shows how market trends and competitor activity influence specific company metrics.</p>
            <p>Notice the purple recommendation path - the system can now make decisions with clear connections to the evidence. Each recommendation is transparently connected to the data that supports it.</p>
            <p>The complete graph reveals insights like:</p>
            <ul>
                <li>Market growth positively impacts revenue projections</li>
                <li>Tech investment trends increase customer lifetime value</li>
                <li>Financial data and external context together inform risk assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Configure and display the graph
config = Config(
    width=None,
    height=600,
    directed=True,
    physics=True,
    hierarchical=False,
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    collapsible=False,
    node={'labelProperty': 'label', 'renderLabel': True, 'fontSize': 18},
    link={'labelProperty': 'label', 'renderLabel': True, 'fontSize': 16, 'color': '#FFFFFF'}
)

# Render the graph
st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
agraph(nodes=nodes, edges=edges, config=config)

# Display a key takeaway
if st.session_state.show_external:
    st.markdown("""
    <div style="background-color: #4CAF50; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem; text-align: center;">
        <h3 style="color: white;">Key Insight</h3>
        <p>In traditional systems, data is stored in separate silos. Knowledge graphs reveal the connections between data points across domains, creating a rich context for better decisions.</p>
    </div>
    """, unsafe_allow_html=True)

# Call to action for next page
st.markdown("""
<div style="text-align: center; margin-top: 2rem;">
    <a href="/02_Digital_Twins" target="_self" style="
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;">
        Next: Explore Digital Twins →
    </a>
</div>
""", unsafe_allow_html=True)