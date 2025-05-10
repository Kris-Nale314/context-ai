# pages/1_Understanding_Knowledge_Graphs.py
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from utils.theme import setup_page_config, apply_theme, COLORS
from utils.ui_components import header_with_logo, concept_card
from utils.demo_data import load_applicant_data, generate_all_data
from utils.graph_viz import networkx_matplotlib_graph
from utils.kg_generator import create_initial_knowledge_graph, create_expanded_knowledge_graph

# Set up page config and theme
setup_page_config()
apply_theme()

# Header
header_with_logo()

# Main title
st.title("Understanding Digital Twins & Knowledge Graphs")
st.subheader("Why Relationships Matter in Loan Assessment")

# Introduction section
st.markdown("""
## Beyond Tables: The Knowledge Graph Advantage

Traditional loan assessment systems store data in flat tables or simple relational databases. 
While functional, this approach misses the rich web of relationships that truly define an entity. 
Context-AI takes a fundamentally different approach by representing each loan application as a 
**knowledge graph** - creating a digital twin that captures not just data points, but the 
connections between them.
""")

# Visual comparison between traditional and KG approaches
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Traditional Database Approach")
    
    # Create sample tabular data
    traditional_data = pd.DataFrame({
        "Field": ["Company Name", "Industry", "Revenue", "Years in Business", "Loan Amount", 
                 "Credit Score", "Profit Margin", "Purpose"],
        "Value": ["TechInnovate Solutions", "Software Development", "$2,400,000", "7", 
                 "$500,000", "A", "18%", "Expansion into new markets"]
    })
    
    st.table(traditional_data)
    
    st.markdown("""
    **Limitations:**
    - Data points are isolated
    - Relationships are implicit or missing
    - Context is lost or disconnected
    - Difficult to see patterns across domains
    - Static representation of information
    """)

with col2:
    st.markdown("### Knowledge Graph Approach")
    
    # Try to load a sample company profile to use
    try:
        applicant_data = load_applicant_data("strong_applicant")
        if not applicant_data:
            generate_all_data()
            applicant_data = load_applicant_data("strong_applicant")
        
        company = applicant_data["company_profile"]
        
        # Create a simple KG as an example
        G = create_initial_knowledge_graph(company)
        
        # Visualize the knowledge graph
        networkx_matplotlib_graph(G, height=300)
    except Exception as e:
        st.error(f"Error creating example graph: {e}")
        # Fallback text description
        st.markdown("*Visualization would show a connected graph of company attributes and relationships*")
    
    st.markdown("""
    **Advantages:**
    - Explicit relationship modeling
    - Context is preserved
    - Insights emerge from connections
    - Dynamic representation evolves over time
    - Cross-domain pattern recognition
    """)

# Anatomy of a Knowledge Graph
st.markdown("""
## Anatomy of a Knowledge Graph

Knowledge graphs consist of three main elements:

1. **Nodes (Entities)**: Individual data points like companies, financial metrics, or industry factors
2. **Edges (Relationships)**: Connections between nodes showing how they relate to each other
3. **Properties**: Attributes that describe nodes and relationships, including confidence scores
""")

# Simple node-edge explanation with visual
st.markdown("""
### Basic Structure
""")

# Create a simple educational example
example_G = nx.Graph()

# Add main node
example_G.add_node("Company", size=30, color=COLORS['digital_twin'], title="The Entity")

# Add related nodes
example_G.add_node("Financial Metrics", size=20, color=COLORS['primary'], title="Financial Data")
example_G.add_node("Management Team", size=20, color=COLORS['primary'], title="Leadership Info")
example_G.add_node("Industry", size=20, color=COLORS['external'], title="External Context")

# Add edges
example_G.add_edge("Company", "Financial Metrics", width=2, title="has financials")
example_G.add_edge("Company", "Management Team", width=2, title="led by")
example_G.add_edge("Company", "Industry", width=2, title="operates in")

