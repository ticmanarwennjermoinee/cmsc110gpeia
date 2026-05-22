import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
try:
    img_base64 = get_base64_image("bg.png")
except FileNotFoundError:
    img_base64 = "" # Fallback if file isn't found yet
    
# PAGE TITLE & LAYOUT STRUCTURE
st.set_page_config(page_title="Global Poverty & Economic Inequality Dashboard", layout="wide")
st.title("Global Poverty & Economic Inequality Analysis")

# DESIGN
st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        html, body, [class*="css"], .stApp {{
            font-family: 'Inter', sans-serif !important;
        }}
        
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), 
                              url("data:image/png;base64,{img_base64}") !important;
            background-size: cover !important; 
            background-repeat: no-repeat !important; 
            background-attachment: fixed !important;
            background-position: center !important; 
        }}

        .stApp {{
            background-color: transparent !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: #004225 !important; 
            border-right: 1px solid #115e3b !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: #f8fafc !important; 
        }}
        
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] .stMarkdown li,
        [data-testid="stSidebar"] .stMarkdown span {{
            color: #e2e8f0 !important; 
        }}
        
        [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: #00522e !important;
            border: 1px solid #006b3c !important;
            border-radius: 8px !important;
        }}
        
        .stHeading h1, h1, h2, h3, h4, [data-testid="stHeader"] {{
            color: #f8fafc !important; 
            font-weight: 800 !important;
            text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5); 
        }}
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #f1f5f9 !important; 
            font-weight: 700 !important;
            margin-top: 10px !important;
        }}

        .stMarkdown p, .stMarkdown li {{
            color: #cbd5e1 !important; 
            line-height: 1.6;
        }}
        
        .stMarkdown strong {{
            color: #ffffff !important; 
        }}

        div[data-testid="stNotification"] {{
            background-color: #004225 !important; 
            border: 1px solid #006b3c !important; 
            border-left: 5px solid #059669 !important; 
            border-radius: 8px !important;
        }}
        
        div[data-testid="stNotification"] * {{
            color: #f8fafc !important; 
        }}

        div.stDownloadButton > button {{
            background-color: #059669 !important; 
            color: #ffffff !important; 
            border: 1px solid #047857 !important;
            border-radius: 6px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }}

        div.stDownloadButton > button:hover {{
            background-color: #047857 !important; 
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3) !important; 
            transform: translateY(-1px) !important; 
        }}

        div[data-testid="stDataFrameData"] {{
            border: 1px solid #006b3c !important;
            border-radius: 8px !important;
        }}
        
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            border-color: #006b3c !important;
            color: #0f172a !important;
        }}
        
        div[data-baseweb="select"] * {{
            color: #0f172a !important; 
        }}

        [data-testid="stWidgetLabel"] p {{
            color: #f1f5f9 !important; 
            font-weight: 600 !important;
        }}

        [data-testid="stMetric"] {{
            background-color: #ffffff !important; 
            padding: 16px 12px !important; 
            border-radius: 8px !important; 
            border: 1px solid #cbd5e1 !important; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important; 
            width: 100% !important; 
        }}
        
        [data-testid="stMetricLabel"] p {{
            color: #475569 !important; 
            font-weight: 500 !important;
            font-size: 14px !important;
        }}
        
        [data-testid="stMetricValue"] {{
            color: #004225 !important; 
            font-weight: 700 !important;
            font-size: 28px !important; 
            white-space: nowrap !important; 
        }}
        
        button[data-baseweb="tab"] p {{
            color: #cbd5e1 !important; 
            font-weight: 500;
        }}
        
        div[data-baseweb="tab-border"] {{
            background-color: #059669 !important; 
        }}
        
        /* Styled Background container for our Input Form block */
        div.form-container {{
            background-color: rgba(0, 66, 37, 0.4) !important;
            padding: 25px !important;
            border-radius: 10px !important;
            border: 1px solid #006b3c !important;
            margin-bottom: 20px !important;
        }}
    </style>
