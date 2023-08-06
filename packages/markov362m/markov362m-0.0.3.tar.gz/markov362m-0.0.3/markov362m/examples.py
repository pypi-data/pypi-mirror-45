import math
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout 
from markov362m.base import MarkovChain

def _rst(alpha, sx, sy, dx, dy, x,y):
    """Helper for rotate_scale_translate"""

    PI_OVER_180 = 0.0174533
    cosa = math.cos(alpha*PI_OVER_180)
    sina = math.sin(alpha*PI_OVER_180)
    xp = sx*(cosa * x + sina * y)+dx
    yp = sy*(sina * x - cosa * y)+dy
    return([xp,yp])

def _rotate_scale_translate(point_dict, angle = 0, stretch_x = 1, 
        stretch_y = 1,  move_x = 0, move_y = 0):
    """Applies an affine transformation to a layout dictionary 
    for a Markov chain

    args:
        point_dict (dict): dictionary of states to positions [x,y]
        angle (float, optional) : angle of rotation
        stretch_x(float, optional) : stretch factor in x, defaults to 1
        stretch_y(float, optional) : stretch factor in y, defaults to 1
        move_x(float, optional) : translation in x, defaults to 1
        move_y(float, optional) : translation in y, defaults to 0

    Returns:
        a layout dictionary (dict of positions [x,y,z,...] with z, ...
        discarded)

    """
    return( { k:_rst(angle, stretch_x, stretch_y, move_x, move_y, v[0], v[1]) 
        for k,v in point_dict.items()} )

def attached_cycles(n1 = 4, n2 = 6, pA = 0.5, tail = False):
    """A Markov chain with two attached cycles and a tail.

    Args:
        n1 (int) : size of the first cycle
        n2 (int) : size of the second cycle
        pA (float) : probability of choosing the first cycle
        tail (bool) : whether to add a tail to the chain

    Returns: 
        a MarkovChain object

    """
    assert n1 > 1 and n2 > 1, \
            "Cycles need to be at least 2 states in length"
    
    m=MarkovChain(title="Attached_Cycles")

    # nodes (must make them explicitly blue if you use graphviz)
    m.add_state("AB1")

    for i in range(2,n1+1):
        m.add_state("A"+str(i))
    
    for i in range(2,n2+1):
        m.add_state("B"+str(i))

    m.add_transition("AB1","A2", probability = pA)
    m.add_transition("AB1","B2", probability = pA)
    m.add_transition("A"+str(n1),"AB1")
    m.add_transition("B"+str(n2),"AB1")
    if n1 > 2:
        for i in range(2,n1):
            m.add_transition("A"+str(i), "A"+str(i+1))
    if n2 > 2:
        for i in range(2,n2):
            m.add_transition("B"+str(i), "B"+str(i+1))

    # adding a tail
    if tail:
        m.add_state("C2")
        m.add_transition("AB1","C2")
        m.add_transition("C2","C2")
        m.set_probability("AB1","A2",pA/2)
        m.set_probability("AB1","C2",pA/2)

    # Layout
    ###############
    # pre_layout = graphviz_layout(m.graph, prog="fdp", 
            # args = "-Gmodel=subset -Gnodesep=1.5") 
    pre_layout = nx.kamada_kawai_layout(m, weight=1)
    layout = _rotate_scale_translate(pre_layout, angle = -90, 
            stretch_x = 2, stretch_y = 2)
    for s,pos in layout.items():
        m.states[s]["position"]= pos
    m.set_canvas(180,150)
    m.compute()
    return(m)

def gambler(a=5, p=0.25):
    """The chain for "Gambler's ruin" problem.

    Args: 
        p (float): the probability of winning in a single round
        a (int): the goal amount

    Returns: 
        a MarkovChain object.
    """
    
    assert a>2, "a must be at least 3"
    assert 0<p and p<1, "p must be in (0,1)"

    m=MarkovChain(title="Gambler")

    # nodes (must make them explicitly blue if you use graphviz)
    for i in range(a+1):
        m.add_state(str(i), color="blue", position = [i,0]);
        
    m.set_color(str(0),"orange")
    m.set_color(str(a),"orange")

    # transitions
    for i in range(1,a):
        m.add_transition(str(i), str(i-1), 
                probability = 1-p,
                label = "1-p",curve = 0.2)
        m.add_transition(str(i), str(i+1), 
                probability = p,
                label = "p", curve = 0.2)
    m.set_curve(str(1), str(0),0)
    m.set_curve(str(a-1), str(a),0)

    m.add_transition(str(0), str(0))
    m.add_transition(str(a), str(a))
    m.set_loop_direction(str(0),"u")
    m.set_loop_direction(str(a),"u")

    # Layout
    ###############

    m.set_canvas(180,150)
    m.compute()
    return(m)


