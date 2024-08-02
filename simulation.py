from class_of_cards import Shoe
from class_of_players import Player, Dealer
import time
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy.stats import norm
from tqdm import tqdm 



def plot_with_gaussian(data, title, filename, x_label, y_label, plot_with_gauss):
    # Calculate frequency using Counter
    data_freq = Counter(data)
    values, counts = zip(*data_freq.items())

    # Plotting the scatter of balances
    plt.figure(figsize=(10, 5))
    plt.scatter(values, counts, color='blue')

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
        plt.plot(x, p, 'k', linewidth=2)
        title += f' (fit: μ={mu:.2f}, σ={std:.2f})'

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)

    # Save the plot
    plt.savefig(filename)
    plt.show()





def game_simulation_one_player(num_of_rounds = 1000,num_decks=7,Print = False,deck_penetration= 4):
        # Initialize a player and a shoe
    start_time = time.time()
    lowest_balance = 0 
    player = Player(name="John Doe", initial_balance=0)
    dealer = Dealer()
    shoe = Shoe(num_decks) 
    for round in range(num_of_rounds):
        dealer.round(player=player,shoe = shoe, Print= Print, deck_penetration= deck_penetration,num_of_decks=num_decks)
        if player.balance < lowest_balance:
            lowest_balance = player.balance


    

    duration = time.time() - start_time
    # print(f"Simulation took: {duration:.2f} seconds")

    return [player.balance,lowest_balance]



def run_multiple_simulations_one_player(num_simulations=100, num_rounds=10, num_decks=7, plot_with_gauss=True,Print = False,deck_penetration= 4):
    final_balances = []
    lowest_balances = []

    for i in tqdm(range(num_simulations), desc='Progress Bar'):
        results = game_simulation_one_player(num_rounds, num_decks,Print=Print,deck_penetration= deck_penetration)
        final_balance = results[0]
        lowest_balance = results[1]

        final_balances.append(final_balance)
        lowest_balances.append(lowest_balance)

    # Calculate averages
    average_final_balance = sum(final_balances) / len(final_balances)
    average_lowest_balance = sum(lowest_balances) / len(lowest_balances)

    # Plot or save data
    plot_with_gaussian(final_balances, 'Frequency of Final Balances Across Simulations', 'final_balances_distribution.png', 'Final Balance', 'Frequency', plot_with_gauss)
    plot_with_gaussian(lowest_balances, 'Frequency of Lowest Balances Across Simulations', 'lowest_balances_distribution.png', 'Lowest Balance', 'Frequency', plot_with_gauss)

    # Save results to a text file
    with open('simulation_results.txt', 'w') as file:
        file.write(f"Percentage of simulations with a positive balance: {(len([b for b in final_balances if b > 0]) / num_simulations) * 100}%\n")
        file.write(f"Average final balance: {average_final_balance}\n")
        file.write(f"Average lowest balance: {average_lowest_balance}\n")

    print("Results have been saved to 'simulation_results.txt'")



def game_simulation_multiple_players(num_of_rounds=1000, num_decks=7, Print=False, deck_penetration=4, num_of_players=4):
    # Initialize players and a shoe
    start_time = time.time()
    lowest_balance = [0] * num_of_players
    players = [Player(name=f"Player {i+1}", initial_balance=0) for i in range(num_of_players)]
    dealer = Dealer()
    shoe = Shoe(num_decks)

    for round in range(num_of_rounds):
        for i, player in enumerate(players):
            dealer.round(player=player, shoe=shoe, Print=Print, deck_penetration=deck_penetration, num_of_decks=num_decks)
            if player.balance < lowest_balance[i]:
                lowest_balance[i] = player.balance

    duration = time.time() - start_time
    # print(f"Simulation took: {duration:.2f} seconds")

    final_balances = [player.balance for player in players]
    return final_balances, lowest_balance




def run_multiple_simulations_multiple_players(num_simulations=100, num_rounds=10, num_decks=7, num_of_players=4, plot_with_gauss=True, Print=False, deck_penetration=4):
    final_balances = [[] for _ in range(num_of_players)]
    lowest_balances = [[] for _ in range(num_of_players)]

    for i in tqdm(range(num_simulations), desc='Progress Bar'):
        results = game_simulation_multiple_players(num_rounds, num_decks, Print=Print, deck_penetration=deck_penetration, num_of_players=num_of_players)
        final_balance = results[0]
        lowest_balance = results[1]

        for j in range(num_of_players):
            final_balances[j].append(final_balance[j])
            lowest_balances[j].append(lowest_balance[j])

    # Calculate averages
    average_final_balances = [sum(balances) / len(balances) for balances in final_balances]
    average_lowest_balances = [sum(balances) / len(balances) for balances in lowest_balances]

    print(f'final balances {final_balances}')
    print('\n')
    print(f'lowest balances {lowest_balances}')
    print('\n')
    return average_final_balances, average_lowest_balances










if __name__ == "__main__":
    # run_multiple_simulations_one_player(num_simulations=30,num_rounds= 50, num_decks=7,plot_with_gauss= True,Print= False)
    
    final_balances, lowest_balance = run_multiple_simulations_multiple_players(num_rounds=30,num_of_players=3,num_simulations=5)

    print(f'final balances: {final_balances}')
    print('\n')
    print(f'lowest balances: {lowest_balance}')