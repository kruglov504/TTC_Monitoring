import multiprocessing
import time



def worker1():
    counter = 0
    while True:
        print(counter)
        counter += 1
        time.sleep(1)

def worker2():
    counter = 0
    while True:
        print(counter)
        counter += 1
        time.sleep(1)


if __name__ == '__main__':

    p1 = multiprocessing.Process(target=worker1)
    p2 = multiprocessing.Process(target=worker2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()