def mc8_1():
    # """The chain for problem MC8_1 
    
    # Returns: a MarkovChain object
    # """
    
    m=MarkovChain(title="MC8_1")

    # nodes (must make them explicitly blue if you use graphviz)
    for i in range(8):
        m.add_state(str(i+1), color="blue");

    # From 1
    m.add_transition("1","1",probability = 0.5, label="1/2")
    m.add_transition("1","2",probability = 0.5, label="1/2")

    # From 2
    m.add_transition("2","3",probability = 0.5, label="1/2")
    m.add_transition("2","7",probability = 0.5, label="1/2")

    # From 3
    m.add_transition("3","4",curve = 0.2)

    # From 4
    m.add_transition("4","3",probability = 0.5, label="1/2",curve=0.2);
    m.add_transition("4","5",probability = 0.5, label="1/2")

    # From 5
    m.add_transition("5","6")

    # From 6
    m.add_transition("6","3",probability = 0.5, label="1/2")
    m.add_transition("6","6",probability = 0.5, label="1/2")

    # From 7
    m.add_transition("7","8",curve=0.2);

    # From 5
    m.add_transition("8","7",probability = 0.75, label="3/4", curve=0.2);
    m.add_transition("8","8",probability = 0.25, label="1/4")

    # loops
    m.set_loop_direction("1","ur")
    m.set_loop_direction("8","ur")
    m.set_loop_direction("6","ur")

    # Layout
    ###############
    pre_layout = graphviz_layout(m, prog="fdp", 
            args = "-Gmodel=subset -Gnodesep=1.5") 
    layout = _rotate_scale_translate(pre_layout, angle = -90, 
            stretch_x = 2, stretch_y = 2)
    m.set_layout(layout)
    m.set_canvas(180,150)
    m.compute()
    return(m)

def facility(p=0.4):
    """The chain for problem about the airline reservation system and its
    computers which get repaired
    
    Args: 
        p (float): the probability of a computer breakdown

    Returns: 
        a MarkovChain object
    """

    m = MarkovChain(title = "MC14-1")

    # states
    m.add_state("0-0-1-1", shape = 1);
    m.add_state("2-0-0-0", shape = 1);
    m.add_state("1-1-0-0", shape = 1);
    m.add_state("0-1-0-1", shape = 1);
    m.add_state("1-0-1-0", shape = 1);
    
    # edges
    m.add_transition("0-0-1-1","0-1-0-1",
            label="1", probability = 1)
    m.add_transition("2-0-0-0","0-0-1-1",
            label="p^2", probability = p**2 )
    m.add_transition("2-0-0-0","2-0-0-0",
            label="(1-p)^2", probability = (1-p)**2)
    m.add_transition("2-0-0-0","1-0-1-0",
            label="2p(1-p)", probability = 2* p*(1-p) )
    m.add_transition("1-1-0-0","2-0-0-0",
            label="1-p", probability = (1-p) )
    m.add_transition("1-1-0-0","1-0-1-0",
            label="p",curve=0.2, probability = p)
    m.add_transition("1-0-1-0","1-1-0-0",
            label="1-p",curve=0.2, probability = (1-p) )
    m.add_transition("1-0-1-0","0-1-0-1",
            label="p",curve=0.2, probability = p )
    m.add_transition("0-1-0-1","1-0-1-0",
            label="1",curve=0.2, probability = 1 )
    
    # loops
    m.set_loop_direction("2-0-0-0","d")
    
    # Layout
    pre_layout =  nx.kamada_kawai_layout(m, weight = 1)
    layout = _rotate_scale_translate(pre_layout, angle = -80)
    m.set_layout(layout)
    m.compute()
    return(m)

def mc20_1():
    # """The chain for problem MC20_1."""
    
    m = MarkovChain(title="MC20_1")
    g = m

    m.set_canvas(140,130)

    # nodes
    for i in range(7):
        m.add_state(str(i))

    the_transitions = {
            (1,2,1,"1"),
            (2,3,1,"1"),
            (3,4,1,"1"),
            (4,5,1,"1"),
            (5,1,1,"1"),
            (0,1,0.5,"1/2"),
            (0,6,0.5,"1/2"),
            (6,6,1,"1")
            }

    for (i1,i2,p,l) in the_transitions:
        m.add_transition(str(i1), str(i2), probability = p, label = l)

    # pre_layout =  nx.kamada_kawai_layout(g, weight = 1)
    pre_layout = graphviz_layout(g, prog="neato", args = "-Gnodesep=1.5") 
    layout = _rotate_scale_translate(pre_layout, angle = -90, stretch_x = 20, 
            stretch_y = 20)
    m.set_layout(layout)
    # m.compute()
    return(m)


