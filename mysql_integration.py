import mysql.connector

def create_database(host, username, password):
    """
    Creates mysql database named vlandb, if not exist already.
    """
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password
    )
    db_cursor = mydb.cursor()
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS vlandb")
    db_cursor.execute("use vlandb")
    db_cursor.execute("CREATE TABLE IF NOT EXISTS vlans (id INTEGER, name VARCHAR(255))")

def pull_db_vlans(hostname, username, password, db):
    """
    Returns vlan id and names in a dictionary format.
    """
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=db
        )
        mycursor = mydb.cursor()

        sql = "SELECT id,name FROM vlans;"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return dict(result)
    except:
        pass

def add_vlans_db(hostname, username, password, db, vlans_dict):
    """
    Open a datbase connection and insert vlan details
    """
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=db
        )
        mycursor = mydb.cursor()
        
        for id, name in vlans_dict.items():
            sql = "INSERT INTO vlans (id, name) VALUES (%s, %s)"
            values = (id, name)
            mycursor.execute(sql, values)
        mydb.commit()
    except:
        pass

def remove_vlans_db(hostname, username, password, db, vlans_dict):
    """
    Open a datbase connection and insert vlan details
    """
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=db
        )
        mycursor = mydb.cursor()
        
        for id, name in vlans_dict.items():
            sql = f"DELETE FROM vlans WHERE id = {id};"
            mycursor.execute(sql)
            print(f"vlan {id} is removed!")
        mydb.commit()
    except:
        pass

