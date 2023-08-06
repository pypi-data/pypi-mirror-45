import sys
sys.path.append("..") 

import markov362m as mk
import markov362m.examples as mke

m = mk.MarkovChain("My first chain")
m.add_state("A")
m.add_state("B")
m.add_state("Stop")
m.add_transition("A","B", probability = 0.5)
m.add_transition("A","A", probability = 0.5)
m.add_transition("B","A", probability = 0.5)
m.add_transition("B","Stop", probability = 0.5)
m.add_transition("Stop","Stop")
m.compute()

print(m.info())

mke.list_examples()
