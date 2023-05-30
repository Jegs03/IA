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
        self.actions= [(0,0)]
        self.frontera = []
        
        
    def calc_frontera(self):
        #Tablero es un np.array
        w,h = self.states[-1].shape
        coords = product(range(h), range(w))
        for i,j in coords:
            val = self.see_mat[i,j]
            if val != -1 and val !=0:
                self.frontera.append((i,j,val))

    def program(self):
        # Creamos un plan con una acción aleatoria
        self.plan.append(random.choice(self.choices))