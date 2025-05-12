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
        <img src="https://raw.githubusercontent.com/Kris-Nale314/context-ai/main/images/kgBasics2.gif" width="1000">
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
