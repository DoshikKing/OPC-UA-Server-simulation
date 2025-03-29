import asyncio
import logging
import traceback
from random import randint, uniform
from asyncua import Server, ua

from deviceInit import setup
from globalVars import TEMP_NORMAL_LEVEL, status_bad, status_good, _logger
from simulation import simulate_movement_behavior as smb
from simulation import simulate_heat_behavior as shb
from simulation import simulate_light_behavior as slb
from simulation import simulate_temp_behavior as stb
from simulation import simulate_vent_behavior as svb
from simulation import simulate_fault_behavior as sfb

# Used for keeping status of fault tasks
fault_behavior_tasks = dict([
    ("t1", False),
    ("t2", False),
    ("t3", False),
    ("m1", False),
    ("m2", False),
    ("m3", False),
    ("h1", False),
    ("h2", False),
    ("h3", False),
    ("l1", False),
    ("l2", False),
    ("l3", False),
    ("v1", False),
    ("v2", False),
    ("v3", False)
])

# Finds broken device
def find_fault(device_name):
    for k, v in fault_behavior_tasks.items():
        if k == device_name:
            return v


async def main():
    # Server init
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://127.0.0.1:4840/freeopcua/server/")
    idx = await server.register_namespace("http://my-main-name-space.ru")

    # Setup server objects and variables
    devices = await setup(server.nodes.objects, idx)

    _logger.info("Starting server!")

    async with server:
        while True:
            # Simulating fault behavior
            for k, v in fault_behavior_tasks.items():
                if v:
                    await asyncio.create_task(sfb(devices.get(k)))
                    fault_behavior_tasks.update({k: True})

            # Simulating behaviour for room 1
            # Simulating temp
            if find_fault("v1") is False \
                    and find_fault("t1") is False \
                    and find_fault("h1") is False:
                await asyncio.create_task(
                    stb(devices.get("v1"), devices.get("t1"), devices.get("h1")))
            if find_fault("v1") is False \
                    and find_fault("t1") is False:
                await asyncio.create_task(svb(devices.get("v1"), devices.get("t1"), devices.get("a1")))
            if find_fault("t1") is False \
                    and find_fault("h1") is False:
                await asyncio.create_task(shb(devices.get("h1"), devices.get("t1"), devices.get("a1")))

            # Simulating light
            if find_fault("m1") is False:
                await asyncio.create_task(smb(devices.get("m1")))
            if find_fault("l1") is False \
                    and find_fault("m1") is False:
                await asyncio.create_task(slb(devices.get("l1"), devices.get("m1"), devices.get("p1"), devices.get("a1")))

            # Simulating behaviour for room 2
            # Simulating temp
            if find_fault("v2") is False \
                    and find_fault("t2") is False \
                    and find_fault("h2") is False:
                await asyncio.create_task(
                    stb(devices.get("v2"), devices.get("t2"), devices.get("h2")))
            if find_fault("v2") is False \
                    and find_fault("t2") is False:
                await asyncio.create_task(svb(devices.get("v2"), devices.get("t2"), devices.get("a2")))
            if find_fault("t2") is False \
                    and find_fault("h2") is False:
                await asyncio.create_task(shb(devices.get("h2"), devices.get("t2"), devices.get("a2")))

            # Simulating light
            if find_fault("m2") is False:
                await asyncio.create_task(smb(devices.get("m2")))
            if find_fault("l2") is False \
                    and find_fault("m2") is False:
                await asyncio.create_task(slb(devices.get("l2"), devices.get("m2"), devices.get("p2"), devices.get("a2")))

            # Simulating behaviour for room 3
            # Simulating temp
            if find_fault("v3") is False \
                    and find_fault("t3") is False \
                    and find_fault("h3") is False:
                await asyncio.create_task(
                    stb(devices.get("v3"), devices.get("t3"), devices.get("h3")))
            if find_fault("v3") is False \
                    and find_fault("t3") is False:
                await asyncio.create_task(svb(devices.get("v3"), devices.get("t3"), devices.get("a3")))
            if find_fault("t3") is False \
                    and find_fault("h3") is False:
                await asyncio.create_task(shb(devices.get("h3"), devices.get("t3"), devices.get("a3")))

            # Simulating light
            if find_fault("m3") is False:
                await asyncio.create_task(smb(devices.get("m3")))
            if find_fault("l3") is False \
                    and find_fault("m3") is False:
                await asyncio.create_task(slb(devices.get("l3"), devices.get("m3"), devices.get("p3"), devices.get("a3")))

            await asyncio.sleep(1)


# Prog start point
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
