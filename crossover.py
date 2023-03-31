import numpy as np
import random as rd

def crossover(fh, fw, mh, mw, cuts=2):
    father_h = fh.flat()
    father_w = fw.flat()

    mother_h = mh.flat()
    mother_w = mw.flat()

    size = len(father_h)

    cuts = rd.sample(range(size), k=cuts)

    

