import torch
from class_of_cards import  Hand , Card ,create_a_split_hand,create_soft_hand,create_solid_hand
from tqdm import tqdm  # This imports the tqdm class for progress bars
from strategy import find_blackjack_move
import os
import time
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook



'''
numerical encoding for moves: 'S' -> 1, 'H' -> 2, 'D' -> 3, 'SP' -> 4   None -> 15

'''
def move_to_number(move):
    encoding = {'S': 1, 'H': 2, 'D': 3, 'SP': 4, None: 15}
    return encoding.get(move, "Invalid move")

def number_to_move(number):
    decoding = {1: 'S', 2: 'H', 3: 'D', 4: 'SP', 15: None}
    return decoding.get(number, "Invalid number")





def build_strategy_excel_from_tensor(strategy_version=1):
    tensor_dir = 'strategies_tensors'
    if strategy_version == -15:
        file_name = 'test_strategy.pt'
    else:
        file_name = f'strategy_{strategy_version}.pt'

    file_path = os.path.join(tensor_dir, file_name)
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No strategy file found at {file_path}")
    
    # Load the strategy tensor
    strategy_tensor = torch.load(file_path,weights_only=True)
    
    workbook = Workbook()
    workbook.remove(workbook.active)  # Removes the default sheet created with new workbook

    hand_type_labels = {
        'Solid Hands': ('', range(20, 4, -1)),
        'Soft Hands': ('A,', range(2, 11)),
        'Split Hands': ('', range(2, 12))
    }


    hand_type_to_index = {
    "20": 0, "19": 1, "18": 2, "17": 3, "16": 4, "15": 5, "14": 6, "13": 7, "12": 8, "11": 9, "10": 10,
    "9": 11, "8": 12, "7": 13, "6": 14, "5": 15,
    "A,2": 16, "A,3": 17, "A,4": 18, "A,5": 19, "A,6": 20, "A,7": 21, "A,8": 22, "A,9": 23, "A,10": 24,
    "2,2": 25, "3,3": 26, "4,4": 27, "5,5": 28, "6,6": 29, "7,7": 30, "8,8": 31, "9,9": 32, "10,10": 33,
    "A,A": 34
}

    dealer_cards = [str(i) for i in range(2, 11)] + ['Ace']
    
    # Iterate over each true count
    for true_count in range(strategy_tensor.shape[0]):
        sheet = workbook.create_sheet(title=f'True Count {true_count - 3}')
        df = pd.DataFrame(index=pd.Index([], name='Player Hand'), columns=dealer_cards)
        
        # Populate DataFrame for each hand type
        for hand_type, (prefix, values) in hand_type_labels.items():
            
            
            for value in values:
                hand_label = prefix + str(value)
                if hand_type == 'Split Hands':
                    hand_label = hand_label + ','+hand_label
                    if value == 11:
                        hand_label = 'A,A'
                
                for dealer_index, dealer_card in enumerate(dealer_cards):
                    
  
                    
                    move_number = strategy_tensor[true_count, hand_type_to_index[hand_label], dealer_index, 0].item()
                    
                    move_symbol = number_to_move(move_number)
                    df.at[hand_label, dealer_card] = move_symbol
        
        # Write DataFrame to the sheet in Excel workbook
        for row in dataframe_to_rows(df, index=True, header=True):
            sheet.append(row)
    
    base_name = os.path.splitext(file_name)[0]  # Remove the extension from the tensor file name
    excel_path = f'{base_name}.xlsx'

    workbook.save(excel_path)
    workbook.close()
    print(f"Strategy Excel file saved to {excel_path}")











def build_a_strategy_tensor_from_excel(strategy_version=1):


    output_dir = 'strategies_tensors'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Tensor dimensions: True counts, Hand types, Dealer cards, best move
    num_true_counts = 7  # True counts from -3 to 3
    num_hand_types = 35 # 16 solid, 8 soft, 10 split 1 BJ
    num_dealer_cards = 10  # Dealer cards from 2 to 11 (Ace considered as 11)

    strategy_tensor = torch.zeros((num_true_counts, num_hand_types, num_dealer_cards, 1))

    hand_types = {
        'Solid Hands': (create_solid_hand, range(20, 4, -1), 'Solid Hand '),
        'Soft Hands': (create_soft_hand, range(2, 11), 'Soft Hand A,'),
        'Split Hands': (create_a_split_hand, range(2, 12), 'Split Hand ')
    }

    hand_index = 0  # Initialize hand index
    for tc_index, true_count in enumerate(tqdm(range(-3, 4), desc="True Counts")):
        hand_index = 0  # Reset hand index for each new true count
        for hand_type, details in hand_types.items():
            hand_creator, range_values, key_prefix = details
            for value in tqdm(range_values, desc=f"{hand_type}"):
                cards = hand_creator(value)
                for dc_index, dealer_value in enumerate(range(2, 12), start=0):  # Including Ace as 11
                    dealer_card = Card(suit='Hearts', value= str(dealer_value))
                    if dealer_value == 11:
                        dealer_card = Card(suit='Hearts', value='Ace')

                    hand = Hand(cards=cards) 
                    
                        

                    move_to_make = find_blackjack_move(hand=hand, dealer_card=dealer_card, true_count=true_count,version=strategy_version)
                    number_move = move_to_number(move_to_make)
    

                    if number_move == 0:
                        print('move is 0 we have a problem')
                        exit()

                    # Place the move in the tensor
                    strategy_tensor[tc_index, hand_index, dc_index, 0] = number_move
                hand_index += 1  # Increment hand index after processing each hand


    file_path = f"{output_dir}/strategy_{strategy_version}.pt"
    torch.save(strategy_tensor, file_path)

    return strategy_tensor





