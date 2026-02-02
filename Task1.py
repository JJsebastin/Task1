import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Superstore Business Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    # Try different encodings to load the CSV file
    try:
        # First try with utf-8 encoding
        df = pd.read_csv('Sample - Superstore.csv', encoding='utf-8')
    except:
        try:
            # Try with latin1 encoding
            df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
        except:
            try:
                # Try with ISO-8859-1 encoding
                df = pd.read_csv('Sample - Superstore.csv', encoding='ISO-8859-1')
            except:
                # Try with cp1252 (Windows encoding)
                df = pd.read_csv('Sample - Superstore.csv', encoding='cp1252')
    
    # Convert date columns to datetime with mixed format
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=False)
    
    # Rename columns to remove spaces (for easier coding)
    df.columns = df.columns.str.replace(' ', '_')
    
    return df

# Load the data
df = load_data()

# Sidebar
st.sidebar.image("G:\student_streamlit\Task1\superstore.png", width=95)
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Section:",
    ["🏠 Overview", "📦 Products Deep Dive", "🛠️ Services & Shipping", "🗺️ Regional Analysis", "👥 Customer Insights"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Order_Date'].min(), df['Order_Date'].max()),
    min_value=df['Order_Date'].min(),
    max_value=df['Order_Date'].max()
)

# Region filter
regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category filter
categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Filter data
filtered_df = df[
    (df['Order_Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order_Date'] <= pd.to_datetime(date_range[1])) &
    (df['Region'].isin(regions)) &
    (df['Category'].isin(categories))
]

# Main content
st.markdown('<div class="main-header">📊 Superstore Business Insights Dashboard</div>', unsafe_allow_html=True)

