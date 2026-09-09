import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="FinTech Wealth Pass | Churn & Revenue Risk Analytics",
    page_icon="⚡",
    layout="wide"
)

# Load Processed Data
@st.cache_data
def load_data():
    predictions_df = pd.read_csv("data/model_predictions.csv")
    transactions_df = pd.read_csv("data/transactions.csv")
    return predictions_df, transactions_df

try:
    df, tx_df = load_data()
except Exception as e:
    st.error("⚠️ Data missing! Please ensure `train_model.py` has executed successfully.")
    st.stop()

# Header
st.title("⚡ FinTech Wealth Pass: Churn & Revenue-at-Risk Engine")
st.markdown("Real-time behavioral cohort tracking, RFM customer segmentation, and machine learning risk modeling.")
st.markdown("---")

# Executive Metrics Summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Active Accounts", f"{len(df):,}")
col2.metric("Total Revenue at Risk", f"${df['revenue_at_risk_usd'].sum():,.2f}")
col3.metric("Average Churn Risk", f"{(df['churn_probability'].mean() * 100):.1f}%")
vip_at_risk = len(df[(df['rfm_segment'] == 'VIP') & (df['churn_probability'] > 0.5)])
col4.metric("High-Risk VIP Accounts", f"{vip_at_risk}")

st.markdown("---")

# Dashboard Sections (Added Tab 4 for Tableau BI)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Summary & RFM", 
    "📈 Product Performance & Recency", 
    "🎯 High-Risk Account Intervention",
    "📈 Interactive Tableau BI Dashboard"
])

with tab1:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("RFM Segment Breakdown")
        rfm_counts = df['rfm_segment'].value_counts().reset_index()
        rfm_counts.columns = ['Segment', 'Count']
        fig_rfm = px.pie(
            rfm_counts, values='Count', names='Segment', 
            hole=0.4, color='Segment',
            color_discrete_map={'VIP': '#00CC96', 'At Risk': '#FFA15A', 'Lost / Inactive': '#EF553B'}
        )
        st.plotly_chart(fig_rfm, use_container_width=True)
        
    with col_r:
        st.subheader("Revenue-at-Risk by Account Tier ($)")
        tier_risk = df.groupby('account_tier')['revenue_at_risk_usd'].sum().reset_index()
        fig_tier = px.bar(
            tier_risk, x='account_tier', y='revenue_at_risk_usd',
            color='account_tier', labels={'account_tier': 'Account Tier', 'revenue_at_risk_usd': 'Revenue at Risk ($)'}
        )
        st.plotly_chart(fig_tier, use_container_width=True)

with tab2:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("Total Revenue by Category")
        cat_summary = tx_df.groupby('product_category').agg(total_rev=('amount_usd', 'sum')).reset_index()
        fig_cat = px.bar(
            cat_summary, x='product_category', y='total_rev', 
            color='product_category', labels={'product_category': 'Product Category', 'total_rev': 'Revenue ($)'}
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with col_c2:
        st.subheader("User Recency vs. Total Monetary Value")
        fig_scatter = px.scatter(
            df, x='recency_days', y='total_monetary_value',
            color='churn_probability', size='total_transactions',
            color_continuous_scale='Reds',
            labels={'recency_days': 'Recency (Days Inactive)', 'total_monetary_value': 'Monetary Value ($)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Targeted Account Filter")
    tier_filter = st.multiselect("Filter by Tier", options=df['account_tier'].unique(), default=df['account_tier'].unique())
    segment_filter = st.multiselect("Filter by RFM Segment", options=df['rfm_segment'].unique(), default=df['rfm_segment'].unique())
    
    filtered_df = df[
        (df['account_tier'].isin(tier_filter)) & 
        (df['rfm_segment'].isin(segment_filter))
    ].sort_values(by='revenue_at_risk_usd', ascending=False)
    
    st.dataframe(
        filtered_df[['user_id', 'account_tier', 'primary_product', 'rfm_segment', 'recency_days', 'app_logins_30d', 'churn_probability', 'revenue_at_risk_usd']],
        column_config={
            "churn_probability": st.column_config.ProgressColumn(
                "Churn Risk", format="%.2f", min_value=0, max_value=1
            ),
            "revenue_at_risk_usd": st.column_config.NumberColumn(
                "Revenue at Risk ($)", format="$%.2f"
            )
        },
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.subheader("Executive Tableau BI Dashboard")
    st.caption("Embedded interactive visualization built on Tableau Public.")
    
    # PASTE YOUR TABLEAU SHARE LINK BELOW (Ensure it ends with ?:showVizHome=no&:embed=true)
    tableau_url = "https://public.tableau.com/views/FinTechRevenueRiskDashboard/Dashboard1?:showVizHome=no&:embed=true"
    
    components.html(
        f"""
        <iframe src="{tableau_url}"
                width="100%" 
                height="750" 
                frameborder="0">
        </iframe>
        """,
        height=770
    )