def mc21_1():
    # """The chain for problem MC21_1
    
    # Returns: a MarkovChain object
    # """

    m = Markov(title="MC21_1")
    g = m
   
    # states
    for state in range(1,3+1):
        m.add_state(str(state))
   
    # transitions
    m.add_transition( "1","2", probability = 1, label = "1", curve = 0.1)
    m.add_transition( "2","1", probability = 0.25, label = "1/4", curve = 0.1)
    m.add_transition( "2","2", probability = 0.50, label = "1/2")
    m.add_transition( "2","3", probability = 0.25, label = "1/4")
    m.add_transition( "3","3", probability = 1, label = "1", color="orange")
   
    # loop directions
    m.set_loop_direction("2","d")
    m.set_loop_direction("3","d")
    
    # the layout
    pre_layout = graphviz_layout(g, prog="dot", args = "-GNodesep=1")
    the_layout = _rotate_scale_translate(pre_layout, angle = 90)
    m.set_layout(the_layout)
    m.compute()
    return(m)

def professor(p_morning = 0.05, p_afternoon = 0.20):
    """The Markov chain with the professor and umbrellas.

    Args:
        p_morning (float): probability of raining in the morning. Defaults
            to 0.05.
        p_afternoon (float): probability of raining in the afternoon.
            Defaults to 0.2.

    Returns: 
        a MarkovChain object

    """
    # constants
    q_morning = 1-p_morning
    q_afternoon = 1-p_afternoon
    p_morning_label = "p_m"
    q_morning_label = "q_m"
    p_afternoon_label = "p_a"
    q_afternoon_label = "q_a"
    
    
    m = MarkovChain(title = "professor")
    g = m
    
    for p in ["H", "O"]:
        for u in range(6):
            m.add_state( p+str(u))
    
    # absorbing states get a different color and a loop direction
    m.set_color("H5","orange")
    m.set_color("O5","orange")
    
    m.set_loop_direction("H5","d")
    m.set_loop_direction("O5","u")
    
    # add edges to g
    for i in range(5):
        init = "H" + str(i)
        term = "O" + str(4 - i)
        m.add_transition(init, term, 
                probability=q_morning, 
                label=q_morning_label, 
                curve = 0.2)
    
        if i>0:
            init = "H" + str(i)
            term = "O" + str(5 - i)
            m.add_transition(init, term, 
                    probability=p_morning, 
                    label=p_morning_label, 
                    curve = 0.2)
    
        init = "O" + str(i)
        term = "H" + str(4 - i)
        m.add_transition(init, term, 
                probability=q_afternoon, 
                label=q_afternoon_label, 
                curve = 0.2)
    
        if i>0:
            init = "O" + str(i)
            term = "H" + str(5 - i)
            m.add_transition(init, term, 
                    probability=p_afternoon, 
                    label=p_afternoon_label, 
                    curve = 0.2)
    
    m.add_transition("H0", "H5", 
            probability=p_morning, 
            label=p_morning_label)
    m.add_transition("O0", "O5", 
            probability=p_afternoon, 
            label=p_afternoon_label)
    m.add_transition("H5", "H5")
    m.add_transition("O5", "O5")
    
    # make arrow between O2 and H2 curve a bit more
    m.set_curve("O2","H2",0.5)
    m.set_curve("H2","O2",0.5)
    
    # Layout
    
    manual_layout = {
            'H5': [0.2,0], 'H0': [1,0], 'O4': [2,0], 
            'H1': [3,0], 'O3': [4,0], 'H2': [5,0],
            'O2': [5,1], 'H3': [4,1], 'O1': [3,1], 
            'H4': [2,1], 'O0': [1,1], 'O5': [0.2,1]
            }

    m.set_canvas(220,100)
    the_layout = _rotate_scale_translate(manual_layout, 
            stretch_x =  10, stretch_y = 10, 
            move_x = 20, move_y = 20)
    m.set_layout(the_layout)
    
    # last minute tweaks
    m.rename("H5","Hw")
    m.rename("O5","Ow")
    m.relabel("Hw","Hw")
    m.relabel("Ow","Ow")

    m.compute()
    return(m)

