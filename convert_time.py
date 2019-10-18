import math

def pad(num,size):
    sliced = size * -1
    return ('000{}'.format(num))[sliced:]

def sec2time(timeInSeconds):
    time = float(timeInSeconds)
    print("Time : {}".format(time))
    #time = parseFloat(timeInSeconds).toFixed(3),
    hours = math.floor(time / 60 / 60)
    print("Hours : {}".format(hours))
    minutes = math.floor(time / 60) % 60
    print("Mins : {}".format(minutes))
    seconds = math.floor(time - minutes * 60)
    print("Secs : {}".format(seconds))
    time = str('{:.3f}'.format(time))[-3:]
    milliseconds = int(time)
    print("Ms : {}".format(milliseconds))
    return pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2) + '.' + pad(milliseconds, 3)
