# Sloan Preliminary Project v1: 
## MaxOnes String Matching with AFPO

All code is in basic python 3.6 (no NumPy). MaxOnes is a problem in which a
population of individuals is evaluated based on their proximity to a target
bit string consisting solely of ones. Fitness is defined to be the ratio of 
correct to incorrect guesses (e.g. target=[1,1], i=[0,1], fitness = 0.5).
Mutation, then, corresponds to randomized bit-flipping.

AFPO is a multi-objective evolutionary algorithm which seeks to preserve the
innovations of younger cohorts by protecting them from domination by their 
older counterparts. An individual is only dominated (that is, removed from
the population) if another individual has BOTH higher fitness and a lower age.
Descendants inherit the age of their parent.

In the event of a tie (same fitness; same age) the individual who was spawned 
most recently is preserved. The reason for this is to expose a greater number
of possible phenotypic pathways to selection (Wagner, 2011).

Parameters like population size and length of genetic strings are modifiable 
in the "Run" file.
