import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

# Page setup
st.set_page_config(page_title="Understanding Knowledge Graphs", layout="wide")

# Main title
st.title("Understanding Knowledge Graphs")
st.subheader("The Foundation of Context-AI")

# Option to place the slide at the top
show_slide_at_top = True  # Set to False to show at bottom

if show_slide_at_top:
    # Display the key slide at the top
    #st.video("images/kgBasics.gif")
    
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/Kris-Nale314/context-ai/main/images/kgBasics.gif" width="1000">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

# Introduction
st.markdown("""
## What is a Knowledge Graph?

A knowledge graph represents information as a network of **entities** and their **relationships**, 
rather than as isolated data points in tables. This approach reveals patterns and insights 
that would otherwise remain hidden.

Knowledge graphs are the foundation of Context-AI's ability to understand complex, interconnected data.
Let's explore how they differ from traditional data approaches:
""")

# Create view selector
view_type = st.radio("Compare approaches:", ["Traditional Database View", "Knowledge Graph View"], horizontal=True)

# Display based on selection
if view_type == "Traditional Database View":
    # Display table data
    st.markdown("### Traditional Database Approach")
    
    st.markdown("""
    In traditional database systems, data is stored in separate tables with relationships 
    defined by foreign keys. This creates a rigid structure where context is often lost.
    """)
    
    # Column layout for tables and limitations
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Companies table
        st.markdown("**Companies Table:**")
        companies_df = pd.DataFrame({
            "CompanyID": [1001],
            "Name": ["TechInnovate"],
            "Industry": ["Software"],
            "YearsInBusiness": [7]
        })
        st.dataframe(companies_df, use_container_width=True)
        
        # Financials table
        st.markdown("**Financials Table:**")
        financials_df = pd.DataFrame({
            "FinancialID": [5001],
            "CompanyID": [1001],
            "Revenue": ["$2.4M"],
            "ProfitMargin": ["18%"]
        })
        st.dataframe(financials_df, use_container_width=True)
        
        # Loans table
        st.markdown("**Loans Table:**")
        loans_df = pd.DataFrame({
            "LoanID": [8001],
            "CompanyID": [1001],
            "Amount": ["$500K"],
            "Purpose": ["Expansion"]
        })
        st.dataframe(loans_df, use_container_width=True)
    
    with col2:
        st.markdown("**Key Limitations:**")
        st.markdown("""
        - Data points are isolated in separate tables
        - Relationships exist only as IDs linking tables
        - Context and meaning are implicit, not explicit
        - Cross-domain insights are difficult to discover
        - Static representation that doesn't evolve naturally
        - Difficult to incorporate external context
        """)
    
else:
    # Display knowledge graph
    st.markdown("### Knowledge Graph Approach")
    
    st.markdown("""
    Knowledge graphs represent data as an interconnected network of entities and relationships.
    This preserves context and allows insights to emerge from connections.
    
    Try moving nodes around to explore the relationships:
    """)
    
    # Create nodes
    nodes = [
        Node(id="TechInnovate", label="TechInnovate", size=30, color="#4CAF50"),
        Node(id="Software", label="Software Industry", size=20, color="#2196F3"),
        Node(id="Revenue", label="Revenue: $2.4M", size=15, color="#9C27B0"),
        Node(id="Margin", label="Profit: 18%", size=15, color="#9C27B0"),
        Node(id="Loan", label="Loan: $500K", size=20, color="#FF9800"),
        Node(id="Expansion", label="Purpose: Expansion", size=15, color="#FF9800"),
        Node(id="Market", label="Market Growth: 15%", size=15, color="#2196F3"),
        Node(id="Competition", label="Low Competition", size=15, color="#2196F3")
    ]
    
    # Create edges
    edges = [
        Edge(source="TechInnovate", target="Software", label="operates in"),
        Edge(source="TechInnovate", target="Revenue", label="has"),
        Edge(source="TechInnovate", target="Margin", label="has"),
        Edge(source="TechInnovate", target="Loan", label="requests"),
        Edge(source="Loan", target="Expansion", label="for"),
        Edge(source="Software", target="Revenue", label="influences"),
        Edge(source="Software", target="Market", label="experiencing"),
        Edge(source="Market", target="Expansion", label="supports"),
        Edge(source="Software", target="Competition", label="has"),
        Edge(source="Competition", target="Margin", label="allows")
    ]
    
    # Create configuration
    config = Config(
        width=700,
        height=500,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=False
    )
    
    # Render the graph
    agraph(nodes=nodes, edges=edges, config=config)
    
    # Add explanation of the visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Key Advantages:**")
        st.markdown("""
        - Relationships are explicit and meaningful
        - Context is preserved across domains
        - Insights emerge from connections
        - Cross-domain patterns become visible
        - The graph can evolve organically as new information arrives
        """)
    
    with col2:
        st.markdown("**In this example:**")
        st.markdown("""
        - Industry trends directly connect to company financials
        - Market growth supports expansion purpose (implicit in traditional DB)
        - Low competition explains high profit margins (cross-domain insight)
        - The graph can easily add new relationships as they emerge
        """)

