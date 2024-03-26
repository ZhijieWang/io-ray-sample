import ray
import os
import subprocess

import time
# establish inter connections
ray.init()

@ray.remote
class MinerActor():
    def __init__(self):
        # different ways to implement subsystem call from python programm to shell commands
        # the nodes does not share a common file system, so if yo need to execute a binary, you need to download it across
        # i.e. start the entire process with a curl download
        # https://www.digitalocean.com/community/tutorials/python-system-command-os-subprocess-call
        cmd = "git --version"
        returned_value = os.system(cmd)
        print(returned_value)

        returned_value = subprocess.call(cmd, shell=True)


# launching the actor(s) with the detached life cycle, so the actors won't die after the driver program exits
# launching actor(s) with a name so later other porgram can refer to the actor.
# setting number of GPUs to be equal to the number of GPUs on a single machine
# this will make sure the scheduler allocate a single machine dedicated to this actor
# otherwise scheduler will share / pool resources
# see full documentation  here 
# https://docs.ray.io/en/latest/ray-core/scheduling/resources.html#resource-requirements
# https://docs.ray.io/en/latest/ray-core/actors/named-actors.html
minerActor = MinerActor.options(lifetime = "detached", name="MinerActor1", num_gpus=8).remote()
# you can launch multiple copies of the actor across the entire cluster, just use different names.
# you can also allocate 1 GPU per actor, as long as the binary is able to know which GPU to use, for example
# for example launching the actor with some value/id so the function can assign GPUID to the binary program.
time.wait(5)
