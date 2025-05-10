# utils/graph_viz.py
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
from utils.theme import COLORS

def create_pyvis_graph(G, height=500, width=None, notebook=False, 
                       bgcolor=COLORS['bg_dark'], font_color=COLORS['text_primary']):
    """Convert NetworkX graph to PyVis interactive visualization."""
    if width is None:
        width = "100%"
    
    # Create PyVis network
    net = Network(height=f"{height}px", width=width, notebook=notebook, 
                 bgcolor=bgcolor, font_color=font_color)
    
    # Copy node attributes from NetworkX
    for node, node_attrs in G.nodes(data=True):
        size = node_attrs.get('size', 25)
        title = node_attrs.get('title', str(node))
        color = node_attrs.get('color', COLORS['node_default'])
        shape = node_attrs.get('shape', 'dot')
        
        net.add_node(str(node), title=title, color=color, size=size, shape=shape, label=str(node))
    
    # Copy edge attributes from NetworkX
    for source, target, edge_attrs in G.edges(data=True):
        width = edge_attrs.get('width', 1)
        color = edge_attrs.get('color', COLORS['edge_default'])
        title = edge_attrs.get('title', '')
        
        net.add_edge(str(source), str(target), width=width, color=color, title=title)
    
    # Apply physics layout options
    net.toggle_physics(True)
    net.barnes_hut(spring_length=200, spring_strength=0.01, damping=0.09)
    
    # Save and read graph as HTML
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp:
        path = temp.name
        net.save_graph(path)
    
    # Load HTML into a string
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Clean up temporary file
    try:
        os.unlink(path)
    except:
        pass
    
    # Return HTML component
    return components.html(html, height=height, width=width)

# In utils/graph_viz.py, update the simplified_graph_viz function:

def simplified_graph_viz(G, height=500, width=700):
    """Create a simplified graph visualization using Plotly.
    Use this as a fallback if PyVis has issues."""
    
    # Create a spring layout
    pos = nx.spring_layout(G, seed=42)
    
    # Create edge traces
    edge_traces = []
    for edge in G.edges(data=True):
        source, target = edge[0], edge[1]
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        
        width = edge[2].get('width', 1)
        color = edge[2].get('color', COLORS['edge_default'])
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=width, color=color),
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_x = []
    node_y = []
    node_colors = []
    node_sizes = []
    node_text = []
    node_labels = []
    
    for node, attrs in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Get node attributes
        color = attrs.get('color', COLORS['node_default'])
        size = attrs.get('size', 15)
        title = attrs.get('title', str(node))
        
        node_colors.append(color)
        node_sizes.append(size)
        node_text.append(title)
        
        # Create shorter labels for readability
        label = str(node)
        if len(label) > 20:
            label = label[:18] + "..."
        node_labels.append(label)
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_sizes,
            line=dict(width=1, color=COLORS['bg_medium'])
        ),
        text=node_labels,
        hovertext=node_text,
        hoverinfo='text'
    )
    
    # Create separate trace for text labels
    text_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='text',
        text=node_labels,
        textposition="bottom center",
        textfont=dict(
            color=COLORS['text_primary'],
            size=10
        ),
        hoverinfo='none'
    )
    
    # Create figure
    fig = go.Figure(
        data=edge_traces + [node_trace, text_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=width,
            height=height,
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_dark'],
            font=dict(color=COLORS['text_primary'])
        )
    )
    
    # Add title
    fig.update_layout(title="Knowledge Graph Visualization")
    
    return st.plotly_chart(fig, use_container_width=True)

    
def display_knowledge_graph(G, height=500, width=None, use_fallback=False):
    """
    Display a knowledge graph with a fallback option.
    
    Args:
        G: NetworkX graph object
        height: Height of the visualization in pixels
        width: Width of the visualization (or None for full width)
        use_fallback: If True, use Plotly fallback visualization
    """
    if use_fallback:
        return simplified_graph_viz(G, height, width or 700)
    
    try:
        return create_pyvis_graph(G, height, width)
    except Exception as e:
        st.warning(f"PyVis visualization failed. Using fallback visualization. Error: {e}")
        return simplified_graph_viz(G, height, width or 700)

# Add this function to utils/graph_viz.py

def networkx_matplotlib_graph(G, height=500, width=700):
    """
    Create a knowledge graph visualization using NetworkX and Matplotlib.
    This is a very reliable fallback visualization method.
    """
    import matplotlib.pyplot as plt
    import io
    from PIL import Image
    
    # Create figure with the right background color
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#0F172A')  # Dark background
    ax.set_facecolor('#0F172A')  # Dark background
    
    # Create a spring layout
    pos = nx.spring_layout(G, seed=42)
    
    # Collect node attributes
    node_sizes = []
    node_colors = []
    
    for node in G.nodes():
        # Get size or use default
        size = G.nodes[node].get('size', 15)
        node_sizes.append(size * 20)  # Scale up for matplotlib
        
        # Get color or use default
        color = G.nodes[node].get('color', COLORS['node_default'])
        node_colors.append(color)
    
    # Collect edge attributes
    edge_widths = []
    edge_colors = []
    
    for u, v, data in G.edges(data=True):
        # Get width or use default
        width = data.get('width', 1)
        edge_widths.append(width)
        
        # Get color or use default
        color = data.get('color', COLORS['edge_default'])
        edge_colors.append(color)
    
    # Draw the edges
    nx.draw_networkx_edges(
        G, pos, 
        width=edge_widths,
        edge_color=edge_colors,
        alpha=0.7
    )
    
    # Draw the nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9
    )
    
    # Add labels with white text
    labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(
        G, pos,
        labels=labels,
        font_size=8,
        font_color='white'
    )
    
    # Turn off axis
    plt.axis('off')
    
    # Save to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Display the image
    plt.close(fig)  # Close the figure to free memory
    image = Image.open(buf)
    st.image(image, use_container_width=True)
    
    return