import x11_client

ARROW_LEFT=113
ARROW_RIGHT=114
ARROW_UP=111
ARROW_DOWN=116

SUPER=133
ALT=64
CTRL=50

SPACE=65
ENTER=36
TAB=23

def arrow_left():
    x11_client.send_key(ARROW_LEFT)

def arrow_right():
    x11_client.send_key(ARROW_RIGHT)

def arrow_up():
    x11_client.send_key(ARROW_UP)

def arrow_down():
    x11_client.send_key(ARROW_DOWN)

def write(word):
    for letter in word:
        if letter == ' ':
            x11_client.send_key(SPACE)
        else:
            x11_client.type(letter)
