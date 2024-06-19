from class_of_cards import Shoe , Hand , Card
from strategy import find_blackjack_move
import time






class Player:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.hands = []
        # self.is_busted = [False]   #if we want to limit a low value.
        self.balance = initial_balance


    def get_in_this_round():
        #add card counting 
        pass
    
    

    def player_turn(self, shoe, dealer_card,true_count ,initial_bet = 1):
        # Deal an initial hand and set a starting bet
        initial_hand = shoe.deal_initial_hand()
        
        if initial_hand:
            initial_hand.amount_of_bet = initial_bet
            self.hands.append(initial_hand)


        if initial_hand.calculate_sum() == 21:
            # print("check BJ ")
            # print(f'the balance before was: {self.balance} ')

            self.balance += initial_hand.amount_of_bet * 1.5
            # print(f'and now it is {self.balance}')
            
            return 'BJ'


# Prepare to play all hands, initializing results list
        results = []
        hands_to_play = self.hands[:]
        if len(hands_to_play) >1:
            print(f'hands to play are {hands_to_play}      very weird')
            exit()
        # for hand in hands_to_play:
        #     if not hand.Done:
        #         self.play_with_hand(hand, dealer_card, shoe, results,true_count= true_count)
        #     if hand.Done:
        #         print(f'this hand was done: {hand}')
        self.play_with_hand(initial_hand, dealer_card, shoe, results,true_count= true_count)
                
        # Collect results, excluding 'Bust' and include only hand details
        final_results = [result for result in results if result != 'Bust']
        if final_results == []:
            # print('it is empty')
            if results == []:
                print('now')
                print(f'initial hand  {initial_hand}')
                exit()

        return final_results
    



    def play_with_hand(self, hand, dealer_card, shoe, results,true_count):
        if hand.calculate_sum() == 21:
            hand.Done = True
            results.append(hand)

        if hand.Done:
            return results

        move_to_make = find_blackjack_move(hand=hand, dealer_card=dealer_card, true_count=true_count)
        # print(f'should do {move_to_make}')
        if move_to_make == 'H':
            hand.hit(shoe)
            if hand.calculate_sum() > 21:
                # print('too many')
                # print(f'balance before {self.balance}')
                self.balance -= hand.amount_of_bet  
                # print(f'balance after {self.balance}')
                hand.Done = True
                results.append('Bust')
            else:
                # Continue playing if the hand is not bust and not done
                true_count = shoe.true_count()
                return self.play_with_hand(hand, dealer_card, shoe, results,true_count)
        
        elif move_to_make == 'S':
            hand.stand()
            results.append(hand)

        elif move_to_make == 'D':
            if hand.can_double == True:
                hand.double_down(shoe)
                if hand.calculate_sum() > 21:
                    # print('too many')
                    # print(f'balance before {self.balance}')
                    self.balance -= hand.amount_of_bet
                    # print(f'balance after {self.balance}')
                    hand.Done = True
                    results.append('Bust')
                else:
                    results.append(hand)
            else: # can't double so we split
                hand.hit(shoe)
                if hand.calculate_sum() > 21:
                    # print('too many')
                    # print(f'balance before {self.balance}')
                    self.balance -= hand.amount_of_bet  
                    # print(f'balance after {self.balance}')
                    hand.Done = True
                    results.append('Bust')
                else:
                    # Continue playing if the hand is not bust and not done
                    true_count = shoe.true_count()
                    return self.play_with_hand(hand, dealer_card, shoe, results,true_count)
                

        elif move_to_make == 'SP':
            
            # print("split timeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            hand1, hand2 = hand.split(shoe)  # This should return two new hands
            if hand2:  # If a split was successful and two hands were returned
                true_count = shoe.true_count()
       
                self.play_with_hand(hand1, dealer_card, shoe, results,true_count)
                self.play_with_hand(hand2, dealer_card, shoe, results,true_count)
            else:
                # If split fails (usually due to non-matching cards), treat as a hit
                return self.play_with_hand(hand, dealer_card, shoe, results,true_count)
        else:
            print("Invalid move.")
            return results
        if results == []:
            print('results are emptyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
            exit()
        return results


    def new_round(self):
        self.hands = []
    
    def show_hand(self, hand_index=0):
        return ', '.join(str(card) for card in self.hands[hand_index])

    def __repr__(self):
        return '\n'.join(f"{self.name} Hand {i+1}: {self.show_hand(i)} (Score: {self.scores[i]}, Bet: {self.bet[i]}, Bust: {self.is_busted[i]})" for i in range(len(self.hands))) + f"\nBalance: {self.balance}"




class Dealer(Player):
    def __init__(self, name='Dealer'):
        super().__init__(name)



    def round(self,shoe,player, Print = False,deck_penetration = 3,num_of_decks = 7):
        num_of_cards_before_shuffel = int(52 * deck_penetration)
        if num_of_decks *52 < num_of_cards_before_shuffel:
            print('need to shuffel before')
            exit()
  
        if len(shoe.dealt) > num_of_cards_before_shuffel:
            shoe.reset_shoe
        self.hands = []
        dealer_card = shoe.deal()
        dealer_hand = Hand(cards=[dealer_card],shoe=shoe)
        true_count = shoe.true_count()
        player_hands = player.player_turn(shoe= shoe,dealer_card = dealer_card,true_count=true_count)

        if Print:
            print("player's hands:",player_hands)
            print(f'dealer has: {dealer_card}')
            print(f'balance before = {player.balance}')
            print(f'true count is:  {true_count}')
            

    
        if player_hands == 'BJ':
            player.new_round()
            self.new_round()
            if Print:
                print("player had BJ")
                print(f"Player's balance after turn: {player.balance}")
                print('\n')
                print('\n')
            return 


        if not player_hands == []:
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
                        print(f'now player has: {player.balance}')
                

                    player.new_round()
                    self.new_round()

                    # print(f"Player's balance after turn: {player.balance}")
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
                print(f'now player has {player.balance}')


        player.new_round()
        self.new_round()


        # print(f"Player's balance after turn: {player.balance}")
        if Print:
            print(f'at the end player has {player.balance}')
            print('\n')
            print('\n')

        return














if __name__ == '__main__':


    card1 = Card('Hearts', '3')
    card2 = Card('Hearts', '3')

    cards = [card1,card2]
    
      

    # Initialize a player and a shoe
    player = Player(name="John Doe", initial_balance=0)
    dealer = Dealer()
    shoe = Shoe(num_decks=5) 
    print("start")
    dealer.round(player=player,shoe=shoe)









