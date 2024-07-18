import dns.resolver
import socket
import re
import netifaces

from urllib.request import urlopen

def dns_lookup_response(domain, rdtype="A"):
    result = None
    try:
        result = dns.resolver.resolve(domain, rdtype)
    except dns.resolver.NoAnswer:
        print(f"{domain} does not contain any {rdtype} records.")
        return
    except Exception as e:
        print(e)
        return

    if rdtype == "A":
        for ip_value in result:
            print('IP', ip_value.to_text())
    elif rdtype == "CNAME":
        for cname_value in result:
            print(' cname target address:', cname_value.target)
    elif rdtype == "MX":
        for mx_value in result.rrset.items:
            print('MX Record:', mx_value)

def full_dns_lookup(domain):
    dns_lookup_response(domain, "A")
    dns_lookup_response(domain, "CNAME")
    dns_lookup_response(domain, "MX")

def public_ip_address():
    d = str(urlopen('http://checkip.dyndns.com/').read())

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

def get_fqdn():
    return socket.getfqdn(socket.gethostname())

def get_hostname():
    return socket.gethostname()

def local_ip_address():
    ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address

def get_network_interfaces():
    return netifaces.interfaces()

def comma_delimited_string_to_list(string_to_convert):
    this_list = string_to_convert.split(",")
    return_list = []
    for item in return_list:
        if item.strip(" ") not in return_list:
            return_list.append(item.strip())

def full_network_info():
    network_interfaces = {}
    for net_interface in get_network_interfaces():
        if net_interface == 'lo':
            continue
        network_interfaces[net_interface] = {}
        print(f"Network interface: {net_interface}")
        interface_list = comma_delimited_string_to_list(str(netifaces.ifaddresses(net_interface)))
        for interface in interface_list:
            string_to_parse = interface.strip(" ").strip("{").strip("}")
            begin_bracket = string_to_parse.find("[")
            if begin_bracket != -1:
                end_bracket = string_to_parse.find("]", begin_bracket)
            else:
                end_bracket = string_to_parse.find("]")
            if begin_bracket == -1:
                begin_bracket = 0
            if end_bracket == -1:
                end_bracket = len(string_to_parse) - 1
            string_to_parse = string_to_parse[begin_bracket:end_bracket].strip("[").strip("]")
            string_to_parse = interface.strip(" ").strip("{").strip("}")
            addresses = comma_delimited_string_to_list(string_to_parse)
            for address in addresses:
                parts = address.split(":")
                if len(parts) > 1:
                    address_name = parts[0].strip("'")
                if len(parts) > 2:
                    actual_address = parts[1].strip("'")
                    network_interfaces[net_interface][address_name] = actual_address
        gateways = netifaces.gateways()
        for gateway in gateways:
            print(gateway)

    print(network_interfaces)

def main():
    # gateway
    # subnet mask
    # wireless

    hostname = get_fqdn()

    public_ip = public_ip_address()

    print("Your computer's name (hostname) is: " + hostname)
    print("Your Public IP Address is:" + public_ip)

    full_network_info()
    # full_dns_lookup("google.com")

if __name__ == "__main__":
    main()