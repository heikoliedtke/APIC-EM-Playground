import requests

from apic_em_functions import *

requests.packages.urllib3.disable_warnings()  # Disable warnings
controller = "https://sandboxapic.cisco.com/api/v1/"
# controller = "https://192.168.2.50/api/v1/"
# username = "admin"
username = "devnetuser"
password = "Cisco123!"


# test


# password = "DiData2016!"


def main():
    print_header()
    run_event_loop()


def print_header():
    print('---------------------------------')
    print('          APIC-EM Toolkit')
    print('                            Heiko')
    print('---------------------------------')


def cls():
    print("\n" * 20)


def run_event_loop():
    cmd = "wewe"
    ticket = None
    devices = None
    projects = None

    while cmd != 'x' and cmd:
        # cls()
        print("What do you want to do with your APIC-Controller")
        cmd = input("[1] Try to get a Serviceticket\n"
                    "[2] Show credentials\n"
                    "[3] GET Network Devices\n"
                    "[4] GET PnP Projects\n"
                    "[5] GET Device Config\n"
                    "[6] POST new PnP Project\n"
                    "[7] POST new PnP Device\n"
                    "[8] GET PnP Devices\n"
                    "[9] Function 9\n"
                    "E(x)it:")
        cmd = cmd.lower().strip()
        if cmd == "1":
            cls()
            ticket = getTicket(controller, username, password)
            print('Received Serviceticket {}'.format(ticket))
            input("Press Enter to continue")
        elif cmd == "2":
            cls()
            print('Connecting to {} as user {} with password {}'.format(controller, username, password))
            input("Press Enter to continue")
        elif cmd == "3":
            # Get Network Devices
            cls()
            if not ticket:
                ticket = getTicket(controller, username, password)

            devices = getNetworkDevices(controller, ticket)
            printNetworkDevices(devices)
            input("Press Enter to continue")
        elif cmd == "4":
            # Get PnP Projects
            cls()
            if not ticket:
                ticket = getTicket(controller, username, password)
            projects = getPnPProjects(controller, ticket)
            listPnpProjects(projects)
            input("Press Enter to continue")


        elif cmd == "5":
            cls()
            if not ticket:
                ticket = getTicket(controller, username, password)
            if not devices:
                devices = getNetworkDevices(controller, ticket)
            printNetworkDevices(devices)
            actual = int(input("Which device config?"))
            config = getDeviceConfig(controller, ticket, devices[actual].id)
            saveConfig(config, devices[actual].hostname)


        elif cmd == "6":
            # POST PnP Project
            cls()
            if not ticket:
                ticket = getTicket(controller, username, password)
            PutPnPProject(controller, ticket)


        elif cmd == "7":
            # POST PnP Device
            if not ticket:
                ticket = getTicket(controller, username, password)
            if not projects:
                projects = getPnPProjects(controller, ticket)
            listPnpProjects(projects)
            actual = int(input("For wich PnP Project?"))
            PostPnpDevice(controller, ticket, projects[actual].id)





        elif cmd == "8":
            # GET PnP Devices
            if not ticket:
                ticket = getTicket(controller, username, password)
            listPnpDevices(controller, ticket)



        elif cmd == "9":
            print('99999')
        elif cmd != "x" and cmd:
            print("Sorry, we don't understand {}".format(cmd))
    print("Goodbye")


if __name__ == '__main__':
    main()
