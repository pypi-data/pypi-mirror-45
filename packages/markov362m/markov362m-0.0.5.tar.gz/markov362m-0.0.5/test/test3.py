import sys
sys.path.append("..") 

import markov362m as mk
import markov362m.examples as mke
import markov362m.io as mio

m2 = mke.professor()


m = mke.facility(p=0.3)
m.set_probability("2-0-0-0","2-0-0-0", 1)
m.set_probability("2-0-0-0","0-0-1-1",0)
m.set_probability("2-0-0-0","1-0-1-0",0)
m.compute()
mio.view(m)

