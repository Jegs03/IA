import numpy as np
import random
from itertools import product

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
        self.frontera = []
        self.choices =[]
        self.flags = []
        self.tablero=None
        self.destapadas=[]
        self.reglas=[regla1,regla2,regla3,regla4]
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
   
    def calc_frontera(self):
        #Tablero es un np.array
        w,h = self.states[-1].shape
        coords = product(range(h), range(w))
        for i,j in coords:
            val = self.see_mat[i,j]
            if val != -1 and val !=0:
                self.frontera.append((i,j,val))

    def program(self):
        print(self.actions)
        if len(self.actions) == 0:
            self.plan.append((0,0))
        else:
            for x in self.frontera:
                for r in self.reglas:
                    if r == regla2:
                        self.flags.append(r(x[0],x[1],self.tablero,self.flags))
                    else:
                        self.plan.append(r(x[0],x[1],self.tablero))
                        
    
            
            
def regla1(j,i,tablero):
    k=tablero[i,j]
    n=0
    tapadas=[]
    for x in range(-1,2):
        for y in range(-1,2):
            val=(tablero[i+x,j+y])
            if i+x<0 or j+y<0:
                continue
            print(f'val={val}',f'x={j+x}',f'y={i+y}')
            if val==-1:
                n+=1
                tapadas.append((j+x,i+y))
    if n==k:
        return tapadas
def regla2(j,i,tablero,flag):
    k=tablero[i,j]
    n=0
    flageadas=[]
    for x in range(-1,2):
        for y in range(-1,2):
            val=(tablero[i+x,j+y])
            if i+x<0 or j+y<0:
                continue
            print(f'val={val}',f'x={j+x}',f'y={i+y}')

            if (j+x,i+y) in flag:
                n+=1
            else:    
                flageadas.append((j+x,i+y))
    if n==k:
        return flageadas
def regla3(j,i,t):
    res=-1
    ls=[]
    k=t[i,j]
    lineas=np.array([[t[i,j-1],t[i,j],t[i,j+1]],[t[i-1,j],t[i,j],t[i+1,j]]])
    print(lineas)
    #print(lineas)
    if k==2:
        for x in range(2):
            g=np.array([1,2,1])
            if lineas[x].all()==g.all():
                res=x
    if res==0:
        ls.append((i,j-1))
        ls.append((i,j+1))
    if res==1:
        ls.append((i-1,j))
        ls.append((i+1,j))
    return ls


def regla4(j,i,t):
    res=-1
    ls=[]
    k=t[i,j]
    lineas=np.array([[t[i,j-1],t[i,j],t[i,j+1]],[t[i-1,j],t[i,j],t[i+1,j]]])
    print(lineas)
    #print(lineas)
    if k==2:
        for x in range(2):
            g=np.array([1,2,1])
            if lineas[x].all()==g.all():
                res=x
    if res==0:
        ls.append((i,j-1))
        ls.append((i,j+1))
    if res==1:
        ls.append((i-1,j))
        ls.append((i+1,j))
    return ls