def tennis(p = 0.4):
    """The tennis chain.

    Args:
        p (float): the probability that S wins in a single rally

    Returns: 
        a MarkovChain object

    """
    m = MarkovChain(title = "tennis")
    g = m

    points = ["0","15","30","40","A"]
    
    def label(l):
        [i,j] = l
        if i<5 and j<5:
            return(""+points[i]+"-"+points[j]+"")
        elif i==5:
            return("$S_{win}$")
        else:
            return("$R_{win}$")
    
    def name(l):
        [i,j] = l
        if i<5 and j<5:
            return(""+points[i]+"-"+points[j]+"")
        elif i==5:
            return("S")
        else:
            return("R")
    
    
    # BUILDING THE GRAPH
    nodes_game = [ [i,j] for i in range(4) for j in range(4) ]
    nodes_other = [ [3,4], [4,3], [5,0], [0,5] ]
    nodes = nodes_game+nodes_other
    
    for nd in nodes:
        clr = "blue"
        if nd == [5,0] or nd == [0,5]:
            clr = "orange"
        m.add_state(name(nd),label=label(nd),color=clr)
   
    m.set_loop_direction(name([5,0]),"d")
    m.set_loop_direction(name([0,5]),"u")

    p_label = 'p'
    q_label = 'q'
    q=1-p
    
    for i in range(4):
        for j in range(4):
            if i<3:
                m.add_transition(name((i,j)), name((i+1,j)),
                        label=p_label, probability = p)
            elif j<3:
                m.add_transition(name((i,j)), name((5,0)),
                        label=p_label, probability = p)
            if j<3: 
                m.add_transition(name((i,j)), name((i,j+1)),
                        label=q_label, probability = q)
            elif i<3:
                m.add_transition(name((i,j)), name((0,5)),
                        label=q_label, probability = q)

    # advantages back and forth
    m.add_transition(name((3,3)),name((3,4)),
            label=q_label, curve=0.2, probability=q)
    m.add_transition(name((3,3)),name((4,3)),
            label=p_label, curve=0.2, probability=p)
    m.add_transition(name((4,3)),name((3,3)),
            label=q_label, curve=0.2, probability=q)
    m.add_transition(name((3,4)),name((3,3)),
            label=p_label, curve=0.2, probability=p)
    
    # wins
    m.add_transition(name((3,4)),name((0,5)),
            label=q_label,  probability=q)
    m.add_transition(name((4,3)),name((5,0)),
            label=p_label,  probability=p)
    m.add_transition(name((5,0)),name((5,0)))
    m.add_transition(name((0,5)),name((0,5)))
    
    
    # Layout
    m.set_canvas(160,110)
    pre_layout =  nx.kamada_kawai_layout(g, weight = 1)
    the_layout = _rotate_scale_translate(pre_layout, 
            angle = -104, stretch_x = 20, stretch_y = 20, 
            move_x = 30, move_y = 30)
    m.set_layout(the_layout)
    m.compute()
    return(m)

def patterns_HTH():
    """A chain used to analyze coin-tossing patterns"""

    m=MarkovChain(title = "Patterns")
    states = ["0","H","HT","Win"]
    for i,s in enumerate(states):
        m.add_state(s, position = [float(i),0])
    m.set_color("Win","orange")
    m.add_transition("0","0", probability = 0.5, label = "1/2")
    m.add_transition("0","H",probability = 0.5, label = "1/2")
    m.add_transition("H","H",probability = 0.5, label = "1/2")
    m.add_transition("H","HT",probability = 0.5, label = "1/2")
    m.add_transition("HT","0",probability = 0.5, label = "1/2", curve = -0.3)
    m.add_transition("HT","Win",probability = 0.5, label = "1/2")
    m.add_transition("Win","Win")
    m.set_loop_direction("0","u")
    m.set_loop_direction("H","u")
    m.set_loop_direction("Win","u")

    m.set_canvas(180,50)
    m.compute()
    return(m)

def patterns_HHH():
    """A chain used to analyze coin-tossing patterns"""

    m=MarkovChain(title = "Patterns")
    states = ["0","H","HH","Win"]
    for i,s in enumerate(states):
        m.add_state(s, position = [float(i),0])
    m.set_color("Win","orange")
    m.add_transition("0","0", probability = 0.5, label = "1/2")
    m.add_transition("0","H",probability = 0.5, label = "1/2")
    m.add_transition("H","0",probability = 0.5, label = "1/2", curve = 0.3)
    m.add_transition("H","HH",probability = 0.5, label = "1/2")
    m.add_transition("HH","0",probability = 0.5, label = "1/2", curve = -0.3)
    m.add_transition("HH","Win",probability = 0.5, label = "1/2")
    m.add_transition("Win","Win")

    m.set_loop_direction("0","u")
    m.set_loop_direction("H","u")
    m.set_loop_direction("Win","u")

    m.set_canvas(180,50)
    m.compute()
    return(m)
