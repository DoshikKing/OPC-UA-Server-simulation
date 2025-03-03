import asyncio
from random import randint, uniform
from asyncua import Server, ua, uamethod

from globalVars import TEMP_NORMAL_LEVEL

# Initializing servers devices
async def setup(objects, idx):
    # Room 1
    room1 = await objects.add_object(idx, "Room1")
    # Room 2
    room2 = await objects.add_object(idx, "Room2")
    # Room 3
    room3 = await objects.add_object(idx, "Room3")

    # Sensors of room1
    temp1 = await room1.add_variable(idx, "Temperature sensor room 1",
                                     ua.Variant(TEMP_NORMAL_LEVEL, ua.VariantType.Double))
    await temp1.set_read_only()

    move1 = await room1.add_variable(idx, "Movement sensor room 1", ua.Variant(0, ua.VariantType.Double))
    await move1.set_read_only()

    # Devices of room1
    heat1 = await room1.add_variable(idx, "Heat dev room 1", ua.Variant(False, ua.VariantType.UInt16))
    await heat1.set_writable()

    light1 = await room1.add_variable(idx, "Light dev room 1", ua.Variant(False, ua.VariantType.Boolean))
    await light1.set_writable()

    vent1 = await room1.add_variable(idx, "Vent dev room 1", ua.Variant(False, ua.VariantType.UInt16))
    await vent1.set_writable()

    # Service of room1
    fault_var_room1 = await room1.add_variable(idx, "Set fault for concrete device", ua.Variant("", ua.VariantType.String))
    await fault_var_room1.set_writable()

    auto_process_room1 = await room1.add_variable(idx, "Set auto process status", ua.Variant(True, ua.VariantType.Boolean))
    await auto_process_room1.set_writable()

    # Sensors of room2
    temp2 = await room2.add_variable(idx, "Temperature sensor room 2",
                                     ua.Variant(TEMP_NORMAL_LEVEL, ua.VariantType.Double))
    await temp2.set_read_only()

    move2 = await room2.add_variable(idx, "Movement sensor room 2", ua.Variant(0, ua.VariantType.Double))
    await move2.set_read_only()

    # Devices of room2
    heat2 = await room2.add_variable(idx, "Heat dev room 1", ua.Variant(False, ua.VariantType.UInt16))
    await heat2.set_writable()

    light2 = await room2.add_variable(idx, "Light dev room 1", ua.Variant(False, ua.VariantType.Boolean))
    await light2.set_writable()

    vent2 = await room2.add_variable(idx, "Vent dev room 1", ua.Variant(False, ua.VariantType.UInt16))
    await vent2.set_writable()

    # Service of room2
    fault_var_room2 = await room2.add_variable(idx, "Set fault for concrete device", ua.Variant("", ua.VariantType.String))
    await fault_var_room2.set_writable()

    auto_process_room2 = await room2.add_variable(idx, "Set auto process status", ua.Variant(True, ua.VariantType.Boolean))
    await auto_process_room2.set_writable()

    # Sensors of room3
    temp3 = await room3.add_variable(idx, "Temperature sensor room 3",
                                     ua.Variant(TEMP_NORMAL_LEVEL, ua.VariantType.Double))
    await temp3.set_read_only()

    move3 = await room3.add_variable(idx, "Movement sensor room 3", ua.Variant(0, ua.VariantType.Double))
    await move3.set_read_only()

    # Devices of room3
    heat3 = await room3.add_variable(idx, "Heat dev room 3", ua.Variant(False, ua.VariantType.UInt16))
    await heat3.set_writable()

    light3 = await room3.add_variable(idx, "Light dev room 3", ua.Variant(False, ua.VariantType.Boolean))
    await light3.set_writable()

    vent3 = await room3.add_variable(idx, "Vent dev room 3", ua.Variant(False, ua.VariantType.UInt16))
    await vent3.set_writable()

    # Service of room 3
    fault_var_room3 = await room3.add_variable(idx, "Set fault for concrete device", ua.Variant("", ua.VariantType.String))
    await fault_var_room3.set_writable()

    auto_process_room3 = await room3.add_variable(idx, "Set auto process status", ua.Variant(True, ua.VariantType.Boolean))
    await auto_process_room3.set_writable()

    # t - temp device,
    # m - move device,
    # h - heat device,
    # l - light device,
    # v - vent device
    # a - property for auto process
    return dict([
        ("t1", temp1),
        ("t2", temp2),
        ("t3", temp3),
        ("m1", move1),
        ("m2", move2),
        ("m3", move3),
        ("h1", heat1),
        ("h2", heat2),
        ("h3", heat3),
        ("l1", light1),
        ("l2", light2),
        ("l3", light3),
        ("v1", vent1),
        ("v2", vent2),
        ("v3", vent3),
        ("a1", auto_process_room1),
        ("a2", auto_process_room2),
        ("a3", auto_process_room3)
    ])