# Add specific data points
example_G.add_node("Revenue: $2.4M", size=15, color=COLORS['primary'], title="Annual Revenue")
example_G.add_node("CEO: Alice Smith", size=15, color=COLORS['primary'], title="Chief Executive")
example_G.add_node("SaaS Sector", size=15, color=COLORS['external'], title="Software as a Service")

# Connect them
example_G.add_edge("Financial Metrics", "Revenue: $2.4M", width=1)
example_G.add_edge("Management Team", "CEO: Alice Smith", width=1)
example_G.add_edge("Industry", "SaaS Sector", width=1)

# Add a cross-connection
example_G.add_edge("SaaS Sector", "Revenue: $2.4M", width=1, color=COLORS['edge_default'], 
                  title="influences")

# Visualize
networkx_matplotlib_graph(example_G, height=300)

st.markdown("""
In this simple example:
- **Nodes** represent entities like the company and its attributes
- **Edges** show how these entities relate to each other
- Note the cross-connection between industry sector and revenue (showing how external context influences financial metrics)
""")

# Interactive Knowledge Graph Growth Demo
st.markdown("""
## How Knowledge Graphs Grow: Building a Digital Twin

One of the most powerful aspects of knowledge graphs is how they evolve as more information 
becomes available. Let's see how a digital twin builds up over the loan journey:
""")

# Create tabs for different stages of KG growth
tab1, tab2, tab3 = st.tabs(["Initial Application", "After Financial Review", "With External Context"])

# Try to load sample data
try:
    applicant_data = load_applicant_data("strong_applicant")
    company = applicant_data["company_profile"]
    financial_data = applicant_data["financial_data"]
    
    with tab1:
        st.markdown("### Stage 1: Basic Application Information")
        st.markdown("""
        When a loan application is first submitted, the knowledge graph starts with basic information:
        company details, loan request, and fundamental relationships.
        """)
        
        # Create initial knowledge graph
        basic_G = create_initial_knowledge_graph(company)
        networkx_matplotlib_graph(basic_G, height=350)
        
        st.markdown("""
        **Node Count:** {} nodes, {} edges
        
        Even at this early stage, relationships are explicit rather than implicit. The graph shows
        how the company connects to its industry, the loan request details, and basic credit history.
        """.format(len(basic_G.nodes), len(basic_G.edges)))
    
    with tab2:
        st.markdown("### Stage 2: Financial Information Added")
        st.markdown("""
        As financial statements are reviewed, the knowledge graph expands to include detailed financial
        metrics and their relationships to each other and to the company.
        """)
        
        # Create expanded knowledge graph
        expanded_G = create_expanded_knowledge_graph(company, financial_data.iloc[2])
        networkx_matplotlib_graph(expanded_G, height=350)
        
        st.markdown("""
        **Node Count:** {} nodes, {} edges ({}% increase)
        
        Now financial metrics are connected, showing relationships between revenue, profit margins, and
        industry-specific metrics. These connections enable pattern recognition across financial dimensions.
        """.format(len(expanded_G.nodes), len(expanded_G.edges), 
                 round((len(expanded_G.edges) - len(basic_G.edges)) / len(basic_G.edges) * 100)))
    
    with tab3:
        st.markdown("### Stage 3: External Context Integration")
        st.markdown("""
        The knowledge graph continues to evolve as external context is integrated, connecting
        the company to market trends, competitors, and economic factors.
        """)
        
        # Create a more comprehensive graph with external context
        # For this example, we'll manually add some external context nodes
        comprehensive_G = expanded_G.copy()
        
        # Add external context group
        comprehensive_G.add_node("External Context", size=25, color=COLORS['external'], 
                               title="External Context")
        comprehensive_G.add_edge(company['name'], "External Context", width=2)
        
        # Add external factors
        external_factors = [
            "Industry Growth Trend",
            "Technology Adoption Rate",
            "Competitive Landscape",
            "Regulatory Environment"
        ]
        
        for factor in external_factors:
            comprehensive_G.add_node(factor, size=15, color=COLORS['external'], title=factor)
            comprehensive_G.add_edge("External Context", factor, width=1)
        
        # Add cross-connections to show how external factors influence internal metrics
        comprehensive_G.add_edge("Industry Growth Trend", "SaaS Metrics", width=1, 
                              color=COLORS['edge_default'])
        comprehensive_G.add_edge("Technology Adoption Rate", "Revenue: $2,400,000", width=1, 
                              color=COLORS['edge_default'])
        
        networkx_matplotlib_graph(comprehensive_G, height=350)
        
        st.markdown("""
        **Node Count:** {} nodes, {} edges ({}% increase from initial)
        
        The knowledge graph now integrates external context, creating connections between outside
        factors and internal metrics. These connections reveal how the company fits into its broader
        environment and how external factors influence its performance.
        """.format(len(comprehensive_G.nodes), len(comprehensive_G.edges), 
                 round((len(comprehensive_G.edges) - len(basic_G.edges)) / len(basic_G.edges) * 100)))
