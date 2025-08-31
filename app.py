#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 21:16:32 2025

@author: harsh
"""

#Course end project - Analyzing customer orders using python
import mysql.connector
from faker import Faker
import random

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
        for i in range (50):
            query='INSERT INTO CUSTOMER(first_name, last_name, phone_number, email) values (%s, %s, %s, %s)'
            firstName=faker.first_name()
            lastName=faker.last_name()
            phoneNumber=faker.phone_number()
            email=faker.email()
            value=(firstName,lastName,phoneNumber,email)
            cursor.executemany(query,value)
        connection.commit()

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
        for i in range(50):
            productName=Product.create_product_name()
            displayName=productName
            category=random.choice(['Electronics', 'Fashion', 'Home & Kitchen', 'Sports', 'Books'])
            query='INSERT INTO PRODUCT(product_name, display_name, category) VALUES (%s, %s, %s)'
            value=(productName, displayName, category)
            cursor.executemany(query, value)
        connection.commit()
    


#eEstablish connection to mysql server on local machine/localhost
connection = mysql.connector.connect(
    host='localhost',
    user='harsh',
    password='Admin@123',
    database='customer_info'
)
#Read and store the data 
cursor=connection.cursor()

userChoice=0
print('Welcome to the Customer Analysis mini-project !')
while userChoice !=4:
    print('Press 1: To create random data of 50 customers')
    print('Press 2: To create random data of 50 products')
    print('Press 3: To show dashboard')
    print('Press 4: To exit')
    userChoice = int(input())
    if userChoice==1:
        Customer.addCustomerData()
    elif userChoice==2:
        Product.addProductData()
    elif userChoice==3:
        pass
    elif userChoice==4:
        print('Thanks for trying the project !!')
    else:
        print('Please try a valid input')

#close the cursor object
cursor.close()



