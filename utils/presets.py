def breathe_effect():
    return '{"seg": {"fx": 2, "sx": 100, "ix":255} }'

def fast_breathe_effect():
    return '{"seg": { "fx": 2, "sx": 255, "ix":255} }'

def no_blinck():
    return '{"seg": {"fx": 0} }'


def win_color():
    return '{ "playlist": { "ps": [1, 2, 3, 4], "dur": [10, 10, 10, 10], "transition": 5, "repeat": 0, "end": 1 } }'