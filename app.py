import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import plotly.figure_factory as ff
st.set_page_config(layout = 'wide', page_title = 'Marketing Data Analysis ')
st.title("Marketing Data Analysis Dashboard")
tab1,tab2,tab3=st.tabs (['Introduction','Data exploration','Data analysis'])
with tab1:
 st.header('Analysis of Marketing Data',divider=True)
 #st.subheader("    Overview   ")
 st.latex(r'''\textbf{\LARGE Overview}''')
 #st.latex(r'''\text{numerical Descriptive Statistics}''')sntax
 st.latex(r'''\text{The dataset contains customer marketing data with 2240 records and 29 columns.}\\
           \text{It Includes demographic information, purchase history, campaign responses, and customer behavior metrics.}''')   
 #st.text('The dataset contains customer marketing data with 2240 records and 29 columns.\n'
 #'It Includes demographic information, purchase history, campaign responses, and customer behavior metrics.')
 st.markdown("""### Key Variables""")     
 #st.subheader(" Key Variables")
 st.markdown ("""
             - **Demographics:** ID, Year_Birth, Education, Marital_Status, Income, Country.
            - **Household:** Kidhome, Teenhome.
           - **Purchase Behavior:** MntWines, MntFruits, MntMeatProducts, etc.
           - **Marketing Response:** AcceptedCmp1-5, Response, Complain.
           - **Purchase Channels:** NumDealsPurchases, NumWebPurchases, NumCatalogPurchases, NumStorePurchases.
           -  **Web Activity:** NumWebVisitsMonth
           - **Recency:** Days since last purchase.
           """)

 st.subheader("Initial Observations")

 st.markdown("""
       ##  Data Overview
       
       ### 1- Data Quality Assessment
        **Missing Values Detected:**  
       -  Income  field contains missing values that may require imputation
       
       ### 2- Demographic Insights
        **Age Distribution:**  
       - Customers born between 1893-1996 (verify extreme values)  
       - Potential data quality issue with pre-1940 births  
       
       **Education Levels:**  
       - Basic (High School)  
       - 2n Cycle (Some College)  
       - Graduation (Bachelor's)  
       - Master  
       - PhD  
       
        **Geographic Coverage:**  
       8 countries represented:  
       1. Spain (notable high spenders)  
       2. USA  
       3. Canada  
       4. Australia  
       5. India  
       6. Germany  
       7. Saudi Arabia  
       8. Mexico  
       
       ### 3- Purchase Behavior Patterns
        **Spending Distribution:**  
       - Wide range in spending amounts across product categories 
       - Some customers have very high spending in spain
       """)
 st.subheader("Potential Analysis Directions")

 st.markdown("""
   1- Customer Segmentation:")
  - Cluster customers based on demographics and purchase behavior
         Identify high-value customer segments.

     2- Campaign Effectiveness:
  - Analyze response rates to different campaigns (AcceptedCmp1-5)
        Identify which customer segments respond best.
        
       3- Churn Analysis:
  - Identify customers who are at risk of churning 
      and understand the factors contributing to churn.
           """)
