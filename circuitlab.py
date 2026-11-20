import ti_draw
import math
import ti_system
import sys

ti_draw.clear()

ENTER = 105
UP = 25
RIGHT = 26
LEFT = 24
DOWN = 34
ALPHA = 31
DEL = 23

letterLock = False

numbers = {
    92 : 1,
    93 : 2,
    94 : 3,
    82 : 4,
    83 : 5,
    84 : 6,
    72 : 7,
    73 : 8,
    74 : 9,
    102 : 0
}

special = {
    103 : ".",
    104 : "-",
    41 : "A",
    42 : "B",
    43 : "C",
    51 : "D",
    52 : "E",
    53 : "F",
    54 : "G",
    55 : "H",
    61 : "I",
    62 : "J",
    63 : "K",
    64 : "L",
    65 : "M",
    71 : "N",
    72 : "O",
    73 : "P",
    74 : "Q",
    75 : "R",
    81 : "S",
    82 : "T",
    83 : "U",
    84 : "V",
    85 : "W",
    91 : "X",
    92 : "Y",
    93 : "Z"
}

selected = 0
showingDescription = -1
writtenPoint = 1
toolOpen = False

def prompt(text) -> str | None:
    global letterLock
    clear()
    centerWrite(None, (writtenPoint + 2) * 10, text)
    centerWrite(None, None, "< ")

    written = ""
    k = -1

    while True:
        k = ti_system.get_key(1)

        if k == ALPHA:
            letterLock = not letterLock

        if k == ENTER:
            break

        if k == DEL:
            written = written[0:len(written) - 1]

        if not letterLock:
            if numbers.get(k, -1) != -1:
                written += str(numbers[k])
            elif special.get(k):
                written += special[k]
           
           
        elif special.get(k):
            written += special[k]
        ti_draw.clear_rect(0, 50, 300, 300)
        centerWrite(None, None, "< " + written)
    clear()
    return None if written == "" else written

def clear():
    ti_draw.clear()
    writtenPoint = 1
def centerWrite(x, y, text):
    xPos = x if x is not None else 160 - (5 * len(text))
    yPos = y if y is not None else 115

    ti_draw.draw_text(xPos, yPos, text)
def find_resistance(volts, current, power):
    if volts and current:
        return volts / current;
    if current and power:
        return power / math.pow(current, 2);
    if volts and power:
        return math.pow(volts, 2) / power;
    return None
def find_voltage(current, resistance, power):
    if current and resistance:
        return current * resistance
    if power and resistance:
        return math.sqrt(power * resistance)
    if current and power:
        return power / current
    return None
def find_current(voltage, resistance, power):
    if voltage and resistance:
        return voltage / resistance
    if voltage and power:
        return power / voltage
    if resistance and power:
        return math.sqrt(power / resistance)
    return None
def find_power(voltage, resistance, current):
    if voltage and current:
        return voltage * current
    if current and resistance:
        return math.pow(current, 2) * resistance
    if voltage and resistance:
        return math.pow(voltage, 2) / resistance
    return None
def ohmslaw():
    v = prompt("Voltage (Or skip)") or None
    i = prompt("Current (Or skip)") or None
    r = prompt("Resistance (Or skip)") or None
    p = prompt("Power (Or skip)") or None
   
    try:
        if v:
            v = float(v)
        if i:
            i = float(i)
        if r:
            r = float(r)
        if p:
            p = float(p)
    except:
        invalid_input()
        return
    if not v:
        v = find_voltage(i, r, p)
    if not i:
        i = find_current(v, r, p)
    if not r:
        r = find_resistance(v, i, p)
    if not p:
        p = find_power(v, r, i)

    try:
        centerWrite(None, 25, "Results:")
   
        ti_draw.draw_text(5, 45, "Voltage: " + str(round(v, 2)))
        ti_draw.draw_text(5, 60, "Resistance: " + str(round(r, 2)))
        ti_draw.draw_text(5, 75, "Current: " + str(round(i, 2)))
        ti_draw.draw_text(5, 90, "Power: " + str(round(p, 2)))
    except:
       centerWrite(None, None, "Invalid arguments")

    ti_draw.draw_text(5, 200, "Press any key to return")
    ti_system.get_key(1)
    printTools()

conversions = {
    "Coloumbs" : {
        "Possible" : ["C", "µC", "mC", "nC", "pC"],
        "Multiplier" : [1, 0.000001, 0.001, 0.000000001, 0.000000000001],
        "Current" : 1
    },
    "Newtons" : {
        "Possible" : ["N", "µN", "mN", "nN", "pN"],
        "Multiplier" : [1, 0.000001, 0.001, 0.000000001, 0.000000000001],
        "Current" : 0
    },
    "Meters" : {
        "Possible" : ["m", "mm"],
        "Multiplier" : [1, 0.001],
        "Current" : 0
    },
    "Ohms" : {
        "Possible" : ["Ω", "kΩ", "MΩ", "µΩ"],
        "Multiplier" : [1, 1000, 1000000, 0.000001],
        "Current" : 0
    }
}


def convert(unit, value):
    return value * conversions[unit]["Multiplier"][conversions[unit]["Current"]]

