# utils/temporal_viz.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.theme import COLORS

def create_entity_timeline(data, entity_column='entity', 
                          time_column='date', 
                          event_column='event',
                          category_column=None,
                          height=400):
    """Create a timeline visualization for entity evolution."""
    # Convert to DataFrame if list of dicts
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # Create figure
    if category_column and category_column in df.columns:
        fig = px.timeline(df, x_start=time_column, x_end=time_column, 
                         y=entity_column, color=category_column,
                         hover_name=event_column, height=height)
    else:
        fig = px.timeline(df, x_start=time_column, x_end=time_column, 
                         y=entity_column, hover_name=event_column, 
                         height=height)
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="Entity Evolution Timeline",
        xaxis_title="Time",
        yaxis_title="Entity",
    )
    
    # Update marker colors if no category
    if not category_column or category_column not in df.columns:
        fig.update_traces(marker_color=COLORS['primary'])
    
    return fig

def create_confidence_evolution(data, time_column='date', 
                               metrics=None, height=400):
    """Create a visualization of confidence evolution over time."""
    # Convert to DataFrame if list of dicts
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # If metrics not specified, use all numeric columns except time
    if metrics is None:
        metrics = [col for col in df.columns 
                  if col != time_column and pd.api.types.is_numeric_dtype(df[col])]
    
    # Create figure
    fig = go.Figure()
    
    # Add a line for each metric
    for metric in metrics:
        fig.add_trace(go.Scatter(
            x=df[time_column],
            y=df[metric],
            mode='lines+markers',
            name=metric,
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="Confidence Evolution Over Time",
        xaxis_title="Time",
        yaxis_title="Confidence Score",
        height=height,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            gridcolor=COLORS['bg_light'],
            range=[0, 1]
        ),
        xaxis=dict(
            gridcolor=COLORS['bg_light']
        )
    )
    
    return fig

def create_version_chain_visualization(versions, height=400):
    """Create a visualization of entity version chains."""
    # Create a dataframe for the versions
    df = pd.DataFrame(versions)
    
    # Ensure required columns exist
    required_cols = ['version', 'valid_from', 'confidence']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Version data must include '{col}' column")
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for version validity periods
    for i, row in df.iterrows():
        # Extract data
        version = row['version']
        start = row['valid_from']
        end = row.get('valid_to', datetime.now())
        confidence = row.get('confidence', 0.5)
        
        # Determine color based on confidence
        if confidence >= 0.8:
            color = COLORS['high_confidence']
        elif confidence >= 0.5:
            color = COLORS['medium_confidence']
        else:
            color = COLORS['low_confidence']
        
        # Add bar
        fig.add_trace(go.Bar(
            x=[end - start],
            y=[version],
            orientation='h',
            marker_color=color,
            base=start,
            hovertemplate='<b>%{y}</b><br>From: %{base}<br>To: %{x}<br>Confidence: ' + f"{confidence:.2f}",
            name=version
        ))
    
    # Add connections between versions
    if 'next_version' in df.columns:
        for i, row in df.iterrows():
            if not pd.isna(row['next_version']):
                next_ver = row['next_version']
                next_row = df[df['version'] == next_ver].iloc[0]
                
                fig.add_trace(go.Scatter(
                    x=[row.get('valid_to', datetime.now()), next_row['valid_from']],
                    y=[row['version'], next_ver],
                    mode='lines',
                    line=dict(color=COLORS['edge_default'], width=2, dash='dot'),
                    showlegend=False
                ))
    
    # Update layout for dark theme
    fig.update_layout(
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],
        font_color=COLORS['text_primary'],
        title="Entity Version Chain",
        xaxis_title="Time",
        yaxis_title="Version",
        height=height,
        xaxis=dict(
            gridcolor=COLORS['bg_light'],
            type='date'
        ),
        yaxis=dict(
            gridcolor=COLORS['bg_light'],
            autorange="reversed"  # Newest version at top
        ),
        barmode='overlay'
    )
    
    return fig

def temporal_explorer(time_points, data_generator_func, height=400):
    """Create an interactive temporal data explorer."""
    # Time point selection
    selected_time = st.select_slider(
        "Move through time:",
        options=time_points
    )
    
    # Generate data for selected time
    data = data_generator_func(selected_time)
    
    # Display the visualization
    if isinstance(data, tuple) and len(data) == 2:
        fig, events = data
        st.plotly_chart(fig, use_container_width=True)
        
        # Display events up to this point
        if events:
            st.write("### Key Events")
            for event in events:
                event_time = event.get('time', event.get('date', None))
                event_type = event.get('type', event.get('category', 'info'))
                event_desc = event.get('description', event.get('event', ''))
                
                if event_type == 'positive' or event_type == 'success':
                    st.success(f"✅ **{event_time}**: {event_desc}")
                elif event_type == 'negative' or event_type == 'error':
                    st.error(f"❌ **{event_time}**: {event_desc}")
                elif event_type == 'warning':
                    st.warning(f"⚠️ **{event_time}**: {event_desc}")
                else:
                    st.info(f"ℹ️ **{event_time}**: {event_desc}")
    else:
        st.plotly_chart(data, use_container_width=True)
    
    return selected_time