import sys
sys.path.append("..") 

from markov362m import *
from markov362m.io import *
m = patterns_HHH()
print(m.info_QRF())
