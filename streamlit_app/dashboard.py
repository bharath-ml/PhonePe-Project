# PhonePe Pulse Data Visualization Dashboard - Complete Fixed Version
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
import numpy as np
from decimal import Decimal

# Load environment variables
load_dotenv()

# Database connection with environment variables
try:
    Mydb = sql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "P@rimi18"),
        database=os.getenv("DB_NAME", "phonepe_pulse")
    )
    mycursor = Mydb.cursor(buffered=True)
except Exception as e:
    st.error(f"Database connection failed: {e}")

# Streamlit page configuration
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="📱",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #6739b7;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #5d20a6;
    margin-bottom: 1rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #6739b7;
}
.info-box {
    background-color: #e8f4f8;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f77b4;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.header("📱 PhonePe Pulse Analytics")
with st.sidebar:
    selected = option_menu(
        "Navigation Menu", 
        ["Home", "Transaction Dynamics", "Device & User Analysis", "Insurance Analytics", "Market Expansion", "User Engagement", "Geo Analysis"],
        icons=["house", "graph-up", "phone", "shield-check", "geo-alt", "people", "map"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e8d5f2"},
            "nav-link-selected": {"background-color": "#6739b7"}
        }
    )

# Date filters in sidebar
st.sidebar.markdown("### 📅 Time Filters")
available_years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
selected_year = st.sidebar.selectbox("Select Year", available_years, index=len(available_years)-1)
selected_quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4], index=0)

# Date range selector
st.sidebar.markdown("### 📊 Date Range")
from_year = st.sidebar.selectbox("From Year", available_years, index=0)
to_year = st.sidebar.selectbox("To Year", available_years, index=len(available_years)-1)

# Helper function to safely convert decimal to float
def safe_float_conversion(value):
    """Safely convert decimal/numeric values to float"""
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# Helper function to safely convert to list for plotly
def safe_to_list(series):
    """Safely convert pandas series to list for plotly"""
    try:
        return [safe_float_conversion(x) for x in series]
    except:
        return []

# Helper function to format numbers
def format_number(num):
    """Format large numbers for display"""
    num = safe_float_conversion(num)
    if num >= 10000000:  # 1 crore
        return f"₹{num/10000000:.2f}Cr"
    elif num >= 100000:  # 1 lakh
        return f"₹{num/100000:.2f}L"
    elif num >= 1000:
        return f"₹{num/1000:.2f}K"
    else:
        return f"₹{num:.2f}"

# Helper function to get available table columns
def get_table_columns(table_name):
    """Get column names for a table"""
    try:
        mycursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in mycursor.fetchall()]
        return columns
    except:
        return []

