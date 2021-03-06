from model import Model
from problem import Problem
from state import State
from cardinal import action
from tree import TreeNode

from cardinal import *


class Agent:
    """"""
    counter = -1  # Contador de passos no plano, usado na deliberação

    def __init__(self, model):
        """Construtor do agente.
        @param model: Referência do ambiente onde o agente atuará."""
        self.model = model

        self.prob = Problem()

        self.prob.createMaze(9, 9)

        self.prob.mazeBelief.putVerticalWall(0, 1, 0)
        self.prob.mazeBelief.putVerticalWall(0, 0, 1)
        self.prob.mazeBelief.putHorizontalWall(4, 6, 0)
        self.prob.mazeBelief.putVerticalWall(0, 1, 7)
        self.prob.mazeBelief.putHorizontalWall(3, 5, 2)
        self.prob.mazeBelief.putHorizontalWall(3, 5, 3)
        self.prob.mazeBelief.putHorizontalWall(7, 7, 3)
        self.prob.mazeBelief.putHorizontalWall(1, 2, 5)
        self.prob.mazeBelief.putVerticalWall(6, 7, 1)
        self.prob.mazeBelief.putVerticalWall(6, 7, 4)
        self.prob.mazeBelief.putVerticalWall(5, 6, 5)
        self.prob.mazeBelief.putVerticalWall(5, 7, 7)
        self.prob.mazeBelief.putHorizontalWall(1, 2, 8)

        # Posiciona fisicamente o agente no estado inicial
        initial = self.positionSensor()
        self.prob.defInitialState(initial.row, initial.col)

        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Define o estado objetivo
        self.prob.defGoalState(2, 8)

        # o metodo abaixo serve apenas para a view desenhar a pos objetivo
        self.model.setGoalPos(2, 8)

        # Plano de busca - inicialmente vazio (equivale a solucao)
        self.plan = None

    def printPlan(self):
        """Apresenta o plano de busca."""
        print("--- PLANO ---")
        # @TODO: Implementação do aluno
        for plannedAction in self.plan:
            print("{} > ".format(action[plannedAction]), end='')
        print("FIM\n\n")

    def deliberate(self):
        # Primeira chamada, realiza busca para elaborar um plano

        if self.counter == -1:

            self.plan = [N, N, N, NE, L, L, L, L, L, L, NE, N];

            if self.plan != None:
                self.printPlan()
            else:
                print("SOLUÇÃO NÃO ENCONTRADA")
                return -1

        # Nas demais chamadas, executa o plano já calculado
        self.counter += 1

        if self.prob.goalTest(self.positionSensor()):
            return -1

        currentAction = self.plan[self.counter]

        self.executeGo(self.plan[self.counter])
        self.currentState = self.positionSensor()

        cost = 0.0
        for i in range(-1, self.counter):
            cost += self.prob.getActionCost(self.plan[i+1])

        print("*****************************************************")
        print("estado atual  : ({0},{1})".format(self.model.agentPos[0], self.model.agentPos[1]))
        print("acoes possiveis:", end='')
        actions = self.prob.possibleActions(self.positionSensor())
        for i in range (0, len(actions)):
            if actions[i] != -1:
                print(" {0}".format(action[i]), end='')
        print("\nct: {0} de {1}".format(self.counter + 1, len(self.plan)))
        print("custo ate o momento (com a acao escolhida): {0}".format(cost))
        print("*****************************************************\n")

        return 1

    def executeGo(self, direction):
        """Atuador: solicita ao agente física para executar a ação.
        @param direction: Direção da ação do agente
        @return 1 caso movimentação tenha sido executada corretamente."""
        self.model.go(direction)
        return 1

    def positionSensor(self):
        """Simula um sensor que realiza a leitura do posição atual no ambiente e traduz para uma instância da classe Estado.
        @return estado que representa a posição atual do agente no labirinto."""
        pos = self.model.agentPos
        return State(pos[0], pos[1])
