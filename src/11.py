from multiprocessing import Pool
import time


def f(x):
    time.sleep(5)
    return x*x

if __name__ == '__main__':
    s1 = time.time()
    with Pool(3) as p:
        s = p.map(f, [1, 4, 3])
    print(s)
    # for i in [1, 2, 3]:
    #     f(i)
    s2 = time.time()
    print(s2-s1)