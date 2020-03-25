with open('/sys/class/power_supply/BAT1/charge_now', 'r') as f:
    current = f.read()
with open('/sys/class/power_supply/BAT1/charge_full', 'r') as f:
    full = f.read()
battery = int(int(current)*100/int(full))