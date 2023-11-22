# globals.py

is_switch_on = True

def set_switch_status(status):
    global is_switch_on
    is_switch_on = status

def get_switch_status():
    return is_switch_on