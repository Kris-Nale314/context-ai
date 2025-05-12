# pages/4_Interactive_Graph_Test.py
import streamlit as st
import networkx as nx
from utils.theme import setup_page_config, apply_theme, COLORS
from utils.demo_data import load_applicant_data, generate_all_data
from utils.kg_generator import create_initial_knowledge_graph, create_expanded_knowledge_graph

# Import visualization libraries - handle import errors gracefully
st.set_page_config(page_title="Interactive Graph Test", layout="wide")

# Try to import the required libraries
agraph_available = False
pyvis_available = False

try:
    from streamlit_agraph import agraph, Node, Edge, Config
    agraph_available = True
except ImportError:
    st.warning("Streamlit-Agraph not available. Only PyVis will be tested.")

try:
    from pyvis.network import Network
    import streamlit.components.v1 as components
    import tempfile
    import os
    pyvis_available = True
except ImportError:
    st.warning("PyVis not available. Only Agraph will be tested.")

# Header
st.title("Interactive Knowledge Graph Test")
st.subheader("Testing different interactive graph visualization options")

# Load test data
try:
    applicant_data = load_applicant_data("strong_applicant")
    if not applicant_data:
        st.info("Generating sample data...")
        generate_all_data()
        applicant_data = load_applicant_data("strong_applicant")
    
    company = applicant_data["company_profile"]
    G = create_initial_knowledge_graph(company)
    
    # Let user choose which visualization to test
    viz_options = []
    if agraph_available:
        viz_options.append("Agraph")
    if pyvis_available:
        viz_options.append("PyVis")
    
    if not viz_options:
        st.error("Neither Agraph nor PyVis is available. Please install at least one of them.")
        st.stop()
    
    viz_choice = st.radio("Select visualization to test:", viz_options, horizontal=True)
    
    # Test selected visualization
    st.subheader(f"Testing {viz_choice}")
    
    if viz_choice == "Agraph" and agraph_available:
        # Convert NetworkX graph to Agraph nodes and edges
        nodes = []
        edges = []
        
        # Process nodes
        for node, attrs in G.nodes(data=True):
            # Get attributes with defaults
            size = attrs.get('size', 25)
            color = attrs.get('color', COLORS['node_default'])
            title = attrs.get('title', str(node))
            
            # Create node
            nodes.append(Node(
                id=str(node),
                label=str(node),
                size=size,
                color=color,
                title=title
            ))
        
        # Process edges
        for source, target, attrs in G.edges(data=True):
            # Get attributes with defaults
            width = attrs.get('width', 1)
            color = attrs.get('color', COLORS['edge_default'])
            title = attrs.get('title', '')
            
            # Create edge
            edges.append(Edge(
                source=str(source),
                target=str(target),
                label=title if title else None,
                color=color
            ))
        
        # Create configuration
        config = Config(
            width=None,
            height=600,
            directed=True,
            physics=True,
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False,
            node={'labelProperty': 'label'},
            link={'labelProperty': 'label', 'renderLabel': True}
        )
        
        # Render the graph
        st.write("Try dragging nodes, zooming, and interacting with the graph:")
        agraph(nodes=nodes, edges=edges, config=config)
        
        st.success("Agraph visualization successful!")
    
    elif viz_choice == "PyVis" and pyvis_available:
        # Create PyVis network
        net = Network(height="600px", width="100%", bgcolor=COLORS['bg_dark'], 
                     font_color=COLORS['text_primary'])
        
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
        net.force_atlas_2based(spring_length=200, spring_strength=0.05, damping=0.2)
        net.show_buttons(['physics'])
        
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
        st.write("Try dragging nodes, zooming, and interacting with the graph:")
        components.html(html, height=600)
        
        st.success("PyVis visualization successful!")

except Exception as e:
    st.error(f"Error during visualization test: {e}")
    import traceback
    st.code(traceback.format_exc())