# Anatomy of a Knowledge Graph
st.markdown("""
## Anatomy of a Knowledge Graph

Knowledge graphs consist of three main elements:

1. **Nodes (Entities)**: Individual data points like companies, people, or concepts
2. **Edges (Relationships)**: Connections between nodes showing how they relate to each other
3. **Properties**: Attributes that describe nodes and relationships
""")

# Simple KG structure example
st.markdown("### Basic Structure")

# Create a simple educational graph
basic_nodes = [
    Node(id="Company", label="Company", size=30, color="#4CAF50", title="The central entity"),
    Node(id="Financial", label="Financial Metrics", size=20, color="#9C27B0", title="Financial information"),
    Node(id="Industry", label="Industry", size=20, color="#2196F3", title="Industry context"),
    Node(id="Management", label="Management", size=20, color="#9C27B0", title="Company leadership"),
    Node(id="Revenue", label="Revenue", size=15, color="#9C27B0", title="Annual revenue"),
    Node(id="CEO", label="CEO", size=15, color="#9C27B0", title="Chief Executive"),
    Node(id="Growth", label="Growth Rate", size=15, color="#2196F3", title="Industry growth")
]

basic_edges = [
    Edge(source="Company", target="Financial", label="has"),
    Edge(source="Company", target="Industry", label="part of"),
    Edge(source="Company", target="Management", label="led by"),
    Edge(source="Financial", target="Revenue", label="includes"),
    Edge(source="Management", target="CEO", label="includes"),
    Edge(source="Industry", target="Growth", label="has"),
    Edge(source="Growth", target="Revenue", label="influences")
]

basic_config = Config(
    width=700,
    height=300,
    directed=True,
    physics=True,
    hierarchical=False
)

st.markdown("""
The following simple graph shows the basic structure of a knowledge graph. 
Notice how different types of information connect to form a meaningful network:
""")

agraph(nodes=basic_nodes, edges=basic_edges, config=basic_config)

st.markdown("""
In this example:
- **Nodes** represent different entities and concepts
- **Edges** show meaningful relationships between nodes
- **Cross-connections** (like "Growth influences Revenue") reveal insights that would be difficult to see in traditional databases
""")

# How Knowledge Graphs Grow
st.markdown("""
## How Knowledge Graphs Evolve: Building a Digital Twin

One of the most powerful aspects of knowledge graphs is how they evolve over time, 
continuously incorporating new information and connections. This makes them ideal for 
building **digital twins** - virtual representations of real-world entities that grow and change.

In Context-AI, we use knowledge graphs to create digital twins of entities like companies, 
representing not just their attributes but their complex relationships to the world around them.
""")

# Evolution stages
stage = st.select_slider(
    "See how a knowledge graph grows over time:",
    options=["Initial Data", "Added Financials", "External Context", "Complete Picture"]
)

if stage == "Initial Data":
    # Show simplest graph
    simple_nodes = [
        Node(id="TechInnovate", label="TechInnovate", size=30, color="#4CAF50"),
        Node(id="Software", label="Software Industry", size=20, color="#2196F3"),
        Node(id="Founded", label="Founded: 2016", size=15, color="#9C27B0"),
        Node(id="Location", label="Location: Austin", size=15, color="#9C27B0")
    ]
    
    simple_edges = [
        Edge(source="TechInnovate", target="Software", label="operates in"),
        Edge(source="TechInnovate", target="Founded", label="was"),
        Edge(source="TechInnovate", target="Location", label="based in")
    ]
    
    st.markdown("""
    ### Stage 1: Basic Information
    
    The digital twin begins with basic identifying information about the entity.
    Even at this stage, the knowledge graph represents relationships explicitly.
    """)
    
