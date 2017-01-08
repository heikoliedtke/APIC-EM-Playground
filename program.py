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
            ticket = get_ticket(controller, username, password)
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
                ticket = get_ticket(controller, username, password)

            devices = get_network_devices(controller, ticket)
            print_network_devices(devices)
            input("Press Enter to continue")
        elif cmd == "4":
            # Get PnP Projects
            cls()
            if not ticket:
                ticket = get_ticket(controller, username, password)
            projects = get_pnp_projects(controller, ticket)
            print_pnp_projects(projects)
            input("Press Enter to continue")


        elif cmd == "5":
            cls()
            if not ticket:
                ticket = get_ticket(controller, username, password)
            if not devices:
                devices = get_network_devices(controller, ticket)
            print_network_devices(devices)
            actual = int(input("Which device config?"))
            config = get_device_config(controller, ticket, devices[actual].id)
            save_config(config, devices[actual].hostname)


        elif cmd == "6":
            # POST PnP Project
            cls()
            if not ticket:
                ticket = get_ticket(controller, username, password)
            post_pnp_project(controller, ticket)


        elif cmd == "7":
            # POST PnP Device
            if not ticket:
                ticket = get_ticket(controller, username, password)
            if not projects:
                projects = get_pnp_projects(controller, ticket)
            print_pnp_projects(projects)
            actual = int(input("For wich PnP Project?"))
            post_pnp_device(controller, ticket, projects[actual].id)





        elif cmd == "8":
            # GET PnP Devices
            if not ticket:
                ticket = get_ticket(controller, username, password)
            print_pnp_devices(controller, ticket)



        elif cmd == "9":
            print('99999')
        elif cmd != "x" and cmd:
            print("Sorry, we don't understand {}".format(cmd))
    print("Goodbye")


if __name__ == '__main__':
    main()