# Home Page
if selected == "Home":
    st.markdown('<h1 class="main-header">📱 PhonePe Pulse Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Comprehensive Digital Payment Analytics Platform</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🚀 Dashboard Overview
        This comprehensive analytics platform provides deep insights into PhonePe's digital payment ecosystem through:
        
        - **Transaction Dynamics Analysis**: Understanding payment patterns across states and categories
        - **Device & User Engagement**: Analyzing user preferences across different device brands
        - **Insurance Penetration**: Tracking growth in insurance domain adoption
        - **Market Expansion**: Identifying opportunities for geographical expansion
        - **User Engagement**: Comprehensive user behavior analysis
        - **Geographical Analytics**: State and district-wise performance metrics
        
        ### 🛠️ Technologies Used
        - **Frontend**: Streamlit, Plotly for interactive visualizations
        - **Backend**: MySQL database with Python connectivity
        - **Data Processing**: Pandas for data manipulation and analysis
        - **Visualization**: Plotly Express for charts and geographical maps
        """)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        try:
            # Get some quick stats
            mycursor.execute("SELECT COUNT(DISTINCT State) FROM aggregated_transaction")
            result = mycursor.fetchone()
            states_count = result[0] if result else 0
            
            mycursor.execute("SELECT SUM(Transacion_count) FROM aggregated_transaction")
            result = mycursor.fetchone()
            total_transactions = safe_float_conversion(result[0]) if result else 0
            
            mycursor.execute("SELECT SUM(Transacion_amount) FROM aggregated_transaction")
            result = mycursor.fetchone()
            total_amount = safe_float_conversion(result[0]) if result else 0
            
            st.metric("Total States", f"{states_count}")
            st.metric("Total Transactions", f"{total_transactions:,.0f}" if total_transactions else "N/A")
            st.metric("Total Amount", format_number(total_amount) if total_amount else "N/A")
            
        except Exception as e:
            st.error(f"Unable to fetch quick stats: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# 1. Transaction Dynamics Analysis
elif selected == "Transaction Dynamics":
    st.markdown('<h1 class="main-header">📊 Decoding Transaction Dynamics on PhonePe</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💳 Transaction Amount by State")
        try:
            query = f"""
            SELECT State, SUM(Transacion_amount) as Total_Amount, SUM(Transacion_count) as Total_Count
            FROM aggregated_transaction 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
            GROUP BY State 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            mycursor.execute(query)
            result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['State', 'Total_Amount', 'Total_Count'])
                
                # Convert to float safely
                df['Total_Amount'] = df['Total_Amount'].apply(safe_float_conversion)
                df['Total_Count'] = df['Total_Count'].apply(safe_float_conversion)
                
                # Format state names for better display
                df['State'] = df['State'].str.replace('-', ' ').str.title()
                
                fig = px.bar(df, x='State', y='Total_Amount', 
                           title=f'Top 10 States by Transaction Amount (Q{selected_quarter} {selected_year})',
                           color='Total_Amount',
                           color_continuous_scale='viridis',
                           text='Total_Amount')
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data table
                st.markdown("#### Top States Data")
                df_display = df.copy()
                df_display['Total_Amount_Formatted'] = df_display['Total_Amount'].apply(format_number)
                df_display['Total_Count'] = df_display['Total_Count'].astype(int)
                df_display.index = range(1, len(df_display) + 1)  # Add serial numbers
                st.dataframe(df_display[['State', 'Total_Amount_Formatted', 'Total_Count']], use_container_width=True)
            else:
                st.warning("No data available for selected period")
        except Exception as e:
            st.error(f"Error fetching transaction data: {e}")
    
    with col2:
        st.markdown("### 📈 Transaction Types Distribution")
        try:
            query = f"""
            SELECT Transacion_type, SUM(Transacion_count) as Count, SUM(Transacion_amount) as Amount
            FROM aggregated_transaction 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
            GROUP BY Transacion_type
            """
            mycursor.execute(query)
            result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['Transaction_Type', 'Count', 'Amount'])
                
                # Convert to float safely
                df['Count'] = df['Count'].apply(safe_float_conversion)
                df['Amount'] = df['Amount'].apply(safe_float_conversion)
                
                # Format transaction types for better display
                df['Transaction_Type'] = df['Transaction_Type'].str.replace('-', ' ').str.title()
                
                fig = px.pie(df, values='Amount', names='Transaction_Type',
                           title=f'Transaction Distribution by Type (Q{selected_quarter} {selected_year})',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
                
                # Show summary
                st.markdown("#### Transaction Types Summary")
                df_display = df.copy()
                df_display['Amount_Formatted'] = df_display['Amount'].apply(format_number)
                df_display['Count'] = df_display['Count'].astype(int)
                df_display.index = range(1, len(df_display) + 1)  # Add serial numbers
                st.dataframe(df_display[['Transaction_Type', 'Count', 'Amount_Formatted']], use_container_width=True)
            else:
                st.warning("No transaction type data available")
        except Exception as e:
            st.error(f"Error fetching transaction type data: {e}")

# 2. Device & User Analysis
elif selected == "Device & User Analysis":
    st.markdown('<h1 class="main-header">📱 Device Dominance and User Engagement Analysis</h1>', unsafe_allow_html=True)
    
    # Debug: Check table structure first
    st.sidebar.markdown("### 🔍 Debug Info")
    user_columns = get_table_columns("aggregated_user")
    st.sidebar.write(f"User table columns: {user_columns}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📱 Top Device Brands by User Count")
        try:
            # First check what data is available
            check_query = f"""
            SELECT COUNT(*) as total_records, 
                   COUNT(DISTINCT Device_Brand) as unique_brands,
                   SUM(User_Count) as total_users
            FROM aggregated_user 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                AND Device_Brand IS NOT NULL 
                AND User_Count > 0
            """
            mycursor.execute(check_query)
            check_result = mycursor.fetchone()
            
            st.info(f"Data check: {check_result[0]} records, {check_result[1]} brands, {check_result[2]} total users")
            
            if check_result[0] > 0:
                query = f"""
                SELECT Device_Brand, 
                       SUM(User_Count) as Total_Users, 
                       AVG(User_Percentage) as Avg_Percentage
                FROM aggregated_user 
                WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                    AND Device_Brand IS NOT NULL 
                    AND User_Count > 0
                GROUP BY Device_Brand 
                ORDER BY Total_Users DESC 
                LIMIT 10
                """
                mycursor.execute(query)
                result = mycursor.fetchall()
                
                if result:
                    df = pd.DataFrame(result, columns=['Device_Brand', 'Total_Users', 'Avg_Percentage'])
                    
                    # Convert to float safely
                    df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
                    df['Avg_Percentage'] = df['Avg_Percentage'].apply(safe_float_conversion)
                    
                    # Clean device brand names
                    df['Device_Brand'] = df['Device_Brand'].str.title()
                    
                    fig = px.bar(df, x='Device_Brand', y='Total_Users',
                               title=f'Device Brand Usage (Q{selected_quarter} {selected_year})',
                               color='Avg_Percentage',
                               color_continuous_scale='sunset',
                               text='Total_Users')
                    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                    fig.update_layout(xaxis_tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table with serial numbers
                    st.markdown("#### Device Brand Data")
                    df_display = df.copy()
                    df_display['Total_Users'] = df_display['Total_Users'].astype(int)
                    df_display['Avg_Percentage'] = df_display['Avg_Percentage'].round(2)
                    df_display.index = range(1, len(df_display) + 1)
                    st.dataframe(df_display, use_container_width=True)
                else:
                    st.warning("No device brand data found for the selected period")
            else:
                st.warning("No device data available for selected period. Showing overall trends:")
                
                # Show overall device trends
                query = """
                SELECT Device_Brand, 
                       SUM(User_Count) as Total_Users, 
                       AVG(User_Percentage) as Avg_Percentage
                FROM aggregated_user 
                WHERE Device_Brand IS NOT NULL AND User_Count > 0
                GROUP BY Device_Brand 
                ORDER BY Total_Users DESC 
                LIMIT 10
                """
                mycursor.execute(query)
                result = mycursor.fetchall()
                
                if result:
                    df = pd.DataFrame(result, columns=['Device_Brand', 'Total_Users', 'Avg_Percentage'])
                    df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
                    df['Avg_Percentage'] = df['Avg_Percentage'].apply(safe_float_conversion)
                    df['Device_Brand'] = df['Device_Brand'].str.title()
                    
                    fig = px.bar(df, x='Device_Brand', y='Total_Users',
                               title='Overall Device Brand Usage (All Time)',
                               color='Avg_Percentage',
                               color_continuous_scale='sunset')
                    fig.update_layout(xaxis_tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table with serial numbers
                    df_display = df.copy()
                    df_display['Total_Users'] = df_display['Total_Users'].astype(int)
                    df_display['Avg_Percentage'] = df_display['Avg_Percentage'].round(2)
                    df_display.index = range(1, len(df_display) + 1)
                    st.dataframe(df_display, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error fetching device data: {e}")
    
    with col2:
        st.markdown("### 👥 User Engagement by State")
        try:
            # Check column names first
            map_user_columns = get_table_columns("map_user")
            st.info(f"Map user columns: {map_user_columns}")
            
            # Try different column name variations
            possible_queries = [
                f"""
                SELECT State, SUM(RegisteredUsers) as Total_Users, SUM(AppOpens) as Total_Opens
                FROM map_user 
                WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                    AND RegisteredUsers > 0
                GROUP BY State 
                ORDER BY Total_Users DESC 
                LIMIT 15
                """,
                f"""
                SELECT State, SUM(Registered_users) as Total_Users, SUM(App_opens) as Total_Opens
                FROM map_user 
                WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                    AND Registered_users > 0
                GROUP BY State 
                ORDER BY Total_Users DESC 
                LIMIT 15
                """
            ]
            
            result = None
            for query in possible_queries:
                try:
                    mycursor.execute(query)
                    result = mycursor.fetchall()
                    if result:
                        break
                except Exception as query_error:
                    continue
            
            if result:
                df = pd.DataFrame(result, columns=['State', 'Total_Users', 'Total_Opens'])
                
                # Convert to float safely
                df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
                df['Total_Opens'] = df['Total_Opens'].apply(safe_float_conversion)
                
                # Clean state names
                df['State'] = df['State'].str.replace('-', ' ').str.title()
                
                # Calculate engagement ratio safely
                df['Engagement_Ratio'] = df.apply(
                    lambda row: safe_float_conversion(row['Total_Opens'] / row['Total_Users']) 
                    if row['Total_Users'] > 0 else 0, axis=1
                )
                
                # Create scatter plot
                fig = px.scatter(
                    df,
                    x='Total_Users', 
                    y='Total_Opens',
                    size='Engagement_Ratio',
                    hover_name='State',
                    title=f'User Engagement Analysis (Q{selected_quarter} {selected_year})',
                    color='Engagement_Ratio',
                    color_continuous_scale='plasma',
                    labels={'Total_Users': 'Registered Users', 'Total_Opens': 'App Opens'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show top engagement states with serial numbers
                st.markdown("#### Top Engagement States")
                df_display = df.sort_values('Engagement_Ratio', ascending=False).head(10).copy()
                df_display['Engagement_Ratio'] = df_display['Engagement_Ratio'].round(2)
                df_display['Total_Users'] = df_display['Total_Users'].astype(int)
                df_display['Total_Opens'] = df_display['Total_Opens'].astype(int)
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display, use_container_width=True)
            else:
                st.warning("No user engagement data available for selected period")
        except Exception as e:
            st.error(f"Error fetching user engagement data: {e}")

# 3. Insurance Analytics
elif selected == "Insurance Analytics":
    st.markdown('<h1 class="main-header">🛡️ Insurance Penetration and Growth Analysis</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Insurance Transactions by State")
        try:
            query = f"""
            SELECT State, SUM(Insurance_count) as Total_Count, SUM(Insurance_amount) as Total_Amount
            FROM aggregated_insurance 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                AND Insurance_count > 0 AND Insurance_amount > 0
            GROUP BY State 
            ORDER BY Total_Amount DESC 
            LIMIT 15
            """
            mycursor.execute(query)
            result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['State', 'Total_Count', 'Total_Amount'])
                
                # Convert to float safely
                df['Total_Count'] = df['Total_Count'].apply(safe_float_conversion)  
                df['Total_Amount'] = df['Total_Amount'].apply(safe_float_conversion)
                
                # Clean state names
                df['State'] = df['State'].str.replace('-', ' ').str.title()
                
                fig = px.bar(df, x='State', y='Total_Amount',
                           title=f'Insurance Amount by State (Q{selected_quarter} {selected_year})',
                           color='Total_Count',
                           color_continuous_scale='blues',
                           text='Total_Amount')
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data table with serial numbers
                st.markdown("#### State-wise Insurance Data")
                df_display = df.copy()
                df_display['Total_Amount_Formatted'] = df_display['Total_Amount'].apply(format_number)
                df_display['Total_Count'] = df_display['Total_Count'].astype(int)
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display[['State', 'Total_Count', 'Total_Amount_Formatted']], use_container_width=True)
            else:
                st.warning("No insurance data available for selected period")
        except Exception as e:
            st.error(f"Error fetching insurance data: {e}")
    
    with col2:
        st.markdown("### 🏥 Insurance Types Distribution")
        try:
            query = f"""
            SELECT Insurance_type, SUM(Insurance_count) as Count, SUM(Insurance_amount) as Amount
            FROM aggregated_insurance 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                AND Insurance_count > 0 AND Insurance_amount > 0
            GROUP BY Insurance_type
            HAVING SUM(Insurance_amount) > 0
            """
            mycursor.execute(query)
            result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['Insurance_Type', 'Count', 'Amount'])
                
                # Convert to float safely
                df['Count'] = df['Count'].apply(safe_float_conversion)
                df['Amount'] = df['Amount'].apply(safe_float_conversion)
                
                # Clean insurance type names
                df['Insurance_Type'] = df['Insurance_Type'].str.replace('-', ' ').str.title()
                
                fig = px.pie(df, values='Amount', names='Insurance_Type',
                           title=f'Insurance Distribution by Type (Q{selected_quarter} {selected_year})',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data table with serial numbers
                st.markdown("#### Insurance Types Data")
                df_display = df.copy()
                df_display['Amount_Formatted'] = df_display['Amount'].apply(format_number)
                df_display['Count'] = df_display['Count'].astype(int)
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display[['Insurance_Type', 'Count', 'Amount_Formatted']], use_container_width=True)
            else:
                st.warning("No insurance type data available for selected period")
                
        except Exception as e:
            st.error(f"Error fetching insurance type data: {e}")

# 4. Market Expansion Analysis
elif selected == "Market Expansion":
    st.markdown('<h1 class="main-header">🌍 Transaction Analysis for Market Expansion</h1>', unsafe_allow_html=True)
    
    # State selection for detailed analysis
    state_options = [
        'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
        'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa',
        'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka',
        'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur',
        'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'
    ]
    
    selected_state = st.selectbox("Select State for Detailed Analysis", state_options, index=30)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📍 District-wise Transactions in {selected_state.title()}")
        try:
            query = f"""
            SELECT District, SUM(Transaction_count) as Total_Count, SUM(Transaction_amount) as Total_Amount
            FROM map_transaction 
            WHERE State = '{selected_state}' AND Year = {selected_year} AND Quarter = {selected_quarter}
                AND Transaction_count > 0 AND Transaction_amount > 0
            GROUP BY District 
            ORDER BY Total_Amount DESC 
            LIMIT 15
            """
            mycursor.execute(query)
            result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['District', 'Total_Count', 'Total_Amount'])
                
                # Convert to float safely
                df['Total_Count'] = df['Total_Count'].apply(safe_float_conversion)
                df['Total_Amount'] = df['Total_Amount'].apply(safe_float_conversion)
                
                # Clean district names
                df['District'] = df['District'].str.replace('-', ' ').str.title()
                
                fig = px.bar(df, x='District', y='Total_Amount',
                           title=f'District Performance in {selected_state.replace("-", " ").title()}',
                           color='Total_Count',
                           color_continuous_scale='viridis',
                           text='Total_Amount')
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show district performance metrics with serial numbers
                st.markdown("#### District Performance Metrics")
                df_display = df.copy()
                df_display['Total_Amount_Formatted'] = df_display['Total_Amount'].apply(format_number)
                df_display['Total_Count'] = df_display['Total_Count'].astype(int)
                # Calculate average transaction safely
                df_display['Avg_Transaction'] = df_display.apply(
                    lambda row: format_number(row['Total_Amount'] / row['Total_Count']) if row['Total_Count'] > 0 else "₹0",
                    axis=1
                )
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display[['District', 'Total_Count', 'Total_Amount_Formatted', 'Avg_Transaction']], use_container_width=True)
            else:
                st.warning(f"No district data available for {selected_state} in the selected period")
        except Exception as e:
            st.error(f"Error fetching district data: {e}")
    
    with col2:
        st.markdown("### 🏆 Top Performing Areas")
        try:
            # Check column names for top_user table
            top_user_columns = get_table_columns("top_user")
            st.info(f"Top user columns: {top_user_columns}")
            
            # Try different column name variations
            possible_queries = [
                f"""
                SELECT District, SUM(Registered_users) as Total_Users
                FROM top_user 
                WHERE State = '{selected_state}' AND Year = {selected_year} AND Quarter = {selected_quarter}
                    AND Registered_users > 0
                GROUP BY District 
                ORDER BY Total_Users DESC 
                LIMIT 10
                """,
                f"""
                SELECT District, SUM(RegisteredUsers) as Total_Users
                FROM top_user 
                WHERE State = '{selected_state}' AND Year = {selected_year} AND Quarter = {selected_quarter}
                    AND RegisteredUsers > 0
                GROUP BY District 
                ORDER BY Total_Users DESC 
                LIMIT 10
                """
            ]
            
            result = None
            for query in possible_queries:
                try:
                    mycursor.execute(query)
                    result = mycursor.fetchall()
                    if result:
                        break
                except Exception as e:
                    pass  # You can log or handle the exception if needed
            
            if result:
                df = pd.DataFrame(result, columns=['District', 'Total_Users'])
                
                # Convert to float safely
                df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
                
                # Clean district names
                df['District'] = df['District'].str.replace('-', ' ').str.title()
                
                fig = px.treemap(df, path=['District'], values='Total_Users',
                               title=f'User Distribution in {selected_state.replace("-", " ").title()}',
                               color='Total_Users',
                               color_continuous_scale='oranges')
                st.plotly_chart(fig, use_container_width=True)
                
                # Show top districts with serial numbers
                st.markdown("#### Top Districts by Users")
                df_display = df.head(10).copy()
                df_display['Total_Users'] = df_display['Total_Users'].astype(int)
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display, use_container_width=True)
            else:
                st.warning(f"No user data available for {selected_state}")
        except Exception as e:
            st.error(f"Error fetching top user data: {e}")

