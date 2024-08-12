from class_of_cards import Shoe , Hand , Card , generate_shoe_with_true_count,create_a_split_hand,create_soft_hand,create_solid_hand
from tensor_strategies import find_blackjack_move_tensor, find_blackjack_move_tensor_test , move_to_number , number_to_move ,get_true_count_index,get_hand_index
import time
import random
from class_of_players import Player , Dealer
import csv
from tqdm import tqdm  
import json
import os
import pandas as pd
from io import StringIO
import torch




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






def play_what_is_known(player,dealer_card,shoe,true_count,Print = False):
    '''
    plays the known moves from the table that we already built
    
    '''
    hands = player.hands
    if hands == [] or not hands[0].status['active']:
        return hands
    
    else:
        hand = hands[0]
        # print(f'the hand is {hand}')
        
        move_to_make = find_blackjack_move_tensor_test(hand=hand,dealer_card= dealer_card,true_count = true_count)
        if Print:
            print(f'player hands are {player.hands}')
            print(f'the move to make for the hand {hand} when dealer has {dealer_card} is {move_to_make}')
        

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
            
            if hand.status['active'] == False:
                rotate_first_to_last(hands)
                
        
        else:
            hand1, hand2 = hand.split(shoe)  # This should return two new hands
            # print(f'hand 1 {hand1} and hand 2 {hand2}')
            if hand2:  # If a split was successful and two hands were returned
                    replace_first_with_two(lst= hands,new_first=hand1,new_second=hand2)
      

  
    return play_what_is_known(player=player,dealer_card=dealer_card,shoe=shoe,true_count=true_count)




def test_first_move(player,dealer_card,move,shoe,true_count,Print = False):
    
    hand = player.hands[0]
    
    # print(f'hand before is {hand}')

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
            
            hands = play_what_is_known(player=player,dealer_card=dealer_card,shoe=shoe,true_count=true_count,Print=Print)
            # print(f'after turn players hands are {hands}')
            # exit()
    else:

        hand1, hand2 = hand.split(shoe)
        hands = [hand1,hand2]
        player.hands = hands
        
        hands = play_what_is_known(player=player,dealer_card=dealer_card,shoe=shoe,true_count=true_count,Print=Print)
        player.hands = hands
        

    return 







def test_a_move_with_dealer_one_time(player,dealer,move_to_test,shoe,true_count,Print= False):
    dealer_hand = dealer.hands[0]
    dealer_card = dealer_hand.cards[0]

    test_first_move(player=player,dealer_card=dealer_card,move=move_to_test,shoe=shoe,true_count=true_count,Print=Print)
    if Print:
        print(f'after playing players hands are: {player.hands}')
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

        if hand.calculate_sum() > dealer_sum:
            bet = hand.amount_of_bet
            player.balance += bet


        if Print:
            print(f'now player has {player.balance}')


    if Print:
        print(f'at the end player has {player.balance}')
        print('\n')
        print('\n')

    return player.balance


def test_a_move_with_dealer_average(players_cards, dealer_card, move_to_test, true_count, Print=False, repetitions=50):
    # Create a copy of the initial player cards to keep them unchanged across iterations
    initial_cards = players_cards[:]

    jb = Player(name='JB', initial_balance=0)
    dealer = Dealer()
    final_balances = []

    start_time = time.time()  # Start timing the function

    for i in range(repetitions):
        # Use a fresh copy of the initial player cards for each iteration
        current_player_cards = initial_cards[:]
        num_of_decks = random.randint(3,6)
        shoe = generate_shoe_with_true_count(true_count=true_count, num_of_decks=num_of_decks)
        jb_hand = Hand(shoe=shoe, cards=current_player_cards, amount_of_bet=1)
        jb.hands = [jb_hand]
        dealer_hand = Hand(cards=[dealer_card], shoe=shoe)
        dealer.hands = [dealer_hand]

        final_balance = test_a_move_with_dealer_one_time(player=jb, dealer=dealer, move_to_test=move_to_test, shoe=shoe, true_count=true_count, Print=Print)
        final_balances.append(final_balance)
        jb.balance = 0  # Reset the balance after each simulation

    total_duration = time.time() - start_time  # Calculate the total duration of the test
    if Print:
        print(f"The move '{move_to_test}' was tested {repetitions} times.")
        print(f"Total duration: {total_duration:.2f} seconds.")

    if not final_balances:  # Avoid division by zero if final_balances is empty
        return 0

    return sum(final_balances) / len(final_balances)




def find_expected_balances_of_moves(cards, dealer_card, moves, true_count, repetitions):
    # This function will now return a list of tuples where each tuple is (move, balance),
    # sorted such that the tuple with the highest balance is first.

    balances = []

    # Calculate balances for each move
    for move in moves:
        average_balance = test_a_move_with_dealer_average(players_cards=cards,
                                                         dealer_card=dealer_card, move_to_test=move, 
                                                         true_count=true_count, repetitions=repetitions)
        balances.append((move, average_balance))
    
    # Sort the list based on the balance, descending order
    sorted_balances = sorted(balances, key=lambda x: x[1], reverse=True)

    return sorted_balances






