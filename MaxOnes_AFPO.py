#!/usr/bin/env python3.6
# AFPO.py
# Author: Shawn Beaulieu
# July 20th, 2018

import copy
import math
import random

def Initialize_Population(size, length):

    pop = []

    for p in range(size):
        child = dict()
        child['genome'] = [random.choice(range(2)) for _ in range(length)]
        child['fitness'] = 0
        child['age'] = 0
        pop.append(child)

    return(pop)

class AFPO():

    P = {

        'popsize': 100,
        'max_gene_len': 20,
        'target': [1]*20,
        'max_generations': 500

    }

    def __init__(self, parameters=dict()):
   
        # Receive parameters dictionary from Run_AFPO.py
        # and convert all entries to self.key = value:
        # e.g. parameters = {'popsize':100}
        # >> self.popsize = 100
        # *: non-keyworded dynamic update
        # **: key-worded dynamic update
        self.__dict__.update(AFPO.P, **parameters)

        self.children = Initialize_Population(self.popsize, self.max_gene_len)
        self.Evolve()
    
    def Evolve(self):

        self.parents = list()
        self.current_gen = 0
        for g in range(self.max_generations):

            for child in self.children:
                child['fitness'] = self.Evaluate(child)

            self.Selection()
            # Report current champion fitness:
            champ = self.champion['fitness']
            print("Generation {0}/{1}: Champion={2}".format(self.current_gen, self.max_generations, champ))
            # Spawn a new population of individuals
            self.Spawn()
 
            # Increment sel
            self.current_gen += 1
            
    def Evaluate(self, child):

        score = sum([int(child['genome'][x] == self.target[x]) for x in range(self.max_gene_len)])
        return(float(score)/len(child['genome']))

    def Selection(self):

        if self.current_gen == 0:
   
            # For first generation, just take the fittest individual
            self.Find_Champion(seed=0.0)
            self.parents.append(self.champion)

        else:

            self.Age_Fitness_Selection()
            self.Find_Champion(seed=self.champion['fitness'])        

    def Find_Champion(self, seed):

        max_score = seed
        for child in self.children:
            if child['fitness'] > max_score:
                max_score = child['fitness']
                self.champion = child

    def Age_Fitness_Selection(self):

        # Held out (non-dominated) parents during evaluation
        self.children = self.children + self.parents
        self.parents = list()
 
        for i in range(len(self.children)):

            candidate = self.children[i]

            # Find evidence to reverse prior:
            dominated = False

            # Slice population for comparing "candidate" to remaining individuals
            # candidate vs. challenger

            other = list(range(len(self.children)))
            competitors = other[:i] + other[i+1:]

            for j in competitors:
               
                challenger = self.children[j]

                # If challenger is fitter, candidate must be younger
                if challenger['fitness'] > candidate['fitness']:
                    if not candidate['age'] < challenger['age']:
                        dominated = True
                        break

                # If challenger is younger, candidate must be fitter
                elif challenger['age'] < candidate['age']:
                    if not candidate['fitness'] > challenger['fitness']:
                        dominated = True
                        break
 
                # If identical, take the individual more recently generated (phenotype maps)
                elif challenger['age'] == candidate['age'] and candidate['fitness'] == challenger['fitness']:
                    if j > i:
                        dominated = True
                        break

            # If individual survives tests above, they survive (non-dominated)
            if not dominated:
                # Increment age and append
                candidate['age'] += 1
                self.parents.append(candidate)

    def Spawn(self):

        self.children = list()

        # Only need to evaluate (popsize-len(parents)) strings:
        while len(self.children) < (self.popsize - len(self.parents) - 1):
        
            # Randomly select a parent to copy and mutate
            progenitor = self.parents[random.choice(range(len(self.parents)))]
            # Add mutated parent to new child population:
            new_child = self.Mutate(copy.deepcopy(progenitor))
            self.children.append(new_child)

        self.children += Initialize_Population(1, self.max_gene_len)

    def Mutate(self, child):
   
        # S:ingle N:ucleotide P:olymorphism
        # Single gene mutation (bit flip)
        SNP = random.choice(range(self.max_gene_len))
        child['genome'][SNP] = abs(child['genome'][SNP]-1)
        return(child)

