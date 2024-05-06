import mysql.connector
import streamlit as st


#Conección 
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="mydb",
)


c=conn.cursor()

#fetch o Buscar
def view_all_data():
    c.execute('SELECT * FROM insurance ORDER BY id ASC')
    data = c.fetchall()
    return data
