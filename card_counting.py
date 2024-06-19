from class_of_cards import Shoe
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from collections import Counter
import os





high_low_method = {
    '2': +1,   # Low cards, good for the player
    '3': +1,
    '4': +1,
    '5': +1,
    '6': +1,
    '7': 0,    # Neutral cards
    '8': 0,
    '9': 0,
    '10': -1,  # High cards, bad for the player
    'Jack': -1,
    'Queen': -1,
    'King': -1,
    'Ace': -1
}


def num_of_decks_estimation(shoe):
    # Calculate the total number of cards dealt
    num_cards_dealt = len(shoe.dealt)

    # Each deck has 52 cards
    num_decks_dealt = num_cards_dealt / 52

    # Calculate the number of decks remaining by subtracting the number of decks dealt from the total decks
    num_decks_remaining = shoe.num_decks - num_decks_dealt

    # Return the integer value of the remaining decks (rounded down)
    return int(num_decks_remaining)





def high_low_method(shoe):
    running_count = 0
    delt_cards = shoe.dealt
    for card in delt_cards:
        value = int(card.value)
        if value > 9:
            running_count += -1
        if value < 7:
            running_count += 1

    number_of_decks_remaining = num_of_decks_estimation(shoe= shoe)

    true_count = int(running_count/number_of_decks_remaining)

    return true_count,running_count
    



def simulate_blackjack(num_deals, num_of_decks_defore_shuffel):
    num_cards_before_reshuffle = num_of_decks_defore_shuffel *52
    shoe = Shoe(num_decks=6)
    true_counts = []

    for i in range(num_deals):
        if len(shoe.dealt) >= num_cards_before_reshuffle:
            shoe.reset_shoe  # Reshuffle/recreate the shoe
        card = shoe.deal()
        true_count, _ = high_low_method(shoe)
        true_counts.append(true_count)

    # Count the frequencies of each unique true count
    count_frequencies = Counter(true_counts)
    total_counts = sum(count_frequencies.values())

    # Calculate percentages for positive and negative counts
    positive_counts = sum(freq for count, freq in count_frequencies.items() if float(count) > 0)
    negative_counts = sum(freq for count, freq in count_frequencies.items() if float(count) < 0)
    positive_percentage = (positive_counts / total_counts) * 100
    negative_percentage = (negative_counts / total_counts) * 100

    # Save results to a text file
    with open('True_Count_Frequencies.txt', 'w') as file:
        file.write('True Count, Frequency, Percentage\n')
        for count, frequency in sorted(count_frequencies.items()):
            percentage = (frequency / total_counts) * 100
            file.write(f'{count}, {frequency}, {percentage:.2f}%\n')
        file.write(f'\nPercentage of Positive Counts: {positive_percentage:.2f}%\n')
        file.write(f'Percentage of Negative Counts: {negative_percentage:.2f}%\n')

    # Prepare data for the pie chart
    labels = [f'True Count {k}' for k in count_frequencies.keys()]
    sizes = [f for f in count_frequencies.values()]
    colors = plt.cm.tab20c(np.linspace(0, 1, len(labels)))  # More distinguishable colors

    # Create a pie chart
    fig, ax = plt.subplots()
    wedges, _ = ax.pie(sizes, colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Adjust legend position to lower left, outside the plot area
    legend_labels = [f'{label} = {size/total_counts*100:.2f}%' for label, size in zip(labels, sizes)]
    legend = ax.legend(wedges, legend_labels, title="True Counts", loc="center left", bbox_to_anchor=(0.1, -0.1, 0.5, 1))
    
    # Set the legend text color to match the pie segments
    for text, color in zip(legend.get_texts(), colors):
        text.set_color(color)

    plt.title('Percentage Distribution of True Counts')
    plt.savefig('True_Counts_Pie_Chart.png')  # Save the pie chart as a PNG file
    plt.show()

    # Plot and save the histogram of true counts
    plt.hist(true_counts, bins=30, edgecolor='black', color='skyblue')
    plt.title('Frequency Distribution of True Counts')
    plt.xlabel('True Count')
    plt.ylabel('Frequency')
    plt.savefig('True_Counts_Histogram.png')  # Save the histogram as a PNG file
    plt.show()







if __name__ == "__main__":

    simulate_blackjack(100, 5)


