# Customer-Churn-Prediction-Insight-Analysis
This project focuses on analysing customer behaviour and predicting churn using transactional, demographic, and feedback data.  The goal is to help the business identify at-risk customers and enable targeted retention strategies through data-driven insights and machine learning.


### 🎯 Objectives
Extract and integrate data from an SQL database and CSV file
Perform data cleaning and feature engineering
Conduct exploratory data analysis (EDA) to uncover patterns
Build a machine learning model to predict customer churn
Communicate insights and recommend business actions

### 🧰 Tech Stack
Python (Spyder / Anaconda)
pandas, numpy
matplotlib, seaborn
sqlite3
scikit-learn

### 🛠️ Data Preparation
Connected to SQL database using sqlite3
Merged multiple tables with customer feedback data
Handled missing values using statistical imputation
Engineered key features:
customer_tenure (customer lifetime)
avg_spend_per_txn
complaint_rate
Created target variable:
churn_flag (1 = churned, 0 = active)

### 📈 Exploratory Data Analysis

Key insights uncovered:

High-value customers are concentrated in specific regions
Customers with low satisfaction scores and high complaints show higher churn likelihood
Spending behaviour varies significantly by account type
Visualisations
Average spend per region (bar chart)
Feature correlation heatmap
Spend distribution by account type (boxplot)

(See /outputs/charts/ for all visuals)

### 🤖 Machine Learning Model
Model: Random Forest Classifier
Train-test split: 75% / 25%
Evaluation Metrics
Accuracy
Precision
Recall
F1-score
Key Drivers of Churn

Top influencing features:

Loyalty score
Satisfaction score
Complaint flag
Customer tenure

### 📊 Results

The model successfully identifies customers at risk of churning, enabling proactive intervention.

Strong performance in distinguishing active vs churned customers
Feature importance highlights behavioural patterns linked to churn
