from ps1 import partition_enumerator, partition_eval, find_best_solution, brute_force_cow_transport, \
    greedy_cow_transport, sort_cows, select_cows_per_trip
import pytest
from assertpy import assert_that
import collections


class TestBruteForceCowsTransport:

    @pytest.fixture(autouse=True)
    def prepare_brute_force_cow_transport(self):
        self.brute_force_cow_transport = brute_force_cow_transport

    # case1
    cows_to_transport_1 = {'Miss Bella': 25, 'Boo': 20, 'Milkshake': 40, 'Lotus': 40, 'Horns': 25, 'MooMoo': 50}
    space_limit_1 = 100
    expected_1 = [['MooMoo', 'Miss Bella', 'Horns'], ['Milkshake', 'Lotus', 'Boo']]
    case_1 = cows_to_transport_1, space_limit_1, expected_1

    # case2
    cows_to_transport_2 = {'Daisy': 50, 'Buttercup': 72, 'Betsy': 65}
    space_limit_2 = 75
    expected_2 = [['Buttercup'], ['Betsy'], ['Daisy']]
    case_2 = cows_to_transport_2, space_limit_2, expected_2

    # case3
    cows_to_transport_3 = {'Starlight': 54, 'Buttercup': 11, 'Luna': 41, 'Betsy': 39}
    space_limit_3 = 145
    expected_3 = [['Buttercup', 'Starlight', 'Betsy', 'Luna']]
    case_3 = cows_to_transport_3, space_limit_3, expected_3

    @pytest.mark.parametrize("cows_to_transport, space_limit, expected", [case_1, case_2, case_3])
    def test_brute_force_cow_transport(self, cows_to_transport, space_limit, expected):
        # when
        brute_force = self.brute_force_cow_transport(cows_to_transport, space_limit)

        # helper function to compare lists containing same values (no specific order necessary)
        def eval_lists(brute_force_result, expected_solution):
            unordered_transports_comparisons = []
            for transport in range(len(expected_solution)):
                print()
                print(brute_force_result[transport], expected_solution[transport])
                compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
                unordered_transports_comparisons.append(compare(brute_force_result[transport],
                                                                expected_solution[transport]))
            if all([x == True for x in unordered_transports_comparisons]):
                return True
            else:
                return False

        # then
        result = eval_lists(brute_force, expected)
        assert_that(result).is_true()

    def test_partition_enumerator(self):
        # given
        partitions = [["a", "b"], ["c", "d"]]
        expected = [(0, ["a", "b"]), (1, ["c", "d"])]
        # when
        result = partition_enumerator(partitions)
        # then
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_partition_eval(self):
        self.partition_eval = partition_eval

    def test_partition_eval(self):
        # given
        spaces_menu = {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 'Moo Moo': 3,
                       'Milkshake': 2, 'Millie': 5, 'Lola': 2, 'Florence': 2, 'Henrietta': 9}
        test_partition = [(12, ['Betsy', 'Henrietta'])]
        expected = [(12, 18, ['Betsy', 'Henrietta'])]
        # when
        result = self.partition_eval(spaces_menu, test_partition)
        # then
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_find_best_solution(self):
        self.find_best_solution = find_best_solution

    def test_find_best_solution(self):
        # given
        space_limit = 10
        evaluated_partitions = [(12, 18, ['Betsy', 'Henrietta']),
                                (0, 48,
                                 ['Henrietta', 'Millie', 'Lola', 'Florence', 'Moo Moo', 'Herman', 'Betsy', 'Milkshake',
                                  'Maggie', 'Oreo']),
                                (1007, 15, ['Millie', 'Lola', 'Florence', 'Moo Moo', 'Maggie']),
                                (876, 10, ['Florence', 'Lola', 'Maggie', 'Moo Moo'])]
        expected = ['Florence', 'Lola', 'Maggie', 'Moo Moo']
        # when
        result = self.find_best_solution(evaluated_partitions, space_limit)
        print(result)
        # then
        assert_that(result).is_equal_to(expected)


