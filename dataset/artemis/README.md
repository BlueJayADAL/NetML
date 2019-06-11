This folder contains the .pcap files for two captures.  Both captures were taken during the same session while Artemis infected NodeA.  It also contains the results of a DNS' capture and a web server's capture.

Infected host: 
NodeA
192.168.1.152
10.1.1.3

Second host:
NodeB
192.168.1.150
10.1.1.2

DETERLab details:

Experiment: malwareml/MalwareTraffic
State: swapped

Virtual Node Info:
ID              Type         OS              Qualified Name
--------------- ------------ --------------- --------------------
nodeA           pc           WINXP-UPDATE    nodeA.MalwareTraffic.malwareml.isi.deterlab.net
nodeB           pc                           nodeB.MalwareTraffic.malwareml.isi.deterlab.net

Virtual Lan/Link Info:
ID              Member/Proto    IP/Mask         Delay     BW (Kbs)  Loss Rate
--------------- --------------- --------------- --------- --------- ---------
link0           nodeA:0         10.1.1.3        25        30000     0
                ethernet        255.255.255.0   25        30000     0
link0           nodeB:0         10.1.1.2        25        30000     0
                ethernet        255.255.255.0   25        30000     0

Virtual Queue Info:
ID              Member          Q Limit    Type    weight/min_th/max_th/linterm
--------------- --------------- ---------- ------- ----------------------------
link0           nodeA:0         100 slots  Tail    0/0/0/0
link0           nodeB:0         100 slots  Tail    0/0/0/0

Event Groups:
Group Name      Members
--------------- ---------------------------------------------------------------
link0-tracemon  link0-nodeA-tracemon,link0-nodeB-tracemon
__all_tracemon  link0-nodeA-tracemon,link0-nodeB-tracemon
__all_lans      link0
