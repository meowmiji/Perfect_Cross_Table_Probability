'''
The short code verifies the probability of when n teams play a BO1 Robin round in a game
and finish up with a perfect score table where teams get all possible scores from the highest
(all wins) to the lowest (all losses), which is n!/2**n (n = #teams).
The code performs very poorly due to the nested loops recursion structure and is almost infeasible when n > 7.

Also I am a noob and super uncomfortable with the no-declaration and avoiding-global-variables way of python coding,
so the code is far from dry and clean.

The inspiration comes from the following reddit post:
https://www.reddit.com/r/DotA2/comments/8929is/group_b_of_dac_is_actually_more_satisfying_than/
'''

import numpy as np

# DANGEROUS globals
total = 0  # #outcomes of all matches
ordered = 0  # #possible combinations that match results form a perfect table
matches = []  # list of all match outcomes: matches=[ai=-1 or 1, i in range(nmatches)]


def scores(matches, nteams):  # set of all teams' scores
    matrix = np.zeros((nteams, nteams), dtype=int)  # matrix is the score cross table
    for i in range(nteams - 1):
        slice_down = i * nteams - i * (i + 1) // 2
        slice_up = slice_down + nteams - i - 1
        matrix[i] = np.concatenate((np.zeros(i + 1, dtype=int), matches[slice_down:slice_up]))
    matrix = matrix - np.transpose(matrix)
    '''
    This part looks quite confusing so let's illustrate with 5 teams A, B, C, D and E.
    This is how the cross table (half) looks like: (1 as win and -1 as loss)
         A	 B	 C	 D	 E
    A		 1	-1	-1	 1
    B			 1	 1	 1
    C				-1	 1
    D					-1
    E	
    The matches list is [AvsB(AB), AC, AD, AE, BC, BD, BE, CD, CE, DE].
    The sentence in the for loop slices corresponding match outcomes (eg: B vs teams that are alphebatically after B)
    and concatenates with some zeros to form a row of the cross table.
    The complete table is Table - Table.T
    '''
    scores = set()
    for i in range(nteams):
        scores.add(np.sum(matrix[i]))  # add up to get one team's score
    return scores  # all different scores teams get


# Nested loops with #matches hierarchies (super clunky)
def recursive(nteams, nmatches, i=0):
    global total
    global ordered
    global matches
    if i <= nmatches - 1:
        for matches[i] in [-1, 1]:
            recursive(nteams, nmatches, i + 1)
    else:
        total += 1
        ordered_scores = {x for x in range(-nteams + 1, nteams, 2)}
        # eg: 5 teams -> {-4, -2, 0, 2, 4}
        if scores(matches, nteams) == ordered_scores:  # when match outcomes are perfect!
            ordered += 1


def calculate_prob(nteams):
    global total
    global ordered
    global mathches
    nmatches = nteams * (nteams - 1) // 2
    matches.extend([None] * nmatches)  # matches global variable initialization
    recursive(nteams, nmatches)
    print('The probability for %d teams is %d / %d = %.4f%%' % (nteams, ordered, total, 100 * ordered / total))


calculate_prob(6)  # Do NOT even try 7 which takes about 130+ s
