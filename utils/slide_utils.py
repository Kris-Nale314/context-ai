# utils/slide_utils.py
import streamlit as st
import base64
from PIL import Image
import io

def display_slide(slide_path, width=None):
    """Display a slide image with proper styling."""
    st.image(slide_path, width=width)

def display_slide_with_overlay(slide_path, overlay_func=None):
    """Display a slide with interactive overlay elements."""
    # Display the base slide
    st.image(slide_path)
    
    # If there's an overlay function, call it
    if overlay_func and callable(overlay_func):
        overlay_func()

def slide_with_bullet_reveal(slide_path, bullets, key_prefix="bullet"):
    """Display a slide with progressively revealed bullet points."""
    # Display slide
    st.image(slide_path)
    
    # Display bullets with checkboxes
    for i, bullet in enumerate(bullets):
        if st.checkbox(bullet, key=f"{key_prefix}_{i}"):
            st.markdown(f"**{bullet}**")
            if isinstance(bullet, dict) and "details" in bullet:
                st.markdown(bullet["details"])

def slides_as_tabs(slide_paths, tab_names=None):
    """Display multiple slides as tabs."""
    if tab_names is None:
        tab_names = [f"Slide {i+1}" for i in range(len(slide_paths))]
    
    tabs = st.tabs(tab_names)
    
    for i, (tab, slide_path) in enumerate(zip(tabs, slide_paths)):
        with tab:
            st.image(slide_path)

def slide_with_buttons(slide_path, buttons):
    """Display a slide with action buttons below."""
    # Display slide
    st.image(slide_path)
    
    # Create columns for buttons
    cols = st.columns(len(buttons))
    
    # Add buttons
    for i, (col, button) in enumerate(zip(cols, buttons)):
        with col:
            if "action" in button:
                if st.button(button["label"], key=f"slide_btn_{i}"):
                    button["action"]()
            else:
                st.button(button["label"], key=f"slide_btn_{i}")

def slide_with_tabs(slide_path, tabs_content):
    """Display a slide with tabbed content below."""
    # Display slide
    st.image(slide_path)
    
    # Create tabs
    tab_names = list(tabs_content.keys())
    tabs = st.tabs(tab_names)
    
    # Add content to each tab
    for i, tab in enumerate(tabs):
        with tab:
            content = tabs_content[tab_names[i]]
            if callable(content):
                content()
            else:
                st.markdown(content)