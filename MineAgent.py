import numpy as np
from random import shuffle
from itertools import product
import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

class Agent :
    '''
    Defines the basic methods for the agent.
    '''

    def __init__(self):
        self.plan = []
        self.states = []
        self.actions = []
        self.rewards = [np.nan]
        self.dones = [False]
        self.turn = 0

    def make_decision(self):
        '''
        Agent makes a decision according to its model.
        '''
        # Chequeamos si ya el agente no tiene un plan (lista de acciones)
        if len(self.plan) == 0:
            # Usamos el programa para crear un plan
            self.program()
        try:
            # La acción a realizar es la primera del plan
            action = self.plan.pop(0)
        except:
            # ¡No hay plan!
            state = self.states[-1]
            raise Exception(f'¡Plan vacío! Revisar reglas en estado {state}')
        self.turn += 1
        return action

    def program(self):
        '''
        Debe ser modificada por cada subclase
        '''
        pass

    def reset(self):
        self.restart()

    def restart(self):
        '''
        Restarts the agent for a new trial.
        '''
        self.plan = []
        self.states = []
        self.actions = []
        self.rewards = [np.nan]
        self.dones = [False]


class MineSweeper_Agent(Agent):
    '''Agente que implementa la lógica hasta no ser posible y después implementa redes Bayesianas'''
    def __init__(self):
        #Tablero es el tablero de MineSweeper
        super().__init__()
        self.start=False
        self.frontera = []
        self.choices =[]
        self.flags = []
        self.tablero=None
        self.plan =[]
        self.reglas=[regla1,regla3]   
   
    def calc_frontera(self):
        #Tablero es un np.array
        w,h = self.states[-1].shape
        coords = product(range(w), range(h))
        for i,j in coords:
            val = self.states[-1][i,j]
            if val != -1 and val !=0:
                self.frontera.append((i,j,val))

    def program(self):
        print(self.actions)
        if len(self.actions) == 0 and not self.start:
            self.plan.append((1,1))
            self.start=True
        else:
            a=regla0(self.states[-1])
            print(a)
            self.plan.extend(a[0])
            self.flags.extend(a[1])
            self.plan = list(set(self.plan))
            self.flags = list(set(self.flags))
            if len(self.plan) == 0:
                self.calc_frontera()
                for x in self.frontera:
                    a=regla2(x[0],x[1],self.states[-1],self.flags)
                    self.plan.extend(a[0])
                    self.flags.extend(a[1])
                    self.plan = list(set(self.plan))
                    self.flags = list(set(self.flags))
                    for r in self.reglas:
                        a = r(x[0],x[1],self.states[-1])
                        if a is not None:
                            if len(a[0]) > 0 or len(a[1])>0:
                                    self.plan.extend(a[0])
                                    self.flags.extend(a[1])
                                    self.plan = list(set(self.plan))
                                    self.flags = list(set(self.flags))
                #if len(self.plan) ==0: #Se calcula la probabilidad  
                    #for x in self.frontera:
                        #BN_x = create_BN(x,self.states[-1])
                        #pass

def regla0(tablero):
    n=0
    for x in range(-1,2):
        for y in range(-1,2):
            k=tablero[x,y]
            if k==-1:
                n+=1
                
    safe=[]
    if n==8:
        safe=[(0,1)]
    return safe,[]
def regla1(i,j,tablero):
    safe=[]
    flags=[]
    k=tablero[i,j]
    n=0
    for x in range(-1,2):
        for y in range(-1,2):
            if tablero.shape[0]>i+x>=0 and tablero.shape[1]>j+y>=0:
                val=(tablero[i+x,j+y])
                if val==-1:
                    n+=1
                    flags.append((j+x,i+y))
    if n==k:
        return safe , flags
    else:
        return [],[]

def regla2(i,j,tablero,flag):
    k=tablero[i,j]
    n=0
    safe=[]
    flageadas=[]
    for x in range(-1,2):
        for y in range(-1,2):
            if tablero.shape[0]>i+x>=0 and tablero.shape[1]>j+y>=0:
                val=(tablero[i+x,j+y])
                continue
            if type(flag) ==list:
                if (i+x,j+y) in flag:
                    n+=1
            else:    
                safe.append((j+x,i+y))
    if n==k: #OJO QUE AQUÍ PUEDE (podía*) DEVOLVER NONES
        return safe ,flageadas 
    else:
        return [],[]

def regla3(i,j,t):
    k=t[i,j]
    if k == 2:
        res=-1
        flags=[]
        safe = []
        w,h = t.shape
        coords = set(list(product(range(w), range(h))))
        lines = [[(i,j-1),(i,j),(i,j+1)],[(i-1,j),(i,j),(i+1,j)]]
        lns_in = []
        for l in lines:
            if coords.intersection(set(l)) == set(l):
                   lns_in.append(l)
        if len(lns_in) == 0:
            return None
        
        for x,s in enumerate(lns_in):
            if [1,2,1] == [t[s[0]],t[s[1]],t[s[2]]]:
                res=x
        if res==0:
            if 0<= i-1 < 8 and 0<= i+1 < 8:
                if t[i-1,j] == -1:
                    flags.append((i-1,j-1))
                    safe.append((i-1,j))
                    flags.append((i-1,j+1))
                else:
                    flags.append((i+1,j-1))
                    safe.append((i+1,j))
                    flags.append((i+1,j+1))       
        if res==1:
            if 0<= j-1 < 8 and 0<= j+1 < 8:
                if t[i,j-1] == -1:
                    flags.append((i-1,j-1))
                    safe.append((i,j-1))
                    flags.append((i+1,j-1))
                else:
                    flags.append((i-1,j+1))
                    safe.append((i,j+1))
                    flags.append((i+1,j+1))
    else:
        return None
    
    return safe, flags
def create_BN(c,t): #c es una casilla que hace parte de la frontera
    x, y = c
    w,h = t.shape
    coords = set(list(product(range(w), range(h))))
    adyacentes =set((x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1))
    nodos_coords = list(coords.intersection(adyacentes))
    nodos = {} #Estos son los nodos en la frontera que tienen números y determinan la probabilidad de una casilla con mina.
    for n in nodos_coords:
        x_n, y_n = n
        if t[x_n,y_n] != -1:
            nodos[str(n)] = t[x_n,y_n]

#IDEAS PARA LOS METODOS DE LA BN
'''
def utility(self, casilla, supuestos):
    #Supuestos: dic de la forma (x,y): z, z siendo el numero que indica cuantas bombas hay alrededor
    q,p = self.calc_prob_CPT(casilla,supuestos)
    return -10000*q+p

def calc_prob_CPT(self, casilla, supuestos):
    #Supuestos: dic de la forma (x,y): z, z siendo el numero que indica cuantas bombas hay alrededor
    w,h = self.states[-1].shape
    prob = 1/w*h
    for s in supuestos:
        casillas = set(self.flags)
        num = supuestos[s]
        adyacentes = set((x+1,y),(x-1,y),(x+1,y+1),(x-1,y+1), (x,y+1),(x+1,y-1),(x-1,y-1),(x,y-1))
        if num-len(adyacentes.intersection(casillas)) >0:
            prob += prob
    return [1-prob, prob]
'''    