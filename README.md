# SCA25-NVIDIA-Quantum-Workshop
This is a repository for SCA25 NVIDIA Quantum Workshop Material

# VPN Connections
To access the GPU server at Singtel Re:AI, please follow the guidlines in VPN instruction

#SSH connections
Please ssh and portforwarding to the following server

Server      <space> <space>       IP     <space>      username   
NV-H100-01  <space> <space>   10.0.0.10  <space>     nv-user1, nv-user2, ..., nv-user8  
NV-H100-02  <space> <space>   10.0.0.11  <space>     nv-user9, nv-user10, ..., nv-user16  
NV-H100-03  <space> <space>   10.0.0.12  <space>     nv-user17, nv-user18, ..., nv-user24  

For mac users, you may ssh with the following command 

```
ssh -L localhost:<port>:localhost:<port> username@10.0.0.10
```

For windows users, you may install MobaXterm or putty for the access. 
