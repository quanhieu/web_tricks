#!/data/data/com.termux/files/usr/bin/sh
/system/bin/iptables -I FORWARD -i wlan0 -o tun0 -j ACCEPT
/system/bin/iptables -I FORWARD -i tun0 -o wlan0 -j ACCEPT
/system/bin/iptables -t nat -I PREROUTING -i wlan0 -p udp --dport 53 -j DNAT --to 1.1.1.1:53
ip rule add pref 500 fwmark 0x0/0x10000 lookup local_network
ip route add default dev tun0 table 6666
ip rule add pref 600 iif wlan0 lookup 6666