elif stage == "Added Financials":
    # Show graph with financial data
    simple_nodes = [
        Node(id="TechInnovate", label="TechInnovate", size=30, color="#4CAF50"),
        Node(id="Software", label="Software Industry", size=20, color="#2196F3"),
        Node(id="Founded", label="Founded: 2016", size=15, color="#9C27B0"),
        Node(id="Location", label="Location: Austin", size=15, color="#9C27B0"),
        Node(id="Revenue", label="Revenue: $2.4M", size=15, color="#9C27B0"),
        Node(id="Margin", label="Profit: 18%", size=15, color="#9C27B0"),
        Node(id="Financials", label="Financial Metrics", size=20, color="#9C27B0"),
        Node(id="CAC", label="CAC: $1,200", size=15, color="#9C27B0"),
        Node(id="LTV", label="LTV: $6,500", size=15, color="#9C27B0")
    ]
    
    simple_edges = [
        Edge(source="TechInnovate", target="Software", label="operates in"),
        Edge(source="TechInnovate", target="Founded", label="was"),
        Edge(source="TechInnovate", target="Location", label="based in"),
        Edge(source="TechInnovate", target="Financials", label="has"),
        Edge(source="Financials", target="Revenue", label="includes"),
        Edge(source="Financials", target="Margin", label="includes"),
        Edge(source="Financials", target="CAC", label="includes"),
        Edge(source="Financials", target="LTV", label="includes"),
        Edge(source="Software", target="CAC", label="influences")
    ]
    
    st.markdown("""
    ### Stage 2: Financial Information Added
    
    As financial data is analyzed, the knowledge graph expands to include detailed metrics.
    Notice how industry-specific metrics (like CAC and LTV for SaaS) are connected to the 
    industry node, showing context-awareness.
    """)
    
elif stage == "External Context":
    # Show graph with external context
    simple_nodes = [
        Node(id="TechInnovate", label="TechInnovate", size=30, color="#4CAF50"),
        Node(id="Software", label="Software Industry", size=20, color="#2196F3"),
        Node(id="Founded", label="Founded: 2016", size=15, color="#9C27B0"),
        Node(id="Location", label="Location: Austin", size=15, color="#9C27B0"),
        Node(id="Revenue", label="Revenue: $2.4M", size=15, color="#9C27B0"),
        Node(id="Margin", label="Profit: 18%", size=15, color="#9C27B0"),
        Node(id="Financials", label="Financial Metrics", size=20, color="#9C27B0"),
        Node(id="CAC", label="CAC: $1,200", size=15, color="#9C27B0"),
        Node(id="LTV", label="LTV: $6,500", size=15, color="#9C27B0"),
        Node(id="Market", label="Market Growth: 15%", size=15, color="#2196F3"),
        Node(id="Trend", label="Tech Investment", size=15, color="#2196F3"),
        Node(id="External", label="External Context", size=20, color="#2196F3")
    ]
    
    simple_edges = [
        Edge(source="TechInnovate", target="Software", label="operates in"),
        Edge(source="TechInnovate", target="Founded", label="was"),
        Edge(source="TechInnovate", target="Location", label="based in"),
        Edge(source="TechInnovate", target="Financials", label="has"),
        Edge(source="Financials", target="Revenue", label="includes"),
        Edge(source="Financials", target="Margin", label="includes"),
        Edge(source="Financials", target="CAC", label="includes"),
        Edge(source="Financials", target="LTV", label="includes"),
        Edge(source="Software", target="CAC", label="influences"),
        Edge(source="Software", target="External", label="has"),
        Edge(source="External", target="Market", label="includes"),
        Edge(source="External", target="Trend", label="includes"),
        Edge(source="Market", target="Revenue", label="influences"),
        Edge(source="Trend", target="LTV", label="enhances")
    ]
    
    st.markdown("""
    ### Stage 3: External Context Integration
    
    External market context is now connected to the digital twin, showing how 
    industry trends and market conditions influence specific company metrics.
    
    These connections allow the system to understand, for example, that strong SaaS market 
    growth positively impacts the company's revenue potential.
    """)
    
