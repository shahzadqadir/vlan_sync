#!/home/python/venvs/vlan_sync/bin/python

import netmiko
import mysql.connector

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

def pull_switch_vlans(hostname, username, password):
    """
    Pull Vlan information and return a vlan-id, name dictionary.
    """
    switch1 = {
        "device_type": "cisco_ios",
        "host": hostname,
        "username": username,
        "password": password       
    }
    with netmiko.ConnectHandler(**switch1) as cli_handle:
        output = cli_handle.send_command("show vlan brief", use_textfsm=True)

    vlans_dict = {}
    invalid_vlans = ['1002', '1003', '1004', '1005']
    for item in output:
        if item['vlan_id'] not in invalid_vlans:
            vlans_dict[int(item['vlan_id'])] = item['name']
    
    return vlans_dict

#############################################
# Function calls and main logic

db_vlans = pull_db_vlans("localhost", "sqadir", "cisco123", "vlandb")
sw_hostname = input("Swith IP: ")
sw_username = input("Username: ")
sw_password = input("Password: ")

switch_vlans = pull_switch_vlans(sw_hostname, sw_username, sw_password)



if len(switch_vlans) > len(db_vlans):
    missing_vlans = {}    
    for vlan in switch_vlans:
        if vlan not in db_vlans:
            missing_vlans[vlan] = switch_vlans[vlan]
    print(f"Missing vlans {missing_vlans} were created on Switch but not updated to database.")
    print("Updating now...")
    add_vlans_db("localhost", "sqadir", "cisco123", "vlandb", missing_vlans)
    print("Done, run script again to verify.")
elif len(switch_vlans) < len(db_vlans):
    extra_vlans = {}
    for vlan in db_vlans:
        if vlan not in switch_vlans:
            extra_vlans[vlan] = db_vlans[vlan]
    print(f"Vlans {list(extra_vlans.keys())} have been removed from the switch but still exist in database.")
    print(f"Removing extra vlans now.")
    remove_vlans_db("localhost", "sqadir", "cisco123", "vlandb", extra_vlans)
else:
    print("Both databases are in sync!")



