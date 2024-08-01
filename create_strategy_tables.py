from class_of_cards import Shoe , Hand , Card , generate_shoe_with_true_count,create_a_split_hand,create_soft_hand,create_solid_hand
from strategy import  find_move_test,write_move_to_excel
import time
import random
from class_of_players import Player , Dealer
import csv
from tqdm import tqdm  # This imports the tqdm class for progress bars
import json
import os
import pandas as pd
from io import StringIO


def rotate_first_to_last(lst):
    if lst:  # Check if the list is not empty
        first_element = lst.pop(0)  # Remove the first element
        lst.append(first_element)  # Append it to the end of the list
    return lst

def replace_first_with_two(lst, new_first, new_second):
    if type(lst) != list:
        print('lst is not a list')
        exit()
    if lst:  # Check if the list is not empty
        lst.pop(0)  # Remove the first element
    lst.insert(0, new_second)  # Insert the second new element at the beginning
    lst.insert(0, new_first)  # Insert the first new element at the beginning
    return lst






def play_what_is_known(player,dealer_card,shoe,true_count):
    '''
    plays the known moves from the table that we already built
    
    '''
    hands = player.hands
    if hands == [] or not hands[0].status['active']:
        return hands
    
    else:
        hand = hands[0]
        # print(f'the hand is {hand}')
        
        move_to_make = find_move_test(hand=hand,dealer_card= dealer_card,true_count = true_count)
        # print(f'the move to make is {move_to_make}')

        if not move_to_make in ['SP','D','H','S']:
            move_to_make = random.choice(['H', 'S'])

        if move_to_make != 'SP':
            hand.play_move(move_to_make=move_to_make,shoe = shoe)
            hand_sum = hand.calculate_sum()
            if hand_sum > 21:
                hands.remove(hand)
                player.balance -= hand.amount_of_bet
            if hand_sum == 21:
                hand.status['active'] = False
                rotate_first_to_last(hands)
        
        else:
            hand1, hand2 = hand.split(shoe)  # This should return two new hands
            # print(f'hand 1 {hand1} and hand 2 {hand2}')
            if hand2:  # If a split was successful and two hands were returned
                    replace_first_with_two(lst= hands,new_first=hand1,new_second=hand2)
      


    return play_what_is_known(player=player,dealer_card=dealer_card,shoe=shoe,true_count=true_count)




def test_first_move(player,dealer_card,move,shoe,true_count):
    
    hand = player.hands[0]
    

    if move != 'SP':
        
        hand.play_move(move_to_make=move,shoe= shoe)

        # print(f'players hand is {hand}')

        hand_sum = hand.calculate_sum()
        if hand_sum>21:
            player.balance -= hand.amount_of_bet
            player.hands.remove(hand)
            return
        elif hand_sum == 21:
            return
            
        
        else:
        
            player.hands = [hand]
            
            hands = play_what_is_known(player=player,dealer_card=dealer_card,shoe=shoe,true_count=true_count)
            # print(f'players hands are {hands}')
    else:

        hand1, hand2 = hand.split(shoe)
        hands = [hand1,hand2]
        player.hands = hands
        
        hands = play_what_is_known(player=player,dealer_card=dealer_card,shoe=shoe,true_count=true_count)
        player.hands = hands
        # print(f'players hands are {hands}')

    return 







def test_a_move_with_dealer_one_time(player,dealer,move_to_test,shoe,true_count,Print= False):
    dealer_hand = dealer.hands[0]
    dealer_card = dealer_hand.cards[0]

    test_first_move(player=player,dealer_card=dealer_card,move=move_to_test,shoe=shoe,true_count=true_count)
    if Print:
        print(f'players hands are: {player.hands}')
    Player_hands = player.hands
    if not Player_hands == []:
    
        while dealer_hand.calculate_sum() < 17:
            dealer_hand.hit(shoe=shoe)
            if Print:
                print(f'dealers has:  {dealer_hand.calculate_sum()}')
            if dealer_hand.calculate_sum() > 21:
                # print("too many")
                for hand in Player_hands:
                    bet = hand.amount_of_bet
                    player.balance += bet
                if Print:
                    print(f'now player has: {player.balance}')

                if Print:
                    print('\n')
                    print('\n')
                return player.balance
            

    
    dealer_sum = dealer_hand.calculate_sum()
    for hand in Player_hands:
        if hand.calculate_sum() < dealer_sum:
            bet = hand.amount_of_bet
            player.balance -= bet

        if hand.calculate_sum() > dealer_sum :
            bet = hand.amount_of_bet
            player.balance += bet


        if Print:
            print(f'now player has {player.balance}')


    if Print:
        print(f'at the end player has {player.balance}')
        print('\n')
        print('\n')

    return player.balance




