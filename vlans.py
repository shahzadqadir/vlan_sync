#!/home/python/venvs/vlan_sync/bin/python

import netmiko
from getpass import getpass

from mysql_integration import create_database, pull_db_vlans, add_vlans_db, remove_vlans_db

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
sw_password = getpass("Password: ")

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



