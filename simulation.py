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





def game_simulation_one_player(num_of_rounds = 1000,num_decks=7,Print = False):
        # Initialize a player and a shoe
    start_time = time.time()
    lowest_balance = 0 
    player = Player(name="John Doe", initial_balance=0)
    dealer = Dealer()
    shoe = Shoe(num_decks) 
    for round in range(num_of_rounds):
        dealer.round(player=player,shoe = shoe, Print= Print, deck_penetration= 4)
        if player.balance < lowest_balance:
            lowest_balance = player.balance


    shoe.reset_shoe

    duration = time.time() - start_time
    # print(f"Simulation took: {duration:.2f} seconds")

    return [player.balance,lowest_balance]



# def run_multiple_simulations(num_simulations=100, num_rounds=10, num_decks=7):
#     final_balances = []
#     lowest_balances = []

#     for i in tqdm(range(num_simulations), desc = 'Progress Bar'):
#         results = game_simulation_one_player(num_rounds, num_decks)
#         final_balance = results[0]
#         lowest_balance = results[1]

#         final_balances.append(final_balance)
#         lowest_balances.append(lowest_balance)

#     # Calculate averages
#     average_final_balance = sum(final_balances) / len(final_balances)
#     average_lowest_balance = sum(lowest_balances) / len(lowest_balances)

#     # Calculate the frequency of each balance for plotting
#     final_balance_freq = Counter(final_balances)
#     lowest_balance_freq = Counter(lowest_balances)

#     # Plotting final balance frequencies with Gaussian fit
#     plt.figure(figsize=(10, 5))
#     balance_values, balance_counts = zip(*final_balance_freq.items())
#     plt.scatter(balance_values, balance_counts, color='green')
#     # Fit and plot Gaussian
#     mu, std = norm.fit(final_balances)
#     x = np.linspace(min(balance_values), max(balance_values), 100)
#     p = norm.pdf(x, mu, std) * max(balance_counts) / max(norm.pdf(x, mu, std))
#     plt.plot(x, p, 'k', linewidth=2)
#     plt.xlabel('Final Balance')
#     plt.ylabel('Frequency')
#     plt.title(f'Frequency of Final Balances Across Simulations (μ={mu:.2f}, σ={std:.2f})')
#     plt.grid(True)
#     plt.savefig('final_balances_distribution.png')
#     plt.show()

#     # Plotting lowest balance frequencies with Gaussian fit
#     plt.figure(figsize=(10, 5))
#     low_balance_values, low_balance_counts = zip(*lowest_balance_freq.items())
#     plt.scatter(low_balance_values, low_balance_counts, color='red')
#     # Fit and plot Gaussian
#     mu_low, std_low = norm.fit(lowest_balances)
#     x_low = np.linspace(min(low_balance_values), max(low_balance_values), 100)
#     p_low = norm.pdf(x_low, mu_low, std_low) * max(low_balance_counts) / max(norm.pdf(x_low, mu_low, std_low))
#     plt.plot(x_low, p_low, 'k', linewidth=2)
#     plt.xlabel('Lowest Balance')
#     plt.ylabel('Frequency')
#     plt.title(f'Frequency of Lowest Balances Across Simulations (μ={mu_low:.2f}, σ={std_low:.2f})')
#     plt.grid(True)
#     plt.savefig('lowest_balances_distribution.png')
#     plt.show()

#     # Save results to a text file
#     with open('simulation_results.txt', 'w') as file:
#         file.write(f"Percentage of simulations with a positive balance: {(len([b for b in final_balances if b > 0]) / num_simulations) * 100}%\n")
#         file.write(f"Average final balance: {average_final_balance}\n")
#         file.write(f"Average lowest balance: {average_lowest_balance}\n")

#     print("Results have been saved to 'simulation_results.txt'")





def run_multiple_simulations(num_simulations=100, num_rounds=10, num_decks=7, plot_with_gauss=True,Print = False):
    final_balances = []
    lowest_balances = []

    for i in tqdm(range(num_simulations), desc='Progress Bar'):
        results = game_simulation_one_player(num_rounds, num_decks,Print=Print)
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






if __name__ == "__main__":
    run_multiple_simulations(num_simulations=10,num_rounds= 30, num_decks=7,plot_with_gauss= True,Print= False)