else:  # Complete Picture
    # Show most complex graph
    simple_nodes = [
        Node(id="TechInnovate", label="TechInnovate", size=30, color="#4CAF50"),
        Node(id="Software", label="Software Industry", size=20, color="#2196F3"),
        Node(id="Founded", label="Founded: 2016", size=15, color="#9C27B0"),
        Node(id="Location", label="Location: Austin", size=15, color="#9C27B0"),
        Node(id="Revenue", label="Revenue: $2.4M", size=15, color="#9C27B0"),
        Node(id="Margin", label="Profit: 18%", size=15, color="#9C27B0"),
        Node(id="Financials", label="Financial Metrics", size=20, color="#9C27B0"),
        Node(id="CAC", label="CAC: $1,200", size=15, color="#9C27B0"),
        Node(id="LTV", label="LTV: $6,500", size=15, color="#9C27B0"),
        Node(id="Market", label="Market Growth: 15%", size=15, color="#2196F3"),
        Node(id="Trend", label="Tech Investment", size=15, color="#2196F3"),
        Node(id="External", label="External Context", size=20, color="#2196F3"),
        Node(id="Risk", label="Risk Assessment", size=20, color="#FFC107"),
        Node(id="FinRisk", label="Financial Risk: Low", size=15, color="#FFC107"),
        Node(id="MktRisk", label="Market Risk: Low", size=15, color="#FFC107"),
        Node(id="Recommend", label="Recommendation", size=20, color="#FFC107"),
        Node(id="Approve", label="Approve Loan", size=15, color="#FFC107")
    ]
    
    simple_edges = [
        Edge(source="TechInnovate", target="Software", label="operates in"),
        Edge(source="TechInnovate", target="Founded", label="was"),
        Edge(source="TechInnovate", target="Location", label="based in"),
        Edge(source="TechInnovate", target="Financials", label="has"),
        Edge(source="Financials", target="Revenue", label="includes"),
        Edge(source="Financials", target="Margin", label="includes"),
        Edge(source="Financials", target="CAC", label="includes"),
        Edge(source="Financials", target="LTV", label="includes"),
        Edge(source="Software", target="CAC", label="influences"),
        Edge(source="Software", target="External", label="has"),
        Edge(source="External", target="Market", label="includes"),
        Edge(source="External", target="Trend", label="includes"),
        Edge(source="Market", target="Revenue", label="influences"),
        Edge(source="Trend", target="LTV", label="enhances"),
        Edge(source="TechInnovate", target="Risk", label="has"),
        Edge(source="Risk", target="FinRisk", label="includes"),
        Edge(source="Risk", target="MktRisk", label="includes"),
        Edge(source="Financials", target="FinRisk", label="informs"),
        Edge(source="External", target="MktRisk", label="informs"),
        Edge(source="Risk", target="Recommend", label="leads to"),
        Edge(source="Recommend", target="Approve", label="suggests")
    ]
    
    st.markdown("""
    ### Stage 4: Complete Assessment
    
    The complete digital twin now includes risk assessment and recommendations, 
    with clear connections showing how each conclusion is supported by evidence.
    
    This transparent reasoning path helps explain why specific recommendations are made,
    connecting data directly to decisions.
    """)

evolution_config = Config(
    width=700,
    height=500,
    directed=True,
    physics=True,
    hierarchical=False
)

agraph(nodes=simple_nodes, edges=simple_edges, config=evolution_config)

# Key benefits
st.markdown("""
## Key Benefits of the Knowledge Graph Approach

Knowledge graphs provide several fundamental advantages that make them ideal for Context-AI:
""")

ben_col1, ben_col2 = st.columns(2)

with ben_col1:
    st.markdown("""
    ### Relationship-First Design
    Traditional systems store data as isolated records. Knowledge graphs prioritize relationships as 
    first-class entities, making connections explicit rather than implicit. This reveals patterns that 
    remain invisible in traditional analysis.
    
    ### Network Effects in Data
    Each new piece of information adds value not just by itself, but by creating new connections with 
    existing data. This creates compounding returns as the knowledge graph grows, unlike the linear 
    improvements seen in traditional systems.
    """)

with ben_col2:
    st.markdown("""
    ### Context Preservation
    Traditional systems often lose context when storing data. Knowledge graphs maintain the essential 
    context around each data point, preserving its meaning and relevance to other information.
    
    ### Cross-Domain Integration
    Knowledge graphs easily connect information across different domains - financial metrics, management details, 
    market factors - creating a unified representation that spans traditional data silos.
    """)

# Next steps
st.markdown("""
## From Knowledge Graphs to Digital Twins

Now that you understand the fundamentals of knowledge graphs, the next step is to explore how 
Context-AI uses them to create comprehensive digital twins that evolve over time.

In the next section, we'll explore how digital twins grow and change, incorporating temporal 
intelligence and external context to provide deeper insights.
""")

# CTA button for next section
st.markdown("""
<div style="text-align: center; margin-top: 30px;">
    <a href="/02_Digital_Twins" target="_self" style="
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;">
        Continue to Digital Twins →
    </a>
</div>
""", unsafe_allow_html=True)

# Option to place the slide at the bottom
if not show_slide_at_top:
    st.markdown("---")
    st.markdown("## Knowledge Graph Foundation")
    st.image("images/kgSlide.png", use_column_width=True)