def test_a_move_with_dealer_avrage(players_cards, dealer_card, move_to_test, true_count, Print=False, repetitions=50):
    card1 , card2 = players_cards[0] , players_cards[1]
    start_time = time.time()  # Start timing the function

    jb = Player(name='JB', initial_balance=0)
    dealer = Dealer()   
    final_balances = []
    
    

    for i in range(repetitions):
        players_cards = [card1,card2]
        num_of_decks = random.randint(4,6)
        shoe = generate_shoe_with_true_count(true_count=true_count, num_of_decks=num_of_decks)
        jb_hand = Hand(shoe=shoe, cards=players_cards, amount_of_bet=1)
        jb.hands = [jb_hand]
        dealer_hand = Hand(cards=[dealer_card], shoe=shoe)
        dealer.hands = [dealer_hand]

        final_balance = test_a_move_with_dealer_one_time(player=jb, dealer=dealer, move_to_test=move_to_test, shoe=shoe, true_count=true_count, Print=Print)
        final_balances.append(final_balance)
        jb.balance = 0

     

    if not final_balances:  # Check if the list is empty to avoid division by zero
        return 0
    
    total_duration = time.time() - start_time
    if Print:
        print(f'the move was {move_to_test} we repeated it for {repetitions} times')
        print(f'Total duration: {total_duration:.2f} seconds.')

    return sum(final_balances) / len(final_balances)




def build_a_strategy_table(true_count=0,repetitions = 200):
    backup_file = f'back_up_results_true_count_{true_count}.txt'  # Including true_count in filename

    results = {
        'Solid Hands': {f'Solid Hand {total}': {} for total in range(19, 4, -1)},
        'Soft Hands': {f'Soft Hand A,{second_card_value}': {} for second_card_value in range(2, 10)},
        'Split Hands': {f'Split Hand {card_value},{card_value}': {} for card_value in range(2, 11)}
    }
    moves = ['H', 'S', 'D']  # Default moves for most hands

    # Adjusted hand_types dictionary to include the key_prefix
    hand_types = {
        'Solid Hands': (create_solid_hand, range(19, 4, -1), 'Solid Hand '),
        'Soft Hands': (create_soft_hand, range(2, 10), 'Soft Hand A,'),
        'Split Hands': (create_a_split_hand, range(2, 11), 'Split Hand ')
    }


 
    for hand_type, (hand_creator, range_values, key_prefix) in tqdm(hand_types.items(), desc="Processing hand types"):
        # Adjust moves for split hands
        if hand_type == 'Split Hands':
            current_moves = ['H', 'S', 'D', 'SP']
        else:
            current_moves = moves  # Use default moves for other types

        for value in tqdm(range_values, desc=f"{hand_type}"):
            cards = hand_creator(value)
            card3 , card4 = cards[0] , cards[1]
            if card3.suit != 'Hearts' or card4.suit != 'Hearts':
                print(card3,card4)
                exit()
            for dealer_value in tqdm(range(2, 12), desc="Dealer Card Progress", leave=False):  # Including Ace as 11
                dealer_card = Card(suit='Hearts', value= str(dealer_value))
                if dealer_value == 11:
                    dealer_card = Card(suit='Hearts', value='Ace')

                best_move, best_balance = determine_best_move(cards= cards, dealer_card = dealer_card, moves=current_moves,
                                                    true_count= true_count,repetitions = repetitions)
                key = f'{key_prefix}{value}'

                store_results(result_dict=results[hand_type],key= key,dealer_value= dealer_value,best_move = best_move,best_balance= best_balance,hand_type=hand_type)

                write_move_to_excel(player_cards=cards,dealer_card=dealer_card,move_to_write=best_move,
                                    true_count=true_count)
                with open(backup_file, 'w') as f:
                    json.dump(results, f, indent=4)

    save_results_to_csv(results= results,true_count=true_count)



