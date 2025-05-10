# utils/state.py
import streamlit as st

def init_session_state(defaults=None):
    """Initialize session state variables with defaults."""
    if defaults is None:
        defaults = {}
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_state(key, default=None):
    """Get a session state variable with default fallback."""
    return st.session_state.get(key, default)

def set_state(key, value):
    """Set a session state variable."""
    st.session_state[key] = value

def increment_state(key, step=1, min_value=None, max_value=None):
    """Increment a numeric session state variable."""
    if key not in st.session_state:
        st.session_state[key] = 0
    
    new_value = st.session_state[key] + step
    
    if min_value is not None:
        new_value = max(min_value, new_value)
    
    if max_value is not None:
        new_value = min(max_value, new_value)
    
    st.session_state[key] = new_value
    
    return new_value

def toggle_state(key):
    """Toggle a boolean session state variable."""
    if key not in st.session_state:
        st.session_state[key] = False
    
    st.session_state[key] = not st.session_state[key]
    
    return st.session_state[key]

def track_page_flow(pages, current_page=None):
    """Track and manage multi-page flow."""
    # Initialize if needed
    if 'page_index' not in st.session_state:
        st.session_state.page_index = 0
    
    # Update current page if specified
    if current_page is not None and current_page in pages:
        st.session_state.page_index = pages.index(current_page)
    
    # Navigation functions
    def next_page():
        if st.session_state.page_index < len(pages) - 1:
            st.session_state.page_index += 1
            st.experimental_rerun()
    
    def prev_page():
        if st.session_state.page_index > 0:
            st.session_state.page_index -= 1
            st.experimental_rerun()
    
    def goto_page(page_name):
        if page_name in pages:
            st.session_state.page_index = pages.index(page_name)
            st.experimental_rerun()
    
    # Current page info
    current_index = st.session_state.page_index
    current_page = pages[current_index]
    is_first = current_index == 0
    is_last = current_index == len(pages) - 1
    
    return {
        'current_page': current_page,
        'is_first': is_first,
        'is_last': is_last,
        'next_page': next_page,
        'prev_page': prev_page,
        'goto_page': goto_page
    }