import random
from typing import Generator
from time import sleep


getting = '\033[44;97;1mG\033[0m'
waiting = '\033[33;41;100;1mW\033[0m'
limit = 25
mut = [0]

def tsk(quantity) -> set:
    return [random.randint(1, 10) for x in range(quantity)]


def progress(row_: int, ls: list, mode='net') -> Generator:
    cnt = 1
    for a in ls:
        while mode == 'disk' and mut[0]:
            yield f'\033[{str(row_)};{str(cnt)}H{waiting}'
        mut[0] = 1
        for x in range(a):
            sleep(.2)
            yield f'\033[{str(row_)};{str(cnt)}H{getting}'
        mut[0] = 0
        for x in range(a):
            sleep(.1)
            if cnt > limit:
                yield f'\033[{str(row_)};{str(cnt)}H OK'
                return
            yield f'\033[{str(row_)};{str(cnt)}H*'
            cnt += 1
    else:
        yield f'\033[{str(row_ + 1)}HEnd of data'


def single():
    for c in range(1, 13, 3):
        for x in progress(c, tsk(5)):
            print(x, end='', flush=True)


def multi():
    while True:
        res = [next(x, '') for x in threads]
        if any(res):
            for s in res:
                print(s, end='', flush=True)
        else:
            return

match input('Choose mode:\n\t1 - Monothread\n\t2 - Multithread with\
 disk\n\t3 - Multithread with net\n\n\t'):
    case '1':
        print('\033[1J')
        single()
    case '2':
        print('\033[1J')
        threads = [progress(x, tsk(6), mode='disk')\
         for x in range(1, 13, 3)]
        multi()
    case '3':
        print('\033[1J')
        threads = [progress(x, tsk(5)) for x in range(1, 13, 3)]
        multi()
    case _:
        print('Incorrect input')

print('\033[16H')