def store_results(result_dict, key, dealer_value, best_move, best_balance,hand_type):
    
    # Check if the key format indicates a split hand (based on comma presence in key)
    if hand_type == 'Split Hands':
        # Extract the card value from the key format "Split Hand X,X"
        card_value = key.split(' ')[-1].split(',')[0]
        # Reformat the key to ensure it uses the correct double card notation
        key = f'Split Hand {card_value},{card_value}'

    
    # Store the results with the correctly formatted key
    if isinstance(best_balance, float):
        result_dict[key][dealer_value] = (best_move, best_balance)
    else:
        print(best_balance)
        exit()
        result_dict[key][dealer_value] = (best_move, 'NA')  # Handling non-floats or errors in computation





def determine_best_move(cards, dealer_card, moves, true_count, repetitions, epsilon=0.001):
    best_balance = float('-inf')
    best_move = None
    balance_details = {}

    # First round to find the best balance
    for move in moves:
        average_balance = test_a_move_with_dealer_avrage(players_cards=cards,
                                                         dealer_card=dealer_card, move_to_test=move, 
                                                         true_count=true_count, repetitions=repetitions)
        balance_details[move] = average_balance
        if average_balance > best_balance:
            best_balance = average_balance
            best_move = move

    # Check if other moves are close to the best balance within epsilon
    # close_moves = [move for move, balance in balance_details.items() if (best_balance - balance) < epsilon ]

    # If close moves are found, rerun with higher repetitions for these moves
    # if close_moves:
    #     # print(f"Re-evaluating moves: {close_moves} due to close balances.")
    #     for move in close_moves:
    #         # Recalculate with increased repetitions
    #         new_repetitions = min(5000, repetitions * 2)
    #         average_balance = test_a_move_with_dealer_avrage(players_cards=cards,
    #                                                          dealer_card=dealer_card, move_to_test=move, 
    #                                                          true_count=true_count, repetitions=new_repetitions)
    #         # Update if a new better result is found
    #         if average_balance > best_balance:
    #             best_balance = average_balance
    #             best_move = move
        # print(f"Updated best move to {move} with a balance of {best_balance} after extended simulation.")

    # Handle the case where no best move is determined
    if best_move is None:
        print("No valid move was determined.")
        exit()

    return best_move, best_balance





def save_results_to_csv(results, true_count=0):
    filename = f'blackjack_strategy_results_true_count_{true_count}.csv'  # Including true_count in filename
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        # Defining headers for dealer values from 2 to Ace
        headers = ['Hand Type', 'Player Hand'] + [f'Dealer {i}' if i != 11 else 'Dealer Ace' for i in range(2, 12)]
        writer.writerow(headers)
        
        # Write each hand's results
        for hand_description, dealer_results in results.items():
            for player_hand, hand_values in dealer_results.items():
                row = [hand_description, player_hand]  # Begin row with hand description and player hand value
                for dealer_value in range(2, 12):  # Dealer cards 2 to 11 (11 represents Ace)
                    dealer_key = dealer_value
                    move, balance = hand_values.get(dealer_key, ('NA', 'NA'))

                    try:
                        if isinstance(balance, float):
                            formatted_balance = f"{balance:.4f}" 
                        else: 
                            formatted_balance = balance 
                            print('balance is not corect')
                            print(balance)
                            exit()
                    except ValueError:
                        formatted_balance = 'NA'  # Safety net for unexpected data types
                    row.append(f'{move}, {formatted_balance}')
                writer.writerow(row)





def csv_to_excel(csv_file_path):
    # Check if the file exists
    if not os.path.isfile(csv_file_path):
        print("File does not exist.")
        return
    # Reading the CSV file
    df = pd.read_csv(csv_file_path)

    # Creating the Excel file path by changing the extension
    excel_file_path = os.path.splitext(csv_file_path)[0] + '.xlsx'

    # Writing to an Excel file
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    print(f"Excel file created at: {excel_file_path}")





if __name__ == '__main__':

    build_a_strategy_table(repetitions=1,true_count=-3 )
    # csv_to_excel('blackjack_strategy_results_true_count_0.csv')