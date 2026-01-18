import asyncio
from network_scanner import NetworkScanner
import httpx

async def main():
    scanner = NetworkScanner("192.168.2.0/24")
    
    # 1. Nur die IPs holen
    print(f"--- Starte Discovery in 192.168.2.0/24 ---") #{self.target_network} 
    ips = scanner.discover_network()
    #print(f"Gefundene IPs: {ips}")

    # Hier könntest du jetzt manuell IPs hinzufügen oder entfernen
    # z.B. ips.remove("192.168.1.1") # Router ignorieren

    # 2. Die Liste abarbeiten
    if ips:
        async with httpx.AsyncClient() as client:
            tasks = [scanner.identify_device(ip, client) for ip in ips]
            devices = await asyncio.gather(*tasks)
            
            print("\nScan-Ergebnis:")
            for d in devices:
                print(f"{d['ip']:<15} | {d['type']:<10} | {d['model']}")
        print(f"dicovered devices: {len(ips)}")
if __name__ == "__main__":
    asyncio.run(main())