# ========================================
# PAGE 1: OVERVIEW
# ========================================
if page == "🏠 Overview":
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Sales'].sum()
        sales_formatted = "$" + str(round(total_sales, 2))
        st.metric("💰 Total Sales", sales_formatted)
    
    with col2:
        total_profit = filtered_df['Profit'].sum()
        total_profit_formatted = "$" + str(round(total_profit, 2)) 
        profit_margin = (total_profit / total_sales * 100) 
        st.metric("📈 Total Profit", total_profit_formatted )
    
    with col3:
        total_orders = len(filtered_df)
        st.metric("🛒 Total Orders", f"{total_orders:,}" )
    
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Sales & Profit Trend Over Time")
        monthly_data = filtered_df.groupby(filtered_df['Order_Date'].dt.to_period('M')).agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        monthly_data['Order_Date'] = monthly_data['Order_Date'].astype(str)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=monthly_data['Order_Date'], y=monthly_data['Sales'], name="Sales", line=dict(color='#3498db', width=3)),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=monthly_data['Order_Date'], y=monthly_data['Profit'], name="Profit", line=dict(color='#2ecc71', width=3)),
            secondary_y=True
        )
        fig.update_layout(height=400, hovermode='x unified')
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Sales ($)", secondary_y=False)
        fig.update_yaxes(title_text="Profit ($)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Sales by Category")
        category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig = px.pie(category_sales, values='Sales', names='Category', 
                     color_discrete_sequence=px.colors.qualitative.Set3,
                     hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌎 Regional Performance")
        region_data = filtered_df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order_Date': 'count'
        }).reset_index()
        region_data.columns = ['Region', 'Sales', 'Profit', 'Orders']
        
        fig = go.Figure(data=[
            go.Bar(name='Sales', x=region_data['Region'], y=region_data['Sales'], marker_color='#3498db'),
            go.Bar(name='Profit', x=region_data['Region'], y=region_data['Profit'], marker_color='#2ecc71')
        ])
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 👥 Customer Segment Distribution")
        segment_data = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
        fig = px.bar(segment_data, x='Segment', y='Sales', 
                     color='Segment',
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ========================================
# PAGE 2: PRODUCTS DEEP DIVE
# ========================================
elif page == "📦 Products Deep Dive":
    st.markdown('<div class="section-header">📦 Product Analysis & Insights</div>', unsafe_allow_html=True)
    
    # Product metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        unique_products = filtered_df['Product_ID'].nunique()
        st.metric("🏷️ Unique Products", f"{unique_products:,}")
    
    with col2:
        avg_order_value = filtered_df['Sales'].mean()
        st.metric("💵 Avg Order Value", f"${avg_order_value:,.2f}")
    
    with col3:
        total_quantity = filtered_df['Quantity'].sum()
        st.metric("📊 Total Quantity Sold", f"{total_quantity:,}")
    
    with col4:
        best_category = filtered_df.groupby('Category')['Sales'].sum().idxmax()
        st.metric("🏆 Best Category", best_category)
    
    st.markdown("---")
    
    # Sub-category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Top 10 Sub-Categories by Sales")
        subcategory_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(subcategory_sales, x='Sales', y='Sub-Category', orientation='h',
                     color='Sales', color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Profitability by Sub-Category")
        subcategory_profit = filtered_df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(subcategory_profit, x='Profit', y='Sub-Category', orientation='h',
                     color='Profit', color_continuous_scale='Greens')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Product performance matrix
    st.markdown("### 📈 Product Performance Matrix (Sales vs Profit)")
    category_performance = filtered_df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    fig = px.scatter(category_performance, x='Sales', y='Profit', size='Quantity', color='Category',
                     hover_data=['Category'], size_max=60,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top and Bottom products
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌟 Top 10 Products by Revenue")
        top_products = filtered_df.groupby('Product_Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        st.dataframe(top_products, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📉 Bottom 10 Products by Profit")
        bottom_products = filtered_df.groupby('Product_Name')['Profit'].sum().sort_values().head(10).reset_index()
        st.dataframe(bottom_products, use_container_width=True, hide_index=True)



# ========================================
# PAGE 3: SERVICES & SHIPPING
# ========================================
elif page == "🛠️ Services & Shipping":
    st.markdown('<div class="section-header"> Shipping & Service Analysis</div>', unsafe_allow_html=True)
    
    # Shipping metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_ship_time = (filtered_df['Ship_Date'] - filtered_df['Order_Date']).dt.days.mean()
        st.metric("⏱️ Avg Shipping Time", f"{avg_ship_time:.1f} days")
    
    with col2:
        same_day_pct = (filtered_df['Ship_Mode'] == 'Same Day').sum() / len(filtered_df) * 100
        st.metric("🚀 Same Day Delivery", f"{same_day_pct:.1f}%")
    
    with col3:
        standard_orders = (filtered_df['Ship_Mode'] == 'Standard Class').sum()
        st.metric("📦 Standard Orders", f"{standard_orders:,}")
    
    with col4:
        premium_revenue = filtered_df[filtered_df['Ship_Mode'].isin(['First Class', 'Same Day'])]['Sales'].sum()
        st.metric("💎 Premium Ship Revenue", f"${premium_revenue:,.0f}")
    
    st.markdown("---")
    
    # Shipping mode analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Orders by Shipping Mode")
        ship_mode_data = filtered_df['Ship_Mode'].value_counts().reset_index()
        ship_mode_data.columns = ['Ship_Mode', 'Count']
        fig = px.pie(ship_mode_data, values='Count', names='Ship_Mode',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Revenue by Shipping Mode")
        ship_revenue = filtered_df.groupby('Ship_Mode')['Sales'].sum().reset_index()
        fig = px.bar(ship_revenue, x='Ship_Mode', y='Sales',
                     color='Ship_Mode', color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping time analysis
    st.markdown("### ⏰ Shipping Time Distribution")
    filtered_df['Shipping_Days'] = (filtered_df['Ship_Date'] - filtered_df['Order_Date']).dt.days
    fig = px.histogram(filtered_df, x='Shipping_Days', nbins=30,
                       color_discrete_sequence=['#3498db'])
    fig.update_layout(height=400)
    fig.update_xaxes(title_text="Days to Ship")
    fig.update_yaxes(title_text="Number of Orders")
    st.plotly_chart(fig, use_container_width=True)
    
    # Service performance by region
    st.markdown("### 🌍 Shipping Performance by Region")
    region_ship = filtered_df.groupby(['Region', 'Ship_Mode']).size().reset_index(name='Count')
    fig = px.bar(region_ship, x='Region', y='Count', color='Ship_Mode',
                 barmode='group', color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ========================================
# PAGE 4: REGIONAL ANALYSIS
# ========================================
elif page == "🗺️ Regional Analysis":
    st.markdown('<div class="section-header"> Geographic Performance Analysis</div>', unsafe_allow_html=True)
    
    # Regional metrics
    col1, col2, col3, col4 = st.columns(4)
    
    regions_count = filtered_df['Region'].nunique()
    states_count = filtered_df['State'].nunique()
    cities_count = filtered_df['City'].nunique()
    top_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()
    
    with col1:
        st.metric("🌎 Total Regions", regions_count)
    
    with col2:
        st.metric("🏛️ Total States", states_count)
    
    with col3:
        st.metric("🏙️ Total Cities", cities_count)
    
    with col4:
        st.metric("🏆 Top Region", top_region)
    
    st.markdown("---")
    
    # Regional comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Sales by Region")
        region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig = px.bar(region_sales, x='Region', y='Sales',
                     color='Region', color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💹 Profit Margin by Region")
        region_metrics = filtered_df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        region_metrics['Profit_Margin'] = (region_metrics['Profit'] / region_metrics['Sales'] * 100)
        fig = px.bar(region_metrics, x='Region', y='Profit_Margin',
                     color='Profit_Margin', color_continuous_scale='RdYlGn')
        fig.update_layout(height=400)
        fig.update_yaxes(title_text="Profit Margin (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # State-level analysis
    st.markdown("### 🏛️ Top 10 States by Sales")
    state_sales = filtered_df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order_Date': 'count'
    }).reset_index()
    state_sales.columns = ['State', 'Sales', 'Profit', 'Orders']
    state_sales = state_sales.sort_values('Sales', ascending=False).head(10)
    
    fig = go.Figure(data=[
        go.Bar(name='Sales', x=state_sales['State'], y=state_sales['Sales'], marker_color='#3498db'),
        go.Bar(name='Profit', x=state_sales['State'], y=state_sales['Profit'], marker_color='#2ecc71')
    ])
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # City performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏙️ Top 15 Cities by Revenue")
        city_sales = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(city_sales, y='City', x='Sales', orientation='h',
                     color='Sales', color_continuous_scale='Blues')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Regional Growth Trend")
        regional_monthly = filtered_df.groupby([filtered_df['Order_Date'].dt.to_period('M'), 'Region'])['Sales'].sum().reset_index()
        regional_monthly['Order_Date'] = regional_monthly['Order_Date'].astype(str)
        fig = px.line(regional_monthly, x='Order_Date', y='Sales', color='Region',
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

# ========================================
# PAGE 5: CUSTOMER INSIGHTS
# ========================================
else:  # Customer Insights
    st.markdown('<div class="section-header"> Customer Behavior & Insights</div>', unsafe_allow_html=True)
    
    # Customer metrics
    col1, col2, col3, col4 = st.columns(4)
    
    unique_customers = filtered_df['Customer_ID'].nunique()
    avg_customer_value = filtered_df.groupby('Customer_ID')['Sales'].sum().mean()
    repeat_customers = filtered_df.groupby('Customer_ID').size()
    repeat_rate = (repeat_customers > 1).sum() / unique_customers * 100
    top_segment = filtered_df.groupby('Segment')['Sales'].sum().idxmax()
    
    with col1:
        st.metric("👤 Total Customers", f"{unique_customers:,}")
    
    with col2:
        st.metric("💰 Avg Customer Value", f"${avg_customer_value:,.2f}")
    
    with col3:
        st.metric("🔄 Repeat Customer Rate", f"{repeat_rate:.1f}%")
    
    
    st.markdown("---")
    
    # Customer segment analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Customer Segment Distribution")
        segment_data = filtered_df.groupby('Segment').agg({
            'Customer_ID': 'nunique',
            'Sales': 'sum'
        }).reset_index()
        segment_data.columns = ['Segment', 'Customers', 'Sales']
        
        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'pie'}, {'type':'pie'}]],
                           subplot_titles=['By Customer Count', 'By Sales Value'])
        
        fig.add_trace(go.Pie(labels=segment_data['Segment'], values=segment_data['Customers'],
                            name='Customers'), row=1, col=1)
        fig.add_trace(go.Pie(labels=segment_data['Segment'], values=segment_data['Sales'],
                            name='Sales'), row=1, col=2)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💵 Average Order Value by Segment")
        segment_aov = filtered_df.groupby('Segment')['Sales'].mean().reset_index()
        fig = px.bar(segment_aov, x='Segment', y='Sales',
                     color='Segment', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(height=400, showlegend=False)
        fig.update_yaxes(title_text="Average Order Value ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer purchase behavior
    st.markdown("### 🛒 Purchase Frequency Distribution")
    customer_orders = filtered_df.groupby('Customer_ID').size().reset_index(name='Order_Count')
    fig = px.histogram(customer_orders, x='Order_Count', nbins=20,
                       color_discrete_sequence=['#9b59b6'])
    fig.update_layout(height=400)
    fig.update_xaxes(title_text="Number of Orders")
    fig.update_yaxes(title_text="Number of Customers")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top customers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌟 Top 10 Customers by Revenue")
        top_customers = filtered_df.groupby('Customer_Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        top_customers['Sales'] = top_customers['Sales'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(top_customers, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 🏆 Top 10 Customers by Order Count")
        frequent_customers = filtered_df.groupby('Customer_Name').size().sort_values(ascending=False).head(10).reset_index()
        frequent_customers.columns = ['Customer_Name', 'Order_Count']
        st.dataframe(frequent_customers, use_container_width=True, hide_index=True)
    
    # Customer lifetime value
    st.markdown("### 📈 Customer Segment Performance Over Time")
    segment_monthly = filtered_df.groupby([filtered_df['Order_Date'].dt.to_period('M'), 'Segment'])['Sales'].sum().reset_index()
    segment_monthly['Order_Date'] = segment_monthly['Order_Date'].astype(str)
    fig = px.area(segment_monthly, x='Order_Date', y='Sales', color='Segment',
                  color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
        <p><strong>Superstore Business Insights Dashboard</strong></p>
        <p>Built with Streamlit • Data Analytics & Visualization</p>
    </div>
""", unsafe_allow_html=True)