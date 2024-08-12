import cProfile
import pstats
from functools import partial
import time

# Import your function or anything else required
from create_strategy_tables import test_a_move_with_dealer_avrage, build_a_strategy_table
from class_of_cards import Card, Hand


from strategy import find_blackjack_move

from tensor_strategies import get_move, find_blackjack_move_tensor
from simulation import multi_process_multi_player_simulation









def profile_function(func, *args, **kwargs):
    """
    Profiles a given function with the specified arguments and keyword arguments.
    
    Args:
        func (callable): The function to profile.
        *args: Positional arguments passed to the function.
        **kwargs: Keyword arguments passed to the function.
    """
    profiler = cProfile.Profile()
    profiler.enable()  # Start profiling

    func(*args, **kwargs)  # Call the function with provided arguments

    profiler.disable()  # Stop profiling
    
    # Correctly accessing the function name from a functools.partial object
    if isinstance(func, partial):
        function_name = func.func.__name__
    else:
        function_name = func.__name__
    
    # Save the stats to a text file named after the function
    filename = f'{function_name}_profiling_results.txt'
    with open(filename, 'w') as file:
        stats = pstats.Stats(profiler, stream=file)
        stats.sort_stats('cumulative')
        stats.print_stats()  # Output directly into the file



def measure_time(func, iterations=100, *args, **kwargs):
    total_time = 0
    min_time = float('inf')
    max_time = 0

    for _ in range(iterations):
        start_time = time.time()
        func(*args, **kwargs)
        duration = time.time() - start_time
        total_time += duration
        min_time = min(min_time, duration)
        max_time = max(max_time, duration)

    average_time = total_time / iterations
    print(f"Average execution time over {iterations} runs: {average_time:.5f} seconds")
    print(f"Min time: {min_time:.5f} seconds, Max time: {max_time:.5f} seconds")
    print(f'Total time for {iterations} runs: {total_time:.2f} seconds')


if __name__ == '__main__':
    # Example usage with a specific function
    # card1, card2 = Card(suit='Hearts', value=7), Card(suit='Hearts', value=7)
    # player_cards = [card1, card2]
    # dealer_card = Card(suit='Hearts', value=7)
    # hand =  Hand(cards = player_cards)
    # # move_to_test = 'SP'
    # true_count = 0

    # # profile_function(find_blackjack_move_tensor,hand=hand, dealer_card=dealer_card, true_count=true_count, strategy_version=1)
    # measure_time(find_blackjack_move_tensor,hand=hand, dealer_card=dealer_card, true_count=true_count, strategy_version=1)


    num_of_players = 3
    num_of_rounds = 50
    num_of_sim = 100
    num_decks = 7
    deck_penetration = 4
    strategy_version = 1



    profile_function(func=multi_process_multi_player_simulation,num_simulations=num_of_sim,num_rounds=num_of_rounds,
                                          num_of_players= num_of_players,strategy_version=strategy_version)



