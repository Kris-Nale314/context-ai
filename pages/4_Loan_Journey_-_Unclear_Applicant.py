# pages/2_Loan_Journey_-_Unclear_Applicant.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.theme import setup_page_config, apply_theme, COLORS
from utils.ui_components import header_with_logo, step_progress, concept_card, metric_card
from utils.state import init_session_state, get_state, set_state
from utils.demo_data import load_applicant_data, generate_all_data
from utils.kg_generator import get_graph_for_stage
from utils.graph_viz import networkx_matplotlib_graph

# Set up page config and theme
setup_page_config()
apply_theme()

# Initialize session state for journey navigation
init_session_state({
    "journey_stage": 0  # Start at first stage
})

# Header
header_with_logo()

# Check if data exists, generate if needed
try:
    # Try to load the data
    applicant_data = load_applicant_data("unclear_applicant")
    if not applicant_data:
        st.info("Generating sample data...")
        generate_all_data()
        applicant_data = load_applicant_data("unclear_applicant")
except Exception as e:
    st.error(f"Error loading data: {e}")
    if st.button("Generate Sample Data"):
        generate_all_data()
        st.rerun()
    st.stop()

# Get company profile and other data
company = applicant_data["company_profile"]
financial_data = applicant_data["financial_data"]
risk_scores = applicant_data["risk_scores"]
events = applicant_data["events"]
kg_data = applicant_data["knowledge_graphs"]
journey_stages = kg_data["stages"]

# Get current stage based on session state
current_stage_idx = st.session_state.journey_stage
current_stage = journey_stages[current_stage_idx]

# Main content
st.title(f"Loan Journey: {company['name']}")
st.subheader("An Unclear Applicant Scenario")

# Company overview card
st.markdown(f"""
<div style="border-left: 4px solid {COLORS['medium_confidence']}; 
            background-color: {COLORS['bg_medium']}; 
            border-radius: 4px; 
            padding: 15px; 
            margin-bottom: 15px;">
    <h3 style="color: {COLORS['text_primary']}; margin-top: 0;">{company['name']}</h3>
    <div style="display: flex; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 200px;">
            <p><strong>Industry:</strong> {company['industry']}<br>
            <strong>Years in Business:</strong> {company['years_in_business']}<br>
            <strong>Employees:</strong> {company['employees']}<br>
            <strong>Location:</strong> {company['location']}</p>
        </div>
        <div style="flex: 1; min-width: 200px;">
            <p><strong>Loan Request:</strong> ${company['loan_amount_requested']:,}<br>
            <strong>Purpose:</strong> {company['loan_purpose']}<br>
            <strong>Term:</strong> {company['loan_term_requested']} years<br>
            <strong>Collateral:</strong> {company['collateral_offered']}</p>
        </div>
    </div>
    <p><strong>Description:</strong> {company['description']}</p>
</div>
""", unsafe_allow_html=True)

# Progress tracker
step_progress(journey_stages, current_stage_idx)

# Stage-specific content
st.header(f"Stage: {current_stage}")

# For demo purposes, map stages to data points
stage_to_index = {
    "Initial Application": 0,
    "Information Gathering": 2,
    "Risk Assessment": 5,
    "Decision Point": 8,
    "Monitoring Phase": 11
}

current_index = min(stage_to_index.get(current_stage, 0), len(financial_data) - 1)

# Create columns for key metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "Revenue", 
        f"${financial_data['revenue'][current_index]:,.0f}", 
        f"+{((financial_data['revenue'][current_index] / financial_data['revenue'][0]) - 1) * 100:.1f}%" if current_index > 0 else None,
        "Monthly"
    )

with col2:
    metric_card(
        "Profit Margin", 
        f"{financial_data['profit_margin'][current_index] * 100:.1f}%", 
        f"{((financial_data['profit_margin'][current_index] / financial_data['profit_margin'][0]) - 1) * 100:.1f}%" if current_index > 0 else None
    )

with col3:
    metric_card(
        "Risk Score", 
        f"{risk_scores['risk_score'][current_index]:.2f}", 
        f"{(risk_scores['risk_score'][current_index] - risk_scores['risk_score'][0]) * 100:.1f}%" if current_index > 0 else None
    )

with col4:
    metric_card(
        "Confidence", 
        f"{risk_scores['confidence_score'][current_index]:.2f}", 
        f"+{(risk_scores['confidence_score'][current_index] - risk_scores['confidence_score'][0]) * 100:.1f}%" if current_index > 0 else None
    )

# Generate appropriate knowledge graph based on stage
st.subheader(f"Digital Twin{': Initial Knowledge Graph' if current_stage == 'Initial Application' else ''}")