except Exception as e:
    st.error(f"Error loading sample data: {e}")
    st.markdown("*Example visualizations would show the knowledge graph growing in complexity across stages*")

# Explain key innovations of using KGs
st.markdown("""
## Key Innovations of the Knowledge Graph Approach

The knowledge graph approach offers several fundamental advantages over traditional data models:
""")

innovation_cols = st.columns(2)

with innovation_cols[0]:
    concept_card(
        "Relationship-First Design",
        """
        Traditional systems store data as records with foreign keys. Knowledge graphs prioritize relationships as first-class entities, making connections explicit rather than implicit. This reveals patterns invisible to traditional analysis.
        """,
        layer="digital_twin"
    )
    
    concept_card(
        "Network Effects in Data",
        """
        Each new piece of information adds value not just by itself, but by creating new connections with existing data. This creates compounding returns as the knowledge graph grows, unlike linear improvements in traditional systems.
        """,
        layer="digital_twin"
    )

with innovation_cols[1]:
    concept_card(
        "Context Preservation",
        """
        Traditional systems often lose context when storing data. Knowledge graphs maintain the essential context around each data point, preserving its meaning and relevance to other information.
        """,
        layer="digital_twin"
    )
    
    concept_card(
        "Cross-Domain Integration",
        """
        Knowledge graphs easily connect information across different domains - financial metrics, management details, market factors - creating a unified representation that spans traditional data silos.
        """,
        layer="digital_twin"
    )

# Comparative example: Traditional vs. KG approach
st.markdown("""
## Real-World Example: Detecting Customer Concentration Risk

Let's see how a traditional approach and the knowledge graph approach would differ when 
analyzing a manufacturing company with customer concentration risk:
""")

example_cols = st.columns(2)

with example_cols[0]:
    st.markdown("### Traditional Approach")
    
    # Create sample customer data
    customers_data = pd.DataFrame({
        "Customer ID": ["C001", "C002", "C003", "C004", "C005", "Others"],
        "Revenue": ["$210,000", "$84,000", "$63,000", "$42,000", "$21,000", "$80,000"],
        "% of Total": ["42%", "16.8%", "12.6%", "8.4%", "4.2%", "16%"]
    })
    
    st.dataframe(customers_data)
    
    st.markdown("""
    **Process:**
    1. Store customer revenue in database table
    2. Calculate percentage of total revenue
    3. Manually identify customers above threshold
    4. Separately analyze industry benchmarks
    5. Manually assess risk implications
    
    **Limitations:**
    - Connection to industry standards is separate
    - Risk assessment requires manual judgment
    - No automatic connection to similar past cases
    - Temporal trends require separate analysis
    - No integration with external factors affecting customers
    """)

