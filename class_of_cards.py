import random
import time







class Card:
    def __init__(self, suit, value):
        self.suit = suit
        # Check if the card is a Jack, Queen, or King and assign the value as 10
        if value in ['Jack', 'Queen', 'King']:
            self.value = 10
        elif value == 'Ace':
            self.value = 11
        else:
            self.value = int(value)

    def __repr__(self):
        # Adjust the representation to show numeric value for face cards if needed
        return f"{self.value} of {self.suit}"

    def __eq__(self, other):
        # Return True if the values of the two cards are the same
        if isinstance(other, Card):
            return self.value == other.value
        return False



class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, high_low=False):
        if high_low:
            self.high_cards, self.low_cards, self.medium_cards = self._create_high_low_medium_lists()
        else:
            self.cards = [Card(suit, value) for suit in self.suits for value in self.values]

    def _create_high_low_medium_lists(self):
        # Convert values to the actual values assigned in the Card class
        high_cards = [Card(suit, value) for suit in self.suits for value in self.values if value in ['10', 'Jack', 'Queen', 'King', 'Ace']]
        low_cards = [Card(suit, value) for suit in self.suits for value in ['2', '3', '4', '5', '6']]
        medium_cards = [Card(suit, value) for suit in self.suits for value in ['7', '8', '9']]

        return high_cards, low_cards, medium_cards







class Shoe:
    def __init__(self, num_decks=6,deck_list = None):
        if deck_list == None:
            self.num_decks = num_decks
            self.decks = [Deck() for _ in range(num_decks)]
            self.cards = [card for deck in self.decks for card in deck.cards]
            self.dealt = []  # List to store dealt cards
            self.shuffle()

        else:
            #check if deck is type Deck
            self.num_decks = num_decks
            self.decks = [Deck() for _ in range(num_decks - 1)]  # Create additional decks
            self.cards = deck_list # Start with the cards from deck1

            # Now add the cards from the additional decks
            for deck in self.decks:
                self.cards.extend(deck.cards)

            self.dealt = [] # List to store dealt cards
            self.shuffle()



    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        """Deal the top card from the shoe, add it to the dealt list, and return the card."""
        if self.cards:
            card = self.cards.pop(0)  # Take the top card
            self.dealt.append(card)  # Add to the dealt list
            return card
        else:
            print('No more cards in the shoe')
            return None  # Return None if there are no cards left to deal
            



    def deal_initial_hand(self):
        """Deal two cards from the shoe to create and return a new Hand instance."""
        if len(self.cards) >= 2:
            card1 = self.deal()  # Deal the first card
            card2 = self.deal()  # Deal the second card
            if card1 and card2:
                return Hand([card1, card2],shoe=self )
            else:
                print("not enough cards for a full deal")
                return None  # In case there are not enough cards for a full deal
        else:
            print("Not enough cards to deal an initial hand.")
            return None
        

    def remaining_cards(self):
        return len(self.cards)

    def __repr__(self):
        return f"Shoe with {self.remaining_cards()} cards (Dealt: {len(self.dealt)} cards)"

    @property
    def reset_shoe(self):
        """Resets the shoe by combining dealt and remaining cards, reshuffling, and clearing the dealt list."""
        self.cards.extend(self.dealt)  # Return dealt cards back to the deck
        self.dealt = []  # Clear the dealt list
        self.shuffle()  # Reshuffle the combined deck


    def true_count(self):
        running_count = 0
        delt_cards = self.dealt
        for card in delt_cards:
            value = int(card.value)
            if value > 9:
                running_count += -1
            if value < 7:
                running_count += 1
            # Calculate the total number of cards dealt
        num_cards_dealt = len(self.dealt)

    # Each deck has 52 cards
        num_decks_dealt = num_cards_dealt / 52

    # Calculate the number of decks remaining by subtracting the number of decks dealt from the total decks
        num_decks_remaining = self.num_decks - num_decks_dealt

    # Return the integer value of the remaining decks (rounded down)
       
        number_of_decks_remaining =  max(int(num_decks_remaining),1)

        true_count = int(running_count/number_of_decks_remaining)

        return true_count




