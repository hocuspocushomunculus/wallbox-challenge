#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function and unit test cases for problem #2:

`A function that given a path of the file system finds the first file that meets the
following requirements
    a. The file owner is admin (== root in Linux)
    b. The file is executable
    c. The file has a size lower than 14*2^20`

"""

import os
import shutil
import logging
import itertools
import unittest
import subprocess
from pathlib import Path

LOGGER = logging.getLogger(__name__)
SIZE_LIMIT = 14*2**20

def find_first_file_with_criteria(path_to_be_checked: str) -> str:
    """
    Given a path, find and return the first file that
    meets the following requirements:
        a. The file owner is admin (== root in Linux)
        b. The file is executable
        c. The file has a size lower than 14*2^20

    If no such file was found, raise an IndexError.

    :param path_to_be_checked:      str, path to look for files fulfilling
                                    all the criteria.
    :return:                        str, path to the file fulfilling all the
                                    criteria.
    """
    p_find = subprocess.check_output(
        ["find", path_to_be_checked,
         "-type", "f",
         "-user", "root",
         "-perm", "-u+x",
         "-size", "-" + str(SIZE_LIMIT) + "c"]
    )

    files_meeting_criteria = p_find.decode().split("\n")

    LOGGER.debug("path_to_be_checked was: %s", path_to_be_checked)
    LOGGER.debug("files_meeting_criteria: %s", files_meeting_criteria)

    # We'll always get at least a list: [''], so check the first element
    if files_meeting_criteria[0] != '':
        return files_meeting_criteria[0]

    raise IndexError("No files were found fulfilling the search criteria.")


class TestsForFindFirstFileWithCriteria(unittest.TestCase):
    """
    Class to contain test cases for function `find_first_file_with_criteria`
    """

    @classmethod
    def setUpClass(cls):
        """
        Create directories and files that will be tried against
        `find_first_file_with_criteria` function
        """
        # Generic class attributes
        cls.features = ["root", "executable", "smaller"]
        cls.positive_file = "test_file_root_executable_smaller"

        # Create directories
        cls.base_folder = "/tmp/"
        cls.positive_folder = os.path.join(cls.base_folder, "positive")
        Path(cls.positive_folder).mkdir(parents=True, exist_ok=True)
        cls.negative_folder = os.path.join(cls.base_folder, "negative")
        Path(cls.negative_folder).mkdir(parents=True, exist_ok=True)

        # Create files
        cls._create_test_files()

        # Print out the files that were created for both positive and negative case
        LOGGER.debug(subprocess.check_output(["ls", "-la", "/tmp/positive/"]).decode())
        LOGGER.debug(subprocess.check_output(["ls", "-la", "/tmp/negative/"]).decode())


    @classmethod
    def _create_test_files(cls):
        """
        Create as many files as many combinations are possible with `cls.features`.
        Currently there are 3 features, so there are 2**3=8 possible different
        combination.

        Put the file having all the features in `cls.positive_folder` and the
        rest of the files in `cls.negative_folder`.
        """
        # Generate all possible combinations
        combinations = cls._generate_combinations_of_features()
        test_file_names = ["test_file_" + "_".join(combination) \
                           for combination in combinations]

        # Loop through the filenames
        for test_file_name in test_file_names:
            path_to_test_file = os.path.join(cls.negative_folder, test_file_name)

            # Handle file size specifications
            if "smaller" in test_file_name:
                # SIZE_LIMIT - 2 will be 1 byte less than the limit we set
                file_size = SIZE_LIMIT - 2
            else:
                # SIZE_LIMIT will be 1 byte greater than the limit we set
                file_size = SIZE_LIMIT

            # Create a file of certain size
            with open(path_to_test_file, "wb") as out:
                out.seek(file_size)
                out.write(b'\0')

            # Handle file ownership
            if "root" in test_file_name:
                # uid & gid of 0 is 'root'
                os.chown(path_to_test_file, 0, 0)
            else:
                # We're using the overflowuid (usually the id for user 'nobody')
                overflowuid = subprocess.check_output(["cat", "/proc/sys/fs/overflowuid"]) \
                                .decode().strip()
                os.chown(path_to_test_file, int(overflowuid), int(overflowuid))

            if "executable" in test_file_name:
                # Using octal representation of file permissions
                os.chmod(path_to_test_file, 0o777)

        # Move the only positive file having all 3 features to `cls.positive_folder`
        shutil.move(os.path.join(cls.base_folder, cls.negative_folder, cls.positive_file),
                    os.path.join(cls.base_folder, cls.positive_folder, cls.positive_file),)


    @classmethod
    def _generate_combinations_of_features(cls):
        """
        Use itertools to generate all the possible combinations of features of:
        - owner is root
        - file is executable
        - file is smaller in size than `SIZE_LIMIT` global variable
        """
        combinations = []

        for i in range(0, len(cls.features) + 1):
            for subset in itertools.combinations(cls.features, i):
                combinations.append(subset)

        return combinations


    def test_file_fulfilling_conditions_is_found(self):
        """
        Run the `find_first_file_with_criteria` function against `cls.positive_folder`
        and see that we indeed get back `cls.positive_file` as result
        """
        self.assertEqual(find_first_file_with_criteria(self.positive_folder),
                         os.path.join(self.positive_folder, self.positive_file),
                         f"{self.positive_file} not returned by function")


    def test_file_fulfilling_conditions_is_not_found(self):
        """
        Run the `find_first_file_with_criteria` function against `cls.negative_folder`
        and see that IndexError is raised
        """

        with self.assertRaises(IndexError) as context:
            find_first_file_with_criteria(self.negative_folder)

        self.assertTrue('No files were found fulfilling' in str(context.exception),
                        "Did not receive expected error message.")


if __name__ == "__main__":
    unittest.main()
