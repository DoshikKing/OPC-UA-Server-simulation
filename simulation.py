import asyncio
from asyncua import ua
from globalVars import status_good, status_bad, TEMP_NORMAL_LEVEL, _logger

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


def random_for_temp_device(value):
    new_value = calculate_smooth_random(value, TEMP_NORMAL_LEVEL, 10, 5)


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


async def simulate_basic_behavior(device, range_of_values):
    type_of_data = await device.read_data_type_as_variant_type()
    random_value = None
    if type_of_data == ua.VariantType.Boolean:
        random_value = (False if randint(0, 1) >= 0 else True)
    if type_of_data == ua.VariantType.Double:
        random_value = uniform(range_of_values[0], range_of_values[1])

    await set_value(device, random_value, status_good)


async def simulate_fault_behavior(device):
    type_of_data = await device.read_data_type_as_variant_type()
    critical_value = None
    if type_of_data == ua.VariantType.Boolean:
        critical_value = (False if randint(0, 1) >= 0 else True)
    if type_of_data == ua.VariantType.Double:
        critical_value = uniform(10.0, 10000000.0)

    await set_value(device, critical_value, status_bad)


async def simulate_light_behavior(device, sensor):
    val_s = await sensor.read_data_value()

    if val_s.Value.Value >= 7.5:
        await set_value(device, True, status_good)
    else:
        await set_value(device, False, status_good)


async def simulate_temp_behavior(vent_device, temp_device, heat_device, auto_status):
    val_v = await vent_device.read_data_value()
    val_t = await temp_device.read_data_value()
    val_h = await heat_device.read_data_value()

    if auto_status.Value.Value:
        if val_v.Value.Value:
            await set_value(temp_device, val_t.Value.Value - uniform(0.0, 35.5), status_good)
        if val_h.Value.Value:
            await set_value(temp_device, val_t.Value.Value + uniform(0.0, 35.5), status_good)
        

async def simulate_heat_behavior(heat_device, temp_device):
    val_t = await temp_device.read_data_value()

    if val_t.Value.Value <= TEMP_NORMAL_LEVEL:
        await set_value(heat_device, True, status_good)
    else:
        await set_value(heat_device, False, status_good)


async def simulate_vent_behavior(vent_device, temp_device):
    val_t = await temp_device.read_data_value()

    if val_t.Value.Value >= TEMP_NORMAL_LEVEL:
        await set_value(vent_device, True, status_good)
    else:
        await set_value(vent_device, False, status_good)