def generate_shoe_with_true_count(true_count: int, num_of_decks: int):
    """
    Generates a random shoe with a given true count.
    """

    running_count = true_count * num_of_decks
    if abs(running_count) > 18:
        raise ValueError("Running count exceeds the allowed limit of ±18.")
    

    noise1 = random.randint(-3, 3)  
    num_of_high_cards = int(abs(running_count) / 2) + noise1
    
    if running_count + num_of_high_cards > 18:
        num_of_high_cards = 18 - running_count  # Adjust high cards to ensure the sum does not exceed 18

     
    noise2 = random.randint(-3, 3)  
    num_of_medium_cards = int((abs(running_count) + 2 * num_of_high_cards) / 3) + noise2


    if num_of_high_cards < 0 :
        num_of_high_cards = 0
    if num_of_medium_cards < 0:
        num_of_medium_cards = random.randint(0, 5) 

    num_of_low_cards = num_of_high_cards 


    if running_count >= 0:
        num_of_low_cards += running_count
    else:
        num_of_high_cards += -running_count


    
    #creating the show
    deck1 = Deck(high_low=True)
    high_card_list = deck1.high_cards
    low_card_list = deck1.low_cards
    medium_card_list = deck1.medium_cards

        # Shuffle each list to remove cards randomly
    random.shuffle(high_card_list)
    random.shuffle(low_card_list)
    random.shuffle(medium_card_list)

    # Remove the specified number of cards
    removed_high_cards = high_card_list[:20- num_of_high_cards]
    removed_low_cards = low_card_list[:20- num_of_low_cards]
    removed_medium_cards = medium_card_list[:12-num_of_medium_cards]



    # Combine the removed cards
    cards = removed_high_cards + removed_low_cards + removed_medium_cards

    # Shuffle the combined list of removed cards
    random.shuffle(cards)

    shoe_with_true_count = Shoe(num_decks= num_of_decks, deck_list= cards)
    return shoe_with_true_count







class Hand:
    def __init__(self, cards,shoe = Shoe() , Status = {}, amount_of_bet=0):
        self.cards = cards
        self.amount_of_bet = amount_of_bet  # Initialize the betting amount for this hand
        self.Done = False  # To track whether the player has stood
        self.shoe = shoe
        self.status = {'active' : True, 'can_double': True,'num_of_splits':0,'for_dealer': None}
        self.amount_of_bet = amount_of_bet


    def calculate_sum(self):
        hand_sum = 0
        ace_count = 0
        for card in self.cards:
            hand_sum += int(card.value)
            if card.value == 11:  # Assuming Ace is initially 11
                ace_count += 1
        # Adjust for Aces if the sum exceeds 21
        while hand_sum > 21 and ace_count:
            hand_sum -= 10
            ace_count -= 1
        return hand_sum



    def type_of_hand(self):
        
        if len(self.cards) > 2:
            cards_values = [card.value for card in self.cards]
            if 11 in cards_values:
                hand_sum = 0
                # we start counting with -1 aces because we want to check if we can use this ace as 11
                ace_count = -1
                for card in self.cards:
                    hand_sum += int(card.value)
                    if card.value == 11:  # Assuming Ace is initially 11
                        ace_count += 1
                # Adjust for Aces if the sum exceeds 21
                while hand_sum > 21 and ace_count:
                    hand_sum -= 10
                    ace_count -= 1

                if hand_sum < 22:
                    return f"A,{str(hand_sum-11)}"

            return str(self.calculate_sum())
        
        if len(self.cards)<2:
            print('for hand type you need 2 cards')
            exit()
        card1, card2 = self.cards[0], self.cards[1]
        if card1.value == 11 and card2.value == 11:
            return "A,A"
        elif card1.value == 11:
            return f"A,{card2.value}"
        elif card2.value == 11:
            return f"A,{card1.value}"
        elif card1.value == card2.value:
            return f"{card1.value},{card2.value}"
        else:
            return str(int(card1.value) + int(card2.value))





    def __repr__(self):
        return f"Hand({self.cards}) with bet: {self.amount_of_bet}"

    def hit(self, shoe):
        """Add a card from the shoe to the hand."""
        # if self.calculate_sum()<21:
        new_card = shoe.deal()
            # self.can_double = False
        self.status['can_double'] = False
        if new_card:
            self.cards.append(new_card)
        # else:
        #     raise Exception('Sum is over 21, cannot hit.')

    def stand(self):
        """Player stands; no more actions can be taken."""
        self.status['active'] = False

    def split(self, shoe):
        """Split the hand into two hands if the first two cards have the same value.
        we are allowed to double down after Splitting
        
        
        """
        if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value:

            num_of_splits = self.status['num_of_splits'] + 1
            status = {'active':True,'can_double':True , 'num_of_splits':num_of_splits,'for_dealer':None}
            hand1 = Hand([self.cards[0]],shoe= shoe, amount_of_bet=self.amount_of_bet,Status= status)
            hand2 = Hand([self.cards[1]], shoe= shoe, amount_of_bet=self.amount_of_bet,Status= status)
            hand1.hit(shoe)
            hand2.hit(shoe)
            hand1.status['can_double'] = True
            hand2.status['can_double'] = True
            
            return hand1, hand2
        else:
            print("Cannot split this hand.")
            return None, None

    def double_down(self,shoe):
        """Double the bet of the hand."""
        if self.status['can_double'] == True:

            self.amount_of_bet *= 2
            self.hit(shoe)  # Assuming you hit when doubling down
        
            self.status['active'] = False
        else: 

            raise Exception('Cant double')


    def play_move(self,move_to_make,shoe):
        """
        plays the move with this hand
        no split
        if can't double hit        
        """
        if move_to_make == 'S':
            self.stand()

        elif move_to_make == 'H':
            self.hit(shoe=shoe)        

        elif move_to_make == 'D':
            if self.status['can_double'] == True:
                self.double_down(shoe=shoe)
            else:
                self.hit(shoe=shoe) 

        else:
            
            raise Exception(f'{move_to_make} is Not a a legal move')
            

        
        return