def ensureCurrent(unit):
    if conversions[unit]["Current"] >= len(conversions[unit]["Possible"]):
        conversions[unit]["Current"] = 0

    if conversions[unit]["Current"] < 0:
        conversions[unit]["Current"] = len(conversions[unit]["Possible"]) - 1

def getConversion(unit):
    return conversions[unit]["Possible"][conversions[unit]["Current"]]

def setConversions():
    clear()
    centerWrite(None, 30, "Configurations")
    selected = 0
    writtenPoint = 3

    for conversion in conversions.keys():
            ti_draw.draw_text(5, writtenPoint * 15, conversion + " - " + getConversion(conversion))
            writtenPoint += 1
   
    while True:
        k = ti_system.get_key(1)
        c = list(conversions.keys())[selected]

        if k == UP: # no match statements
            selected -= 1
        if k == DOWN:
            selected += 1

        if k == RIGHT:
            conversions[c]["Current"] += 1
            ensureCurrent(c)
        if k == LEFT:
            conversions[c]["Current"] -= 1
            ensureCurrent(c)

        if k == ENTER:
            clear()
            printTools()
            break

        if selected < 0:
            selected = len(conversions) - 1
        if selected >= len(conversions):
            selected = 0

        clear()

        centerWrite(None, 30, "Configurations")

        writtenPoint = 3
       
        for conversion in conversions.keys():
            ti_draw.draw_text(5, writtenPoint * 15, ("> " if writtenPoint - 3 == selected else "  ") + conversion + " -" + getConversion(conversion))
            writtenPoint += 1

def coloumbsLaw():
    try:
        k = 8.99 * math.pow(10, 9)
        q1 = prompt("Point charge 1 (" + getConversion("Coulomb") + ")") or None
        q2 = prompt("Point charge 2 (" + getConversion("Coulomb") + ")") or None
        d = prompt("Distance (If known) (" + getConversion("Meter") + ")") or None
        f = prompt("Force (If known) (" + getConversion("Newton") + ")") or None

   
        if q1:
            q1 = convert("Coloumbs", float(q1)) # converts to configured conversion
        if q2:
            q2 = convert("Coloumbs", float(q2))
        if d:
            d = convert("Meters", float(d))
        if f:
            f = float(f)
    except Exception as e:
        clear()
        ti_draw.set_color(255, 0, 0)
        centerWrite(None, None, "Error: " + str(e))
        ti_draw.set_color(0, 0, 0)
        ti_system.get_key(1)
        printTools()
        return

   
    # like charges repel

    if (not d and not f) or not q1 or not q2:
        invalid_input()

    a = q1 > 0 and q2 < 0 or q1 < 0 and q2 > 0

    if not f:
        f = convert("Newton", k * (abs(q1 * q2)) / math.pow(d, 2))
    if not d:
        d = math.sqrt((k * abs(q1 * q2)) / f)

    centerWrite(None, 25, "Results:")

    ti_draw.draw_text(5, 45, "Force: " + str(round(f, 2)))
    ti_draw.draw_text(5, 60, "Distance: " + str(round(d, 2)) + getConversion("Meters"))
    ti_draw.draw_text(5, 75, "Q1: " + str(q1) + getConversion("Coloumbs"))
    ti_draw.draw_text(5, 90, "Q2: " + str(2) + getConversion("Coloumbs"))
    ti_draw.draw_text(5, 105, "Attractive" if a else "Repulsive")

    ti_draw.draw_text(5, 200, "Press any key to return")

    ti_system.get_key(1)
    printTools()

tools = {
    "Ohm's Law" : ohmslaw,
    "Coloumb's Law" : coloumbsLaw,
    "Set Conversions" : setConversions,
    "bar" : None,
    "lorum" : None,
    "ipsum" : None
}

toolDescriptions = {
   "Ohm's Law" : "V = IR"
}

def printTools():
    global toolOpen
    toolOpen = False
    index = 0
    ti_draw.clear_rect(0, 0, 500, 500)

    centerWrite(None, 30, "Circuit Lab Tools")
    for tool in tools.keys():
        if index != showingDescription or not toolDescriptions.get(tool):
            ti_draw.draw_text(5, (writtenPoint + index + 3) * 15, "  " + tool if index != selected else "> " + tool)
        else:
            ti_draw.draw_text(5, (writtenPoint + index + 3) * 15, "< " + tool + " " + toolDescriptions[tool] if index != selected else "- " + tool + " " + toolDescriptions[tool])
        index += 1

def empty_tool():
    clear()
    centerWrite(None, None, "Tool does not exist")
    ti_system.get_key(1)
    printTools()

def invalid_input():
    clear()
    centerWrite(None, None, "Tool's input was invalid")
    ti_system.get_key(1)
    printTools()
   

printTools()

while not ti_system.escape():
    try:
        k = ti_system.get_key(1)

        if toolOpen:
            continue

        if k == UP: # no match statements
            selected -= 1
        if k == DOWN:
            selected += 1

        if k == RIGHT:
            showingDescription = selected

        if k == LEFT:
            if showingDescription == selected:
                showingDescription = -1
            else:
                continue

        if selected < 0:
            selected = len(tools) - 1
        if selected >= len(tools):
            selected = 0

        printTools()

        if k == ENTER:
            l = list(tools.values())
            toolOpen = True
            if l[selected] is None:
                empty_tool()
            else:
                l[selected]()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
