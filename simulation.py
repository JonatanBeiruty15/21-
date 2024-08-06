from class_of_cards import Shoe
from class_of_players import Player, Dealer
import time
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy.stats import norm
from tqdm import tqdm 
import multiprocessing






def plot_with_gaussian(data_lists, title, filename, x_label, y_label, plot_with_gauss):
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']  # Extend this list if you have more players

    plt.figure(figsize=(10, 5))

    for index, data in enumerate(data_lists):
        if len(data) == 0:
            continue  # Skip empty data sets

        # Calculate frequency using Counter
        data_freq = Counter(data)
        values, counts = zip(*data_freq.items())

        # Plotting the scatter of balances
        plt.scatter(values, counts, color=colors[index % len(colors)], label=f'Player {index + 1}')

        if plot_with_gauss:
            # Fit a Gaussian to these data
            mu, std = norm.fit(data)  # Fit a normal distribution to the data

            # Create a range of values for plotting the Gaussian
            xmin, xmax = min(values), max(values)
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mu, std)

            # Scale the Gaussian fit to the maximum count to better visualize overlay
            p *= max(counts)/max(p)

            # Add the density line
            plt.plot(x, p, color=colors[index % len(colors)], linewidth=2, label=f'Gaussian Fit Player {index + 1} (μ={mu:.2f}, σ={std:.2f})')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)

    # Save the plot
    plt.savefig(filename)
    plt.show()









def update_progress(q, total):
    pbar = tqdm(total=total, desc='Progress Bar')
    for _ in iter(q.get, None):  # Terminates on 'None'
        pbar.update()
    pbar.close()






def game_simulation_multiple_players(num_of_rounds=1000, num_decks=7, Print=False, deck_penetration=4, num_of_players=4,strategy_version = 1):
    # Initialize players and a shoe
    start_time = time.time()
    lowest_balance = [0] * num_of_players
    players = [Player(name=f"Player {i+1}", initial_balance=0) for i in range(num_of_players)]
    dealer = Dealer()
    shoe = Shoe(num_decks)

    for round in range(num_of_rounds):
        for i, player in enumerate(players):
            dealer.round(player=player, shoe=shoe, Print=Print, deck_penetration=deck_penetration, num_of_decks=num_decks,strategy_version= strategy_version)
            if player.balance < lowest_balance[i]:
                lowest_balance[i] = player.balance

    duration = time.time() - start_time
    if Print:
        print(f"Simulation took: {duration:.2f} seconds")

    final_balances = [player.balance for player in players]
    return final_balances, lowest_balance




def run_simulation_batch_multi_player(num_simulations, num_rounds, num_decks, Print, deck_penetration, progress_queue, num_of_players):
    results = []
    for _ in range(num_simulations):
        result = game_simulation_multiple_players(num_rounds, num_decks, Print, deck_penetration, num_of_players)
        results.append(result)
        progress_queue.put(1)  # signal progress
    return results



def multi_process_multi_player_simulation(num_simulations=100, num_rounds=10, num_decks=7, num_of_players=4, plot_with_gauss=True, Print=False, deck_penetration=4,strategy_version =1):
    start_time = time.time()  # Start timing here
    num_processes = 4
    simulations_per_process = num_simulations // num_processes

    manager = multiprocessing.Manager()
    progress_queue = manager.Queue()

    pool = multiprocessing.Pool(processes=num_processes)
    watcher = multiprocessing.Process(target=update_progress, args=(progress_queue, num_simulations))
    watcher.start()

    results = pool.starmap(run_simulation_batch_multi_player, [
        (simulations_per_process, num_rounds, num_decks, Print,strategy_version, deck_penetration, progress_queue, num_of_players)
        for _ in range(num_processes)
    ])

    pool.close()
    pool.join()
    progress_queue.put(None)
    watcher.join()

    final_balances = [[] for _ in range(num_of_players)]
    lowest_balances = [[] for _ in range(num_of_players)]
    for batch_results in results:
        for sim_result in batch_results:
            for player_index in range(num_of_players):
                final_balances[player_index].append(sim_result[0][player_index])
                lowest_balances[player_index].append(sim_result[1][player_index])

    positive_balance_percentages = [
        (len([b for b in balances if b > 0]) / num_simulations * 100)
        for balances in final_balances
    ]

    average_final_balances = [sum(balances) / len(balances) for balances in final_balances]
    average_lowest_balances = [sum(balances) / len(balances) for balances in lowest_balances]
    std_final_balances = [np.std(balances) for balances in final_balances]

    filename = f'multi_player_simulation_{num_rounds}_rounds_{num_simulations}_simulations.txt'
    

    with open(filename, 'w') as file:
        file.write("Simulation Parameters:\n")
        file.write(f"Number of Simulations: {num_simulations}\n")
        file.write(f"Strategy version: {strategy_version}\n")
        file.write(f"Number of Rounds: {num_rounds}\n")
        file.write(f"Number of Decks: {num_decks}\n")
        file.write(f"Number of Players: {num_of_players}\n")
        file.write(f"Deck Penetration: {deck_penetration}\n")

        file.write("\n\n")
        for player_index in range(num_of_players):
            file.write(f"Player {player_index + 1} Results:\n")
            file.write(f"Percentage of simulations with a positive balance: {positive_balance_percentages[player_index]:.2f}%\n")
            file.write(f"Average final balance: {average_final_balances[player_index]:.2f}\n")
            file.write(f"Standard deviation of final balance: {std_final_balances[player_index]:.2f}\n")
            file.write(f"Average lowest balance: {average_lowest_balances[player_index]:.2f}\n")
            file.write("\n")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total simulation time: {total_time:.2f} seconds")
    print(f"Results have been saved to '{filename}'")
    plot_with_gaussian(final_balances, 'Frequency of Final Balances Across Simulations', 'final_balances_distribution.png', 'Final Balance', 'Frequency', plot_with_gauss)
    plot_with_gaussian(lowest_balances, 'Frequency of Lowest Balances Across Simulations', 'lowest_balances_distribution.png', 'Lowest Balance', 'Frequency', plot_with_gauss)


    return average_final_balances, average_lowest_balances






if __name__ == "__main__":
    num_of_players = 1
    num_of_rounds = 30
    num_of_sim = 10
    num_decks = 7
    deck_penetration = 4


    multi_process_multi_player_simulation(num_simulations=num_of_sim,num_rounds=num_of_rounds,
                                          num_of_players= num_of_players)
    
 