# 5. User Engagement Analysis
elif selected == "User Engagement":
    st.markdown('<h1 class="main-header">👥 Comprehensive User Engagement Analysis</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Quarterly User Growth Trend")
        try:
            query = f"""
            SELECT Year, Quarter, SUM(RegisteredUsers) as Total_Users, SUM(AppOpens) as Total_Opens
            FROM map_user 
            WHERE Year BETWEEN {from_year} AND {to_year}
                AND RegisteredUsers > 0
            GROUP BY Year, Quarter 
            ORDER BY Year, Quarter
            """
            
            # Try alternative column names if first query fails
            try:
                mycursor.execute(query)
                result = mycursor.fetchall()
            except:
                query = f"""
                SELECT Year, Quarter, SUM(Registered_users) as Total_Users, SUM(App_opens) as Total_Opens
                FROM map_user 
                WHERE Year BETWEEN {from_year} AND {to_year}
                    AND Registered_users > 0
                GROUP BY Year, Quarter 
                ORDER BY Year, Quarter
                """
                mycursor.execute(query)
                result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['Year', 'Quarter', 'Total_Users', 'Total_Opens'])
                
                # Convert to float safely
                df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
                df['Total_Opens'] = df['Total_Opens'].apply(safe_float_conversion)
                
                # Create period column
                df['Period'] = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)
                
                # Calculate engagement ratio safely
                df['Engagement_Ratio'] = df.apply(
                    lambda row: safe_float_conversion(row['Total_Opens'] / row['Total_Users']) 
                    if row['Total_Users'] > 0 else 0, axis=1
                )
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Period'], y=df['Total_Users'], 
                                       mode='lines+markers', name='Registered Users',
                                       line=dict(color='blue', width=3)))
                fig.add_trace(go.Scatter(x=df['Period'], y=df['Total_Opens'], 
                                       mode='lines+markers', name='App Opens',
                                       line=dict(color='red', width=3), yaxis='y2'))
                
                fig.update_layout(
                    title='User Growth and Engagement Trends',
                    xaxis_title='Period',
                    yaxis=dict(title='Registered Users', side='left'),
                    yaxis2=dict(title='App Opens', side='right', overlaying='y'),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show trend data with serial numbers
                st.markdown("#### Growth Trend Data")
                df_display = df[['Period', 'Total_Users', 'Total_Opens', 'Engagement_Ratio']].copy()
                df_display['Total_Users'] = df_display['Total_Users'].astype(int)
                df_display['Total_Opens'] = df_display['Total_Opens'].astype(int)
                df_display['Engagement_Ratio'] = df_display['Engagement_Ratio'].round(2)
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display, use_container_width=True)
            else:
                st.warning("No user trend data available")
        except Exception as e:
            st.error(f"Error fetching user trend data: {e}")
    
    with col2:
        st.markdown("### 🏅 State-wise User Rankings")
        try:
            query = f"""
            SELECT State, SUM(RegisteredUsers) as Total_Users, SUM(AppOpens) as Total_Opens
            FROM map_user 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                AND RegisteredUsers > 0
            GROUP BY State 
            ORDER BY Total_Users DESC 
            LIMIT 15
            """
            
            # Try alternative column names if first query fails
            try:
                mycursor.execute(query)
                result = mycursor.fetchall()
            except:
                query = f"""
                SELECT State, SUM(Registered_users) as Total_Users, SUM(App_opens) as Total_Opens
                FROM map_user 
                WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                    AND Registered_users > 0
                GROUP BY State 
                ORDER BY Total_Users DESC 
                LIMIT 15
                """
                mycursor.execute(query)
                result = mycursor.fetchall()
            
            if result:
                df = pd.DataFrame(result, columns=['State', 'Total_Users', 'Total_Opens'])
                
                # Convert to float safely
                df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
                df['Total_Opens'] = df['Total_Opens'].apply(safe_float_conversion)
                
                # Clean state names
                df['State'] = df['State'].str.replace('-', ' ').str.title()
                
                # Calculate engagement metrics
                df['Engagement_Score'] = df.apply(
                    lambda row: safe_float_conversion(row['Total_Opens'] / row['Total_Users']) 
                    if row['Total_Users'] > 0 else 0, axis=1
                )
                
                fig = px.bar(df, x='State', y='Total_Users',
                           title=f'State Rankings by User Base (Q{selected_quarter} {selected_year})',
                           color='Engagement_Score',
                           color_continuous_scale='plasma',
                           text='Total_Users')
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show rankings with serial numbers
                st.markdown("#### State Rankings")
                df_display = df[['State', 'Total_Users', 'Total_Opens', 'Engagement_Score']].copy()
                df_display['Total_Users'] = df_display['Total_Users'].astype(int)
                df_display['Total_Opens'] = df_display['Total_Opens'].astype(int)
                df_display['Engagement_Score'] = df_display['Engagement_Score'].round(2)
                df_display.index = range(1, len(df_display) + 1)
                st.dataframe(df_display, use_container_width=True)
            else:
                st.warning("No state ranking data available")
        except Exception as e:
            st.error(f"Error fetching state ranking data: {e}")

