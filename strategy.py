import pandas as pd
from class_of_cards import Card, Hand, Shoe






def find_blackjack_move(hand, dealer_card, true_count=0,Print =False):
    # Assuming Card is defined elsewhere with attributes suit and value
    strategy_sheets = pd.ExcelFile('Strategy1.xlsx')
    
    # Select the right sheet based on true count
    if true_count < -1:
        sheet_name = "-1"
    elif true_count > 4:
        sheet_name = "4"
    else:
        sheet_name = str(true_count)
    
    # Read the specific sheet and set the header to the 6th row (index 5)
    # Assuming you want to read from column G to the end of the sheet
    df = strategy_sheets.parse(sheet_name, header=5, usecols="G:Q")  # Adjust "X" as needed based on your last column

    type_of_hand = hand.type_of_hand()
    if Print:
        print("The hand is:",type_of_hand)
        print('The dealer has', dealer_card.value)

    if len(type_of_hand) < 3:
        type_of_hand = int(type_of_hand)

    index = df[df['Hand'] == type_of_hand].index[0]
    # print(index)  # This prints the index where 'Hand' matches 'type_of_hand'


    dealer_card_value = dealer_card.value
    if dealer_card_value == 11:
        dealer_card_value = 'A'
    else:
        dealer_card_value = int(dealer_card_value)


    
      # Access the value at the found index and specific dealer card column
    if dealer_card_value in df.columns:
        move = df.loc[index, dealer_card_value]
        if Print:
            print(f"The recommended move for {type_of_hand} against a dealer's {dealer_card_value} is: {move}")
    else:
        print(f"No column found for dealer's card value: {dealer_card_value}")
        
    return move








if __name__ == '__main__':


    card1 = Card('Hearts', '2')
    card2 = Card('Hearts', '8')
    card3 = Card('Hearts', '4')

    shoe = Shoe()

    dealers_card = Card('Hearts', 'Ace')

    cards = [card1,card2]

    hand = Hand(cards= cards,shoe=shoe)


    find_blackjack_move(hand= hand, dealer_card= dealers_card,true_count=-3,Print=True)