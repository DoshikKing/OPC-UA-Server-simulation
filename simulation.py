import asyncio
import random
from random import randint, uniform, getrandbits
from asyncua import ua
from globalVars import status_good, status_bad, TEMP_NORMAL_LEVEL, POWER_SCALE, _logger

# Generating distributed random value
# Alg:
# Calculating Min and Max for Avr
# Calculating limits for distribution: 
#   Getting current value + varience if its greater than Max (helps sliding distribution windows)
#   Getting current value - varience if its lower than Min (helps sliding distribution windows)
# Calculating total varience of given limits
# Calculating new current value based on min limit
# 
# Caviats:
# Need to put in account that value has to change (gravitate) towards some target if auto state is off for devices
# Need to test if "window" would slide randomly (will it go inf up or down?)
def calculate_smooth_random(current_value, average, oscillation, variance):
    max_value = average + oscillation
    min_value = average - oscillation

    max_limit = min(max_value, current_value + variance)
    min_limit = max(min_value, current_value - variance)
    total_variance = max_limit - min_limit

    current_value = min_limit + random.random() * total_variance

    return current_value


def random_for_temp_device(current_value):
    return calculate_smooth_random(current_value, TEMP_NORMAL_LEVEL, 10, 5)


async def set_value(device, value, status):
    status_code = ua.StatusCode(value=status)
    try:
        await device.write_attribute(
            ua.AttributeIds.Value,
            ua.DataValue(
                ua.Variant(value, await device.read_data_type_as_variant_type()),
                StatusCode_=status_code
            )
        )
    except ua.UaStatusCodeError as ex:
        _logger.error(traceback.format_exc())
        pass


async def simulate_movement_behavior(device):
    await set_value(device, bool(getrandbits(1)), status_good)


async def simulate_fault_behavior(devices, fault_status, fault_devices_status):
    val_f = await fault_status.read_data_value()

    if val_f.Value.Value != "":
        device_to_make_fault = devices.get(val_f.Value.Value)

        for k, v in fault_devices_status.items():
            if k == val_f.Value.Value and not v:
                val_d_f = await device_to_make_fault.read_data_value()
                fault_devices_status.update({k: True})
                await set_value(device_to_make_fault, val_d_f.Value.Value, status_bad)
                    


async def simulate_light_behavior(device, sensor, power, auto_status):
    val_s = await sensor.read_data_value()
    val_p = await power.read_data_value()
    val_a = await auto_status.read_data_value()

    if val_a.Value.Value:
        if val_s.Value.Value == True:
            await set_value(device, val_p.Value.Value, status_good)
        else:
            await set_value(device, int(0), status_good)


async def simulate_temp_behavior(vent_device, temp_device, heat_device):
    val_v = await vent_device.read_data_value()
    val_t = await temp_device.read_data_value()
    val_h = await heat_device.read_data_value()

    new_temp = random_for_temp_device(val_t.Value.Value) - (val_v.Value.Value) + (val_h.Value.Value)

    await set_value(temp_device, new_temp, status_good)
        
async def simulate_heat_behavior(heat_device, temp_device, auto_status):
    val_t = await temp_device.read_data_value()
    val_a = await auto_status.read_data_value()
    current_value = val_t.Value.Value

    if val_a.Value.Value:
        if current_value <= TEMP_NORMAL_LEVEL:
            power = -int((round(current_value - TEMP_NORMAL_LEVEL) / POWER_SCALE)) # bug with power sim
            await set_value(heat_device, power, status_good)


async def simulate_vent_behavior(vent_device, temp_device, auto_status):
    val_t = await temp_device.read_data_value()
    val_a = await auto_status.read_data_value()
    current_value = val_t.Value.Value

    if val_a.Value.Value:
        if current_value >= TEMP_NORMAL_LEVEL:
            power = int(round(current_value - TEMP_NORMAL_LEVEL) / POWER_SCALE) # bug with power sim
            await set_value(vent_device, power, status_good)
