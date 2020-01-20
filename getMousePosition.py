import pyautogui as pg
print('Press Ctrl-C to stop')
try:
    while True:
        x,y = pg.position()
        positionStr = 'X: ' + str(x).rjust(8) + 'Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone.')