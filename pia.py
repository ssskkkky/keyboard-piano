from  pynput.keyboard import Key, Listener
from pyo import *
import numpy as np

    
class myfreq(object):
    def __init__(self):
        self.bf = 440
        self.sp = np.linspace(0,11,12)
        self.tune = self.bf*2**(1/12*self.sp)

    def incres(self):
        self.tune *= 2

    def decres(self):
        self.tune /= 2

        
def on_press(key):
    global am,flag
    keyStr = eval(key.__str__())
    if keyStr in fqdict:
        am.freq = float(fq.tune[fqdict[keyStr]])
        env.play()
    elif keyStr == 'g':
        fq.decres()
    elif keyStr == 'h':
        fq.incres()
    elif key == Key.tab:
        if flag:
            am = Sine(ap.rnd, mul=globalamp*env).out()
        else:
            am = Sine(ap.rnd, mul=.2).out()
        flag = not(flag)
    elif key == Key.esc:
        s.stop()
        return False
    else:
        print('Wrong key:')
        print(keyStr)

class autoMusic:
    global am
    def __init__(self):
        self.freqs = midiToHz([60,62,64,65,67,69,71,72])
        self.rnd = Choice(choice=self.freqs, freq=[6,8])

if __name__ == '__main__':
    global am,flag
    flag = False
    fq = myfreq()
    fqdict = {'w':0, 'e':1, 'r':2, 's':3, 'd':4, 'f':5,
              'u':6, 'i':7, 'o':8, 'j':9, 'k':10, 'l':11}
    s = Server()
    s.setOutputDevice(8)
    s.boot()
    s.amp = 0.1
    s.start()
    ap = autoMusic()
    # amp = Fader(dur=1,mul=1).play()    
    globalamp = Fader(fadein=2, fadeout=2, dur=0).play()
    env = Adsr(attack=0.005, decay=0.05, sustain=0.25, release=0.75, dur=1, mul=0.5)
    env.setExp(0.75)
    # am = Adsr(attack=0.01, decay=0.1, sustain=0.5, release=1.5, dur=2, mul=0.5)
    am = Sine(ap.rnd, mul=globalamp*env).out()
    with Listener(
            suppress = True,
            on_press = on_press) as listener:
        listener.join() 
