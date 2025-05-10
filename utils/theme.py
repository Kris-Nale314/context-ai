# utils/theme.py
import streamlit as st

# Color palette for dark theme
COLORS = {
    # Primary brand colors
    "primary": "#3B82F6",         # Bright blue
    "secondary": "#10B981",       # Emerald green
    "accent": "#F59E0B",          # Amber
    
    # Layer-specific colors
    "digital_twin": "#4F46E5",    # Indigo
    "temporal": "#10B981",        # Emerald
    "external": "#F59E0B",        # Amber
    "guidance": "#EC4899",        # Pink
    
    # Confidence levels
    "high_confidence": "#22C55E", # Green
    "medium_confidence": "#EAB308", # Yellow
    "low_confidence": "#EF4444",  # Red
    
    # Background shades
    "bg_dark": "#0F172A",         # Deep navy
    "bg_medium": "#1E293B",       # Slate
    "bg_light": "#334155",        # Light slate
    
    # Text colors
    "text_primary": "#F8FAFC",    # Very light gray
    "text_secondary": "#CBD5E1",  # Light gray
    "text_muted": "#94A3B8",      # Muted blue-gray
    
    # Graph visualization colors
    "node_default": "#64748B",    # Gray blue
    "edge_default": "#475569",    # Dark gray blue
    "highlight": "#F472B6",       # Pink highlight
}

def setup_page_config():
    """Configure page settings for consistent experience."""
    st.set_page_config(
        page_title="Context-AI: Adaptive Intelligence",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_theme():
    """Apply custom theme styling to the app."""
    st.markdown(f"""
    <style>
        /* Base theme customization */
        .stApp {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_primary']};
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background-color: {COLORS['bg_medium']};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {COLORS['text_primary']};
        }}
        h4, h5, h6 {{
            color: {COLORS['text_secondary']};
        }}
        
        /* Cards and containers */
        .card {{
            background-color: {COLORS['bg_medium']};
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid {COLORS['primary']};
        }}
        
        /* Layer-specific cards */
        .card-digital-twin {{
            border-left: 4px solid {COLORS['digital_twin']};
        }}
        .card-temporal {{
            border-left: 4px solid {COLORS['temporal']};
        }}
        .card-external {{
            border-left: 4px solid {COLORS['external']};
        }}
        .card-guidance {{
            border-left: 4px solid {COLORS['guidance']};
        }}
        
        /* Button styling */
        .stButton button {{
            background-color: {COLORS['primary']};
            color: {COLORS['text_primary']};
            border: none;
            transition: all 0.3s ease;
        }}
        .stButton button:hover {{
            background-color: {COLORS['digital_twin']};
            color: white;
        }}
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
            background-color: {COLORS['bg_medium']};
            border-radius: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {COLORS['bg_medium']};
            color: {COLORS['text_secondary']};
            padding: 10px 20px;
            border-radius: 4px 4px 0 0;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['bg_light']};
            color: {COLORS['text_primary']};
        }}
        
        /* Slider and input widgets */
        .stSlider [data-baseweb="slider"] div::before {{
            background-color: {COLORS['bg_light']};
        }}
        .stSlider [data-baseweb="slider"] div div {{
            background-color: {COLORS['primary']};
        }}
        
        /* Metric styling */
        .stMetric label {{
            color: {COLORS['text_secondary']};
        }}
        .stMetric [data-testid="stMetricValue"] {{
            color: {COLORS['text_primary']};
        }}
    </style>
    """, unsafe_allow_html=True)

def styled_container(title, content, layer=None):
    """Create a styled container with optional layer styling."""
    layer_class = f"card-{layer}" if layer else ""
    
    st.markdown(f"""
    <div class="card {layer_class}">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def layer_badge(layer_name):
    """Create a styled badge for layer identification."""
    layer_colors = {
        "digital_twin": COLORS["digital_twin"],
        "temporal": COLORS["temporal"],
        "external": COLORS["external"],
        "guidance": COLORS["guidance"],
    }
    
    color = layer_colors.get(layer_name.lower().replace(" ", "_"), COLORS["primary"])
    
    st.markdown(f"""
    <div style="display: inline-block; padding: 5px 10px; background-color: {color}; 
                border-radius: 15px; color: white; font-size: 0.8em; margin-right: 10px;">
        {layer_name}
    </div>
    """, unsafe_allow_html=True)