# Config in docker

## 1. MLRun installation

 - install MLRun under public IP (e.g. 192.168.0.150), relevant IP address see 
command `ipconfig`

## 2. Nuclio functions

 - access to the nuclio function will be under public IP and specific port
(e.g. 192.168.0.150:16455)
 - in case, that nuclio function will use e.g. RedisTarget, etc. you have to
use public IP address not localhost fot this Target, because node/pod with nuclio function 
will not have access to this target (localhost in node/pod is different that localhost in 
your notebook/server) 