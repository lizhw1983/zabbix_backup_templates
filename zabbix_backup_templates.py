#!/usr/bin/python3
#     zabbix backup all template
#     $Revision: 301 $
#     $Date: 2020-04-01 11:06:57 +0800 (周三, 2020-04-01) $
import sys
from pyzabbix import ZabbixAPI
from xml.dom import minidom
import os
import configparser



def isDir(path):
    if os.path.exists(path) == False:
        os.mkdir(path)
        
        
def export_templates(url, user, password,path="backup"):
    try:
        zapi = ZabbixAPI(url)
        zapi.login(user, password)
    except Exception as e:
        print('Failed to connect with the Zabbix API. Please check your credentials.')
        print(str(e))
        exit(1)

    templates = zapi.template.get(
        output=['name', 'id']
    )

    isDir(path)
    
    for t in templates:
        template_id = t['templateid']
        name = t['name'].replace(' ', '_')

        config = zapi.configuration.export(
            format='xml',
            options={
                'templates': [template_id]
            }
        )
        
        print('Exporting %s...' % name)
        xmlstr = minidom.parseString(config).toprettyxml(indent="   ")
        fileName = os.path.join(path,"%s.xml" % name)
        with open(fileName, "w") as f:
            f.write(xmlstr)
            
            
            
def main():
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    user = config.get("default", "zabbix_user")
    password = config.get("default", "zabbix_password")
    url = config.get("default", "zabbix_url")
    export_templates(url, user, password)
    

if __name__ == "__main__":
    main()