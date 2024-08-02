from class_of_cards import Shoe , Hand , Card 
from strategy import find_blackjack_move ,find_move_test


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



class Player:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.hands = []
        self.balance = initial_balance


    def get_in_this_round():
        #add card counting 
        pass
    


    def player_turn(self, shoe, dealer_card,true_count ,initial_bet = 1):
        # Deal an initial hand and set a starting bet
        initial_hand = shoe.deal_initial_hand()

        if true_count > 1: # bet speard as the true count.
            initial_hand.amount_of_bet = true_count 
        
        else:
            initial_hand.amount_of_bet = initial_bet

        self.hands.append(initial_hand)


        if initial_hand.calculate_sum() == 21:
            # print("check BJ ")
            # print(f'the balance before was: {self.balance} ')

            self.balance += initial_hand.amount_of_bet * 1.5
            # print(f'and now it is {self.balance}')
            initial_hand.status['active'] = False
            initial_hand.status['for_dealer'] = 'BJ'
            return 


# Prepare to play all hands, initializing results list

        self.play_player_hands(dealer_card= dealer_card, shoe = shoe,true_count= true_count)

     
    
    
                 


    def play_player_hands(self, dealer_card, shoe,true_count):

        hands = self.hands
        if hands == [] or not hands[0].status['active']:
            return 

        hand = hands[0]
        move_to_make = find_blackjack_move(hand=hand, dealer_card=dealer_card, true_count=true_count)
        '''
        In test I use the find_move_test fucntion
        '''
        # move_to_make = find_move_test(hand=hand, dealer_card=dealer_card, true_count=true_count)

        if move_to_make == 'H':
            hand.hit(shoe)
            if hand.calculate_sum() > 21:
                self.balance -= hand.amount_of_bet  
                self.hands.remove(hand)  # Use remove instead of pop

            if hand.calculate_sum() == 21:
                hand.status['active'] = False
                rotate_first_to_last(self.hands)


            else:
                pass

        
        elif move_to_make == 'S':
            hand.stand()
            self.play_player_hands(dealer_card= dealer_card, shoe=shoe,true_count= true_count)

        elif move_to_make == 'D':
            if hand.status['can_double']:
                hand.double_down(shoe)
                if hand.calculate_sum() > 21:
                    self.balance -= hand.amount_of_bet
                    self.hands.remove(hand)  # Use remove instead of pop

                if hand.calculate_sum() == 21:
                    hand.status['active'] = False
                    rotate_first_to_last(self.hands)


            else: # can't double so we hit
                hand.hit(shoe)
                if hand.calculate_sum() > 21:
                    self.balance -= hand.amount_of_bet  
                    self.hands.remove(hand)  # Use remove instead of pop


                if hand.calculate_sum() == 21:
                    hand.status['active'] = False
                    rotate_first_to_last(self.hands)


                else:
                    pass
                

        elif move_to_make == 'SP':
            
    
            hand1, hand2 = hand.split(shoe)  # This should return two new hands
            # print(f'hand 1 {hand1} and hand 2 {hand2}')
            if hand2:  # If a split was successful and two hands were returned
                replace_first_with_two(lst= self.hands,new_first=hand1,new_second=hand2)
    
  
            else:
                print('problem with splitting')
                exit()

        else:
            print(f'tried to do {move_to_make}')
            print("Invalid move.")
            exit()
        

        true_count = shoe.true_count()
        self.play_player_hands(dealer_card= dealer_card, shoe=shoe,true_count= true_count) 


    def new_round(self):
        self.hands = []
    
    def show_hand(self, hand_index=0):
        return ', '.join(str(card) for card in self.hands[hand_index])

    def __repr__(self):
        return '\n'.join(f"{self.name} Hand {i+1}: {self.show_hand(i)} (Score: {self.scores[i]}, Bet: {self.bet[i]}, Bust: {self.is_busted[i]})" for i in range(len(self.hands))) + f"\nBalance: {self.balance}"




class Dealer(Player):
    def __init__(self, name='Dealer'):
        super().__init__(name)



    def calculate_money(self,players):
        pass

    def round(self,shoe,player, Print = False,deck_penetration = 3,num_of_decks = 7):

        num_of_cards_before_shuffel = int(52 * deck_penetration)
        if num_of_decks *52 < num_of_cards_before_shuffel:
            print('not enough cards for this deck penetration')
            exit()
  
        if len(shoe.dealt) > num_of_cards_before_shuffel:
            shoe.reset_shoe
        self.hands = []
        dealer_card = shoe.deal()
        dealer_hand = Hand(cards=[dealer_card],shoe=shoe)
        true_count = shoe.true_count()



        player.player_turn(shoe= shoe,dealer_card = dealer_card,true_count=true_count)

        if Print:
            print(f"{player.name}'s hands:",player.hands)
            print(f'dealer has: {dealer_card}')
            print(f'balance before = {player.balance}')
            print(f'true count is:  {true_count}')
            

        player_hands = player.hands
        if not player_hands == []:

            if player_hands[0].status['for_dealer'] == 'BJ':
                player.new_round()
                self.new_round()
                if Print:
                    print("player had BJ")
                    print(f"Player's balance after turn: {player.balance}")
                    print('\n')
                    print('\n')
                return 


        
            while dealer_hand.calculate_sum() < 17:
                dealer_hand.hit(shoe=shoe)
                if Print:
                    print(f'dealers has:  {dealer_hand.calculate_sum()}')
                if dealer_hand.calculate_sum() > 21:
                    # print("too many")
                    for hand in player_hands:
                        bet = hand.amount_of_bet
                        player.balance += bet
                    if Print:
                        print(f'now {player.name} has: {player.balance}')
                

                    player.new_round()
                    self.new_round()

                    if Print:
                        print('\n')
                        print('\n')
                    return
                

        
        dealer_sum = dealer_hand.calculate_sum()
        for hand in player_hands:
            if hand.calculate_sum() < dealer_sum:
                bet = hand.amount_of_bet
                player.balance -= bet

            if hand.calculate_sum() > dealer_sum :
                bet = hand.amount_of_bet
                player.balance += bet


            if Print:
                print(f'now {player.name} has {player.balance}')


        player.new_round()
        self.new_round()

        if Print:
            print(f'at the end {player.name} has {player.balance}')
            print('\n')
            print('\n')

        return





if __name__ == '__main__':


    card1 = Card('Hearts', '6')
    card2 = Card('Hearts', '10')
    dealer_card = Card('Hearts','10')
    
    shoe = Shoe()
    true_count = 0
    
    cards = [card1,card2]
    
   






   




