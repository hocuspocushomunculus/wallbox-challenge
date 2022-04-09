#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function and unit test cases for problem #3:

`A function that given a sequence of coin flips (0 is tails, 1 is heads) finds the
minimum quantity of permutations so that the sequence ends interspersed. For
example, given the sequence 0,1,1,0 how many changes are needed so that the
result is 0,1,0,1`

"""

import unittest
from typing import List

def find_minimum_quantity_of_flips(sequence: List[int]) -> int:
    """
    Given a sequence (list) of coin flips (0 is tails, 1 is heads),
    find the minimum quantity of flips so that the sequence forms an
    alternating sequence of ones and zeros, e.g.: 0,1,0,1 or 1,0,1,0.

    Examples:
    - from 0,1,1,0 it takes 2 flips to end up in 0,1,0,1
    - from 0,1,1,0 it takes 2 flips to end up in 1,0,1,0
    --> Minimum quantity of flips is 2
    - from 0,1,1,1 it takes 1 flip to end up in 0,1,0,1
    - from 0,1,1,1 it takes 3 flips to end up in 1,0,1,0
    --> Minimum quantity of flips is 1

    :param sequence:        list, sequence of coinflips (ones and zeros)
    :return:                int, minimum quantity of flips achieving the
                            alternating sequence.
    """
    # Specify ideal sequences of alternating 1s and 0s
    ideal_sequence_0 = [0 if i % 2 == 0 else 1 for i in range(len(sequence))]
    ideal_sequence_1 = [0 if i % 2 == 1 else 1 for i in range(len(sequence))]

    # Calculate difference between ideal alternating sequences
    diff_0 = len(sequence) - len([i for idx, i in enumerate(sequence) \
                 if ideal_sequence_0[idx] == sequence[idx]])
    diff_1 = len(sequence) - len([idx for idx, i in enumerate(sequence) \
                 if ideal_sequence_1[idx] == sequence[idx]])

    # Return the minimum
    return min(diff_0, diff_1)


class TestsForFindMinimumQuantityOfFlips(unittest.TestCase):
    """
    Class to contain test cases for function `find_minimum_quantity_of_flips`
    """

    def test_minimum_quantity_found_for_short_sequences(self):
        """
        Run the `find_minimum_quantity_of_flips` function for relatively short
        sequences of coin flips
        """
        sequences_needing_no_flips = [
            [0],
            [1],
            [0, 1],
            [1, 0]
        ]
        for sequence in sequences_needing_no_flips:
            self.assertEqual(find_minimum_quantity_of_flips(sequence), 0)

        # Note: not taking into account all the combinations 3 flips could yield
        sequences_needing_1_flip = [
            [0, 0],
            [1, 1],
            [0, 1, 1],
            [0, 0, 1]
        ]
        for sequence in sequences_needing_1_flip:
            self.assertEqual(find_minimum_quantity_of_flips(sequence), 1)


    def test_minimum_quantity_found_for_long_sequence(self):
        """
        Run the `find_minimum_quantity_of_flips` function for a longer sequence
        of coin flips
        """
        sequence = [0, 1, 1, 0, 0, 0, 1, 0, 1]
        #           ^  ^        ^               (needs 3 flips)

        self.assertEqual(find_minimum_quantity_of_flips(sequence), 3)


if __name__ == "__main__":
    unittest.main()
