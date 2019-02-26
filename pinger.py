from scapy.all import sr1, IP, ICMP
import asyncio
import ipaddress


def ping(ip, ttl=20, retries=2, verbose=0, timeout=2):
    packet = IP(dst=ip, ttl=ttl) / ICMP()
    reply = sr1(packet, retry=retries, verbose=verbose, timeout=timeout)
    if reply:
        status = True
        print(ip, 'is pingable')
    else:
        status = False
        print(ip, 'is not pingable')
    return ip, status


async def ping_coroutine(ip):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, ping, ip)


async def main():
    ip_network = ipaddress.ip_interface('10.0.1.0/24')
    tasks = [ping_coroutine(ip.exploded) for ip in ip_network.network.hosts()]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == '__main__':
    asyncio.run(main())
