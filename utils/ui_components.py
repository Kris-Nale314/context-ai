# utils/ui_components.py (continued)
import streamlit as st
from utils.theme import COLORS, layer_badge

def header_with_logo():
    """Create a header with logo."""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.image("images/logo.png", width=150)
    
    with col2:
        st.markdown("# Context-AI: Interactive Presentation & Demo")
        st.markdown("### Adaptive Intelligence Through Evolving Knowledge Graphs")

def concept_card(title, description, icon=None, layer=None):
    """Create a styled card for concept explanations."""
    # Determine color based on layer
    if layer == "digital_twin":
        color = COLORS['digital_twin']
    elif layer == "temporal":
        color = COLORS['temporal']
    elif layer == "external":
        color = COLORS['external']
    elif layer == "guidance":
        color = COLORS['guidance']
    else:
        color = COLORS['primary']
    
    # Create card with border on left
    st.markdown(f"""
    <div style="border-left: 4px solid {color}; 
                background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px;">
        <h3 style="color: {COLORS['text_primary']}; margin-top: 0;">{title}</h3>
        <p style="color: {COLORS['text_primary']};">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def comparison_card(title, traditional, context_ai):
    """Create a comparison card between traditional and Context-AI approaches."""
    st.markdown(f"""
    <div style="background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px;">
        <h3 style="color: {COLORS['text_primary']}; margin-top: 0;">{title}</h3>
        
        <div style="display: flex; margin-top: 10px;">
            <div style="flex: 1; margin-right: 10px;">
                <h4 style="color: {COLORS['text_secondary']};">Traditional Approach</h4>
                <div style="background-color: {COLORS['bg_dark']}; padding: 10px; border-radius: 4px;">
                    <p style="color: {COLORS['text_primary']};">{traditional}</p>
                </div>
            </div>
            
            <div style="flex: 1; margin-left: 10px;">
                <h4 style="color: {COLORS['primary']};">Context-AI Approach</h4>
                <div style="background-color: {COLORS['bg_dark']}; padding: 10px; border-radius: 4px;">
                    <p style="color: {COLORS['text_primary']};">{context_ai}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def layer_card(layer_name, what_it_is, what_it_does, why_better):
    """Create a card explaining a specific layer of the Context-AI architecture."""
    # Map layer name to color and icon
    layer_colors = {
        "Digital Twin Layer": COLORS['digital_twin'],
        "Temporal Intelligence Layer": COLORS['temporal'],
        "External Integration Layer": COLORS['external'],
        "Adaptive Guidance Layer": COLORS['guidance']
    }
    
    layer_icons = {
        "Digital Twin Layer": "🔄",
        "Temporal Intelligence Layer": "⏱️",
        "External Integration Layer": "🌐",
        "Adaptive Guidance Layer": "🧭"
    }
    
    color = layer_colors.get(layer_name, COLORS['primary'])
    icon = layer_icons.get(layer_name, "")
    
    # Create expandable card for the layer - set expanded to False by default
    with st.expander(f"{icon} {layer_name}", expanded=False):
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"#### What it is")
            st.markdown(f'<div style="border-left: 4px solid {color}; padding-left: 10px;">{what_it_is}</div>', 
                       unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"#### What it does")
            st.markdown(f'<div style="border-left: 4px solid {color}; padding-left: 10px;">{what_it_does}</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"#### Why it's better")
            st.markdown(f'<div style="border-left: 4px solid {color}; padding-left: 10px;">{why_better}</div>', 
                       unsafe_allow_html=True)

def step_progress(steps, current_step, colors=None):
    """Create a step progress indicator."""
    if colors is None:
        colors = {
            "active": COLORS['primary'],
            "completed": COLORS['high_confidence'],
            "incomplete": COLORS['bg_light']
        }
    
    # Create HTML for steps
    html = '<div style="display: flex; justify-content: space-between; margin: 20px 0;">'
    
    for i, step in enumerate(steps):
        # Determine step status
        if i < current_step:
            status = "completed"
            icon = "✓"
        elif i == current_step:
            status = "active"
            icon = str(i+1)
        else:
            status = "incomplete"
            icon = str(i+1)
        
        # Determine color
        color = colors[status]
        
        # Create step indicator
        html += f'''
        <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="width: 30px; height: 30px; background-color: {color}; 
                       border-radius: 50%; display: flex; justify-content: center; 
                       align-items: center; color: white; margin-bottom: 5px;">
                {icon}
            </div>
            <div style="text-align: center; max-width: 100px; 
                       color: {COLORS['text_primary'] if status != 'incomplete' else COLORS['text_muted']}; 
                       font-size: 0.8em;">
                {step}
            </div>
        </div>
        '''
        
        # Add connector if not the last step
        if i < len(steps) - 1:
            connector_color = colors["completed"] if i < current_step else colors["incomplete"]
            html += f'<div style="flex-grow: 1; height: 2px; background-color: {connector_color}; margin-top: 15px;"></div>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def metric_card(title, value, delta=None, description=None):
    """Create a styled metric card."""
    # Determine color based on delta
    if delta is not None:
        try:
            delta_float = float(delta.replace('%', '').replace('+', ''))
            if delta_float > 0:
                delta_color = COLORS['high_confidence']
                delta_prefix = "+"
            elif delta_float < 0:
                delta_color = COLORS['low_confidence']
                delta_prefix = ""
            else:
                delta_color = COLORS['text_secondary']
                delta_prefix = ""
                
            delta_html = f'<span style="color: {delta_color};">{delta_prefix}{delta}</span>'
        except:
            delta_html = f'<span style="color: {COLORS["text_secondary"]};">{delta}</span>'
    else:
        delta_html = ""
    
    # Create card HTML
    st.markdown(f"""
    <div style="background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px; 
                text-align: center;">
        <h4 style="color: {COLORS['text_secondary']}; margin-bottom: 5px; font-size: 0.9em;">{title}</h4>
        <div style="font-size: 1.8em; font-weight: bold; color: {COLORS['text_primary']}; margin-bottom: 5px;">
            {value} {delta_html}
        </div>
        {f'<div style="color: {COLORS["text_muted"]}; font-size: 0.8em;">{description}</div>' if description else ''}
    </div>
    """, unsafe_allow_html=True)

def image_with_caption(image_path, caption=None, width=None):
    """Display an image with optional caption."""
    st.image(image_path, width=width)
    if caption:
        st.caption(caption)

def feature_list(title, features, icon="✓"):
    """Create a styled feature list."""
    st.markdown(f"### {title}")
    
    for feature in features:
        st.markdown(f"""
        <div style="display: flex; margin-bottom: 10px; align-items: flex-start;">
            <div style="color: {COLORS['primary']}; font-size: 1.2em; margin-right: 10px; flex-shrink: 0;">{icon}</div>
            <div style="color: {COLORS['text_primary']};">{feature}</div>
        </div>
        """, unsafe_allow_html=True)

def tabbed_content(tabs_content):
    """Create tabbed content with consistent styling."""
    tab_names = list(tabs_content.keys())
    tabs = st.tabs(tab_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            content = tabs_content[tab_names[i]]
            if callable(content):
                content()
            else:
                st.markdown(content)