def retrieve_move_from_tensor(strategy_tensor, true_count_index, hand_index, dealer_card_index):
    # Access the tensor at the specified indices, ensuring to grab the first element of the last dimension
    move_data = strategy_tensor[true_count_index, hand_index, dealer_card_index]
    move_number = move_data[0]  # This accesses the first element, regardless of the length of the last dimension
 
    move = number_to_move(int(move_number))
    
    return move

def get_move(strategy_version, true_count_index, hand_index, dealer_card_index):
    # Construct the file path for the tensor
    file_path = f'strategies_tensors/strategy_{strategy_version}.pt'
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Load the tensor from the file
    strategy_tensor = torch.load(file_path, weights_only=True)
    
    # Use the previously defined function to retrieve the move
    move = retrieve_move_from_tensor(strategy_tensor, true_count_index, hand_index, dealer_card_index)
    
    return move

def get_move_test(true_count_index, hand_index, dealer_card_index):
    # Construct the file path for the tensor
    file_path = 'strategies_tensors/test_strategy.pt'
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Load the tensor from the file
    strategy_tensor = torch.load(file_path, weights_only=True)
    
    # Use the previously defined function to retrieve the move
    move = retrieve_move_from_tensor(strategy_tensor, true_count_index, hand_index, dealer_card_index)
    
    return move




def find_blackjack_move_tensor(hand, dealer_card, true_count=0, strategy_version=1):
    type_of_hand = hand.type_of_hand()
    hand_index = get_hand_index(type_of_hand)
    dealer_card_index = int(dealer_card.value) - 2
    true_count_index = get_true_count_index(true_count=true_count)
    move  = get_move(strategy_version=strategy_version , true_count_index=true_count_index,hand_index= hand_index,dealer_card_index=dealer_card_index)
    return move



def find_blackjack_move_tensor_test(hand, dealer_card, true_count=0):
    type_of_hand = hand.type_of_hand()
    hand_index = get_hand_index(type_of_hand)
    dealer_card_index = int(dealer_card.value) - 2
    true_count_index = get_true_count_index(true_count=true_count)
    move = get_move_test(true_count_index=true_count_index, hand_index=hand_index, dealer_card_index=dealer_card_index)
    return move


def get_true_count_index(true_count):
    # Clamp the true_count between -3 and 3
    clamped_true_count = max(-3, min(3, true_count))
    # Convert the clamped true count starting from 0 index (-3 maps to 0, 3 maps to 6)
    return clamped_true_count + 3

def get_hand_index(hand_type):
    hand_type_to_index = {
    "20": 0, "19": 1, "18": 2, "17": 3, "16": 4, "15": 5, "14": 6, "13": 7, "12": 8, "11": 9, "10": 10,
    "9": 11, "8": 12, "7": 13, "6": 14, "5": 15,

    "A,2": 16, "A,3": 17, "A,4": 18, "A,5": 19, "A,6": 20, "A,7": 21, "A,8": 22, "A,9": 23, "A,10": 24,

    "2,2": 25, "3,3": 26, "4,4": 27, "5,5": 28, "6,6": 29, "7,7": 30, "8,8": 31, "9,9": 32, "10,10": 33,
    "A,A": 34  
}
    # Check if the hand type is in the dictionary and return the index
    if hand_type in hand_type_to_index:
        return hand_type_to_index[hand_type]
    else:
        # Raise an error if the hand type is not found
        raise ValueError(f"Hand type '{hand_type}' is not valid.")
    










if __name__ == '__main__':


    print('start')
    # build_a_strategy_tensor_from_excel(strategy_version=1)
    # build_a_strategy_tensor_from_excel(strategy_version=2)

    # strategy_version = 2
    # true_count_index = 6 # Index for true count -3 in your example if it starts from -3
    # hand_index = 4    # Index for the first hand type in your example
    # dealer_card_index = 4 # Index for the dealer card '2'
    # move = get_move(strategy_version, true_count_index, hand_index, dealer_card_index)
    # print("The recommended move is:", move)
   

    

    card1 = Card('Hearts', '9')
    card2 = Card('Hearts', '9')
    # card3 = Card('Hearts', '6')


    dealers_card = Card('Hearts', '7')

    cards = [card1,card2]
    hand = Hand(cards=cards)
    print(f'type of hand is {hand.type_of_hand()}')
    version = 3

    true_count =-3
    test_move =find_blackjack_move_tensor(hand= hand, dealer_card= dealers_card,true_count=true_count,strategy_version=version)
    print(f"The test recommended move when hand is {hand.cards} against a dealer {dealers_card} is:", test_move)


    build_strategy_excel_from_tensor(strategy_version=3)


    