with example_cols[1]:
    st.markdown("### Knowledge Graph Approach")
    
    # Create a KG showing customer concentration
    concentration_G = nx.Graph()
    
    # Add main company node
    concentration_G.add_node("ManufacturePro", size=30, color=COLORS['digital_twin'], 
                           title="Manufacturing Company")
    
    # Add customers group
    concentration_G.add_node("Customers", size=20, color=COLORS['primary'], title="Customer Base")
    concentration_G.add_edge("ManufacturePro", "Customers", width=2)
    
    # Add individual customers
    customers = [
        {"id": "Customer A", "revenue": 210000, "percentage": 0.42},
        {"id": "Customer B", "revenue": 84000, "percentage": 0.168},
        {"id": "Customer C", "revenue": 63000, "percentage": 0.126},
        {"id": "Customer D", "revenue": 42000, "percentage": 0.084},
        {"id": "Customer E", "revenue": 21000, "percentage": 0.042},
        {"id": "Others", "revenue": 80000, "percentage": 0.16}
    ]
    
    for customer in customers:
        # Size node based on percentage
        size = 10 + (customer["percentage"] * 50)
        
        # Color based on concentration risk
        if customer["percentage"] > 0.25:
            color = COLORS['low_confidence']  # Risk color
        elif customer["percentage"] > 0.15:
            color = COLORS['medium_confidence']  # Warning color
        else:
            color = COLORS['primary']  # Normal color
        
        # Add node
        node_name = f"{customer['id']}: {customer['percentage']*100:.1f}%"
        concentration_G.add_node(node_name, size=size, color=color, 
                               title=f"${customer['revenue']:,} ({customer['percentage']*100:.1f}%)")
        concentration_G.add_edge("Customers", node_name, width=1 + (customer["percentage"] * 5))
    
    # Add risk assessment
    concentration_G.add_node("Risk Assessment", size=20, color=COLORS['guidance'], title="Risk Evaluation")
    concentration_G.add_edge("ManufacturePro", "Risk Assessment", width=2)
    
    # Add specific risk factor
    concentration_G.add_node("Customer Concentration Risk", size=15, color=COLORS['low_confidence'], 
                           title="High concentration with Customer A")
    concentration_G.add_edge("Risk Assessment", "Customer Concentration Risk", width=2)
    
    # Connect high concentration customer to risk
    concentration_G.add_edge("Customer A: 42.0%", "Customer Concentration Risk", width=2, 
                           color=COLORS['low_confidence'])
    
    # Add industry benchmark
    concentration_G.add_node("Industry Benchmark: 20%", size=15, color=COLORS['external'], 
                           title="Manufacturing industry recommendation")
    concentration_G.add_edge("Customer Concentration Risk", "Industry Benchmark: 20%", width=1)
    
    # Add similar past cases
    concentration_G.add_node("Similar Past Cases", size=15, color=COLORS['temporal'], 
                           title="Historical patterns")
    concentration_G.add_edge("Customer Concentration Risk", "Similar Past Cases", width=1)
    
    # Add mitigation recommendation
    concentration_G.add_node("Diversification Plan", size=15, color=COLORS['guidance'], 
                           title="Customer acquisition strategy")
    concentration_G.add_edge("Risk Assessment", "Diversification Plan", width=1)
    
    # Visualize
    networkx_matplotlib_graph(concentration_G, height=400)
    
    st.markdown("""
    **Process:**
    1. Automatically detect concentration patterns in knowledge graph
    2. Automatically connect to industry benchmarks
    3. Link to similar historical cases and outcomes
    4. Integrate with external factors affecting key customers
    5. Generate specific recommendations based on patterns
    
    **Advantages:**
    - Risk patterns automatically emerge from the graph structure
    - Industry context is integrated directly in the knowledge model
    - Similar historical cases provide context for assessment
    - Connections show specific mitigation strategies
    - Risk factors link to specific data points, creating transparency
    """)

# Technical implementation insights
st.markdown("""
## Technical Implementation Insights

The Digital Twin approach in Context-AI is implemented through several technical innovations:
""")

