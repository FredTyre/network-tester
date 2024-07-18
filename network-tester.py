import dns.resolver
import socket
import re

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

def main():
    hostname = get_fqdn()

    local_ip = local_ip_address()
    # public_ip = public_ip_address()

    print("Your computer's name (hostname) is: " + hostname)
    print("Your Local IP Address is:" + local_ip)
    # print("Your Public IP Address is:" + public_ip)

    full_dns_lookup("example.com")

if __name__ == "__main__":
    main()