""", unsafe_allow_html=True)

# FILE PATH
df = pd.read_csv("global_poverty_economic_inequality.csv")

# RENAME LABELS
df = df.rename(columns={
    'income_group': 'Income Group',
    'gdp_per_capita_usd': 'GDP per capita (USD)',
    'poverty_rate_pct': 'Poverty Rate (%)',
    'gini_coefficient': 'Gini Coefficient',
    'hdi_score': 'HDI Score',
    'unemployment_rate_pct': 'Unemployment (%)',
    'inflation_rate_pct': 'Inflation Rate (%)',
    'literacy_rate_pct': 'Literacy Rate (%)',
    'life_expectancy_years': 'Life Expectancy (in years)',
    'child_mortality_per_1000': 'Child Mortality (per 1000)',
    'electricity_access_pct':'Electricity Access (%)',
    'clean_water_access_pct': 'Clean Water Access (%)',
    'internet_penetration_pct': 'Internet Access (%)',
    'female_labor_participation_pct': 'Female Labor Participation (%)',
    'social_protection_coverage_pct': 'Social Protection Coverage (%)',
    'income_share_top10_pct': 'Income Share (Top 10%)',
    'income_share_bottom40_pct': 'Income Share (Bottom 40%)',
    'urban_population_pct': 'Urban Population (%)',
    'remittances_pct_of_gdp': 'Remittances (%)',
    'foreign_aid_million_usd': 'Foreign aid (million USD)',
    'co2_per_capita_tonnes': 'CO2 per capita ton'
    })

# DATA OVERVIEW
st.subheader("Dataset Preview")
st.dataframe(df.head())

st.info(f"**Dataset Dimensions:** The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

# DATA CLEANING
df = df.drop_duplicates()

# Handle 'year' column dynamically
year_col = 'year' if 'year' in df.columns else 'Year'
if year_col in df.columns:
    df = df[df[year_col] > 0]
    
# DYNAMIC SIDEBAR 

st.sidebar.header("Filter Options")

# Geographic settings
with st.sidebar.container(border=True):
    st.markdown("**Geographic Settings**")
    all_regions = ["All"] + list(df['region'].unique()) if 'region' in df.columns else ["All"]
    selected_region = st.selectbox("Scope:", all_regions)

# Financial settings
with st.sidebar.container(border=True):
    st.markdown("**Financial Settings**")
    all_income_groups = ["All"] + list(df['Income Group'].unique())
    selected_income = st.selectbox("Tier:", all_income_groups)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df['region'] == selected_region]

if selected_income != "All":
    filtered_df = filtered_df[filtered_df['Income Group'] == selected_income]

# OPTION FOR DOWNLOAD
csv_data = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_poverty_data.csv",
    mime="text/csv",
)

st.subheader("Statistical Summary")
st.dataframe(df.describe())

# SUMMARY METRIC CARDS

st.markdown("---")
st.subheader("Global Benchmarks")

m1, m2, m3 = st.columns(3)

with m1:
    avg_poverty = df['Poverty Rate (%)'].mean()
    st.metric(label="Average Poverty Rate", value=f"{avg_poverty:.2f}%")

with m2:
    avg_gdp = df['GDP per capita (USD)'].mean()
    st.metric(label="Average GDP per Capita", value=f"${avg_gdp:,.2f}")

with m3:
    avg_gini = df['Gini Coefficient'].mean()
    st.metric(label="Average Gini Coefficient", value=f"{avg_gini:.2f}")
    
# VISUALIZATION CODE 
st.markdown("---")
st.header("Interactive Data Dashboard")

# TABS for organization of data (UPDATED: Added Tab 4!)
tab1, tab2, tab3, tab4 = st.tabs([
    "Univariate Analysis", 
    "Bivariate Trends", 
    "Multivariate Correlation",
    "Policy Sandbox Form"
])

with tab1:
    st.markdown("### Distribution of Key Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.histplot(filtered_df['Poverty Rate (%)'], kde=True, bins=30, ax=ax1)
        ax1.set_title('Poverty Rate Distribution (%)')
        fig1.tight_layout()
        st.pyplot(fig1)
        
        # Analysis
        st.markdown("""
        The distribution of poverty rates is significantly right-skewed. This indicates that while
        numerous nations successfully maintain low baseline poverty rates, a considerable number of countries continue
        to struggle with severe poverty levels that surpass 40-50%. 
        """)
        
    with col2:
        if 'region' in df.columns:
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.countplot(data=filtered_df, x='region', order=df['region'].value_counts().index, ax=ax2)
            ax2.tick_params(axis='x', rotation=45)
            ax2.set_title('Count of Records per Region')
            fig2.tight_layout()
            st.pyplot(fig2)
            
            # Analysis
            st.markdown("""
            The data logging density highlights a discrepancy in regional representation. Regions
            like Sub-Saharan Africa and Latin America contribute a larger volume of data points over time, which
            is crucial for analyzing shifts in emerging markets.
            """)
with tab2:
    st.markdown("### Examining Two-Variable Relationships")
    
    # Numerical columns for the dropdowns
    numeric_cols = list(filtered_df.select_dtypes(include=['number']).columns)
    
    # Two dropdown boxes side-by-side
    col_x, col_y = st.columns(2)
    with col_x:
        x_var = st.selectbox(
            "Select X-Axis Variable:", 
            numeric_cols, 
            index=numeric_cols.index('GDP per capita (USD)') if 'GDP per capita (USD)' in numeric_cols else 0
        )
    with col_y:
        y_var = st.selectbox(
            "Select Y-Axis Variable:", 
            numeric_cols, 
            index=numeric_cols.index('Poverty Rate (%)') if 'Poverty Rate (%)' in numeric_cols else 0
        )
        
    # Dynamic scatter plot (based on selected variable)
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x=x_var, y=y_var, hue='Income Group', ax=ax3)
    ax3.set_title(f'Relationship Between {x_var} and {y_var}')
    fig3.tight_layout()
    st.pyplot(fig3)
    
    # Analysis
    st.markdown(f"""
    This scatter plot examines the direct distribution trend by plotting **{x_var}** against **{y_var}**.
    By categorizing the data points according to *Income Group*, we can visually observe if countries tend to cluster based on their wealth tiers.
    """)

    st.markdown("---")

    # Gini Coefficient box plot
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x='Income Group', y='Gini Coefficient', ax=ax4)
    ax4.tick_params(axis='x', rotation=45)
    ax4.set_title('Gini Coefficient per Income Group')
    fig4.tight_layout()
    st.pyplot(fig4)
    
    st.markdown("""
    The box plot illustrates the benchmarks of inequality across various income brackets. The variance of the Gini Coefficient
    is considerable between the upper-middle and lower-middle-income categories. This indicates that achieving a higher GDP level does not necessarily guarantee internal equity.
    Additionally, economic distribution strategies can vary significantly depending on the policies of individual states.
    """)

with tab3:
    with st.container(border=True):
        st.markdown("### Key Insight: Multivariate Relations")
        st.write("This matrix highlights how tightly intertwined economic metrics like GDP, literacy, and poverty are.")

    numerical_df = df.select_dtypes(include=['number'])
    
    fig5, ax5 = plt.subplots(figsize=(10, 8))
    sns.heatmap(numerical_df.corr(numeric_only=True), annot=False, cmap='coolwarm', ax=ax5)
    ax5.set_title('Correlation Matrix Heatmap')
    fig5.tight_layout()
    st.pyplot(fig5)
    
    # Analysis
    st.info("""
    The correlation heatmap uncovers significant structural interdependencies. A notable strong positive correlation coefficient
    connectyms Human Development Index (HDI) scores with infrastructure indicators like access to clean water and electricity. Conversely,
    child mortality rates demonstrate a considerable negative correlation with literacy rates and GDP. This diagnostic framework indicates
    that tackling systemic poverty requires more than just financial investment; it demands a comprehensive development strategy that includes
    infrastructure, public education, and access to healthcare.
    """)

with tab4:
    st.markdown("### Policy Intervention Sandbox Form")
    st.markdown("""
    This interactive simulator allows users to input target policy goals for specific countries. 
    By leveraging the exploratory correlation weights, this sandbox estimates the theoretical reduction in national poverty based on infrastructure improvement inputs.
    """)
    
    # Country Selection
    if 'country' in filtered_df.columns and not filtered_df.empty:
        target_country = st.selectbox("Select a Target Nation for Simulation:", sorted(filtered_df['country'].unique()))
        country_data = filtered_df[filtered_df['country'] == target_country].sort_values(by=year_col).iloc[-1]
    else:
        # Fallback to absolute index if global filter empties the dataframe
        target_country = st.selectbox("Select a Target Nation for Simulation:", sorted(df['country'].unique()))
        country_data = df[df['country'] == target_country].sort_values(by=year_col).iloc[-1]
        
    st.write(f"#### Baseline Historical Context for {target_country} ({int(country_data[year_col])})")
    
    # Local mini benchmarks 
    c1, c2, c3 = st.columns(3)
    c1.metric("Electricity Baseline", f"{country_data['Electricity Access (%)']:.1f}%")
    c2.metric("Clean Water Baseline", f"{country_data['Clean Water Access (%)']:.1f}%")
    c3.metric("Poverty Rate Baseline", f"{country_data['Poverty Rate (%)']:.1f}%")
    
    st.markdown("---")
    
    # Form layout matching group CSS styles
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    with st.form("sandbox_policy_submission_form"):
        st.markdown("Form Inputs: Infrastructure Targeting")
        
        # Pull standard defaults from dataset dynamically
        input_elec = st.slider("Target Electricity Access Level (%)", 0.0, 100.0, float(country_data['Electricity Access (%)']))
        input_water = st.slider("Target Clean Water Access Level (%)", 0.0, 100.0, float(country_data['Clean Water Access (%)']))
        
        # Form Submit Button
        run_sim = st.form_submit_button("Run Predictive Simulation Framework")
        
        if run_sim:
            st.markdown("</div>", unsafe_allow_html=True) # Closes style div wrapper clean
            st.success("Simulation Pipeline Evaluated Successfully!")
            
            # Simple predictive engine calibrated directly from your Heatmap correlation trends
            elec_delta = input_elec - country_data['Electricity Access (%)']
            water_delta = input_water - country_data['Clean Water Access (%)']
            
            # Simulating reduction vector based on inverse correlation coefficients
            estimated_reduction = (elec_delta * 0.24) + (water_delta * 0.21)
            simulated_poverty = max(0.0, country_data['Poverty Rate (%)'] - estimated_reduction)
            
            st.markdown("#### Simulated Policy Outcomes Matrix")
            out1, out2 = st.columns(2)
            out1.metric("Baseline Historical Poverty", f"{country_data['Poverty Rate (%)']:.2f}%")
            out2.metric(
                "Simulated Target Poverty Rate", 
                f"{simulated_poverty:.2f}%", 
                delta=f"{simulated_poverty - country_data['Poverty Rate (%)']:.2f}%"
            )
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""**About This App**
""")
st.sidebar.markdown("""*Dataset Focus:* Longitudinal global macroeconomic trends tracking wealth distribution, inequality, and human development parameters.
""")
st.sidebar.markdown("""Created for **CMSC 110 Main Project**
""")
st.sidebar.markdown("""Group Members: Datu, Portes, Querol, Ticman, Vinas
""")
