# pages/external_integration.py
import streamlit as st
from utils.theme import apply_theme, COLORS
from utils.ui_components import header_with_logo, concept_card, comparison_card
from utils.context_viz import context_integration_demo
from utils.state import init_session_state, get_state, set_state

# Set up page
st.set_page_config(
    page_title="External Integration Layer - Context-AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_theme()

# Header
header_with_logo()

# Page content
st.title("🌐 External Integration Layer")

st.markdown("""
## Connecting Entities to Their World

The External Integration Layer connects each digital twin to its broader context, including market 
conditions, industry trends, news events, and regulatory changes. This creates a more complete 
picture than internal data alone can provide.
""")

# Explanation of concept
concept_card(
    "Why External Context Matters",
    """
    In traditional systems, entities exist in isolation - evaluated only on their internal attributes. 
    But real-world entities are deeply influenced by their environment. A manufacturing company's 
    risk profile is affected by industry trends, supply chain disruptions, and economic shifts.
    The External Integration Layer ensures this critical context is part of the decision process.
    """,
    layer="external"
)

# Comparison with traditional approach
comparison_card(
    "Traditional vs. Context-Aware Assessment",
    """
    Relies on the information directly provided by or about the entity itself, with perhaps
    some manual annotation by analysts about broader context. External factors are often
    considered informally or inconsistently.
    """,
    """
    Automatically connects entities to relevant external context from multiple sources,
    weighing information by source reliability and relevance. This creates a complete
    picture that accounts for the environment the entity operates in.
    """
)

# Explain the concept of signal amplification
st.markdown("""
## Signal Amplification: The Power of Context

One of the most important capabilities enabled by external context integration is **signal amplification**. 
Multiple weak signals from different sources, when properly connected, can combine to create 
a strong predictive signal that would be missed when looking at any single data point.

For example, earnings call comments from major manufacturers about supply challenges, combined with 
shipping container cost increases, and news of a regional government policy change, might together 
indicate a significant risk for a small manufacturer seeking a loan - even though any single 
signal might be too weak to notice.
""")

# Interactive demo
st.markdown("""
## External Context Integration Demo

Explore how external context integration works by toggling different context sources and 
seeing how they affect the knowledge graph and risk assessment.
""")

# Run the demo from the utility
active_sources = context_integration_demo()

# Explain the connection to other layers
st.markdown("""
## How External Integration Connects with Other Layers

The External Integration Layer works together with the other platform layers:

1. It enriches the **Digital Twin Layer** with relevant external context
2. It tracks changes in external factors through the **Temporal Intelligence Layer**
3. It provides critical environmental information to the **Adaptive Guidance Layer**

By connecting internal and external information, we create a comprehensive view that enables 
more accurate, context-aware recommendations.
""")

# Key integration points examples
st.markdown("""
## Key External Integration Sources for Loan Assessment

For loan applications, some particularly valuable external context sources include:

### Earnings Call Intelligence
Analyzing earnings calls from publicly traded companies in the same sector can reveal emerging 
challenges or opportunities that could impact the loan applicant. For example, if multiple 
industry leaders mention supply chain disruptions, this could be an early warning signal 
for smaller companies in the same industry.

### News Event Monitoring
Processing news about regional economic conditions, regulatory changes, or market shifts 
that could affect the applicant's operations. For instance, news of a major employer 
leaving a region might indicate increased risk for service businesses in that area.

### Competitive Landscape Changes
Identifying new market entrants, technology disruptions, or business model innovations 
in the applicant's space that could present either threats or opportunities. This helps 
anticipate how the competitive environment might evolve during the loan term.
""")

# Next steps
st.markdown("## Next Steps")

col1, col2 = st.columns(2)

with col1:
    if st.button("Learn About Adaptive Guidance", key="btn_guidance"):
        st.switch_page("pages/adaptive_guidance_layer.py")

with col2:
    if st.button("Experience the Loan Journey Demo", key="btn_journey"):
        st.switch_page("pages/loan_journey_demo.py")