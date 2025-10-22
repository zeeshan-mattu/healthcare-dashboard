import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page to wide layout for a more professional feel
st.set_page_config(layout="wide")

# --- DATA: Updated with detailed breakdowns for drill-down functionality ---
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
    "financialDetailsFY2024": {
        "totalRevenues": 904789000,
        "totalExpenses": 953280000,
        "revenueBreakdown": [
            {"category": "Net Patient Service Revenue", "amount": 878024000},
            {"category": "Contributions & Grants", "amount": 9500000},
            {"category": "Other Revenue", "amount": 17265000}
        ],
        "expenseBreakdown": [
            {"category": "Salaries and Wages", "amount": 475100000},
            {"category": "Medical Supplies", "amount": 182300000},
            {"category": "Purchased Services", "amount": 135500000},
            {"category": "Depreciation", "amount": 75880000},
            {"category": "Interest", "amount": 25000000},
            {"category": "Other Expenses", "amount": 59500000}
        ]
    },
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
      {
        "metricName": "Patient falls and injuries", "NCH Score": 0.544, "Average Score": 0.384,
        "description": "Measures the rate of patient falls resulting in injury per 1,000 patient days. A higher score is worse, indicating a higher rate of preventable harm. NCH is currently performing worse than the national average."
      },
      {
        "metricName": "Infection in the blood", "NCH Score": 0.500, "Average Score": 0.651,
        "description": "Measures the rate of central line-associated bloodstream infections (CLABSI). A lower score is better, indicating stronger infection control protocols. NCH is performing better than the national average in this area."
      },
      {
        "metricName": "MRSA Infection", "NCH Score": 0.996, "Average Score": 0.719,
        "description": "Measures the rate of Methicillin-resistant Staphylococcus aureus (MRSA) infections. A higher score indicates a higher infection rate and is worse. NCH is performing worse than the national average here."
      }
    ]
  },
  "governanceAndLeadership": {
    "topExecutive_FY2022": {
      "name": "Paul Hiltz",
      "title": "President/CEO/Trustee",
      "totalCompensation": 1488059,
      "compensationBreakdown": [
          {"type": "Base Salary", "amount": 950000},
          {"type": "Bonus & Incentives", "amount": 450000},
          {"type": "Other Compensation", "amount": 88059}
      ]
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
    st.metric(label="Operating Margin", value=f"{kpi['operatingMargin']:.1%}")
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
    df_financials = pd.DataFrame(data['financialPerformance']['historicalFinancials'])
    df_financials_melted = pd.melt(df_financials, id_vars=['fiscalYear'], 
                                   value_vars=['Operating Income', 'Net Income (Change in Net Assets)'],
                                   var_name='Metric', value_name='Amount (USD)')
    
    fig_line = px.line(df_financials_melted, x='fiscalYear', y='Amount (USD)', color='Metric',
                       title="The Profitability Story: Operations vs. Net Income",
                       labels={'fiscalYear': 'Fiscal Year', 'Amount (USD)': 'Amount (USD)'},
                       markers=True)
    fig_line.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_line, use_container_width=True)

with fin_col2:
    df_payor = pd.DataFrame(data['financialPerformance']['payorMixFY2024'])
    fig_donut = px.pie(df_payor, names='payor', values='percentage',
                       title=f"Payor Mix (FY {data['primaryFiscalYear']})",
                       hole=0.4)
    st.plotly_chart(fig_donut, use_container_width=True)

# --- NEW: Financial Drill-Down Section ---
if 'show_financial_details' not in st.session_state:
    st.session_state.show_financial_details = False

# Use a button to toggle the visibility of the drill-down section
if st.button('🔍 Show Detailed Financial Breakdown', key='show_details_btn'):
    st.session_state.show_financial_details = not st.session_state.show_financial_details

if st.session_state.show_financial_details:
    st.markdown(f"#### Detailed Financials for Fiscal Year {data['primaryFiscalYear']}")
    
    details_data = data['financialPerformance']['financialDetailsFY2024']
    df_rev = pd.DataFrame(details_data['revenueBreakdown'])
    df_exp = pd.DataFrame(details_data['expenseBreakdown'])

    drill_col1, drill_col2 = st.columns(2)
    
    with drill_col1:
        st.markdown("**Revenue Breakdown**")
        fig_rev_bar = px.bar(df_rev, x='amount', y='category', orientation='h', text='amount')
        fig_rev_bar.update_traces(texttemplate='$%{text:,.0s}', textposition='outside')
        fig_rev_bar.update_layout(yaxis_title=None, xaxis_title="Amount (USD)")
        st.plotly_chart(fig_rev_bar, use_container_width=True)

    with drill_col2:
        st.markdown("**Expense Breakdown**")
        fig_exp_bar = px.bar(df_exp, x='amount', y='category', orientation='h', text='amount')
        fig_exp_bar.update_traces(texttemplate='$%{text:,.0s}', textposition='outside')
        fig_exp_bar.update_layout(yaxis_title=None, xaxis_title="Amount (USD)")
        st.plotly_chart(fig_exp_bar, use_container_width=True)

st.markdown("---")

# --- Supporting Insights: Operations & Quality ---
st.subheader("Operations & Quality")
op_col1, op_col2 = st.columns([1, 2])

with op_col1:
    df_util = pd.DataFrame(data['operationalUtilization']['historicalUtilization']).set_index('fiscalYear')
    st.markdown("**Utilization Trends**")
    st.dataframe(df_util)

with op_col2:
    st.markdown("**Quality Performance vs. National Average**")
    # --- NEW: Using Expanders for Interactive Drill-Down ---
    for metric in data['qualityAndSafety']['performanceComparison']:
        with st.expander(f"**{metric['metricName']}**"):
            st.markdown(f"> _{metric['description']}_")
            
            df_quality_metric = pd.DataFrame({
                'Score Type': ['NCH Score', 'Average Score'],
                'Score': [metric['NCH Score'], metric['Average Score']]
            })
            
            fig_quality = px.bar(df_quality_metric, x='Score', y='Score Type', orientation='h', 
                                 color='Score Type', text='Score')
            fig_quality.update_layout(showlegend=False, yaxis_title=None, height=200)
            st.plotly_chart(fig_quality, use_container_width=True)

st.markdown("---")

# --- The Human Element: Governance & Leadership ---
st.subheader("Governance & Leadership (FY 2022)")
gov_col1, gov_col2 = st.columns(2)

with gov_col1:
    exec_data = data['governanceAndLeadership']['topExecutive_FY2022']
    st.markdown(f"**Top Compensated Executive**")
    st.info(f"**Name:** {exec_data['name']}  \n**Title:** {exec_data['title']}  \n**Total Compensation:** ${exec_data['totalCompensation']:,}")
    
    # --- NEW: Compensation Drill-Down ---
    with st.expander("Show Compensation Breakdown"):
        df_comp = pd.DataFrame(exec_data['compensationBreakdown'])
        st.dataframe(df_comp.style.format({"amount": "${:,.0f}"}))

with gov_col2:
    board_data = data['governanceAndLeadership']['boardMetrics_FY2022']
    st.markdown(f"**Board Governance**")
    st.info(f"**Total Voting Members:** {board_data['totalVotingMembers']}  \n**Independent Voting Members:** {board_data['independentVotingMembers']}  \n**Independence Ratio:** {board_data['independenceRatio']:.1%}")