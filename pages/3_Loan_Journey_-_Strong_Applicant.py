# pages/3_Loan_Journey_-_Strong_Applicant.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.theme import setup_page_config, apply_theme, COLORS
from utils.ui_components import header_with_logo, step_progress, concept_card, metric_card
from utils.graph_viz import display_knowledge_graph, simplified_graph_viz  # Include simplified as fallback
from utils.state import init_session_state, get_state, set_state
from utils.demo_data import load_applicant_data, generate_all_data
from utils.kg_generator import get_graph_for_stage

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
    applicant_data = load_applicant_data("strong_applicant")
    if not applicant_data:
        st.info("Generating sample data...")
        generate_all_data()
        applicant_data = load_applicant_data("strong_applicant")
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
st.subheader("A Strong Applicant Scenario")

# Company overview card
st.markdown(f"""
<div style="border-left: 4px solid {COLORS['digital_twin']}; 
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
    st.write(f"Graph contains {len(G.nodes)} nodes and {len(G.edges)} edges.")

# Get the appropriate graph for the current stage
G = get_graph_for_stage(applicant_data, current_stage, stage_to_index)

# Display the graph with NetworkX
try:
    from utils.graph_viz import networkx_matplotlib_graph
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
        with all its initial relationships. Even at this early stage, we can see how the company 
        connects to its industry, credit history, and loan request details - forming a foundation
        for understanding the application in context rather than as isolated data points.
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
    # Show the expanded knowledge graph explanation
    concept_card(
        "Digital Twin + Temporal Intelligence",
        """
        As more information is gathered, the knowledge graph grows richer. Financial metrics are now 
        connected to the company entity, and we can begin to see patterns in the data. The Temporal 
        Intelligence layer is now tracking how these metrics evolve over time, revealing trends that
        would be invisible in traditional systems that capture only snapshots.
        """,
        layer="temporal"
    )
    
    # Show financial metrics over time
    st.subheader("Temporal Intelligence: Financial Evolution")
    
    # Select metrics to plot - handling data safely to avoid PyArrow issues
    metrics_to_plot = ['revenue', 'profit_margin', 'cash_balance']
    
    # Create a safe copy for plotting with proper date handling
    try:
        plot_data = financial_data.copy()
        plot_data['date'] = pd.to_datetime(plot_data['date'])
        plot_subset = plot_data[['date'] + metrics_to_plot].iloc[:current_index+1]
        
        # Let's try alternative approach to chart creation
        chart_data = pd.DataFrame()
        for metric in metrics_to_plot:
            chart_data[metric] = plot_subset[metric].values
        
        # Use the date as index but converted to string first to avoid PyArrow issues
        chart_data.index = [d.strftime('%Y-%m-%d') for d in plot_subset['date']]
        
        # Display chart
        st.line_chart(chart_data)
    except Exception as e:
        st.error(f"Error creating financial evolution chart: {e}")
        # Fallback to displaying the raw data
        st.write("Financial data:", financial_data[['date'] + metrics_to_plot].iloc[:current_index+1].to_dict())
    
    # Show SaaS-specific metrics
    st.subheader("Industry-Specific Metrics")
    
    # Create columns for SaaS metrics
    cols = st.columns(3)
    
    try:
        with cols[0]:
            metric_card(
                "Customer Acquisition Cost", 
                f"${financial_data['customer_acquisition_cost'][current_index]:.0f}", 
                f"{((financial_data['customer_acquisition_cost'][current_index] / financial_data['customer_acquisition_cost'][0]) - 1) * 100:.1f}%"
                if current_index > 0 else None
            )
        
        with cols[1]:
            metric_card(
                "Monthly Recurring Revenue", 
                f"${financial_data['monthly_recurring_revenue'][current_index]:,.0f}", 
                f"+{((financial_data['monthly_recurring_revenue'][current_index] / financial_data['monthly_recurring_revenue'][0]) - 1) * 100:.1f}%"
                if current_index > 0 else None
            )
        
        with cols[2]:
            # Calculate LTV/CAC ratio
            ltv = financial_data['customer_lifetime_value'][current_index]
            cac = financial_data['customer_acquisition_cost'][current_index]
            ltv_cac_ratio = ltv / cac
            
            old_ltv = financial_data['customer_lifetime_value'][0]
            old_cac = financial_data['customer_acquisition_cost'][0]
            old_ltv_cac_ratio = old_ltv / old_cac
            
            metric_card(
                "LTV/CAC Ratio", 
                f"{ltv_cac_ratio:.1f}x", 
                f"+{((ltv_cac_ratio / old_ltv_cac_ratio) - 1) * 100:.1f}%"
                if current_index > 0 else None,
                "Healthy ratio > 3x"
            )
    except Exception as e:
        st.error(f"Error displaying metrics: {e}")
        st.write("SaaS metrics data is available but couldn't be displayed properly.")

# ...rest of the code remains the same...

elif current_stage == "Risk Assessment":
    # Show external context integration
    concept_card(
        "Digital Twin + External Integration",
        """
        The External Integration layer connects the digital twin to broader market and industry 
        context. For this SaaS company, we're analyzing industry growth trends, technology
        adoption patterns, competitive landscape, and economic indicators. These external
        factors often determine business success but are missed by traditional systems that
        only look at internal company data.
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
    
    # Show temporal risk evolution
    st.subheader("Temporal Intelligence: Risk Evolution")
    
    # Select risk metrics to plot
    risk_metrics = ['risk_score', 'confidence_score', 'financial_health_score', 'industry_risk_score']
    risk_data = risk_scores[['date'] + risk_metrics].iloc[:current_index+1]
    
    # Convert date column to datetime for better plotting
    risk_data['date'] = pd.to_datetime(risk_data['date'])
    
    # Display chart
    st.line_chart(risk_data.set_index('date'))
    
    # Show signal amplification
    st.subheader("Signal Amplification")
    
    st.markdown("""
    Multiple signals from different sources combine to create a strong positive assessment:
    """)
    
    # Create columns for signals
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("**Internal Signals**")
        st.success("✅ Strong financial performance")
        st.success("✅ Healthy LTV/CAC ratio")
        st.success("✅ Experienced management team")
    
    with cols[1]:
        st.markdown("**Industry Signals**")
        st.success("✅ Strong SaaS market growth")
        st.success("✅ Increasing technology adoption")
        st.info("ℹ️ Competitive landscape intensifying")
    
    with cols[2]:
        st.markdown("**Economic Signals**")
        st.info("ℹ️ Interest rates rising")
        st.success("✅ Technology spending resilient")
        st.success("✅ Enterprise digital transformation")

elif current_stage == "Decision Point":
    # Show decision recommendation
    concept_card(
        "Adaptive Guidance Layer",
        """
        The Adaptive Guidance layer analyzes the complete knowledge graph to generate 
        specific, actionable recommendations with transparent reasoning paths. Unlike
        traditional systems that provide only risk scores without explanation, Context-AI
        helps users understand exactly why a recommendation is being made and what factors
        contributed most to the decision.
        """,
        layer="guidance"
    )
    
    # Show recommendation
    st.subheader("Loan Assessment Recommendation")
    
    # Get reasoning data
    reasoning = applicant_data["reasoning_paths"]
    
    # Create recommendation card
    st.markdown(f"""
    <div style="border-left: 4px solid {COLORS['high_confidence']}; 
                background-color: {COLORS['bg_medium']}; 
                border-radius: 4px; 
                padding: 15px; 
                margin-bottom: 15px;">
        <h3 style="color: {COLORS['text_primary']}; margin-top: 0;">{reasoning['conclusion']}</h3>
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="background: linear-gradient(to right, {COLORS['high_confidence']} {reasoning['confidence']*100}%, {COLORS['bg_light']} {reasoning['confidence']*100}%); 
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
    
    # Show counterfactuals
    st.subheader("What Would Change This Decision?")
    
    st.markdown("Context-AI analyzes counterfactual scenarios to understand decision boundaries:")
    
    for counterfactual in reasoning['counterfactuals']:
        st.markdown(f"- {counterfactual}")
    
    # Show confidence components
    st.subheader("Confidence Component Analysis")
    
    # Get confidence components
    confidence = applicant_data["confidence_components"]
    
    # Create columns for components
    cols = st.columns(len(confidence))
    
    for i, (component, value) in enumerate(confidence.items()):
        with cols[i]:
            st.metric(component, f"{value:.2f}")
            st.progress(value)

elif current_stage == "Monitoring Phase":
    # Show the complete integrated system
    concept_card(
        "Complete Integrated System",
        """
        In the monitoring phase, all layers of Context-AI work together to create a comprehensive
        understanding that evolves over time. The Digital Twin layer maintains the knowledge graph,
        the Temporal Intelligence layer tracks how it evolves, the External Integration layer
        continuously updates with new context, and the Adaptive Guidance layer provides ongoing
        recommendations based on the complete picture.
        """,
        layer="temporal"
    )
    
    # Show monitoring timeline
    st.subheader("Loan Monitoring Timeline")
    
    # Display events chronologically
    for event in events:
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
    
    # Show long-term trends
    st.subheader("Long-Term Performance Trends")
    
    # Plot all financial data
    metrics_to_plot = ['revenue', 'profit_margin', 'cash_balance']
    
    # Convert date to datetime
    plot_data = financial_data.copy()
    plot_data['date'] = pd.to_datetime(plot_data['date'])
    
    # Create chart
    st.line_chart(plot_data[['date'] + metrics_to_plot].set_index('date'))
    
    # Show performance against plan
    st.subheader("Performance Against Plan")
    
    # Create columns for performance metrics
    cols = st.columns(3)
    
    with cols[0]:
        # Calculate actual vs target metrics
        actual_growth = ((financial_data['revenue'].iloc[-1] / financial_data['revenue'].iloc[0]) - 1) * 100
        target_growth = 36  # 3% monthly = ~36% annual
        performance = (actual_growth / target_growth) * 100
        
        metric_card(
            "Revenue Growth", 
            f"{actual_growth:.1f}%", 
            f"{actual_growth - target_growth:+.1f}% vs target",
            f"{performance:.0f}% of plan"
        )
    
    with cols[1]:
        # Customer metrics
        new_customers = 28
        target_customers = 25
        customer_performance = (new_customers / target_customers) * 100
        
        metric_card(
            "New Customers", 
            f"{new_customers}", 
            f"{new_customers - target_customers:+d} vs target",
            f"{customer_performance:.0f}% of plan"
        )
    
    with cols[2]:
        # Calculate LTV/CAC improvement
        initial_ltv_cac = financial_data['customer_lifetime_value'][0] / financial_data['customer_acquisition_cost'][0]
        current_ltv_cac = financial_data['customer_lifetime_value'][current_index] / financial_data['customer_acquisition_cost'][current_index]
        ltv_cac_change = ((current_ltv_cac / initial_ltv_cac) - 1) * 100
        
        metric_card(
            "LTV/CAC Improvement", 
            f"{ltv_cac_change:.1f}%", 
            f"{ltv_cac_change - 10:+.1f}% vs target",
            f"Currently {current_ltv_cac:.1f}x"
        )

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