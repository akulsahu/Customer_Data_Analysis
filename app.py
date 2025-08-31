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

    def getCustomerData():
        query='SELECT * FROM customer'
        cursor.execute(query)
        result=cursor.fetchall()
        result=[x[0] for x in result]
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

    def getProductData():
        query='SELECT * FROM product'
        cursor.execute(query)
        result=cursor.fetchall()
        result=[x[0] for x in result]
        return result

class Orders():
    def __init__(self, order_id, customer_id, product_id, quantity, order_date):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

    def addOrderData():
        orders = []
        for i in range(50):
            customer_id = random.choice(Customer.getCustomerData())
            order_amount = random.uniform(25, 10000)
            order_date = faker.date_between(start_date='-1y', end_date='today')
            orders.append((customer_id, order_amount, order_date))
        query = 'INSERT INTO order_details(customer_id, order_amount, order_date) VALUES (%s, %s, %s)'
        cursor.executemany(query, orders)
        connection.commit()

    def getOrderData():
        query = 'SELECT * FROM order_details'
        cursor.execute(query)
        result = cursor.fetchall()
        result = [x[0] for x in result]
        return result

    def addProductOrderMapping():
        product_order_mapping = []
        for i in range(50):
            order_id = random.choice(Orders.getOrderData())
            quantity = random.uniform(1, 5)
            product_id=random.choice(Product.getProductData())
            product_order_mapping.append((order_id, product_id, quantity))
        query = 'INSERT INTO product_order_mapping(order_id, product_id, quantity) VALUES (%s, %s, %s)'
        cursor.executemany(query, product_order_mapping)
        connection.commit()


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
    if st.button('Generate Orders'):
        Orders.addOrderData()
        Orders.addProductOrderMapping()
        st.success('50 orders added!')
elif option == 'Show Dashboard':
    st.info('Dashboard feature coming soon!')

#close the cursor object
cursor.close()



