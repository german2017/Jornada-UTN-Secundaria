DEBUG = False

def set_mode():
    global DEBUG
    DEBUG = not DEBUG

def get_mode():
    return DEBUG