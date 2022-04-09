#!/usr/bin/env python3
"""
Function and unit test cases for problem #1:

`A function that given 2 vectors of integers finds the first repeated number`

"""

import unittest
from typing import List


def find_first_repeated_number(vector_a: List[int], vector_b: List[int]) -> int:
    """
    Given 2 vectors (lists) of integers, find the first repeated number.

    If there were no repeated numbers, raise an IndexError.

    :param vector_a:    list, first vector of integers
    :param vector_b:    list, second vector of integers
    :return:            int, first repeated number
    """
    common_numbers = [i for i in vector_a if i in vector_b]

    if common_numbers:
        return common_numbers[0]

    raise IndexError("No repeated numbers in vector_a and vector_b")


class TestsForFindFirstRepeatedNumber(unittest.TestCase):
    """
    Class to contain test cases for function `find_first_repeated_number`
    """

    def test_repeated_numbers(self):
        """
        Check if given 2 vectors which have repeating numbers, that the
        first one is found and returned.
        """
        # Initialize vectors and common_number
        common_number = 4
        vector_a = [1, 2, 3, common_number, 5]
        vector_b = [8, common_number, 5, 6, 7]

        self.assertEqual(find_first_repeated_number(vector_a, vector_b),
                         common_number,
                         ("Repeated number wasn't found, although should have been"
                          f" {common_number}."))


    def test_no_repeated_numbers(self):
        """
        Check if given 2 vectors which don't have any repeating numbers
        that IndexError is raised.
        """
        # Initialize vectors
        vector_a = [1, 2, 3]
        vector_b = [4, 5, 6]

        with self.assertRaises(IndexError) as context:
            find_first_repeated_number(vector_a, vector_b)

        self.assertTrue('No repeated numbers' in str(context.exception),
                        "Did not receive expected error message.")


if __name__ == "__main__":
    unittest.main()
