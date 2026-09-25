import streamlit as st
import pandas as pd
import numpy as np
import os
import altair as alt

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SalesIQ — Retail Sales Forecasting & Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #18181C;
        border: 1px solid #27272A;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.4rem;
        color: #38BDF8;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADERS
# -----------------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_DATA_PATH = os.path.join(APP_DIR, "cleaned_data.csv")
FORECAST_DATA_PATH = os.path.join(APP_DIR, "forecast_data.csv")

# Also check subfolder if not yet promoted
if not os.path.exists(CLEANED_DATA_PATH):
    CLEANED_DATA_PATH = os.path.join(APP_DIR, "FUTURE_ML_01-main", "cleaned_data.csv")
if not os.path.exists(FORECAST_DATA_PATH):
    FORECAST_DATA_PATH = os.path.join(APP_DIR, "FUTURE_ML_01-main", "forecast_data.csv")

@st.cache_data
def load_data():
    raw_df = pd.read_csv(CLEANED_DATA_PATH)
    raw_df['Order Date'] = pd.to_datetime(raw_df['Order Date'])
    raw_df['YearMonth'] = raw_df['Order Date'].dt.to_period('M').dt.to_timestamp()
    
    fc_df = pd.read_csv(FORECAST_DATA_PATH)
    fc_df['Date'] = pd.to_datetime(fc_df['Date'])
    return raw_df, fc_df

df, fc = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.shields.io/badge/SalesIQ-Forecasting%20Engine-38BDF8?style=for-the-badge&logo=target", use_container_width=True)
st.sidebar.markdown("### **Executive Planning Filters**")

selected_regions = st.sidebar.multiselect("Select Regions", options=list(df['Region'].unique()), default=list(df['Region'].unique()))
selected_categories = st.sidebar.multiselect("Select Categories", options=list(df['Category'].unique()), default=list(df['Category'].unique()))
selected_segments = st.sidebar.multiselect("Select Customer Segments", options=list(df['Segment'].unique()), default=list(df['Segment'].unique()))

st.sidebar.divider()
st.sidebar.markdown("#### **Engineer Attribution**")
st.sidebar.markdown("**Purushotham Balamurali**")
st.sidebar.caption("Machine Learning Intern @ Future Interns")
st.sidebar.markdown("[GitHub Profile](https://github.com/pbalamurali74-hue) • [LinkedIn](https://www.linkedin.com/in/purushothambalamurali/)")

# Filtered data
filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories)) &
    (df['Segment'].isin(selected_segments))
]

# -----------------------------------------------------------------------------
# HEADER & KPIS
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">📈 SalesIQ — Retail Sales Forecasting & Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Year Transaction Analytics • Time-Series Forecasts • Supply Chain What-If Planning</div>', unsafe_allow_html=True)

# Tabs
tab_overview, tab_forecast, tab_scenario = st.tabs([
    "📊 Executive Summary",
    "🔮 Time-Series Forecaster",
    "⚡ What-If Scenario Simulator"
])