def save_to_tensor(sorted_balances, strategy_tensor, tc_index, hand_index, dc_index):
    """
    Saves move data and corresponding balances into the specified location in a tensor.
    
    Parameters:
    - sorted_balances: List of tuples (move, balance) sorted by balance descending.
    - strategy_tensor: The tensor where data will be saved.
    - tc_index: Index for the true count dimension in the tensor.
    - hand_index: Index for the hand type dimension in the tensor.
    - dc_index: Index for the dealer card dimension in the tensor.
    """
    # Initialize move data list with capacity for 8 elements (4 moves * 2 entries per move)
    move_data = [0] * 8  # Pre-fill with zeros to handle cases with fewer than 4 moves

    # Fill move_data with actual move numbers and balances
    for i, (move, balance) in enumerate(sorted_balances[:4]):  # Ensure only top 4 moves are considered
        move_data[2 * i] = move_to_number(move)  # Move number
        move_data[2 * i + 1] = balance  # Corresponding balance

    # Convert move_data to a tensor and save in the appropriate place
    strategy_tensor[tc_index, hand_index, dc_index] = torch.tensor(move_data, dtype=torch.float32)




def build_a_strategy_table_tensor(true_count=0, repetitions=50):

    output_dir = 'strategies_tensors'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)   



    tc_index = get_true_count_index(true_count=true_count)

    num_true_counts = 7  # True counts from -3 to 3
    num_hand_types = 35 # 16 solid, 8 soft, 10 split 1 BJ
    num_dealer_cards = 10  # Dealer cards from 2 to 11 (Ace considered as 11)
    moves_with_balances = 8  # 4 moves each next to its balance starting with the move with the highest balance going down

    strategy_tensor = torch.zeros((num_true_counts, num_hand_types, num_dealer_cards, moves_with_balances))


    file_path = f"{output_dir}/test_strategy.pt"
    torch.save(strategy_tensor, file_path)

    moves = ['H', 'S', 'D']  # Default moves for most hands

    hand_orders = [
        ('Solid Hands - High', create_solid_hand, range(20, 9, -1)),  # Solid hands from 20 to 10
        ('Soft Hands', create_soft_hand, range(10, 1, -1)),           # Soft hands from A,10 to A,2
        ('Solid Hands - Low', create_solid_hand, range(9, 4, -1)),    # Solid hands from 9 to 5
        ('Split Hands', create_a_split_hand, range(2, 12))            # Split hands from 2,2 to A,A
    ]

   
    for hand_type, hand_creator,range_values in tqdm(hand_orders,desc=f'hands types'):

        if hand_type == 'Split Hands':
            current_moves = ['H', 'S', 'D', 'SP']
        else:
            current_moves = moves

        for value in tqdm(range_values, desc=f"{hand_type}"):
            cards = hand_creator(value)
            
            hand_of_player = Hand(cards=cards)
            type_of_hand = hand_of_player.type_of_hand()
            hand_index = get_hand_index(type_of_hand)
            

            for dc_index, dealer_value in enumerate(range(2, 12), start=0):  # Including Ace as 11
                dealer_card = Card(suit='Hearts', value= str(dealer_value))



                if dealer_value == 11:
                    dealer_card = Card(suit='Hearts', value='Ace')

              
                moves_details = find_expected_balances_of_moves(cards=cards, dealer_card=dealer_card, moves=current_moves,
                                                              true_count=true_count, repetitions=repetitions)
               


                save_to_tensor(sorted_balances=moves_details,strategy_tensor=strategy_tensor,tc_index=tc_index,hand_index=hand_index,dc_index=dc_index)

            
            
    



            torch.save(strategy_tensor, file_path)



if __name__ == '__main__':




    build_a_strategy_table_tensor(repetitions=1000,true_count= 0 )


    # card1 = Card(suit='Heart',value='10')
    # cards = [card1,card1]
    # hand = Hand(cards=cards,amount_of_bet=1)
    # player = Player(name='JB' ,initial_balance=0)
    # player.hands = [hand]

    # dealer_card = Card(suit='Heart',value='4')
    # # dealer_hand = Hand(cards=[dealer_card])
    # # dealer = Dealer(name='dealer')
    # # dealer.hands = [dealer_hand]

    

    # # test_a_move_with_dealer_one_time(player=player,dealer=dealer,move_to_test='H',shoe=Shoe(),true_count=0,Print=True)
    # avrage = test_a_move_with_dealer_average(players_cards=cards, dealer_card=dealer_card, move_to_test= 'SP', true_count=0, Print=False, repetitions=10)

    # print(f'after 50 times the average of is {avrage}')