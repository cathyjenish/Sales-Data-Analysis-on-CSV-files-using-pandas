#!/usr/bin/env python3
"""
Sales Data Analysis Runner
A simple script to run the sales data analysis without Jupyter
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def load_and_analyze_data(csv_file='sales_data.csv'):
    """Load CSV file and perform basic analysis"""
    
    try:
        # Load data
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Basic info
        print("=== DATASET INFO ===")
        print(f"Total records: {len(df)}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Products: {len(df['Product'].unique())}")
        print(f"Regions: {len(df['Region'].unique())}")
        print(f"Salespeople: {len(df['Salesperson'].unique())}")
        
        # Basic statistics
        print("\n=== BASIC STATISTICS ===")
        print(df.describe())
        
        # Sales analysis
        print("\n=== SALES ANALYSIS ===")
        
        # Top products by sales
        product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
        print("\nTop 5 Products by Sales:")
        print(product_sales.head())
        
        # Sales by region
        region_sales = df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False)
        print("\nSales by Region:")
        print(region_sales)
        
        # Sales by salesperson
        salesperson_sales = df.groupby('Salesperson')['Total_Sales'].sum().sort_values(ascending=False)
        print("\nSales by Salesperson:")
        print(salesperson_sales)
        
        # Monthly trends
        df['Year_Month'] = df['Date'].dt.to_period('M')
        monthly_sales = df.groupby('Year_Month')['Total_Sales'].sum()
        print("\nMonthly Sales Trend:")
        print(monthly_sales.head())
        
        # Save insights
        insights = {
            'total_sales': df['Total_Sales'].sum(),
            'avg_transaction': df['Total_Sales'].mean(),
            'best_product': product_sales.index[0],
            'top_region': region_sales.index[0],
            'top_salesperson': salesperson_sales.index[0]
        }
        
        return df, insights
        
    except FileNotFoundError:
        print(f"File {csv_file} not found. Creating sample data...")
        return create_sample_data()

def create_sample_data():
    """Create sample sales data for demonstration"""
    
    import random
    from datetime import datetime, timedelta
    
    # Generate sample data
    np.random.seed(42)
    random.seed(42)
    
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'USB Cable', 'Hard Drive']
    regions = ['North', 'South', 'East', 'West']
    salespeople = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
    
    sales_data = []
    for _ in range(1000):
        date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364))
        product = random.choice(products)
        region = random.choice(regions)
        salesperson = random.choice(salespeople)
        quantity = random.randint(1, 10)
        unit_price = random.uniform(50, 2000)
        total_sales = quantity * unit_price
        
        sales_data.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Product': product,
            'Region': region,
            'Salesperson': salesperson,
            'Quantity': quantity,
            'Unit_Price': round(unit_price, 2),
            'Total_Sales': round(total_sales, 2)
        })
    
    df = pd.DataFrame(sales_data)
    df.to_csv('sales_data.csv', index=False)
    print("Sample data created and saved to 'sales_data.csv'")
    
    return load_and_analyze_data()

def create_visualizations(df):
    """Create basic visualizations"""
    
    plt.style.use('seaborn-v0_8')
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Sales Data Analysis Dashboard', fontsize=16)
    
    # 1. Sales by Product
    product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
    product_sales.plot(kind='bar', ax=axes[0,0], color='skyblue')
    axes[0,0].set_title('Total Sales by Product')
    axes[0,0].set_xlabel('Product')
    axes[0,0].set_ylabel('Total Sales ($)')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. Sales by Region
    region_sales = df.groupby('Region')['Total_Sales'].sum()
    region_sales.plot(kind='pie', ax=axes[0,1], autopct='%1.1f%%')
    axes[0,1].set_title('Sales Distribution by Region')
    axes[0,1].set_ylabel('')
    
    # 3. Sales by Salesperson
    salesperson_sales = df.groupby('Salesperson')['Total_Sales'].sum().sort_values(ascending=False)
    salesperson_sales.plot(kind='bar', ax=axes[1,0], color='lightgreen')
    axes[1,0].set_title('Total Sales by Salesperson')
    axes[1,0].set_xlabel('Salesperson')
    axes[1,0].set_ylabel('Total Sales ($)')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # 4. Monthly Sales Trend
    df['Year_Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_sales = df.groupby('Year_Month')['Total_Sales'].sum()
    monthly_sales.plot(ax=axes[1,1], marker='o', color='coral')
    axes[1,1].set_title('Monthly Sales Trend')
    axes[1,1].set_xlabel('Month')
    axes[1,1].set_ylabel('Total Sales ($)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('sales_analysis_charts.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Charts saved to 'sales_analysis_charts.png'")

def main():
    """Main execution function"""
    
    print("Starting Sales Data Analysis...")
    print("=" * 50)
    
    # Run analysis
    df, insights = load_and_analyze_data()
    
    # Create visualizations
    create_visualizations(df)
    
    # Save summary
    with open('analysis_summary.txt', 'w') as f:
        f.write("=== SALES DATA ANALYSIS SUMMARY ===\\n\\n")
        f.write(f"Total Sales: ${insights.get('total_sales', 0):,.2f}\\n")
        f.write(f"Average Transaction: ${insights.get('avg_transaction', 0):.2f}\\n")
        f.write(f"Best Product: {insights.get('best_product', 'N/A')}\\n")
        f