# =============================================================================
# TAB 1: EXECUTIVE SUMMARY
# =============================================================================
with tab_overview:
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    total_orders = filtered_df['Order ID'].nunique()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Total Historical Revenue", f"${total_sales:,.0f}")
    with kpi2:
        st.metric("Net Operating Profit", f"${total_profit:,.0f}")
    with kpi3:
        st.metric("Operating Margin", f"{profit_margin:.1f}%")
    with kpi4:
        st.metric("Unique Customer Orders", f"{total_orders:,}")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("##### 🌍 Revenue Contribution by Region")
        reg_df = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        reg_chart = alt.Chart(reg_df).mark_bar(cornerRadius=6).encode(
            x=alt.X('Sales:Q', title="Total Sales ($)"),
            y=alt.Y('Region:N', sort='-x', title="Region"),
            color=alt.Color('Region:N', scale=alt.Scale(scheme='tableau10')),
            tooltip=['Region', 'Sales']
        ).properties(height=280)
        st.altair_chart(reg_chart, use_container_width=True)

    with col_chart2:
        st.markdown("##### 📦 Sales & Profitability by Category")
        cat_df = filtered_df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
        cat_chart = alt.Chart(cat_df).mark_bar(cornerRadius=6).encode(
            x='Category:N',
            y=alt.Y('Sales:Q', title="Sales ($)"),
            color=alt.Color('Category:N', scale=alt.Scale(scheme='category20b')),
            tooltip=['Category', 'Sales', 'Profit']
        ).properties(height=280)
        st.altair_chart(cat_chart, use_container_width=True)

    st.markdown("##### 🛒 Top Sub-Category Sales vs. Profit Matrix")
    subcat_df = filtered_df.groupby('Sub-Category')[['Sales', 'Profit', 'Quantity']].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
    st.dataframe(subcat_df, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 2: TIME-SERIES FORECASTER
# =============================================================================
with tab_forecast:
    st.markdown("### 12-Month Projected Sales Trajectory")
    st.caption("Prophet time-series regression models historical seasonality and structural trend components.")

    # Historical monthly aggregation
    hist_monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
    hist_monthly.rename(columns={'YearMonth': 'Date', 'Sales': 'Actual Sales'}, inplace=True)

    # Combined visual
    base_hist = alt.Chart(hist_monthly).mark_line(color="#94A3B8", strokeWidth=2).encode(
        x=alt.X('Date:T', title="Timeline"),
        y=alt.Y('Actual Sales:Q', title="Monthly Sales ($)"),
        tooltip=['Date:T', 'Actual Sales:Q']
    )

    base_fc = alt.Chart(fc).mark_line(color="#38BDF8", strokeWidth=3).encode(
        x='Date:T',
        y=alt.Y('Predicted Sales:Q', title="Monthly Sales ($)"),
        tooltip=['Date:T', 'Predicted Sales:Q']
    )

    band_fc = alt.Chart(fc).mark_area(opacity=0.2, color="#38BDF8").encode(
        x='Date:T',
        y='Lower Confidence Interval:Q',
        y2='Upper Confidence Interval:Q'
    )

    chart_fc = (base_hist + band_fc + base_fc).properties(
        title="Historical Monthly Sales (Grey) vs. Model Forecast with 95% Confidence Band (Blue)",
        height=380
    )
    st.altair_chart(chart_fc, use_container_width=True)

    st.markdown("#### 🚨 Supply Chain Seasonal Inventory Warnings")
    q4_surge = fc[fc['Date'].dt.month.isin([10, 11, 12])]
    avg_q4_surge = q4_surge['Predicted Sales'].mean()
    normal_avg = fc[~fc['Date'].dt.month.isin([10, 11, 12])]['Predicted Sales'].mean()
    surge_pct = ((avg_q4_surge - normal_avg) / normal_avg) * 100

    warn_col1, warn_col2 = st.columns([1.5, 1])
    with warn_col1:
        st.warning(f"⚠️ **Q4 Peak Demand Surge Detected:** Projected holiday sales are **+{surge_pct:.1f}%** higher than standard monthly averages. Warehouse inventory buffer for Technology and Office Supplies should be increased by at least 25% by September to avoid costly stockouts.")
    with warn_col2:
        st.info("💡 **Recommended Operational Action:**\n- Lock in supplier purchase orders 60 days in advance.\n- Allocate additional logistics capacity for regional West and East hubs.")

    st.markdown("#### 📋 Forecast Data Table")
    st.dataframe(fc, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 3: WHAT-IF SCENARIO SIMULATOR
# =============================================================================
with tab_scenario:
    st.markdown("### Executive 'What-If' Scenario Planning")
    st.markdown("Simulate how macroeconomic shocks, pricing changes, or marketing campaigns impact future projected revenue.")

    sim_c1, sim_c2 = st.columns(2)
    with sim_c1:
        demand_shock = st.slider("Market Demand Adjustment (%)", min_value=-30, max_value=30, value=10, step=5)
        discount_shift = st.slider("Average Discount Adjustment (%)", min_value=-10, max_value=10, value=0, step=1)
    with sim_c2:
        cogs_inflation = st.slider("Supply Chain Cost Inflation (%)", min_value=0, max_value=25, value=5, step=1)

    sim_fc = fc.copy()
    # Apply demand multiplier
    sim_multiplier = 1.0 + (demand_shock / 100.0) - (discount_shift * 0.5 / 100.0)
    sim_fc['Simulated Revenue'] = sim_fc['Predicted Sales'] * sim_multiplier
    
    baseline_total = fc['Predicted Sales'].sum()
    sim_total = sim_fc['Simulated Revenue'].sum()
    delta_revenue = sim_total - baseline_total

    st.divider()

    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        st.metric("Baseline 12-Month Forecast", f"${baseline_total:,.0f}")
    with sc_col2:
        st.metric("Simulated 12-Month Revenue", f"${sim_total:,.0f}", f"{delta_revenue:+,.0f}")
    with sc_col3:
        pct_change = (delta_revenue / baseline_total) * 100
        st.metric("Revenue Impact", f"{pct_change:+.1f}%")

    sim_chart = alt.Chart(sim_fc).mark_line(color="#10B981", strokeWidth=3).encode(
        x='Date:T',
        y=alt.Y('Simulated Revenue:Q', title="Simulated Sales ($)"),
        tooltip=['Date:T', 'Simulated Revenue:Q']
    ).properties(height=300, title="Projected Scenario Trajectory (Green)")
    st.altair_chart(sim_chart, use_container_width=True)