# Add debug toggle option
debug_mode = st.checkbox("Debug Mode", value=False, key="debug_toggle")
if debug_mode:
    st.write("Current Stage:", current_stage)
    st.write("Current Index:", current_index)
    
    # Show basic graph info
    st.write(f"Graph contains nodes and edges.")

# Get the appropriate graph for the current stage
G = get_graph_for_stage(applicant_data, current_stage, stage_to_index)

# Display the graph with NetworkX
try:
    networkx_matplotlib_graph(G, height=500)
except Exception as e:
    st.error(f"Error displaying graph: {e}")
    # If visualization fails, show basic graph info
    st.write(f"Graph contains {len(G.nodes)} nodes and {len(G.edges)} edges.")
    st.write("Node list:", list(G.nodes))

# Display stage-specific content
if current_stage == "Initial Application":
    # Context-AI layer explanation for this stage
    concept_card(
        "Digital Twin Layer in Action",
        """
        The Digital Twin Layer creates a knowledge graph representation of the loan application 
        with all its initial relationships. Notice how this manufacturing company's profile 
        connects to its industry context, physical assets, and established history. Even at this
        early stage, the knowledge graph begins to reveal the complex relationships that will
        influence risk assessment.
        """,
        layer="digital_twin"
    )
    
    # Show next best information recommendations
    st.subheader("Adaptive Guidance: Next Best Information")
    
    next_info = applicant_data["next_best_information"][current_stage]
    
    # Sort by value
    sorted_info = {k: v for k, v in sorted(next_info.items(), key=lambda item: item[1], reverse=True)}
    
    # Create columns for information value
    cols = st.columns(min(3, len(sorted_info)))
    
    for i, (info, value) in enumerate(sorted_info.items()):
        with cols[i % len(cols)]:
            st.markdown(f"**{info}**")
            st.progress(value)
            st.caption(f"Value: {value:.2f}")