def create_solid_hand(total_value: int):
    '''
    Creates a list of cards of solid type, meaning no Ace or two same cards.
    For a total value of 20, it specifically creates a hand from the cards 10, 2, and 8.
    '''
    if total_value < 5 or total_value > 20 or type(total_value) != int:
        raise ValueError("Total value must be between 5 and 20 and an integer.")
    
    card_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10
    }

    # Special case for a total of 20
    if total_value == 20:
        cards = [
            Card(suit='Hearts', value='10'),
            Card(suit='Diamonds', value='2'),
            Card(suit='Clubs', value='8')
        ]
    else:
        # Select the first card
        if total_value > 11:
            card1 = Card(suit='Hearts', value='10')
        else:
            card1 = Card(suit='Hearts', value='2')
        
        # Calculate the value of the second card based on the total desired
        second_card_value = total_value - int(card1.value)
        second_card_value = str(second_card_value)
        card2 = Card(suit='Hearts', value=second_card_value)

        cards = [card1, card2]
    
    return cards


def create_soft_hand(second_card_value:int):
    '''
    creates a list of 2 cards that the  first is an ACE
    '''
    if second_card_value < 2 or second_card_value > 10 or type(second_card_value) != int:
        raise ValueError("The second card's value must be between 2 and 9 and an integer.")

    card1 = Card(suit='Hearts',value='Ace')
    card2 = Card(suit='Hearts',value= str(second_card_value))

    cards = [card1,card2]
    return cards

def create_a_split_hand(card_value:int):
    '''
    Creates a list of 2 cards of the same value.
    Accepts a card value between 2 and 11, where 11 represents Ace.
    '''
    # Check for valid integer inputs within the required range.
    if card_value < 2 or card_value > 11 or type(card_value) != int:
        raise ValueError("The card's value must be between 2 and 11 and must be an integer.")
    
    # Determine the card representation based on the value.
    if card_value == 11:
        card_representation = 'Ace'
    else:
        card_representation = str(card_value)

    # Create two cards with the same value.
    card = Card(suit='Hearts', value=card_representation)
    cards = [card, card]
    return cards




if __name__ == '__main__':
    card1 = Card(suit='Hearts',value='King')
    card2 = Card(suit='Hearts',value='10')
    card3 = Card(suit='Hearts',value='3')

    cards = [card1,card2]

    hand = Hand(cards=cards)

    print(hand.type_of_hand())




    
    


        




