# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 15:11:04 2025

@author: Luche Louw
"""
import sqlite3
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt



#SECTION A - SQL Integration & Data Preparation
#==============================================================================

#===========================Connect to Database================================
#==============================================================================
conn = sqlite3.connect("C:/Users/SD 1/Downloads/Data Set Creation (1)/src/db/lewis_customers.db")

tables = {}
for tbl in ["Customers", "Stores", "Transactions"]:
    df = pd.read_sql_query(f'SELECT * FROM {tbl};',conn )
    tables[tbl] = df
    print(f"\n=== {tbl} ===") 
    print(df.head())
   
conn.close()

#========================Join, Merge Data and Clean Data=======================
#==============================================================================
df=pd.read_csv('C:/Users/SD 1/Downloads/Data Set Creation (1)/src/feedback.csv')
print(df.head())

 
#converting all the SQL tables into dataframes 
customers_df = tables['Customers']
stores_df = tables['Stores']
transaction_df = tables['Transactions']

#Merging the created dataframes together , including the csv file 
feedback_df = pd.read_csv('C:/Users/SD 1/Downloads/Data Set Creation (1)/src/feedback.csv')


customer_transaction = pd.merge(tables['Customers'],tables['Transactions'],on = 'customer_id',how='inner')
c_t_store_df = pd.merge(customer_transaction, tables['Stores'], on = 'store_id' , how= 'left')
final_df = pd.merge(c_t_store_df , feedback_df, on = 'customer_id', how = 'left')


#Data Exploration 
print(final_df.head())
print(final_df.info())
print(final_df.isnull().sum())

#Formatting colums names 
final_df.columns = final_df.columns.str.replace('_' , ' ').str.title()
print(len(final_df.columns))
final_df.rename(columns = {'Date':'Transaction Date'}, inplace = True)

print(final_df.columns)

final_df['Join Date'] = pd.to_datetime(final_df['Join Date'],errors = 'coerce')
final_df['Customer Tenure(Years)'] = (pd.Timestamp('today') - final_df['Join Date']).dt.days / 365

avg_spend_per_txn = final_df.groupby('Customer Id')['Total Spent'].sum() /final_df.groupby('Customer Id')['Transaction Id'].count()
avg_spend_per_txn = avg_spend_per_txn.sort_values(ascending= False)
print(f' The average spent per transaction is of the top 10 customers is {avg_spend_per_txn.head(10)}')


# Calculate total complaints and total transactions per customer
complaint_rate = ( final_df.groupby('Customer Id')['Complaint Flag'].sum() /
                  final_df.groupby('Customer Id')['Transaction Id'].count())
complaint_rate = complaint_rate.astype(int)
print(f'This is the complaint rate of the first 20 customers recorded {complaint_rate.head(20)} ')

#==============================================================================
#Label Creation:Column indicating if customers churned or not in the last 90 days
#==============================================================================
final_df['Transaction Date'] = pd.to_datetime(final_df['Transaction Date'],errors ='coerce' )
last_date = final_df.groupby('Customer Id')['Transaction Date'].max()#finding the most recent transaction date

today = pd.Timestamp('today')
days_since_last_date = (today - last_date).dt.days#calculating  the number of days since last transaction

churn_flag = (days_since_last_date > 90).astype(int)
final_df['Churn Flag'] = final_df['Customer Id'].map(churn_flag)
RegionChurn = final_df.groupby('Region')['Churn Flag'].sum().sort_values(ascending = False )
print('The Churn count per Region is' , RegionChurn)

#SECTION B - Exploratory Data Analysis 
#------------------------------------------------------------------------------
#==============================================================================
#Compute and visualise:	Average loyalty score by region
#==============================================================================
#Average loyalty score by region
loyalty_by_region = final_df.groupby('Region')['Loyalty Score'].mean().sort_values(ascending = False )
print(f'This is the frequency of loyalty by region {loyalty_by_region}')
plt.bar(loyalty_by_region.index , loyalty_by_region.values, color = 'purple')
plt.title('Average Loyalty Score by Region')
plt.xticks(rotation= 45)
plt.xlabel('Region')

plt.ylabel('Average Loyalty')

plt.show()

#==============================================================================
#Compute and visualise:	Complaint rate by category
#==============================================================================
complaint_by_category = final_df.groupby('Category')['Complaint Flag'].value_counts().reset_index()
print(f' This is the frquency of the complaints and non-complaints from each product category {complaint_by_category} ')

sns.barplot(data= complaint_by_category, x= 'Category' , y = 'count' ,
            hue = 'Complaint Flag' , palette = {0: '#8E44AD', 1: '#E74C3C'})
plt.title('Complaint(1) vs Non Complaint(0)')
plt.ylabel('Number of Transactions')
plt.xticks(rotation= 45)
plt.legend() 
plt.show()

#Display the top 10 customers by lifetime value (total_spent).=================
customer_rev = final_df.groupby('Customer Id')['Total Spent'].sum().sort_values(ascending = False )
print(f'Display the top 10 customers by lifetime value , {customer_rev.head(10)} ')

#==============================================================================
#Compute and visualise:	Satisfaction distribution by account type
#==============================================================================

satisfaction_distribution = final_df.groupby('Account Type')['Satisfaction Score'].sum()
print(satisfaction_distribution)
total_score=3691692+4709990
plt.pie(satisfaction_distribution,labels = satisfaction_distribution.index,
        autopct ='%1.1f%%',startangle = 90 , colors= ['purple' , 'orange'])

plt.title('Satisfaction Distribution by Account Type')

plt.text(0, -1.3, f"Total Satisfaction Score: {total_score}",
        ha='center', fontsize=12)
plt.text(0, -1.5, "Cash : 3691692",
        ha='center', fontsize=12)
plt.text(0, -1.7, "Credit : 4709990",
        ha='center', fontsize=12)

#==============================================================================     
#Bar chart: average spend per region
#==============================================================================
ave_spent_by_region=final_df.groupby('Region')['Total Spent'].mean().sort_values(ascending=True)
plt.figure(figsize=(12,8))
print('The average spent by region is:',ave_spent_by_region)

plt.bar(ave_spent_by_region.index , ave_spent_by_region.values, color = 'purple')
plt.title('Average amount spent in each Region')
plt.xlabel('Region')
plt.xticks(rotation= 45)
plt.ylabel('Average Revenue(R)')
plt.show()

#==============================================================================
#Heatmap: correlation among loyalty_score, satisfaction_score, and total_spent
#==============================================================================
#Calculation of the correction
heatmap_data = final_df[['Loyalty Score', 'Satisfaction Score', 'Total Spent']].corr()
# Plotting the heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(heatmap_data, 
            annot=True,
            fmt='.2f', 
            cmap='BuPu', 
            vmin=-1, 
            vmax=1
)
plt.title('Correlation among Loyalty Score, Satisfaction Score, and Total Spent')
plt.show()

#==============================================================================
#Boxplot: total_spent by account_type
#==============================================================================
#revenue_account_type = final_df.groupby('Account Type')['Total Spent'].sum()
#print(f'The sum of the revenue paid be each account type is {revenue_account_type}')
sns.boxplot(data=final_df ,x='Account Type', y= 'Total Spent',palette='BuPu')
sns.set_style("whitegrid")
plt.title('Total revenue per Account Type' )
plt.ylabel('Total Revenue(R)')
plt.tight_layout()
plt.ticklabel_format(style='plain', axis='y')
plt.figure(figsize =(8,5))

#==============================================================================
final_df['Delivery Time Days'] =final_df['Delivery Time Days'].astype(str)

DeliveryComplaint= final_df.groupby('Delivery Time Days')['Complaint Flag'].sum().sort_values(ascending= False)
print(DeliveryComplaint)
#==============================================================================
print(final_df.columns)

final_df.to_csv('Lewis Churn Prediction Data', index = False)