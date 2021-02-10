# vlan_sync

This simple script logs into switches using SSH, pull VLAN information and save that in a MySQL database.

For every subsequent run, it looks for any changes like additions or deletions of Vlans on switch, it notifies the user and sync changes to database.
