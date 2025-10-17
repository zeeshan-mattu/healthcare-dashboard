import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page to wide layout
st.set_page_config(layout="wide")

# Paste the JSON data directly into the script
data = {
  "institutionName": "NCH Healthcare System, Inc.",
  "primaryFiscalYear": 2024,
  "executiveSummaryKPIs": {
    "safetyGrade": "B",
    "operatingMargin": -0.054,
    "daysCashOnHand": 106.6,
    "governmentPayorDependency": 0.661,
    "auditorName": "RSM US LLP"
  },
  "financialPerformance": {
    "historicalFinancials": [
      {"fiscalYear": 2020, "Operating Income": -46150491, "Net Income (Change in Net Assets)": -2366137},
      {"fiscalYear": 2022, "Operating Income": -66423000, "Net Income (Change in Net Assets)": -113858000},
      {"fiscalYear": 2023, "Operating Income": -70432000, "Net Income (Change in Net Assets)": 8804000},
      {"fiscalYear": 2024, "Operating Income": -48491000, "Net Income (Change in Net Assets)": 38108000}
    ],
    "payorMixFY2024": [
      {"payor": "Medicare", "percentage": 0.595},
      {"payor": "Commercial Insurance", "percentage": 0.248},
      {"payor": "Medicaid", "percentage": 0.066},
      {"payor": "Self-Pay", "percentage": 0.061},
      {"payor": "Other", "percentage": 0.03}
    ]
  },
  "operationalUtilization": {
    "historicalUtilization": [
      {"fiscalYear": 2023, "Admissions": 40381, "Patient Days": 141259, "Emergency Visits": 113333},
      {"fiscalYear": 2024, "Admissions": 44123, "Patient Days": 151675, "Emergency Visits": 120499}
    ]
  },
  "qualityAndSafety": {
    "performanceComparison": [
      {"metricName": "Patient falls and injuries", "NCH Score": 0.544, "Average Score": 0.384},
      {"metricName": "Infection in the blood", "NCH Score": 0.500, "Average Score": 0.651},
      {"metricName": "MRSA Infection", "NCH Score": 0.996, "Average Score": 0.719}
    ]
  },
  "governanceAndLeadership": {
    "topExecutive_FY2022": {
      "name": "Paul Hiltz",
      "title": "President/CEO/Trustee",
      "totalCompensation": 1488059
    },
    "boardMetrics_FY2022": {
      "totalVotingMembers": 13,
      "independentVotingMembers": 11,
      "independenceRatio": 0.846
    }
  }
}

# --- Dashboard Title ---
st.title(f"Institutional Snapshot: {data['institutionName']}")

# --- Executive KPI Bar ---
kpi = data['executiveSummaryKPIs']
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Overall Safety Grade", value=kpi['safetyGrade'])
with col2:
    st.metric(label="Operating Margin", value=f"{kpi['operatingMargin']:.1%}", delta_color="inverse")
with col3:
    st.metric(label="Days Cash on Hand", value=f"{kpi['daysCashOnHand']:.1f} Days")
with col4:
    st.metric(label="Gov't Payor Dependency", value=f"{kpi['governmentPayorDependency']:.1%}")
with col5:
    st.metric(label="Auditor", value=kpi['auditorName'])

st.markdown("---")

# --- Main Dashboard View: The Financial Story ---
st.subheader("Financial Health & Performance")

fin_col1, fin_col2 = st.columns([2, 1])

with fin_col1:
    # Prepare data for line chart
    df_financials = pd.DataFrame(data['financialPerformance']['historicalFinancials'])
    df_financials_melted = pd.melt(df_financials, id_vars=['fiscalYear'], 
                                   value_vars=['Operating Income', 'Net Income (Change in Net Assets)'],
                                   var_name='Metric', value_name='Amount (USD)')
    
    # Create line chart
    fig_line = px.line(df_financials_melted, x='fiscalYear', y='Amount (USD)', color='Metric',
                       title="The Profitability Story: Operations vs. Net Income",
                       labels={'fiscalYear': 'Fiscal Year', 'Amount (USD)': 'Amount (USD)'},
                       markers=True)
    fig_line.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_line, use_container_width=True)

with fin_col2:
    # Prepare data for donut chart
    df_payor = pd.DataFrame(data['financialPerformance']['payorMixFY2024'])
    
    # Create donut chart
    fig_donut = px.pie(df_payor, names='payor', values='percentage',
                       title=f"Payor Mix (FY {data['primaryFiscalYear']})",
                       hole=0.4)
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")

# --- Supporting Insights: Operations & Quality ---
st.subheader("Operations & Quality")
op_col1, op_col2 = st.columns(2)

with op_col1:
    # Prepare data for utilization bar chart
    df_util = pd.DataFrame(data['operationalUtilization']['historicalUtilization'])
    df_util_melted = pd.melt(df_util, id_vars=['fiscalYear'], 
                             value_vars=['Admissions', 'Patient Days', 'Emergency Visits'],
                             var_name='Metric', value_name='Count')
    
    # Create bar chart
    fig_bar = px.bar(df_util_melted, x='fiscalYear', y='Count', color='Metric',
                     barmode='group', title="Utilization Trends")
    st.plotly_chart(fig_bar, use_container_width=True)
    
with op_col2:
    # Prepare data for quality comparison chart
    df_quality = pd.DataFrame(data['qualityAndSafety']['performanceComparison'])
    df_quality_melted = pd.melt(df_quality, id_vars=['metricName'], 
                                value_vars=['NCH Score', 'Average Score'],
                                var_name='Score Type', value_name='Score')
    
    # Create horizontal bar chart
    fig_quality = px.bar(df_quality_melted, y='metricName', x='Score', color='Score Type',
                         barmode='group', orientation='h',
                         title="Quality Performance vs. National Average",
                         labels={'metricName': 'Metric', 'Score': 'Score (Lower is often better)'})
    fig_quality.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_quality, use_container_width=True)

st.markdown("---")

# --- The Human Element: Governance & Leadership ---
st.subheader("Governance & Leadership (FY 2022)")
gov_col1, gov_col2 = st.columns(2)

with gov_col1:
    exec_data = data['governanceAndLeadership']['topExecutive_FY2022']
    st.markdown(f"**Top Compensated Executive**")
    st.text(f"Name: {exec_data['name']}")
    st.text(f"Title: {exec_data['title']}")
    st.text(f"Total Compensation: ${exec_data['totalCompensation']:,}")

with gov_col2:
    board_data = data['governanceAndLeadership']['boardMetrics_FY2022']
    st.markdown(f"**Board Governance**")
    st.text(f"Total Voting Members: {board_data['totalVotingMembers']}")
    st.text(f"Independent Voting Members: {board_data['independentVotingMembers']}")
    st.text(f"Independence Ratio: {board_data['independenceRatio']:.1%}")
    