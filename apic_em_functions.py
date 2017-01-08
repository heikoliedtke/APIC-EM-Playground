import os

import requests
import json
import collections
import pprint

import subprocess

NetworkDevices = collections.namedtuple('NetworkDevices',
                                        'hostname, family, macAddress, type, serialNumber, id, lookup, platformId')
PnpProjects = collections.namedtuple('PnpProjects',
                                     'siteName, deviceCount, provisionedOn, id, lookup')


# "siteName"], i["deviceCount"], i["provisionedOn"

def getTicket(controller, username, password):
    """
    This functions contacts the APIC-EM controller and gets the
    service ticket for further requests.

    :param controller: URL of the APIC-EM controller
    :param username:
    :param password:
    :return: The service ticket
    """
    url = controller + "ticket"
    payload = {"username": username, "password": password}
    header = {"content-type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    r_json = response.json()
    ticket = r_json["response"]["serviceTicket"]
    return ticket


def getPnPProjects(controller, ticket):
    url = controller + "pnp-project"
    header = {"content-type": "application/json", "X-Auth-Token": ticket}
    response = requests.get(url, headers=header, verify=False)
    r_json = response.json()
    result = r_json["response"]
    # pprint.pprint(result)
    projects = dict()
    i = 0
    for r in result:
        n = PnpProjects(
            siteName=r['siteName'],
            deviceCount=r['deviceCount'],
            provisionedOn=r['provisionedOn'],
            id=r['id'],
            lookup=i,
        )
        i = i + 1
        projects[n.lookup] = n

    return projects


def getNetworkDevices(controller, ticket):
    """
    This function contacts the APIC-EM controller and gets all network devices back in
    a dictionary. The dictionary is initialized in a not pythonic style, because not all
    fields in the JSON response will be used for future processing. A named tuple "NetworkDevices"
    with only certain fields is used.
    :param controller:
    :param ticket:
    :return: The devices as a dictionary of "NetworkDevices"
    """
    url = controller + "network-device"
    header = {"content-type": "application/json", "X-Auth-Token": ticket}
    response = requests.get(url, headers=header, verify=False)
    r_json = response.json()
    result = r_json["response"]
    pprint.pprint(result)
    devices = dict()
    i = 0
    for r in result:
        n = NetworkDevices(
            hostname=r['hostname'],
            family=r['family'],
            macAddress=r['macAddress'],
            type=r['type'],
            serialNumber=r['serialNumber'],
            id=r['id'],
            platformId=r['platformId'],
            lookup=i,
        )
        i = i + 1
        devices[n.lookup] = n

    return devices


def printNetworkDevices(devices):
    """
    This function just prints or lists the devices given in the
    dictionary devices. The field lookup is used for selecting devices
    for further processing
    :param devices:
    :return:
    """
    for a in devices:
        print("      {}      {}      {}        {}".format(devices[a].lookup,
                                                          devices[a].hostname,
                                                          devices[a].platformId,
                                                          devices[a].serialNumber))
    return


def listPnpProjects(projects):
    for a in projects:
        print("      {}     {}     {}".format(projects[a].lookup,
                                              projects[a].siteName,
                                              projects[a].deviceCount))
    return


def getDeviceConfig(controller, ticket, id):
    """
    This function contacts the APIC-EM controller and gets a config
    for a specific device.
    :param controller:
    :param ticket:
    :param id:
    :return: The config
    """
    print("Fetching Config for device id {}".format(id))
    url = controller + ("network-device/{}/config".format(id))
    header = {"content-type": "application/json", "X-Auth-Token": ticket}
    response = requests.get(url, headers=header, verify=False)
    r_json = response.json()
    config = r_json['response']
    return config


def saveConfig(config, name):
    """
    This function saves the config to a directory "configs"
    :param config: The config
    :param name: The name of the config-file
    :return:
    """
    #Function needs to be changed for other systems
    path = "/Users/heikoliedtke/Documents/Heiko Liedtke/APIC-EM-Configs"

    filename = os.path.abspath(os.path.join(path, name + '.txt'))
    print("Saving config to {}".format(filename))
    with open(filename, 'w') as fout:
        for entry in config:
            fout.write(entry)

    print("Done!")
    #Following command works well on MAC OS X. Needs to be adopted for other OS
    subprocess.call(['open', filename])

    return


def PutPnPProject(controller, ticket):
    url = controller + "pnp-project"

    project = input("Which Projectname:")

    print("Try to generate a new project {} at {}".format(project, url))

    header = {"content-type": "application/json", "X-Auth-Token": ticket}
    body = [{"siteName": project}]

    r = requests.post(url, headers=header, data=json.dumps(body), verify=False)
    print(r)
    input("Any key to continue")


def PostPnpDevice(controller, ticket, id):
    url = controller + ("pnp-project/{}/device".format(id))
    header = {"content-type": "application/json", "X-Auth-Token": ticket}

    hostname = "ACCESS_A"
    platform = "WS-C2960X-48TD"
    serialnumber = "FOC12345678"

    body = [{"hostName": hostname,
             "platformId": platform,
             "serialNumber": serialnumber,
             "pkiEnabled": True
             }]
    r = requests.post(url, headers=header, data=json.dumps(body), verify=False)
    r_json = r.json()
    pprint.pprint(r_json)
    input("Any key to continue")


def listPnpDevices(controller, ticket):
    url = controller + "pnp-device"
    header = {"content-type": "application/json", "X-Auth-Token": ticket}
    response = requests.get(url, headers=header, verify=False)
    r_json = response.json()
    pprint.pprint(r_json)

