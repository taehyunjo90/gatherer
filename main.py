from Apis import Login
from Apis import Multi
import pythoncom
import sys

from multiprocessing import Process


if __name__ == "__main__":

    p0 = Process(target=Multi.doKosdaq)
    p1 = Process(target=Multi.doKospi)
    p2 = Process(target=Multi.doKoreanDerivatiesAndForeignFutures)

    p0.start()
    p1.start()
    p2.start()

    p0.join()
    p1.join()
    p2.join()