# 6. Geo Analysis
elif selected == "Geo Analysis":
        # 🗺️ User Distribution Analysis
    st.markdown("### 👥 User Distribution Analysis")

    try:
        # Try different column name variations
        possible_queries = [
            f"""
            SELECT State, SUM(RegisteredUsers) as Total_Users, SUM(AppOpens) as Total_Opens
            FROM map_user 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                AND RegisteredUsers > 0
            GROUP BY State 
            ORDER BY Total_Users DESC
            """,
            f"""
            SELECT State, SUM(Registered_users) as Total_Users, SUM(App_opens) as Total_Opens
            FROM map_user 
            WHERE Year = {selected_year} AND Quarter = {selected_quarter}
                AND Registered_users > 0
            GROUP BY State 
            ORDER BY Total_Users DESC
            """
        ]
        
        result = None
        for query in possible_queries:
            try:
                mycursor.execute(query)
                result = mycursor.fetchall()
                if result:
                    break
            except Exception as query_error:
                continue

        if result:
            # Convert query result to DataFrame
            df = pd.DataFrame(result, columns=['State', 'Total_Users', 'Total_Opens'])

            # Convert to float safely
            df['Total_Users'] = df['Total_Users'].apply(safe_float_conversion)
            df['Total_Opens'] = df['Total_Opens'].apply(safe_float_conversion)

            # Clean state names
            df['State_Clean'] = df['State'].str.replace('-', ' ').str.title()

            # Calculate engagement rate
            df['Engagement_Rate'] = df.apply(
                lambda row: safe_float_conversion(row['Total_Opens'] / row['Total_Users'])
                if row['Total_Users'] > 0 else 0, axis=1
            )

            # Create bubble chart visualization
            fig = px.scatter(
                df, 
                x='Total_Users', 
                y='Total_Opens', 
                size='Engagement_Rate', 
                hover_name='State_Clean',
                title=f'User Distribution & Engagement (Q{selected_quarter} {selected_year})',
                color='Engagement_Rate',
                color_continuous_scale='viridis',
                labels={'Total_Users': 'Registered Users', 'Total_Opens': 'App Opens'}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Display tables side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Highest User States")
                user_states = df.head(10).copy()
                user_states['Total_Users'] = user_states['Total_Users'].astype(int)
                user_states['Total_Opens'] = user_states['Total_Opens'].astype(int)
                user_states['Engagement_Rate'] = user_states['Engagement_Rate'].round(2)
                user_states.index = range(1, len(user_states) + 1)
                st.dataframe(
                    user_states[['State_Clean', 'Total_Users', 'Total_Opens', 'Engagement_Rate']],
                    use_container_width=True
                )
            
            with col2:
                st.markdown("#### Best Engagement States")
                engagement_states = df.sort_values('Engagement_Rate', ascending=False).head(10).copy()
                engagement_states['Total_Users'] = engagement_states['Total_Users'].astype(int)
                engagement_states['Engagement_Rate'] = engagement_states['Engagement_Rate'].round(2)
                engagement_states.index = range(1, len(engagement_states) + 1)
                st.dataframe(
                    engagement_states[['State_Clean', 'Total_Users', 'Engagement_Rate']],
                    use_container_width=True
                )

        else:
            st.warning("No user distribution data available")

    except Exception as e:
        st.error(f"Error in user distribution analysis: {e}")


# Summary and Insights Section
st.markdown("---")
st.markdown('<h2 class="sub-header">📈 Key Insights & Business Recommendations</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 Market Penetration Insights
    - Focus on high-potential, low-adoption states
    - Strengthen presence in tier-2 and tier-3 cities
    - Leverage successful state strategies for expansion
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 📱 Technology Adoption
    - Optimize app performance for popular device brands
    - Enhance user experience based on engagement patterns
    - Develop targeted features for different user segments
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 💰 Revenue Optimization
    - Increase transaction frequency in high-value states
    - Develop premium services for affluent user segments
    - Focus on insurance and financial product cross-selling
    """)
    st.markdown('</div>', unsafe_allow_html=True)


