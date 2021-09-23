
from threading import Thread
import time


def sum(max, id):
    global value
    for i in range(0, max):
        value += 1
    print("th[" + str(id) + "] " + str(value))
    return


if __name__ == '__main__':

    
    value = 0
    for i in range(0, 10):
        sum(1000000, i)

    print ("value : " + str(value))
    print ("-------------------------------------")

    value = 0
    thList = []
    for i in range(0, 10):
        th = Thread(target = sum, args=(1000000, i))
        th.start()
        thList.append(th)

    for th in thList:
        th.join()

    print ("thread value : " + str(value))