tech_cols = st.columns(2)

with tech_cols[0]:
    st.markdown("""
    ### Knowledge Graph Implementation
    
    - **Graph Database Backend**: Specialized storage optimized for relationship queries
    - **Triple-level Versioning**: Each subject-predicate-object relationship carries temporal attributes
    - **Confidence Scoring**: Every relationship has confidence metadata based on source reliability
    - **Property Graph Model**: Nodes and edges have rich property sets for detailed modeling
    - **Semantic Typing**: Entities and relationships follow consistent ontology patterns
    """)

with tech_cols[1]:
    st.markdown("""
    ### Integration Approaches
    
    - **Entity Resolution**: Automated matching of entities across different sources
    - **Semantic Alignment**: Mapping between different vocabularies and schemas
    - **Incremental Updates**: Efficient graph updates when new information arrives
    - **Relationship Inference**: Automatic discovery of implicit relationships
    - **Confidence Propagation**: Updates to fact confidence propagate through inference chains
    """)

# Value creation
st.markdown("""
## Value Creation: How Digital Twins Transform Loan Assessment

The knowledge graph approach creates value through several key mechanisms:
""")

value_cols = st.columns(3)

with value_cols[0]:
    st.markdown("""
    ### 1. Pattern Recognition
    
    - Identify risk and opportunity patterns invisible in traditional systems
    - Detect subtle connections between seemingly unrelated factors
    - Recognize patterns that span internal and external data
    - Find similarities to past cases with known outcomes
    """)

with value_cols[1]:
    st.markdown("""
    ### 2. Contextual Intelligence
    
    - Evaluate entities within their full context
    - Understand how external factors influence specific metrics
    - Maintain the meaning and relevance of each data point
    - Preserve the "why" behind recommendations
    """)

with value_cols[2]:
    st.markdown("""
    ### 3. Adaptive Learning
    
    - Continuously refine the knowledge model as new information arrives
    - Learn patterns that improve future assessments
    - Build cumulative intelligence that grows over time
    - Adapt to changing conditions in different industries
    """)

# Call to action
st.markdown("""
## Experience Digital Twins in Action

Now that you understand the power of knowledge graphs and digital twins, explore how they work
in different loan scenarios:
""")

cta_cols = st.columns(2)

with cta_cols[0]:
    st.markdown(f"""
    <a href="/Loan_Journey_-_Strong_Applicant" target="_self">
        <div style="background-color: {COLORS['bg_medium']}; padding: 15px; border-radius: 5px; text-align: center; 
                    border-left: 4px solid {COLORS['high_confidence']};">
            <h4 style="color: {COLORS['text_primary']};">Strong Applicant Journey</h4>
            <p style="color: {COLORS['text_secondary']};">See how the digital twin evolves for a strong SaaS company</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

with cta_cols[1]:
    st.markdown(f"""
    <a href="/Loan_Journey_-_Unclear_Applicant" target="_self">
        <div style="background-color: {COLORS['bg_medium']}; padding: 15px; border-radius: 5px; text-align: center;
                    border-left: 4px solid {COLORS['medium_confidence']};">
            <h4 style="color: {COLORS['text_primary']};">Unclear Applicant Journey</h4>
            <p style="color: {COLORS['text_secondary']};">Explore how mixed signals are handled for a manufacturing company</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

# Additional resources
st.markdown("""
## Further Reading

- [Knowledge Graphs: Fundamentals, Techniques, and Applications](https://www.researchgate.net/publication/332123330_Knowledge_Graphs_-_Fundamentals_Techniques_and_Applications)
- [Knowledge Graphs in Natural Language Processing @ACL 2020](https://github.com/kracr/kg-tutorial-acl-2020)
- [A Comprehensive Survey on Knowledge Graph Embeddings](https://arxiv.org/abs/2206.04420)
- [Temporal Knowledge Graphs](https://arxiv.org/abs/2201.08236)
""")