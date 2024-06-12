import random



class Card:
    def __init__(self, suit, value):
        self.suit = suit
        # Check if the card is a Jack, Queen, or King and assign the value as 10
        if value in ['Jack', 'Queen', 'King']:
            self.value = 10
        elif value == 'Ace':
            self.value = 11
        else:
            self.value = value

    def __repr__(self):
        # Adjust the representation to show numeric value for face cards if needed
        return f"{self.value} of {self.suit}"

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]



class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.decks = [Deck() for _ in range(num_decks)]
        self.cards = [card for deck in self.decks for card in deck.cards]
        self.dealt = []  # List to store dealt cards
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
            return None  # Return None if there are no cards left to deal



    def deal_initial_hand(self):
        """Deal two cards from the shoe to create and return a new Hand instance."""
        if len(self.cards) >= 2:
            card1 = self.deal()  # Deal the first card
            card2 = self.deal()  # Deal the second card
            if card1 and card2:
                return Hand([card1, card2],shoe=self )
            else:
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







class Hand:
    def __init__(self, cards, shoe, amount_of_bet=0):
        self.cards = cards
        self.amount_of_bet = amount_of_bet  # Initialize the betting amount for this hand
        self.Done = False  # To track whether the player has stood
        self.shoe = shoe
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
            return str(self.calculate_sum())
        
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
        new_card = shoe.deal()
        if new_card:
            self.cards.append(new_card)
        else:
            print("No more cards left in the shoe.")

    def stand(self):
        """Player stands; no more actions can be taken."""
        self.Done = True

    def split(self, shoe):
        """Split the hand into two hands if the first two cards have the same value."""
        if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value:
            hand1 = Hand([self.cards[0]], self.amount_of_bet)
            hand2 = Hand([self.cards[1]], self.amount_of_bet)
            hand1.hit(shoe)
            hand2.hit(shoe)
            return hand1, hand2
        else:
            print("Cannot split this hand.")
            return None, None

    def double_down(self,shoe):
        """Double the bet of the hand."""
        self.amount_of_bet *= 2
        self.hit(shoe)  # Assuming you hit when doubling down
        self.Done = True
        

















if __name__ == '__main__':

    card1 = Card('Hearts', '3')
    card2 = Card('Hearts', '3')

    

    card3 = Card('Hearts', 'Ace')
    Card4 = Card('Spades', 'King')

    cards = [card1,card2]

    shoe = Shoe(num_decks=5) 
    hand1 = Hand(cards = cards, shoe= shoe)

    

    split1 , split2 = hand1.split(shoe=shoe)

    print("first hand:",split1 , "  second hand: ",split2 )

