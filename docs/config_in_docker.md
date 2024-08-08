# Config in docker

## 1. MLRun installation

 - install MLRun under public IP (e.g. 192.168.0.150), relevant IP address see 
command `ipconfig` (it is typically IP address with setting of `Default Gateway`)

## 2. Nuclio functions

 - access to the nuclio function will be under public IP and specific port
(e.g. 192.168.0.150:16455). The port will be defined during function deployment.
 - in case, that nuclio function will use e.g. RedisTarget, etc. you have to
use public IP address not localhost fot this Target, because node/pod with nuclio function 
will not have access to this target (localhost in node/pod is different that localhost in 
your notebook/server).

## 3. API Gateway
 - TBD.