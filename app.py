#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 21:16:32 2025

@author: harsh
"""


# Course end project - Analyzing customer orders using python
import mysql.connector
from faker import Faker
import random
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import date

faker=Faker()

class Customer():
    def __init__(self, id, firstName, lastName, fullName, phoneNumber, email):
        self.id=id
        self.firstName=firstName
        self.lastName=lastName
        self.fullName=fullName
        self.phoneNumber=phoneNumber
        self.email=email

    def addCustomerData():
        customer=[]
        for i in range (50):
            query='INSERT INTO customer(first_name, last_name, phone_number, email) values (%s, %s, %s, %s)'
            firstName=faker.first_name()
            lastName=faker.last_name()
            phoneNumber=faker.phone_number()
            email=faker.email()
            customer.append((firstName,lastName,phoneNumber,email))
        cursor.executemany(query,customer)
        connection.commit()

    def getCustomerIds():
        query='SELECT * FROM customer'
        cursor.execute(query)
        result=cursor.fetchall()
        result=[x[0] for x in result]
        return result

    def getCustomerData():
        query='SELECT * FROM customer'
        cursor.execute(query)
        result=cursor.fetchall()
        return result

class Product():
    def __init__(self, productName, displayName, category):
        self.productName=productName
        self.displayName=displayName
        self.category=category
    
    def create_product_name():
        adjectives = ["Smart", "Portable", "Eco", "Premium", "Ultra", "Wireless", "Digital"]
        product_types = ["Phone", "Shoes", "Laptop", "Headphones", "Backpack", "Watch", "Bottle"]
        return f"{random.choice(adjectives)} {random.choice(product_types)}"
    
    def addProductData():
        product=[]
        for i in range(50):
            productName=Product.create_product_name()
            displayName=productName
            category=random.choice(['Electronics', 'Fashion', 'Home & Kitchen', 'Sports', 'Books'])
            query='INSERT INTO product(product_name, display_name, category) VALUES (%s, %s, %s)'
            product.append((productName, displayName, category))
        cursor.executemany(query, product)
        connection.commit()

    def getProductIds():
        query='SELECT * FROM product'
        cursor.execute(query)
        result=cursor.fetchall()
        result=[x[0] for x in result]
        return result

    def getProductData():
        query='SELECT * FROM product'
        cursor.execute(query)
        result=cursor.fetchall()
        return result

class Orders():
    @staticmethod
    def addOrderData(year):
        orders = []
        for i in range(50):
            customer_id = random.choice(Customer.getCustomerIds())
            order_amount = random.uniform(25, 10000)
            start_date=date(int(year), 1, 1)
            end_date=date(int(year), 12, 31)
            order_date = faker.date_between(start_date=start_date, end_date=end_date)
            orders.append((customer_id, order_amount, order_date))
        query = 'INSERT INTO order_details(customer_id, order_amount, order_date) VALUES (%s, %s, %s)'
        cursor.executemany(query, orders)
        connection.commit()

    def getOrderIds():
        query = 'SELECT * FROM order_details'
        cursor.execute(query)
        result = cursor.fetchall()
        result = [x[0] for x in result]
        return result
    
    def getOrderData():
        query = 'SELECT * FROM order_details'
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def addProductOrderMapping():
        product_order_mapping = []
        for i in range(50):
            order_id = random.choice(Orders.getOrderIds())
            quantity = random.uniform(1, 5)
            product_id = random.choice(Product.getProductIds())
            product_order_mapping.append((order_id, product_id, quantity))
        query = 'INSERT INTO product_order_mapping(order_id, product_id, quantity) VALUES (%s, %s, %s)'
        cursor.executemany(query, product_order_mapping)
        connection.commit()

    def getProductOrderMapping():
        query = 'SELECT * FROM product_order_mapping'
        cursor.execute(query)
        result = cursor.fetchall()
        return result

class Dashboard():
    def __init__(self, customer_data, product_data, order_data, product_order_mapping, filterValue):
        self.customer_data = customer_data
        self.product_data = product_data
        self.order_data = order_data
        self.product_order_mapping = product_order_mapping
        self.filterValue = filterValue

    def totalOrdersByMonth(self):
        df = pd.DataFrame(self.order_data, columns=['order_id', 'customer_id', 'order_amount', 'order_date'])
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['month'] = df['order_date'].dt.month
        df['year'] = df['order_date'].dt.year
        df = df[df['year'] == self.filterValue]
        orderByMonth=df.groupby(df['month']).size().reset_index(name='total_orders')
        st.title('Total Orders by Month')
        sns.set_style("darkgrid")
        sns.set_context("talk")
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.lineplot(data=orderByMonth, x='month', y='total_orders', marker='o', ax=ax)
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Orders')
        ax.set_title('Number of Orders by Month')
        ax.grid(True)
        st.pyplot(fig)

    def topSpendingCustomers(self):
        df1 = pd.DataFrame(self.order_data, columns=['order_id', 'customer_id', 'order_amount', 'order_date'])
        df1['order_amount'] = pd.to_numeric(df1['order_amount'], errors='coerce')              #Replace values which are not int/floats into NaN
        df1['order_date'] = pd.to_datetime(df1['order_date'], errors='coerce')
        df1['year'] = df1['order_date'].dt.year
        df1 = df1[df1['year']==self.filterValue]
        top_customers = df1.groupby('customer_id')['order_amount'].sum().reset_index(name='Total_order_amount')
        top_customers = top_customers.sort_values(by='Total_order_amount', ascending=False).head(10)
        customer_df = pd.DataFrame(self.customer_data, columns=['id', 'first_name', 'last_name', 'full_name', 'phone_number', 'email'])
        customer_df.drop(columns=['first_name', 'last_name', 'phone_number', 'email'], inplace=True)
        top_customers = pd.merge(customer_df, top_customers, left_on='id', right_on='customer_id', how='inner')
        top_customers.drop(columns=['id', 'customer_id'], inplace=True)
        top_customers['Total_order_amount'] = np.ceil(top_customers['Total_order_amount']).astype(int)  # Round up to nearest integer
        top_customers = top_customers.sort_values(by='Total_order_amount', ascending=False)
        st.title('Top Spending Customers')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(data=top_customers, x='full_name', y='Total_order_amount', palette='viridis', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_xlabel('Customer Name')
        ax.set_ylabel('Total Order Amount')
        ax.set_title('Top Spending Customers')
        st.pyplot(fig)

    def topSellingProducts(self):
        dfOrders = pd.DataFrame(self.order_data, columns=['order_id', 'customer_id', 'order_amount', 'order_date']) 
        dfOrders['order_date'] = pd.to_datetime(dfOrders['order_date'], errors='coerce')
        dfOrders['year'] = dfOrders['order_date'].dt.year
        dfOrders = dfOrders[dfOrders['year'] == self.filterValue]
        df2 = pd.DataFrame(self.product_order_mapping, columns=['id', 'order_id', 'product_id', 'quantity'])    
        df2['quantity'] = pd.to_numeric(df2['quantity'], errors='coerce')              #Replace values which are not int/floats into NaN
        df2 = df2[df2['order_id'].isin(dfOrders['order_id'])]
        top_products = df2.groupby('product_id')['quantity'].sum().reset_index(name='Total_quantity_sold')
        top_products = top_products.sort_values(by='Total_quantity_sold', ascending=False).head(10)
        product_df = pd.DataFrame(self.product_data, columns=['id', 'product_name', 'display_name', 'category'])
        top_products = pd.merge(product_df, top_products, left_on='id', right_on='product_id', how='inner')
        top_products.drop(columns=['id', 'product_id', 'product_name', 'category'], inplace=True)
        top_products['Total_quantity_sold'] = np.ceil(top_products['Total_quantity_sold']).astype(int)  # Round up to nearest integer
        top_products = top_products.sort_values(by='Total_quantity_sold', ascending=False)
        st.title('Top Selling Products')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(data=top_products, x='display_name', y='Total_quantity_sold', palette='viridis', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_xlabel('Product Name')
        ax.set_ylabel('Total Quantity Sold')
        ax.set_title('Top Selling Products')
        st.pyplot(fig)

    def topSellingProductCategories(self):
        dfOrders = pd.DataFrame(self.order_data, columns=['order_id', 'customer_id', 'order_amount', 'order_date']) 
        dfOrders['order_date'] = pd.to_datetime(dfOrders['order_date'], errors='coerce')
        dfOrders['year'] = dfOrders['order_date'].dt.year
        dfOrders = dfOrders[dfOrders['year'] == self.filterValue]
        df3 = pd.DataFrame(self.product_order_mapping, columns=['id', 'order_id', 'product_id', 'quantity'])
        df4 = pd.DataFrame(self.product_data, columns=['id', 'product_name', 'display_name', 'category'])
        df3 = pd.merge(df3, df4, left_on='product_id', right_on='id', how='inner')
        df3 = df3[df3['order_id'].isin(dfOrders['order_id'])]
        top_categories = df3.groupby('category')['quantity'].sum().reset_index(name='Total_quantity_sold')
        top_categories = top_categories.sort_values(by='Total_quantity_sold', ascending=False).head(10)
        top_categories['Total_quantity_sold'] = np.ceil(top_categories['Total_quantity_sold']).astype(int)  # Round up to nearest integer
        st.title('Top Selling Product Categories')
        fig, ax = plt.subplots(figsize=(14, 7))
        plt.pie(top_categories['Total_quantity_sold'], labels=top_categories['category'], autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)

    def monthByMonthRevenue(self):
        df5 = pd.DataFrame(self.order_data, columns=['order_id', 'customer_id', 'order_amount', 'order_date'])
        df5['order_amount'] = pd.to_numeric(df5['order_amount'], errors='coerce')
        df5['order_date'] = pd.to_datetime(df5['order_date'], errors='coerce')
        df5['month'] = df5['order_date'].dt.month
        df5['year'] = df5['order_date'].dt.year
        df5 = df5[df5['year'] == self.filterValue]
        df5 = df5.groupby('month')['order_amount'].sum().reset_index(name='Total_revenue')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.lineplot(data=df5, x='month', y='Total_revenue', marker='o', ax=ax)
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Revenue')
        ax.set_title('Month by Month Revenue')
        st.title('Month by Month Revenue')
        st.pyplot(fig)

#Establish connection to mysql server on local machine/localhost
connection = mysql.connector.connect(
    host='localhost',
    user='harsh',
    password='Admin@123',
    database='customer_info'
)
#Read and store the data 
cursor=connection.cursor()


# Streamlit UI
st.title('Customer Analysis Mini-Project')
st.write('Interactively generate and analyze customer, product, and order data.')

option = st.selectbox(
    'Choose an action:',
    ('Select...', 'Create 50 Customers', 'Create 50 Products', 'Create 50 Orders', 'Show Dashboard')
)

if option == 'Create 50 Customers':
    if st.button('Generate Customers'):
        Customer.addCustomerData()
        st.success('50 customers added!')
elif option == 'Create 50 Products':
    if st.button('Generate Products'):
        Product.addProductData()
        st.success('50 products added!')
elif option == 'Create 50 Orders':
    year = st.text_input('Enter a year to generate data for:')
    if not (year.isnumeric() and len(year)==4):
        st.error('Please enter a valid year (e.g., 2023).')
    else:
        if st.button('Generate Orders'):
            Orders.addOrderData(year)
            Orders.addProductOrderMapping()
            st.success(f'50 orders added for year {year}!')
elif option == 'Show Dashboard':
    customer_data = Customer.getCustomerData()
    product_data = Product.getProductData()
    order_data = Orders.getOrderData()
    product_order_mapping = Orders.getProductOrderMapping()
    filterYearList = pd.DataFrame(order_data, columns=['order_id', 'customer_id', 'order_amount', 'order_date'])
    filterYearList['order_date'] = pd.to_datetime(filterYearList['order_date'], errors='coerce')
    filterYearList['order_date'] = filterYearList['order_date'].dt.year
    filterYearList = filterYearList['order_date'].unique()           #this converts the dataframe to a numpy series
    filterYearList = np.sort(filterYearList)
    filterValue = st.selectbox('View result for:', filterYearList[::-1], index=0)
    st.write('Please click **Load Dashboard** after changing the year to view the results.')
    if st.button('Load Dashboard'):
        dashboard = Dashboard(customer_data, product_data, order_data, product_order_mapping, filterValue)
        dashboard.totalOrdersByMonth()
        dashboard.monthByMonthRevenue()
        dashboard.topSpendingCustomers()
        dashboard.topSellingProducts()
        dashboard.topSellingProductCategories()
         

#close the cursor object
cursor.close()



