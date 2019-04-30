import socket
import ssl

import dns.resolver
from multiping import multi_ping

genericAtlas = "*.a.extrahop.com"
atlasEU = "atlas-eu.a.extrahop.com"
atlasUS = "atlas-us.a.extrahop.com"

atlasEUIP = "52.31.19.94"
atlasUSIP = "52.11.128.128"

DNSTestEU = dns.resolver.query(atlasEU, "A")
DNSTestUS = dns.resolver.query(atlasUS, "A")


def open_ssl_socket(host):
    context = ssl._create_unverified_context()
    context.check_hostname = False

    with socket.create_connection((host, 443)) as sock:
        with context.wrap_socket(sock, server_side=False) as ssock:
            return ssock.version()


def checkIPAddrs():
    EUaddr = socket.gethostbyname(atlasEU)
    USaddr = socket.gethostbyname(atlasUS)
    if EUaddr == atlasEUIP:
        print(f"...DNS lookup for EU server returns correct IP address: {EUaddr}")
    else:
        print(
            f"...DNS lookup for EU server  has returned a different address than expected. Expected was {atlasEUIP}. Address returned was {EUaddr}")

    if USaddr == atlasUSIP:
        print(f"...DNS lookup for US server returns correct IP address: {USaddr}")
    else:
        print(
            f"...DNS lookup for US server  has returned a different address than expected. Expected was {atlasUSIP}. Address returned was {USaddr}")


def callMain():
    print("Checking IP addresses of the Atlas servers")
    checkIPAddrs()
    print("Using ICMP ping messages to contact servers")
    addrs = [atlasEUIP, atlasUSIP]
    responses, no_responses = multi_ping(addrs, timeout=4, retry=6)
    if not no_responses:
        print(f"Both servers responded to pings")
    else:
        print("...No responses received from:  %s" % no_responses)

    try:
        print_ssl = open_ssl_socket(atlasEU)
    except ssl.SSLError:
        print(f"Could not connect to the Atlas EU server securely")
    print(f"...Opened an SSL connection to atlas EU. Version is {print_ssl}")

    try:
        print_ssl = open_ssl_socket(atlasUS)
    except:
        print(f"Could not connect to the Atlas US server securely")
    print(f"...Opened an SSL connection to atlas US. Version is {print_ssl}")


if __name__ == '__main__':
    callMain()
