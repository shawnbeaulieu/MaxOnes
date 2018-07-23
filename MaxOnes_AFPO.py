#!/usr/bin/env python3.6
# AFPO.py
# Author: Shawn Beaulieu
# July 20th, 2018

import copy
import math
import random

def Save_Data(content):
    """
    Store data for later use.
     
    """    

    keys = sorted(content.keys())
    with open("AFPO_History.csv", "a+") as f:
        # AGE, FITNESS, ID, ORIGIN
        #  .      .      .     .
        #  .      .      .     .
        #  .      .      .     .
        L = ",".join([str(content[key]) for key in keys if key != 'genome'])
        f.write(L)
        f.write("\n")

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
        self.current_gen = 0
        self.idx = 0
        self.children = self.Initialize_Population(self.popsize, self.max_gene_len)
        self.Evolve()

    def Initialize_Population(self, size, length):
  
        """
        Creates a list of size "size" of individuals with genomes
        of length "length".

        """

        pop = []

        for p in range(size):

            child = {

                'genome': [random.choice(range(2)) for _ in range(length)],
                'fitness': 0,
                'age': 0,
                'origin': self.current_gen,
                'id': self.idx

            }

            pop.append(child)
            self.idx += 1
 
        return(pop)

    
    def Evolve(self):

        """
        This function loops through the number of generations, calling 
        other functions that dictate evolution. Champions are printed at
        the end of every generation.

        Logic flow: 

            (1) Initialize parents
            (2) Evaluate children
            (3) Filter by AFPO
            (4) Obtain new parents
            (5) Spawn new children based on (4)

        """

        self.parents = list()
        for g in range(self.max_generations):
            for child in self.children:
                child['fitness'] = self.Evaluate(child)
                # Write information to file:
                Save_Data(child)                

            self.Selection()
            
            # Report current champion fitness:
            champ = self.champion['fitness']
            print("Generation {0}/{1}: Champion={2}".format(self.current_gen, self.max_generations, champ))
           
            self.current_gen += 1
            # Spawn a new population of individuals
            self.Spawn()
            
    def Evaluate(self, child):

        """
        Finds the ratio of correct to incorrect entries

        """

        score = sum([int(child['genome'][x] == self.target[x]) for x in range(self.max_gene_len)])
        return(float(score)/len(child['genome']))

    def Selection(self):

        """
        Filtration.

        If the current generation == 0, then just take the fittest individual to be
        the sole parent for the next generation. Otherwise, call AFPO.

        """

        if self.current_gen == 0:
   
            # For first generation, just take the fittest individual
            self.Find_Champion(seed=0.0)
            self.Mature()
            self.parents.append(self.champion)

        else:

            self.Age_Fitness_Selection()
            self.Mature()
            self.Find_Champion(seed=self.champion['fitness'])        

    def Mature(self):
   
        """
        Increments the age of the surviving parents.

        """

        for parent in self.parents:
            parent['age'] += 1

    def Find_Champion(self, seed):

        """
        Locates the current champion

        """

        max_score = seed
        for child in self.children:
            if child['fitness'] > max_score:
                max_score = child['fitness']
                self.champion = child

    def Age_Fitness_Selection(self):

        """
        Looks for domination by age and fitness. If an individual is non-dominated
        (i.e. no other individual is both younger and fitter) then it survives into
        the next generation and gives birth to offspring.

        """

        # Held out (non-dominated) parents during evaluation
        self.children = self.parents + self.children
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
                # Individuals are only dominated if the challenger has
                # (1) greater fitness and lower age;
                # and (2) greater fitness and same age
                # If challenger has lower age AND lower fitness, the candidate
                # is non-dominated.
                if challenger['fitness'] > candidate['fitness']:
                    if not candidate['age'] < challenger['age']:
                        dominated = True
                        break

                # If identical, take the individual more recently generated (phenotype maps)
                elif (challenger['age'] == candidate['age']) and (candidate['fitness'] == challenger['fitness']):
                    if j < i:
                        dominated = True
                        break

            # If individual survives tests above, they survive (non-dominated)
            if not dominated:
                self.parents.append(candidate)

        # Print age and fitness for validation
        #for p in self.parents:
        #    print(p['age'], p['fitness'])

    def Spawn(self):

        """
        Fills out the rest of the population with mutated versions of the non-dominated 
        parents. One slot is saved for a "baby" individual, with age 0 and randomized genome.

        """

        self.children = list()
        # Only need to evaluate (popsize-len(parents)) strings:
        while len(self.children) < (self.popsize - len(self.parents) - 1):
        
            # Randomly select a parent to copy and mutate
            progenitor = self.parents[random.choice(range(len(self.parents)))]
            # Add mutated parent to new child population:
            new_child = self.Mutate(copy.deepcopy(progenitor))
            self.children.append(new_child)

        # Add baby
        self.children += self.Initialize_Population(1, self.max_gene_len)

    def Mutate(self, child):
   
        """
        Bit-flipper

        """
        # S:ingle N:ucleotide P:olymorphism
        # Single gene mutation (bit flip)
        SNP = random.choice(range(self.max_gene_len))
        child['genome'][SNP] = abs(child['genome'][SNP]-1)
        return(child)