class TestGreedyCowTransport:

    @pytest.fixture(autouse=True)
    def prepare_greedy_cow_transport(self):
        self.greedy_cow_transport = greedy_cow_transport

    # case1
    cows_to_transport_1 = {'Miss Bella': 15, 'Milkshake': 75, 'MooMoo': 85, 'Louis': 45, 'Patches': 60, 'Polaris': 20,
                           'Clover': 5, 'Horns': 50, 'Lotus': 10, 'Muscles': 65}
    space_limit_1 = 100
    expected_1 = [['MooMoo', 'Miss Bella'], ['Milkshake', 'Polaris', 'Clover'], ['Muscles', 'Lotus'], ['Patches'],
                  ['Horns', 'Louis']]
    case_1 = cows_to_transport_1, space_limit_1, expected_1

    # case2
    cows_to_transport_2 = {'Abby': 38, 'Dottie': 85, 'Lilly': 24, 'Buttercup': 72, 'Daisy': 50, 'Betsy': 65,
                           'Willow': 35, 'Rose': 50, 'Coco': 10, 'Patches': 12}
    space_limit_2 = 100
    expected_2 = [['Dottie', 'Patches'], ['Buttercup', 'Lilly'], ['Betsy', 'Willow'], ['Daisy', 'Rose'],
                  ['Abby', 'Coco']]
    case_2 = cows_to_transport_2, space_limit_2, expected_2

    # case3
    cows_to_transport_3 = {'Abby': 28, 'Starlight': 54, 'Buttercup': 11, 'Willow': 59, 'Betsy': 39, 'Luna': 41,
                           'Rose': 42, 'Coco': 59}
    space_limit_3 = 120
    expected_3 = [['Willow', 'Coco'], ['Starlight', 'Rose', 'Buttercup'], ['Luna', 'Betsy', 'Abby']]
    case_3 = cows_to_transport_3, space_limit_3, expected_3

    # case4
    cows_to_transport_4 = {'Patches': 60, 'Polaris': 20, 'Clover': 5, 'Louis': 45, 'Lotus': 10, 'Milkshake': 75,
                           'Miss Bella': 15, 'MooMoo': 85, 'Horns': 50, 'Muscles': 65}
    space_limit_4 = 100
    expected_4 = [['MooMoo', 'Miss Bella'], ['Milkshake', 'Polaris', 'Clover'], ['Muscles', 'Lotus'],
                  ['Patches'], ['Horns', 'Louis']]
    case_4 = cows_to_transport_4, space_limit_4, expected_4

    # case5
    cows_to_transport_5 = {'Daisy': 50, 'Patches': 12, 'Buttercup': 72, 'Betsy': 65, 'Willow': 35, 'Coco': 10,
                           'Dottie': 85, 'Rose': 50, 'Lilly': 24, 'Abby': 38}
    space_limit_5 = 100
    expected_5 = [['Dottie', 'Patches'], ['Buttercup', 'Lilly'], ['Betsy', 'Willow'],
                  ['Rose', 'Daisy'], ['Abby', 'Coco']]
    case_5 = cows_to_transport_5, space_limit_5, expected_5

    # case6
    cows_to_transport_6 = {'Buttercup': 11, 'Betsy': 39, 'Starlight': 54, 'Coco': 59, 'Willow': 59, 'Luna': 41,
                           'Rose': 42, 'Abby': 28}
    space_limit_6 = 120
    expected_6 = [['Willow', 'Coco'], ['Starlight', 'Rose', 'Buttercup'], ['Luna', 'Betsy', 'Abby']]
    case_6 = cows_to_transport_6, space_limit_6, expected_6

    @pytest.mark.parametrize("cows_to_transport, space_limit, expected", [case_1, case_2, case_3, case_4, case_5, case_6])
    def test_greedy_cow_transport(self, cows_to_transport, space_limit, expected):
        # when
        greedy = self.greedy_cow_transport(cows_to_transport, space_limit)

        def eval_lists(greedy_result, expected_solution):
            unordered_transports_comparisons = []
            for transport in range(len(expected_solution)):
                print()
                print(greedy_result[transport], expected_solution[transport])
                compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
                unordered_transports_comparisons.append(compare(greedy_result[transport],
                                                                expected_solution[transport]))
            if all([x == True for x in unordered_transports_comparisons]):
                return True
            else:
                return False

        # then
        result = eval_lists(greedy, expected)
        assert_that(result).is_true()

        # then
        assert_that(result).is_true()

    @pytest.fixture(autouse=True)
    def prepare_sort_cows(self):
        self.sort_cows = sort_cows

    def test_sort_cows(self):
        # given
        cows = {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 'Moo Moo': 3, 'Milkshake': 2, 'Millie': 5, 'Lola': 2,
                'Florence': 2, 'Henrietta': 9}
        expected = {'Betsy': 9, 'Henrietta': 9, 'Herman': 7, 'Oreo': 6, 'Millie': 5, 'Maggie': 3, 'Moo Moo': 3,
                    'Milkshake': 2, 'Lola': 2, 'Florence': 2}
        # when
        result = self.sort_cows(cows)

        # then
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_greedy_one_trip(self):
        self.select_cows_per_trip = select_cows_per_trip

    def test_select_cows_per_trip(self):
        cows_to_transport = {'Abby': 38, 'Dottie': 85, 'Lilly': 24, 'Buttercup': 72, 'Daisy': 50, 'Betsy': 65,
                             'Willow': 35, 'Rose': 50, 'Coco': 10, 'Patches': 12}
        space_limit = 100
        expected = ['Abby', 'Lilly', 'Willow']

        result = self.select_cows_per_trip(cows_to_transport, space_limit)

        assert_that(result).is_equal_to(expected)
