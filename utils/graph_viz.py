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
        title = node_attrs.get('title', node)
        color = node_attrs.get('color', COLORS['node_default'])
        shape = node_attrs.get('shape', 'dot')
        
        net.add_node(node, title=title, color=color, size=size, shape=shape, label=str(node))
    
    # Copy edge attributes from NetworkX
    for source, target, edge_attrs in G.edges(data=True):
        width = edge_attrs.get('width', 1)
        color = edge_attrs.get('color', COLORS['edge_default'])
        title = edge_attrs.get('title', '')
        
        net.add_edge(source, target, width=width, color=color, title=title)
    
    # Apply physics layout options
    net.toggle_physics(True)
    net.barnes_hut(spring_length=200, spring_strength=0.01, damping=0.09)
    
    # Generate HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp:
        path = temp.name
        net.save_graph(path)
    
    # Display in Streamlit
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    components.html(html, height=height, width=width)
    
    # Clean up temp file
    try:
        os.unlink(path)
    except:
        pass

def create_plotly_graph(G, layout=None, width=None, height=600):
    """Create a Plotly-based graph visualization."""
    if layout is None:
        layout = nx.spring_layout(G, seed=42)
    
    # Extract node positions
    pos = layout
    
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
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=[],
            line=dict(width=2)))
    
    # Add node positions and attributes
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        
        # Node styling
        size = G.nodes[node].get('size', 15)
        color = G.nodes[node].get('color', COLORS['node_default'])
        title = G.nodes[node].get('title', str(node))
        
        node_trace['marker']['size'] += (size,)
        node_trace['marker']['color'] += (color,)
        node_trace['text'] += (title,)
    
    # Create figure
    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=5, l=5, r=5, t=5),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=width,
            height=height,
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_dark'],
        )
    )
    
    return fig

def temporal_graph_explorer(time_points, graph_generator_func, height=500):
    """Create an interactive temporal graph explorer."""
    # Time point selection
    selected_time = st.select_slider(
        "Move through time:",
        options=time_points
    )
    
    # Generate graph for selected time
    G = graph_generator_func(selected_time)
    
    # Display the graph
    create_pyvis_graph(G, height=height)
    
    return selected_time, G