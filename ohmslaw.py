import math
import time
import sys

print("Input all known values, must have at least 2")
suppliedTerms = 0
while True:
    voltage = input("Volts: ")
    resistance = input("Ohms: ")
    current = input("Amps: ")
    power = input("Watts: ")

    if power != "":
        suppliedTerms += 1
    if current != "":
        suppliedTerms += 1
    if resistance != "":
        suppliedTerms += 1
    if voltage != "":
        suppliedTerms += 1

    if suppliedTerms < 2:
        print("Not enough terms supplied.")
        suppliedTerms = 0
        continue
    else:
        break

def find_resistance(volts, current, power):
    if volts and current:
        return volts / current;
    if current and power:
        return power / math.pow(current, 2);
    if volts and power:
        return math.pow(volts, 2) / power;
        
def find_voltage(current, resistance, power):
    if current and resistance:
        return current * resistance
    if power and resistance:
        return math.sqrt(power * resistance)
    if current and power:
        return power / resistance

def find_current(voltage, resistance, power):
    if voltage and resistance:
        return voltage / resistance
    if voltage and power:
        return power / voltage
    if resistance and power:
        return math.sqrt(power / resistance)
        
def find_power(voltage, resistance, current):
    if voltage and current:
        return voltage * current
    if current and resistance:
        return math.pow(current, 2) * resistance
    if voltage and resistance:
        return math.pow(voltage, 2) / resistance

def orNone(input) -> float | None:
    if input == "":
        return None
    return float(input)

resistance = orNone(resistance)
voltage = orNone(voltage)
current = orNone(current)
power = orNone(power)

if not resistance:
    resistance = find_resistance(voltage, current, power)
if not voltage:
    voltage = find_voltage(current, resistance, power)
if not current:
    current = find_current(voltage, resistance, power)
if not power:
    power = find_power(voltage, resistance, current)

print(str(voltage) + "V")
print(str(current) + "A " + ((str(current * 0.001) + "mA") if current < 1 else ""))
print(str(resistance) + "Ω")
print(str(power) + "w")

sys.exit(0)

# test cases

print("Beginning tests")
print("Voltage tests")

try:
    print("Test 1 success: " + str(100 == find_voltage(5, 20, None)))
    print("Test 2 success: " + str(10 == find_voltage(None, 20, 5)))
    print("Test 3 success: " + str(4 == find_voltage(5, None, 20)))
except Exception as e:
    print("Voltage tests failed")
    print(e)
time.sleep(3)

print("Current tests")
print("Test 1 success: " + str(4 == find_current(20, 5, None)))
print("Test 2 success: " + str(2 == find_current(None, 5, 20)))
print("Test 3 success: " + str(4 == find_current(5, None, 20)))

time.sleep(3)

print("Power tests")

print("Test 1 success: " + str(1.25 == find_power(5, 20, None)))
print("Test 2 success: " + str(500 == find_power(None, 20, 5)))
print("Test 3 success: " + str(100 == find_power(5, None, 20)))

time.sleep(3)

print("Resistance tests")
print("Test 1 success: " + str(4 == find_resistance(20, 5, None)))
print("Test 2 success: " + str(0.8 == find_resistance(None, 5, 20)))
print("Test 3 success: " + str(1.25 == find_resistance(5, None, 20)))

time.sleep(3)
