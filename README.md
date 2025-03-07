# SCA25-NVIDIA-Quantum-Workshop
This is a repository for SCA25 NVIDIA Quantum Workshop Material

# VPN Connections
To access the GPU server at Singtel Re:AI, please follow the guidlines in VPN instruction
The usernames for VPN access is nv-user1, nv-user2, ..., nv-user24
PW: $nvidia#demo!

# SSH connections
Please ssh and portforwarding to the following server

Server $~~~~~~~~~~~~~~~~$ IP $~~~~~~~~~~~~~~~~~~$ username   
NV-H100-01 $~~~~~~$ 10.0.0.10 $~~~~~~$ nv-user1, nv-user2, ..., nv-user8  
NV-H100-02 $~~~~~~$ 10.0.0.11 $~~~~~~$ nv-user9, nv-user10, ..., nv-user16  
NV-H100-03 $~~~~~~$ 10.0.0.12 $~~~~~~$ nv-user17, nv-user18, ..., nv-user24  

For mac users, you may ssh with the following command 

```
ssh -L localhost:<port>:localhost:<port> username@10.0.0.10
```
e.g. for nv-user10, you will be assigned to NV-H100-02, IP 10.0.0.11, with port number 8810 (80+usrid)
The password for login is $nvidia#demo!
```
ssh -L localhost:8810:localhost:8810 nv-user10!10.0.0.11
```

For windows users, you may install MobaXterm or putty for the access. 
[link to MobaXterm documentations](https://mobaxterm.mobatek.net/documentation.html#2_1_5)


# Launch docker container and jupyterlab
This repository will be made available at /svr/ directory

Follow instructions of each lab and launch respective docker container 
