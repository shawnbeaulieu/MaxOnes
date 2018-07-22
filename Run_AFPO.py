#!/usr/bin/env python3.6
# RUN_AFPO.py
# Author: Shawn Beaulieu
# July 20th, 2018

from MaxOnes_AFPO import AFPO

if __name__ == '__main__':

    parameters = {

        'popsize': 100,
        'max_gene_len': 500,
        'target': [1]*500,
        'max_generations': 500

    }

    AFPO(parameters)
