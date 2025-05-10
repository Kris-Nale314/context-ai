# utils/signal_viz.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import COLORS
import random

def create_single_signal(name, data=None, points=100, amplitude=0.5, 
                         frequency=0.1, noise=0.05, phase=0):
    """Create a single signal visualization."""
    if data is None:
        # Generate synthetic data if not provided
        x = np.linspace(0, 10, points)
        y = amplitude * np.sin(frequency * x * np.pi + phase)
        y += np.random.normal(0, noise, points)
        data = pd.DataFrame({'x': x, 'y': y})
    
    # Create figure
    fig = px.line(data, x='x', y='y', title=name)
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        margin=dict(l=10, r=10, t=40, b=10),
        height=150,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1, 1]
        )
    )
    
    # Update line color
    fig.update_traces(line_color=COLORS['primary'])
    
    return fig

def create_combined_signal(signals, base_amplitudes=None, points=100):
    """Create a visualization of combined signals."""
    if not signals:
        return None, 0
    
    if base_amplitudes is None:
        # Generate random but consistent amplitudes
        random.seed(42)
        base_amplitudes = {name: random.uniform(0.2, 0.5) for name in signals}
    
    x = np.linspace(0, 10, points)
    combined_y = np.zeros(points)
    
    # Add each signal
    for name in signals:
        amplitude = base_amplitudes.get(name, 0.3)
        frequency = random.uniform(0.05, 0.2)
        phase = random.uniform(0, 2*np.pi)
        
        component = amplitude * np.sin(frequency * x * np.pi + phase)
        combined_y += component
    
    # Scale combined signal
    max_val = max(1.0, np.max(np.abs(combined_y)))
    combined_y = combined_y / max_val
    
    # Calculate strength based on number of signals
    strength = min(0.95, 0.3 + (len(signals) * 0.1))
    
    # Apply amplification based on strength
    amplification = 0.4 + (strength * 0.6)
    combined_y *= amplification
    
    # Create dataframe
    df = pd.DataFrame({'x': x, 'y': combined_y})
    
    # Create figure
    fig = go.Figure()
    
    # Add signal line
    fig.add_trace(go.Scatter(
        x=df['x'],
        y=df['y'],
        mode='lines',
        line=dict(
            color=COLORS['primary'],
            width=3
        ),
        name='Combined Signal'
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Combined Signal (Strength: {strength:.2f})",
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['bg_light'],
            zeroline=True,
            zerolinecolor=COLORS['bg_light'],
            showticklabels=True,
            range=[-1, 1]
        )
    )
    
    # Add background color based on strength
    if strength > 0.7:
        bg_color = "rgba(34, 197, 94, 0.1)"  # Green with low opacity
    elif strength > 0.5:
        bg_color = "rgba(234, 179, 8, 0.1)"  # Yellow with low opacity
    else:
        bg_color = "rgba(239, 68, 68, 0.1)"  # Red with low opacity
    
    fig.add_shape(
        type="rect",
        x0=0, y0=-1,
        x1=10, y1=1,
        fillcolor=bg_color,
        line=dict(width=0),
        layer="below"
    )
    
    return fig, strength

def signal_strength_meter(strength, height=100):
    """Create a visual meter for signal strength."""
    # Determine color based on strength
    if strength > 0.7:
        color = COLORS['high_confidence']
        label = "Strong Signal"
    elif strength > 0.5:
        color = COLORS['medium_confidence']
        label = "Moderate Signal"
    else:
        color = COLORS['low_confidence']
        label = "Weak Signal"
    
    # Create figure
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=strength * 100,
        number={'suffix': "%", 'font': {'color': COLORS['text_primary']}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': COLORS['text_secondary']},
            'bar': {'color': color},
            'bgcolor': COLORS['bg_light'],
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [50, 70], 'color': 'rgba(234, 179, 8, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(34, 197, 94, 0.3)'}
            ],
        },
        title={'text': label, 'font': {'color': COLORS['text_primary']}}
    ))
    
    # Update layout
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        height=height,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    
    return fig

def signal_amplification_demo(signal_groups):
    """Create a complete signal amplification demonstration."""
    st.write("### Signal Amplification: Converting Weak Signals into Strong Insights")
    
    st.write("""
    One of the most powerful aspects of Context-AI is its ability to detect and amplify 
    signals that would be too weak to trigger action individually. By combining multiple 
    weak signals through their connections in the knowledge graph, we can identify emerging 
    risks and opportunities much earlier.
    """)
    
    # Create columns for signal selection
    columns = st.columns(len(signal_groups))
    
    # Track selected signals
    selected_signals = []
    
    # Create checkboxes for each signal group
    for i, (group_name, signals) in enumerate(signal_groups.items()):
        with columns[i]:
            st.write(f"#### {group_name}")
            for signal in signals:
                if st.checkbox(signal, key=f"signal_{signal}"):
                    selected_signals.append(signal)
    
    # Display individual signals if selected
    if selected_signals:
        st.write("### Individual Signals")
        signal_cols = st.columns(min(3, len(selected_signals)))
        
        for i, signal in enumerate(selected_signals):
            with signal_cols[i % len(signal_cols)]:
                fig = create_single_signal(signal)
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Weak signal on its own")
    
    # Display combined signal
    st.write("### Combined Signal Effect")
    
    if not selected_signals:
        st.info("Select signals above to see how they combine into a stronger indicator.")
    else:
        # Create combined signal visualization
        combined_fig, strength = create_combined_signal(selected_signals)
        st.plotly_chart(combined_fig, use_container_width=True)
        
        # Display strength meter
        meter_fig = signal_strength_meter(strength)
        st.plotly_chart(meter_fig, use_container_width=True)
        
        # Provide interpretation based on strength
        if strength > 0.7:
            st.success(f"🚨 **Strong Signal Detected**: The combination of {len(selected_signals)} signals creates a strong indicator of potential risk or opportunity that requires attention.")
        elif strength > 0.5:
            st.warning(f"⚠️ **Moderate Signal Detected**: These {len(selected_signals)} signals together suggest an emerging pattern that should be monitored closely.")
        else:
            st.info(f"ℹ️ **Weak Signal Detected**: The current combination of {len(selected_signals)} signals indicates a potential pattern, but more corroborating evidence would be helpful.")
    
    return selected_signals