with tab2:
    st.markdown("""
       ## Data Preprocessing Steps
       
       ### 1-Handle Missing Values
       **Justification:**
       - Missing data exists in only one column (Income)
       - Constitutes <5% of total data
       - Dropping these rows preserves data integrity without introducing bias from imputation
       
       ### 2- Calculate Customer Age
       **Justification:**
       - The maximum value in Dt_Customer is 2014 (latest birth year in dataset)
       - Assumes data was collected in 2012-2014, making this the baseline year for age calculation
       
       ### 3- Remove Outliers (Ages > 80)
       
       ### 4- Set Customer ID as Index
       ### 5-Create Total Spending Feature
       ### 6- Create Total Purchases Feature
       ### 7- Convert Customer Enrollment Date to Datetime Format
   
       """)
    
    df = pd.read_csv('marketing_data.csv')
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
    df['Age'] =2014  - df['Year_Birth']
    age_more_100 = df[df['Age'] >80] 
    age_more_100=age_more_100.index
    df.drop(age_more_100, inplace=True)
    df.dropna(inplace=True)
    df.set_index('ID', inplace=True, drop=True)
    # Calculate Total Spending
    df['Total_Spending'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
    # Calculate Total Purchases
    df['Total_Purchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
    
    st.latex(r'''\text{Descriptive Statistics for Categorical Columns}''')
    basic_statistics_category=df.describe(include='O').T
    st.table(basic_statistics_category) 
    st.latex(r'''\text{numerical Descriptive Statistics}''')
    st.table(df.describe().T)


with tab3:
   st.subheader("1. Customer Segmentation:-")
   st.latex(r'''\text{1-1What are the key customer segments based on spending habits ( high spenders, moderate spenders, low spenders)?}''')
   df['Spending_Segment'] = pd.qcut(df['Total_Spending'], q=[0, 0.33, 0.66, 1], labels=['Low Spender', 'Moderate Spender', 'High Spender'])
   segment_counts = df['Spending_Segment'].value_counts()
   segment_summary = df.groupby('Spending_Segment')['Total_Spending'].describe()
   fig1 = px.pie(names=segment_counts.index, values=segment_counts.values, title='Spending Segment Distribution')
   fig2=px.box(df, x='Spending_Segment', y='Total_Spending', title='Spending Distribution by Segment')
   fig_1 = make_subplots(rows=1, cols=2, subplot_titles=['Spending Distribution by Segment', 'Spending Segment Distribution'],
                   specs=[[{'type': 'box'}, {'type': 'pie'}]])
   fig_1.add_trace(fig1.data[0], row=1, col=2)
   fig_1.add_trace(fig2.data[0], row=1, col=1)
   st.plotly_chart(fig_1, use_container_width=True)
   st.subheader("Customers have been categorized into 3 key segments based on spending behavior:")
   st.markdown(""" 
    - **High Spenders** :Top revenue contributors
    - **Moderate Spenders** :Growth potential
     - **Low Spenders**:Price-sensitive
     """)
   
   st.subheader("Recommendations")
   st.markdown("""
   - **High Spenders**: VIP programs with exclusive benefits
   - **Moderate Spenders**: Cross-selling opportunities
   - **Low Spenders**: Cost-efficient digital engagement
   """)
   st.latex(r'''\text{2-1How do customer demographics (age, income, education, marital status) vary across spending segments?}''')
   df['Spending_Segment'] = pd.qcut(df['Total_Spending'], q=[0, 0.33, 0.66, 1], labels=['Low Spender', 'Moderate Spender', 'High Spender'])
   demographic_analysis=df.groupby('Spending_Segment')[['Age', ' Income ', 'Education', 'Marital_Status']].value_counts()

   
   st.latex(r'''\text{3-1Which products (wine, fruits, meat, etc.) are most popular among different customer segments?}''')
   product_analysis = df.groupby('Spending_Segment')[[ 'MntWines', 'MntFruits',
      'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts',
      'MntGoldProds', ]].sum()
   fig_2= px.bar(product_analysis, barmode='group', title='Product Popularity by Spending Segment')
   st.plotly_chart(fig_2)
   st.markdown("""
   - **High Spenders:** This segment shows the highest popularity for MatWines and MatGoldProds,
                      'indicating a preference for premium products like wines and gold-labeled items. 
    - **Moderate Spenders:** They exhibit balanced popularity across most products, 
             'with notable interest in MatFishProducts and NumWebPurchases, suggesting a mix of online shopping and seafood consumption. 
     - **low spenders:** This segment has the lowest overall popularity but shows relatively higher interest in NumStorePurchases and basic products like
     MatSweetProducts, indicating a preference for in-store shopping and affordable sweet items.       """)


   st.latex(r'''\text{4-1 What products (wine, fruits, meat, etc.) are most popular among different countries?}''')
   country_analysis = df.groupby('Country')[['MntWines', 'MntFruits',
      'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts',
      'MntGoldProds']].sum()
   fig_3= px.bar(country_analysis, barmode='group', title='Product Popularity by Country')
   st.plotly_chart(fig_3)
   
   st.markdown("""
               - Wines (Marivlines) dominate in USA and Spain.
               - Meat (MidMealfProducts) is highly popular in Germany, Spain, and the USA.
               - Sweets (MidSweetProducts) are a standout in India.
               - Fruits (Maffruits) and Fish (MafftabiProducts) are preferred in Mexico.
               - Premium/Luxury (MidGoldPonds) products are notable in Saudi Arabia.
                                       """)
 
   st.latex(r'''\text{5-1 Are there differences in purchase channels (web, catalog, store) across customer segments?}''')
   channel_analysis = df.groupby('Spending_Segment')[['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
   ].sum()
   fig_4= px.bar(channel_analysis, barmode='group', title='Purchase Channels by Spending Segment')
   st.plotly_chart(fig_4)

   st.markdown(""" **High Spenders:-**
   - **Omnichannel Dominance**: Lead in web, catalog, and store purchases.
   - **Catalog Preference**: Favored for curated/premium offerings (e.g., exclusive deals, high-end products).
   - **Why?** Convenience + personalized shopping experiences.
   """)

   st.markdown("""**Moderate Spenders:-**
   - **Web-First**: Prefer online purchases (balance of convenience and cost).
   - **Why?** Competitive pricing, easy comparison, and delivery options.
   """)

   st.markdown("""  **Low Spenders:-**
   - **In-Store Focus**: Rely on physical stores for budget control and immediate access.
   - **Why?** Avoid shipping fees, cash transactions, and instant gratification.
   """)
   
   st.latex(r'''\text{6-1How does the presence of children or teenagers in the household affect spending behavior?}''')
   df['Has_Children'] = (df['Kidhome'] > 0) | (df['Teenhome'] > 0)
   spending_by_children = df.groupby('Has_Children')['Total_Spending'].count() 
   fig_5=px.pie(names=spending_by_children.index, values=spending_by_children.values, title='Spending Distribution by Children')
   st.plotly_chart(fig_5)
   st.markdown("""
           **The data shows a 71.4% to 28.6% split, indicating that:**
               - Households with children/teens account for 71.4% of spending.
                   - Households without children/teens account for 28.6% of spending.
                       """)

   st.markdown("""
               **Recommendations:**
               - **For Families:** Target with bundled offers ("Family Packs"), back-to-school promotions, or child-friendly product lines.
                   - **For Childless Households:** Focus on premium/individualized products or experiences.
                               """)
   
   st.subheader("2. Campaign Analysis:-")
   
   st.latex(r'''\text{1-2/Which marketing campaign (Cmp1, Cmp2, Cmp3, Cmp4, Cmp5) was the most successful in terms of customer acceptance?}''')
   campaign_acceptance = df[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']].sum()
   total_customers = len(df)
   campaign_acceptance_rate = (campaign_acceptance / total_customers) * 100
   campaign_results = pd.DataFrame({
   'Campaign': ['Cmp1', 'Cmp2', 'Cmp3', 'Cmp4', 'Cmp5'],
   'Total_Acceptances': campaign_acceptance,
   'Acceptance_Rate': campaign_acceptance_rate})
   campaign_results
   fig1_2=  px.bar(campaign_results, x='Campaign', y='Acceptance_Rate', title='Campaign Acceptance Rate',height=800 ,width=800)
   fig1_2.update_layout(xaxis_title='Campaign', yaxis_title='Acceptance Rate')
   st.plotly_chart(fig1_2)
   st.markdown("""
       **Campaign Success Ranking:**
       - **Cmp4:** 21.7% (Most successful)
       - **Cmp1:** 21.4%
               - **Cmp2:**
           - **Cmp5:** 4.56% (Least successful)
               """)
 
   st.latex(r'''\text{2-2 Do customers who accepted campaigns have higher spending or purchase frequency compared to those who did not?}''')
   df['Accepted_Any_Campaign'] = df[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']].max(axis=1)
   spending_by_acceptance = df.groupby('Accepted_Any_Campaign')['Total_Spending',].mean().reset_index()

   fig1=px.pie(names=spending_by_acceptance['Accepted_Any_Campaign'], values=spending_by_acceptance['Total_Spending'], title='Spending Distribution by Acceptance')
   Purchases_by_acceptance = df.groupby('Accepted_Any_Campaign')['Total_Purchases'].mean()

   fig2=px.pie(names=Purchases_by_acceptance.index, values=Purchases_by_acceptance.values, title='Purchases Distribution by Acceptance')
   
   fig2_2= make_subplots(rows=1, cols=2, subplot_titles=['Spending Distribution by Acceptance', 'Purchases Distribution by Acceptance'],
                   specs=[[{'type': 'pie'}, {'type': 'pie'}]])
   
   fig2_2.add_trace(fig1.data[0], row=1, col=1)
   fig2_2.add_trace(fig2.data[0], row=1, col=2)
   st.plotly_chart(fig2_2)
   st.markdown("""
       **Interpretation:**
       - **Higher Value**: Customers who accept campaigns are both bigger spenders and more frequent buyers.
       - **Loyalty Link:** Acceptance may indicate engaged customers predisposed to spend more.
       - **Revenue Impact:** Targeting acceptors likely yields better ROI due to their higher lifetime value.
                   """)
   st.markdown(""" **Recommendations:**""")
   st.markdown(""" **Double Down on Acceptors:**
    - Offer exclusive rewards to maintain their engagement.
    - Use cross-selling ( Customers like you also bought).
    """)
   st.markdown("""**Convert Non-Acceptors:**
    - Test smaller incentives (e.g., free samples vs. discounts).
   - Improve targeting (e.g., identify high-spenders who rarely accept campaigns).
   """)

   
   st.latex(r'''\text{2-3/How does the recency of purchases (Recency) influence campaign acceptance?}''')
   
   recency_acceptance = df.groupby('Accepted_Any_Campaign')['Recency'].mean()
   recency_acceptance
   fig2_3=px.pie(names=recency_acceptance.index, values=recency_acceptance.values, title='Acceptance Rate by Recency')
   st.plotly_chart(fig2_3)
   st.markdown("""
           **Recent Purchasers (Recency = 0):**
                   - Show a **50.8% acceptance rate** 
                       - Indicates customers are most receptive to campaigns immediately after a purchase

       **Less Recent Purchasers (Recency = 1):**
               - Have a **40.4% acceptance rate** 
                 - Suggests receptiveness declines as time passes since last purchase
                       """)
   
   st.latex(r'''\text{2-4Are there differences in campaign acceptance rates across countries?}''')
   
   country_acceptance_rate = df.groupby('Country')['Accepted_Any_Campaign'].mean()
   country_acceptance_rate.columns = ['Country', 'Acceptance_Rate']
   
   country_acceptance_rate
   fig2_4=px.pie(names=country_acceptance_rate.index, values=country_acceptance_rate.values, title='Acceptance Rate by Country')
   st.plotly_chart(fig2_4)
   st.markdown("""
          **Campaign Acceptance Rates by Country (Highest to Lowest):**
                   - **USA:** 19.3% (Highest acceptance)
                       - **Australia:** 18.0%
                       - **Canada:** 14.0%
                       - **India:** 12.7%
                   - **Saudi Arabia:** 12.2%
                   - **Germany:** 11.3%
                   - **Mexico:** 10.8%
                   - **Spain:** 8.6% (Lowest acceptance)

                       **Results:**
                       
                       **Top Performers:**
                       - USA leads with 19.3% acceptance - likely due to higher digital engagement
                       - Australia follows closely at 18.0% - suggesting cultural receptiveness
                       
                       **Mid-Tier Markets:**
                       - Canada (14.0%) and India (12.7%) show moderate acceptance
                       - Saudi Arabia (12.2%) performs slightly below this group
                       
                       **Lower Acceptance:**
                       - Spain has the lowest acceptance at 8.6% - may indicate cultural resistance or market saturation
                       - Germany (11.3%) and Mexico (10.8%) also show below-average performance
                       """)
   
   
   st.subheader("3-Churn Analysis:-")

   st.latex(r'''\text{3-1/What is the relationship between Recency (days since last purchase) and churn}''')

   df['Churn'] = df['Recency'].apply(lambda x: 1 if x > 90 else 0)
   churn_analysis = df.groupby('Churn')[['Recency','Total_Spending', 'Total_Purchases']].mean().reset_index()
   churn_analysis.columns = ['Churn', 'Mean_Recency', 'Mean_Total_Spending', 'Mean_Total_Purchases']
   churn_analysis

   complain_churn = df.groupby('Complain')['Churn'].mean().reset_index()
   complain_churn
   fig3_2=px.pie(names=complain_churn['Complain'], values=complain_churn['Churn'], title='Churn Rate by Complain')
   st.plotly_chart(fig3_2)
   st.markdown("""
   **Churn Rate Analysis:**
   - **Customers Who Complained:** 63.3% churn rate
   - **Customers Who Didn't Complain:** 36.7% churn rate
   
   **Interpretation:**
   
   **Complaints Double Churn Risk:**
   - Customers who file complaints are **1.7x more likely** to churn than non-complainers
   -  **Implication:** Unresolved complaints dramatically increase customer attrition
   
   **Critical Warning Sign:**
   - A complaint is a **strong predictor of churn** - nearly 2/3 of complainers leave
   - This represents a **72% higher churn probability** compared to non-complainers
   """)
   st.latex(r'''\text{3\_2-How does spending behavior (Total\_Spending) correlate with churn?}''')

   spending_churn = df.groupby('Churn')['Total_Spending'].count().reset_index()
   spending_churn.columns = ['Churn', 'Total_Spending']
   spending_churn
   fig3_3=px.pie(names=spending_churn['Churn'], values=spending_churn['Total_Spending'], title='Churn Rate by Spending')
   st.plotly_chart(fig3_3)
   st.markdown("""
       **Stark Contrast in Churn Rates**
       
       **Spending Segmentation:**
       -  **Low Spenders:** 91.2% churn rate
       -  **High Spenders:** 8.77% churn rate
       
       ---
       
       Interpretation
       
       **Low Spenders**
       - Customers with minimal spending churn at **91.2%** 
       - **Likely Reasons:**
         - Price sensitivity 
         - Lack of engagement with your brand
         - One-time purchasers with no loyalty
       
       **High Spenders Are Loyal**
       - Only **8.77%** churn rate - these customers are *
       - **Why They Stay:**
         - Perceive higher value in your offerings
         - Receive better service/attention
         - Less price-sensitive
         - More emotionally invested in your brand
          """)

   st.latex(r'''\text{3-3/Are there differences in churn rates across demographic groups (age, income, marital status)?}''')

   df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], labels=['20-30', '30-40', '40-50', '50-60', '60+'])
   age_churn = df.groupby('Age_Group')['Churn'].mean().reset_index()
   age_churn.columns = ['Age_Group', 'Churn_Rate']
   df['Income_Group'] = pd.qcut(df[' Income '], q=[0, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])
   income_churn = df.groupby('Income_Group')['Churn'].mean().reset_index()
   income_churn.columns = ['Income_Group', 'Churn_Rate']
   income_churn
   marital_churn = df.groupby('Marital_Status')['Churn'].count().reset_index()
   marital_churn.columns = ['Marital_Status', 'Churn_Rate']

   marital_churn
   fig__1=px.pie(names=marital_churn['Marital_Status'], values=marital_churn['Churn_Rate'], title='Churn Rate by Marital Status')
 
   
   age_churn
   fig__2=px.pie(names=age_churn['Age_Group'], values=age_churn['Churn_Rate'], title='Churn Rate by Age Group')
   
   income_churn
   fig__3=px.pie(names=income_churn['Income_Group'], values=income_churn['Churn_Rate'], title='Churn Rate by Income Group')
   fig3_4= make_subplots(rows=1, cols=3, subplot_titles=['Churn Rate by Age Group', 'Churn Rate by Income Group', 'Churn Rate by Marital Status'],
                   specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]])
   
   fig3_4.add_trace(fig__1.data[0], row=1, col=1)
   fig3_4.add_trace(fig__2.data[0], row=1, col=2)
   fig3_4.add_trace(fig__3.data[0], row=1, col=3)
   st.plotly_chart(fig3_4)
   
   st.latex(r'''\text{3-4/Do customers who accepted campaigns have a lower churn rate?}''')
   campaign_churn = df.groupby('Accepted_Any_Campaign')['Churn'].mean().reset_index()
   campaign_churn.columns = ['Accepted_Any_Campaign', 'Churn_Rate']
   campaign_churn
   st.markdown("""
       
      **Observation**
       
       - Campaign Acceptors: 8.73% churn rate
       - Non-Acceptors: 8.77% churn rate
          → Difference: 0.04 percentage points (statistically insignificant)
       
       
        **Interpretation**
       -  No Meaningful Reduction in Churn 
        - Accepting campaigns does not significantly lower churn in this dataset.

        - Possible Reasons:
        - Campaigns may focus on new acquisitions rather than retention.
         - Offers might lack relevance
       """)
       
