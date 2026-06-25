"""
Out-of-Pocket Health Spending vs Income — Nigerian Households
Interactive Dashboard | NLSS 2022
Author: Hillary Onah | Finance & Data Science Analyst, DHIN
"""

import streamlit as st
import pandas as pd
import numpy as np
import pyreadstat
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Nigeria Health Spending Dashboard",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.metric-card {
    background:#1e1e2e;
    border:1px solid #333;
    border-radius:10px;
    padding:1rem 1.25rem;
    text-align:center
}
.insight-box {
    background:#1a2a3a;
    border-left:4px solid #4472C4;
    border-radius:0 8px 8px 0;
    padding:.75rem 1rem;
    font-size:14px;
    color:#a8c8f0;
    margin:.75rem 0
}
.warning-box {
    background:#2a1a1a;
    border-left:4px solid #C0392B;
    border-radius:0 8px 8px 0;
    padding:.75rem 1rem;
    font-size:14px;
    color:#f0a8a8;
    margin:.75rem 0
}
</style>
""", unsafe_allow_html=True)

# ── State names ────────────────────────────────────────────
STATE_NAMES = {
    1:'Abia', 2:'Adamawa', 3:'Akwa Ibom', 4:'Anambra',
    5:'Bauchi', 6:'Bayelsa', 7:'Benue', 8:'Borno',
    9:'Cross River', 10:'Delta', 11:'Ebonyi', 12:'Edo',
    13:'Ekiti', 14:'Enugu', 15:'Gombe', 16:'Imo',
    17:'Jigawa', 18:'Kaduna', 19:'Kano', 20:'Katsina',
    21:'Kebbi', 22:'Kogi', 23:'Kwara', 24:'Lagos',
    25:'Nasarawa', 26:'Niger', 27:'Ogun', 28:'Ondo',
    29:'Osun', 30:'Oyo', 31:'Plateau', 32:'Rivers',
    33:'Sokoto', 34:'Taraba', 35:'Yobe', 36:'Zamfara',
    37:'FCT Abuja'
}

ZONE_NAMES = {
    1:'North West', 2:'North East', 3:'North Central',
    4:'South West', 5:'South East', 6:'South South'
}

# ── Load and process data ──────────────────────────────────
@st.cache_data
def load_data():
    df_valid = pd.read_csv('oop_processed_data.csv')
    return df_valid

with st.spinner("Loading NLSS 2022 data..."):
    df = load_data()

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/nigeria.png",
        width=55
    )
    st.title("Nigeria Health\nSpending Dashboard")
    st.caption("NLSS 2022 | Portfolio Project")
    st.divider()

    st.subheader("🔍 Filters")

    selected_zone = st.multiselect(
        "Geopolitical Zone",
        options=sorted(df['zone_name'].dropna().unique()),
        default=sorted(df['zone_name'].dropna().unique())
    )

    selected_area = st.multiselect(
        "Area Type",
        options=['Urban', 'Rural'],
        default=['Urban', 'Rural']
    )

    income_range = st.slider(
        "Annual household income (₦)",
        int(df['total_income'].min()),
        int(df['total_income'].quantile(0.99)),
        (int(df['total_income'].min()),
         int(df['total_income'].quantile(0.99)))
    )

    st.divider()
    st.caption("Built with Python · Streamlit · Plotly")
    st.caption("👤 Hillary Onah | DHIN")

# ── Apply filters ──────────────────────────────────────────
filtered = df[
    (df['zone_name'].isin(selected_zone)) &
    (df['area'].isin(selected_area)) &
    (df['total_income'] >= income_range[0]) &
    (df['total_income'] <= income_range[1])
]

# ── Header ─────────────────────────────────────────────────
st.title("🇳🇬 Out-of-Pocket Health Spending vs Income")
st.caption(
    "How much of what Nigerian households earn goes to healthcare? "
    "| Data: NLSS 2022 · National Bureau of Statistics Nigeria"
)
st.divider()

# ── KPI row ────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Households", f"{len(filtered):,}")
with k2:
    st.metric(
        "Median OOP Burden",
        f"{filtered['oop_burden_pct'].median():.1f}%"
    )
with k3:
    st.metric(
        "Mean OOP Burden",
        f"{filtered['oop_burden_pct'].mean():.1f}%"
    )
with k4:
    cat_pct = filtered['catastrophic'].mean() * 100
    st.metric("Catastrophic Rate", f"{cat_pct:.1f}%")
with k5:
    st.metric(
        "Median Income",
        f"₦{filtered['total_income'].median():,.0f}"
    )

st.divider()

# ── Row 1: Quintile burden + Urban/Rural ──────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### OOP Burden by Income Quintile")
    q_burden = filtered.groupby(
        'income_quintile', observed=True
    )['oop_burden_pct'].median().reset_index()

    fig1 = px.bar(
        q_burden,
        x='income_quintile', y='oop_burden_pct',
        color='oop_burden_pct',
        color_continuous_scale=['#27AE60','#F1C40F','#C0392B'],
        labels={
            'income_quintile': 'Income Quintile',
            'oop_burden_pct': 'Median OOP Burden (%)'
        },
        text=q_burden['oop_burden_pct'].apply(
            lambda x: f'{x:.1f}%'
        )
    )
    fig1.add_hline(
        y=10, line_dash='dash',
        line_color='red', opacity=0.7,
        annotation_text='WHO threshold (10%)',
        annotation_position='top right'
    )
    fig1.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=10)
    )
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        '<div class="warning-box"> The poorest 20% of households '
        'spend over 65% of their income on healthcare — '
        'more than 6x the WHO catastrophic threshold.</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown("#### Catastrophic Expenditure by Quintile")
    cat_q = filtered.groupby(
        'income_quintile', observed=True
    )['catastrophic'].mean().mul(100).reset_index()
    cat_q.columns = ['income_quintile', 'pct_catastrophic']

    fig2 = px.bar(
        cat_q,
        x='income_quintile', y='pct_catastrophic',
        color='pct_catastrophic',
        color_continuous_scale=['#27AE60','#F1C40F','#C0392B'],
        labels={
            'income_quintile': 'Income Quintile',
            'pct_catastrophic': '% Households in Crisis'
        },
        text=cat_q['pct_catastrophic'].apply(
            lambda x: f'{x:.1f}%'
        )
    )
    fig2.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=10)
    )
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        '<div class="warning-box"> The poorest 20% of households '
        'are in catastrophic health expenditure. '
        'This is a financial emergency, not a welfare statistic.</div>',
        unsafe_allow_html=True
    )

# ── Row 2: State burden + Urban/Rural ─────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### OOP Burden by State")
    state_b = filtered.groupby('state_name')[
        'oop_burden_pct'
    ].median().reset_index().sort_values(
        'oop_burden_pct', ascending=True
    )
    fig3 = px.bar(
        state_b, x='oop_burden_pct', y='state_name',
        orientation='h',
        color='oop_burden_pct',
        color_continuous_scale=['#27AE60','#F1C40F','#C0392B'],
        labels={
            'state_name': 'State',
            'oop_burden_pct': 'Median OOP Burden (%)'
        }
    )
    fig3.add_vline(
        x=10, line_dash='dash',
        line_color='red', opacity=0.7
    )
    fig3.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("#### Urban vs Rural Burden")
    area_b = filtered.groupby('area')[
        'oop_burden_pct'
    ].median().reset_index()

    fig4 = px.bar(
        area_b, x='area', y='oop_burden_pct',
        color='area',
        color_discrete_map={
            'Urban': '#2980B9', 'Rural': '#27AE60'
        },
        labels={
            'area': 'Area Type',
            'oop_burden_pct': 'Median OOP Burden (%)'
        },
        text=area_b['oop_burden_pct'].apply(
            lambda x: f'{x:.1f}%'
        )
    )
    fig4.add_hline(
        y=10, line_dash='dash',
        line_color='red', opacity=0.7,
        annotation_text='WHO threshold',
        annotation_position='top right'
    )
    fig4.update_layout(
        showlegend=False,
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=10)
    )
    fig4.update_traces(textposition='outside')
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Zone-Level Burden")
    zone_b = filtered.groupby('zone_name')[
        'oop_burden_pct'
    ].median().reset_index().sort_values(
        'oop_burden_pct', ascending=False
    )
    fig5 = px.bar(
        zone_b, x='zone_name', y='oop_burden_pct',
        color='oop_burden_pct',
        color_continuous_scale=['#27AE60','#F1C40F','#C0392B'],
        labels={
            'zone_name': 'Zone',
            'oop_burden_pct': 'Median OOP Burden (%)'
        },
        text=zone_b['oop_burden_pct'].apply(
            lambda x: f'{x:.1f}%'
        )
    )
    fig5.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        height=280,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=10)
    )
    fig5.update_traces(textposition='outside')
    st.plotly_chart(fig5, use_container_width=True)

# ── Row 3: Scatter + Spending breakdown ───────────────────
st.divider()
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### Income vs OOP Spending — Scatter")
    sample = filtered.sample(
        min(1500, len(filtered)), random_state=42
    )
    fig6 = px.scatter(
        sample,
        x='total_income', y='oop_health_spending',
        color='income_quintile',
        opacity=0.5, size_max=6,
        labels={
            'total_income': 'Annual Household Income (₦)',
            'oop_health_spending': 'OOP Health Spending (₦)',
            'income_quintile': 'Quintile'
        },
        color_discrete_sequence=[
            '#C0392B','#E67E22',
            '#F1C40F','#2ECC71','#27AE60'
        ]
    )
    fig6.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown(
        '<div class="insight-box"> Low-income households '
        'spend a high proportion of income on health despite '
        'lower absolute spending — the burden is '
        'disproportionate.</div>',
        unsafe_allow_html=True
    )

with col6:
    st.markdown("#### Spending Category Breakdown")
    health_raw, _ = pyreadstat.read_dta(
        '2022nlss_sect03_health.dta'
    )
    breakdown = pd.DataFrame({
        'Category': [
            'Consultation', 'Drugs',
            'Hospital Stay', 'Transport'
        ],
        'Total (₦)': [
            health_raw['s3q14'].sum(),
            health_raw['s3q18a'].sum(),
            health_raw['s3q21a'].sum(),
            health_raw['s3q15'].sum()
        ]
    })
    fig7 = px.pie(
        breakdown,
        values='Total (₦)', names='Category',
        color_discrete_sequence=[
            '#E74C3C','#3498DB','#F39C12','#2ECC71'
        ],
        hole=0.45
    )
    fig7.update_layout(
        height=350, margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown(
        '<div class="insight-box"> Hospital stays and drug '
        'purchases account for ~90% of all OOP spending. '
        'Targeted interventions here would address the '
        'majority of the burden.</div>',
        unsafe_allow_html=True
    )

# ── Footer ─────────────────────────────────────────────────
st.divider()
st.caption(
    "Dataset: Nigeria Living Standards Survey 2022 · "
    "National Bureau of Statistics · "
    "Built by Hillary Onah | Finance & Data Science Analyst, "
    "DHIN | June 2026 · "
    "WHO catastrophic threshold: >10% of income on health"
)
