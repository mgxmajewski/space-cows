###########################
# 6.00.2x Problem Set 1: Space Cows

from ps1_partition import get_partitions
import time
from collections import OrderedDict


# ================================
# Part A: Transporting Space Cows
# ================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


def sort_cows(cows_to_sort):
    """
    Sort dictionary with cows
    :param cows_to_sort: unsorted dictionary
    :returns: sorted dictionary
    """
    sorted_cows = OrderedDict(sorted(cows_to_sort.items(), key=lambda item: item[1], reverse = True))
    return sorted_cows


def select_cows_per_trip(cow_left_to_pick, space_limit):
    """
    Selects cows per each trip
    :param cow_left_to_pick: unsorted dictionary
    :param space_limit: limit of space in transporting vessel
    :returns: sorted dictionary
    """
    total_weight = 0
    temp_result = []
    for cow in cow_left_to_pick:
        if total_weight + cow_left_to_pick[cow] <= space_limit:
            total_weight += cow_left_to_pick[cow]
            temp_result.append(cow)
    return temp_result


# Problem 1
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = sort_cows(cows.copy())
    space_limit = limit
    result = []
    while len(cows_copy) > 0:
        transport_partition = select_cows_per_trip(cows_copy, space_limit)
        result.append(transport_partition)
        for cow in transport_partition:
            del cows_copy[cow]
    return result


def unique_combination_filter(partitions):
    unique_combinations = []
    for partition in partitions:
        for cow_combination in partition:
            if cow_combination not in unique_combinations:
                unique_combinations.append(cow_combination)
    return unique_combinations


def partition_enumerator(partitions):
    """
    Enumerate all elements of input list of lists
    :param partitions: list of lists
    :returns: tuple enumerating lists of lists
    """
    partitions_enumerated = list(enumerate(partitions))
    return partitions_enumerated


def partition_eval(spaces_menu, partitions_enumerated):
    """
    Count space taken by cows for each partition
    :param spaces_menu: dictionary with space values of each cow
    :param partitions_enumerated: tuple (index, partition)
    :returns: list of tuples with index and value of space taken by each combination
    """
    space_values_of_partitions = []
    for partition in partitions_enumerated:
        partition_index = partition[0]
        cows_list = partition[1]
        space_counter = 0
        for cow in cows_list:
            space_counter += spaces_menu[cow]
        space_values_of_partitions.append((partition_index, space_counter, cows_list))
    return space_values_of_partitions


def find_best_solution(evaluated_partitions, space_limit):
    """
    :param space_limit: limit of space in transporting vessel
    :param evaluated_partitions: tuple containing index, space value, and list of cows names
    :returns: list of best solutions for given space limit
    :"""
    best_score_temp = 0
    best_list_temp = []
    for partition in evaluated_partitions:
        if space_limit >= partition[1] > best_score_temp:
            best_score_temp = partition[1]
            best_list_temp = partition[2]
            if best_score_temp == space_limit:
                best_list_temp = partition[2]
    return best_list_temp


# Problem 2
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = cows.copy()
    space_limit = limit
    result = []
    while len(cows_copy) > 0:
        unique_cows_combination = unique_combination_filter(get_partitions(cows_copy))
        enumerated_cows_partitions = partition_enumerator(unique_cows_combination)
        evaluated_partitions = partition_eval(cows_copy, enumerated_cows_partitions)
        transport_partition = find_best_solution(evaluated_partitions, space_limit)
        result.append(transport_partition)
        for cow in transport_partition:
            del cows_copy[cow]
    return result


# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    greedy_cow_transport(cows, limit)
    end = time.time()
    print("greedy_cow_transport:")
    print(end - start)

    start = time.time()
    brute_force_cow_transport(cows, limit)
    end = time.time()
    print("brute_force_cow_transport:")
    print(end - start)


"""
Here is some test data for you to see the results of your algorithms with.
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 'Moo Moo': 3,
                       'Milkshake': 2, 'Millie': 5, 'Lola': 2, 'Florence': 2, 'Henrietta': 9}
limit = 10
# print(cows)


def start_cow_transport_optimization(cows_dict):

    compare_cow_transport_algorithms()
    print('greedy', greedy_cow_transport(cows_dict, limit))
    print('brute', brute_force_cow_transport(cows_dict, limit))