elif current_stage == "Information Gathering":
    # Show customer concentration concern
    concept_card(
        "Digital Twin + Signal Detection",
        """
        As more information is gathered, the knowledge graph reveals a potential risk signal:
        28% of revenue comes from a single customer. This concentration risk might not be 
        flagged in traditional systems that treat customer data as isolated records rather 
        than relationships. The knowledge graph makes this connection explicit and quantifiable.
        """,
        layer="digital_twin"
    )
    
    # Customer concentration card
    st.markdown(f"""
    <div style="border-left: 4px solid {COLORS['medium_confidence']}; 
                background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px;">
        <h3 style="color: {COLORS['text_primary']}; margin-top: 0;">Customer Concentration Risk</h3>
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="background: linear-gradient(to right, {COLORS['medium_confidence']} 28%, {COLORS['bg_light']} 28%); 
                        height: 20px; 
                        width: 100%; 
                        border-radius: 4px; 
                        margin-right: 10px;"></div>
        </div>
        <p>Largest customer accounts for <strong>28%</strong> of total revenue</p>
        <p>Industry standard recommends maximum concentration of <strong>20%</strong> for manufacturing businesses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show manufacturing metrics
    st.subheader("Industry-Specific Metrics")
    
    # Create columns for manufacturing metrics
    cols = st.columns(3)
    
    with cols[0]:
        metric_card(
            "Raw Material Costs", 
            f"${financial_data['raw_material_costs'][current_index]:,.0f}", 
            f"+{((financial_data['raw_material_costs'][current_index] / financial_data['raw_material_costs'][0]) - 1) * 100:.1f}%"
            if current_index > 0 else None,
            "Monthly"
        )
    
    with cols[1]:
        metric_card(
            "Capacity Utilization", 
            f"{financial_data['capacity_utilization'][current_index] * 100:.1f}%", 
            f"{((financial_data['capacity_utilization'][current_index] / financial_data['capacity_utilization'][0]) - 1) * 100:.1f}%"
            if current_index > 0 else None
        )
    
    with cols[2]:
        metric_card(
            "Order Backlog", 
            f"${financial_data['order_backlog'][current_index]:,.0f}", 
            f"{((financial_data['order_backlog'][current_index] / financial_data['order_backlog'][0]) - 1) * 100:.1f}%"
            if current_index > 0 else None
        )

elif current_stage == "Risk Assessment":
    # Show external context integration
    concept_card(
        "External Integration Layer",
        """
        The External Integration layer reveals concerning signals in the manufacturing supply chain 
        that could impact the applicant's operations. When combined with the customer concentration 
        risk, these external factors create a more nuanced risk picture than would be visible from 
        internal data alone.
        """,
        layer="external"
    )
    
    # Display external context
    st.subheader("External Context Integration")
    
    # Get active context sources
    context_data = applicant_data["external_context"]
    active_sources = {k: v for k, v in context_data.items() if v.get("active", False)}
    
    # Create context impact visualization
    context_impacts = {}
    for source, data in active_sources.items():
        impact = data.get("impact", 0)
        context_impacts[source] = impact
    
    # Show external context impacts
    cols = st.columns(len(context_impacts))
    
    for i, (source, impact) in enumerate(context_impacts.items()):
        with cols[i]:
            # Determine color based on impact (positive or negative)
            color = COLORS['high_confidence'] if impact > 0 else COLORS['low_confidence']
            
            st.markdown(f"""
            <div style="background-color: {COLORS['bg_medium']}; 
                        border-radius: 4px; padding: 10px; text-align: center;
                        border-left: 4px solid {color};">
                <h4 style="margin: 0;">{source}</h4>
                <p style="font-size: 1.5em; margin: 5px 0; color: {color};">{impact:+.2f}</p>
                <p style="margin: 0; color: {COLORS['text_secondary']};">
                    Impact on Risk Assessment
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show signal amplification
    st.subheader("Signal Amplification")
    
    st.markdown("""
    Multiple signals from different sources combine to reveal a mixed risk profile:
    """)
    
    # Create columns for signals
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("**Internal Signals**")
        st.success("✅ Stable business - 12 years history")
        st.warning("⚠️ Customer concentration risk (28%)")
        st.success("✅ Experienced management team")
    
    with cols[1]:
        st.markdown("**Industry Signals**")
        st.error("❌ Supply chain disruptions")
        st.warning("⚠️ Rising raw material costs")
        st.success("✅ Equipment modernization opportunity")
    
    with cols[2]:
        st.markdown("**Economic Signals**")
        st.warning("⚠️ Interest rates trending up")
        st.warning("⚠️ Transportation disruptions")
        st.success("✅ Manufacturing reshoring trend")

elif current_stage == "Decision Point":
    # Show conditional approval recommendation
    concept_card(
        "Adaptive Guidance Layer",
        """
        Based on the mixed signal profile, the Adaptive Guidance layer recommends a 
        conditional approval with specific terms designed to mitigate the identified risks. 
        Unlike traditional systems that might simply adjust the interest rate or decline 
        the application, Context-AI provides tailored recommendations that address the 
        specific risk factors identified in the knowledge graph.
        """,
        layer="guidance"
    )
    
    # Show recommendation
    st.subheader("Loan Assessment Recommendation")
    
    # Get reasoning data
    reasoning = applicant_data["reasoning_paths"]
    
    # Create recommendation card
    st.markdown(f"""
    <div style="border-left: 4px solid {COLORS['medium_confidence']}; 
                background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px;">
        <h3 style="color: {COLORS['text_primary']}; margin-top: 0;">{reasoning['conclusion']}</h3>
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="background: linear-gradient(to right, {COLORS['medium_confidence']} {reasoning['confidence']*100}%, {COLORS['bg_light']} {reasoning['confidence']*100}%); 
                        height: 8px; 
                        width: 100px; 
                        border-radius: 4px; 
                        margin-right: 10px;"></div>
            <span style="color: {COLORS['text_secondary']};">Confidence: {reasoning['confidence']:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show reasoning path
    st.subheader("Decision Reasoning Path")
    
    # Display reasoning steps
    for i, step_level in enumerate(reasoning['reasoning_steps']):
        st.markdown(f"**Level {i+1}:**")
        for step in step_level:
            st.success(f"✅ {step}")
    
    # Show recommended conditions
    st.subheader("Recommended Conditions")
    
    st.markdown("""
    1. **Customer Concentration Mitigation**: Quarterly progress reports on customer diversification efforts
    
    2. **Phased Equipment Funding**: Release loan in three tranches tied to specific modernization milestones
    
    3. **Supply Chain Monitoring**: Regular reporting on raw material cost variance and supply chain stability
    
    4. **Interest Rate Adjustment**: 25 basis points above standard rate to accommodate identified risks
    """)
    
    # Show counterfactuals
    st.subheader("What Would Change This Decision?")
    
    for counterfactual in reasoning['counterfactuals']:
        st.markdown(f"- {counterfactual}")

elif current_stage == "Monitoring Phase":
    # Show modernization progress
    concept_card(
        "Temporal Intelligence Layer",
        """
        The Temporal Intelligence layer tracks the company's progress on implementing the
        modernization plan and addressing the identified risks. By maintaining a complete
        history of how the entity evolves, Context-AI can identify trends and pattern changes
        that might indicate improving or deteriorating conditions.
        """,
        layer="temporal"
    )
    
    # Show monitoring timeline
    st.subheader("Equipment Modernization Progress")
    
    # Display progress bars for modernization phases
    phases = ["Planning", "Procurement", "Installation", "Testing", "Full Operation"]
    current_phase = 2  # Installation
    
    # Calculate progress
    progress_percent = (current_phase / (len(phases) - 1)) * 100
    
    # Display phases with current highlighted
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
    {"".join([f'<div style="text-align: center; width: 20%;"><div style="height: 30px; margin: 0 5px; background-color: {"#10B981" if i <= current_phase else COLORS["bg_medium"]}; border-radius: 4px;"></div><div style="margin-top: 5px; font-size: 0.8em;">{phases[i]}</div></div>' for i in range(len(phases))])}
    </div>
    <div style="margin-bottom: 20px;">
        <div style="margin-bottom: 5px; display: flex; justify-content: space-between;">
            <span>0%</span>
            <span>{progress_percent:.0f}% Complete</span>
            <span>100%</span>
        </div>
        <div style="height: 8px; background-color: {COLORS['bg_light']}; border-radius: 4px;">
            <div style="height: 100%; width: {progress_percent}%; background-color: #10B981; border-radius: 4px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show customer concentration improvement
    st.subheader("Customer Concentration Risk Mitigation")
    
    # Initial and current concentration
    initial_concentration = 28
    current_concentration = 24
    target_concentration = 20
    
    # Calculate progress
    concentration_progress = ((initial_concentration - current_concentration) / 
                             (initial_concentration - target_concentration)) * 100
    
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <div style="margin-bottom: 5px; display: flex; justify-content: space-between;">
            <span>Initial: {initial_concentration}%</span>
            <span>Current: {current_concentration}%</span>
            <span>Target: {target_concentration}%</span>
        </div>
        <div style="height: 8px; background-color: {COLORS['bg_light']}; border-radius: 4px;">
            <div style="height: 100%; width: {concentration_progress}%; background-color: #10B981; border-radius: 4px;"></div>
        </div>
        <div style="margin-top: 5px; text-align: center;">
            {concentration_progress:.0f}% of the way to target
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show key events timeline
    st.subheader("Key Monitoring Events")
    
    # Display events chronologically
    monitoring_events = [e for e in events if datetime.strptime(e['date'], "%Y-%m-%d") > 
                        datetime.strptime("2023-03-01", "%Y-%m-%d")]  # Filter to monitoring phase
    
    for event in monitoring_events:
        event_date = event['date']
        event_type = event['type']
        event_text = event['event']
        event_desc = event.get('description', '')
        
        # Display based on event type
        if event_type == 'positive':
            st.success(f"**{event_date}**: {event_text} - {event_desc}")
        elif event_type == 'negative':
            st.error(f"**{event_date}**: {event_text} - {event_desc}")
        elif event_type == 'warning':
            st.warning(f"**{event_date}**: {event_text} - {event_desc}")
        else:
            st.info(f"**{event_date}**: {event_text} - {event_desc}")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if current_stage_idx > 0:
        if st.button("⬅️ Previous Stage"):
            st.session_state.journey_stage -= 1
            st.rerun()

with col2:
    if current_stage_idx < len(journey_stages) - 1:
        if st.button("Next Stage ➡️"):
            st.session_state.journey_stage += 1
            st.rerun()

# Layer legend at the bottom
st.markdown("---")
st.markdown("### Context-AI Layer Legend")

legend_cols = st.columns(4)

with legend_cols[0]:
    st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: {COLORS['digital_twin']}; 
                  margin-right: 10px; border-radius: 50%;"></div>
        <span>Digital Twin Layer</span>
    </div>
    """, unsafe_allow_html=True)

with legend_cols[1]:
    st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: {COLORS['temporal']}; 
                  margin-right: 10px; border-radius: 50%;"></div>
        <span>Temporal Intelligence Layer</span>
    </div>
    """, unsafe_allow_html=True)

with legend_cols[2]:
    st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: {COLORS['external']}; 
                  margin-right: 10px; border-radius: 50%;"></div>
        <span>External Integration Layer</span>
    </div>
    """, unsafe_allow_html=True)

with legend_cols[3]:
    st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: {COLORS['guidance']}; 
                  margin-right: 10px; border-radius: 50%;"></div>
        <span>Adaptive Guidance Layer</span>
    </div>
    """, unsafe_allow_html=True)