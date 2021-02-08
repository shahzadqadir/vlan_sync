import netmiko

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
