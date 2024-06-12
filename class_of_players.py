from class_of_cards import Shoe , Hand , Card
from strategy import find_blackjack_move
import time






class Player:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.hands = []
        # self.is_busted = [False]   #if we want to limit a low value.
        self.balance = initial_balance


    def get_to_this_round():
        #add card counting 
        pass
    
    

    def player_turn(self, shoe, dealer_card):
        # Deal an initial hand and set a starting bet
        initial_hand = shoe.deal_initial_hand()
        if initial_hand:
            initial_hand.amount_of_bet = 1
            self.hands.append(initial_hand)
        

        if initial_hand.calculate_sum() == 21:
            self.balance =+ initial_hand.amount_of_bet * 1.5
            return 'BJ'


# Prepare to play all hands, initializing results list
        results = []
        hands_to_play = self.hands[:]
        for hand in hands_to_play:
            if not hand.Done:
                self.play_with_hand(hand, dealer_card, shoe, results)
        
        # Collect results, excluding 'Bust' and include only hand details
        final_results = [result for result in results if result != 'Bust']
                # Print the sum of each remaining hand
        # for hand in final_results:
        #     if isinstance(hand, Hand):  # Check if the result is a Hand object
        #         print(f"Hand: {hand} with sum: {hand.calculate_sum()}")

        return final_results
    



    def play_with_hand(self, hand, dealer_card, shoe, results):
        if hand.calculate_sum() == 21:
            hand.Done = True

        if hand.Done:
            return results

        move_to_make = find_blackjack_move(hand=hand, dealer_card=dealer_card)
        if move_to_make == 'H':
            hand.hit(shoe)
            if hand.calculate_sum() > 21:
                self.balance -= hand.amount_of_bet  
                hand.Done = True
                results.append('Bust')
            else:
                # Continue playing if the hand is not bust and not done
                return self.play_with_hand(hand, dealer_card, shoe, results)
        
        elif move_to_make == 'S':
            hand.stand()
            results.append(hand)

        elif move_to_make == 'D':
            hand.double_down(shoe)
            if hand.calculate_sum() > 21:
                self.balance -= hand.amount_of_bet
                hand.Done = True
                results.append('Bust')
            else:
                results.append(hand)
            

        elif move_to_make == 'SP':
            hand1, hand2 = hand.split(shoe)  # This should return two new hands
            if hand2:  # If a split was successful and two hands were returned
                self.play_with_hand(hand1, dealer_card, shoe, results)
                self.play_with_hand(hand2, dealer_card, shoe, results)
            else:
                # If split fails (usually due to non-matching cards), treat as a hit
                return self.play_with_hand(hand, dealer_card, shoe, results)
        else:
            print("Invalid move.")
            return results
        
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



    def round(self,shoe,player, Print = False):
  
        if len(shoe.dealt) > 70:
            shoe.reset_shoe
        self.hands = []
        dealer_card = shoe.deal()
        dealer_hand = Hand(cards=[dealer_card],shoe=shoe)
        player_hands = player.player_turn(shoe= shoe,dealer_card = dealer_card)

        if Print:
            print("player's hands:",player_hands)
            print(type(player_hands))



      
        if player_hands == 'BJ':
            player.new_round()
            self.new_round()

            # print(f"Player's balance after turn: {player.balance}")
            return 



        while dealer_hand.calculate_sum() < 17:
            dealer_hand.hit(shoe=shoe)
            if Print:
                print(dealer_hand.calculate_sum())
            if dealer_hand.calculate_sum() > 21:
                # print("too many")
                for hand in player_hands:
                    bet = hand.amount_of_bet
                    player.balance += bet
            

                player.new_round()
                self.new_round()

                # print(f"Player's balance after turn: {player.balance}")
                return
                

        
        dealer_sum = dealer_hand.calculate_sum()
        for hand in player_hands:
            # print(hand)
            if hand.calculate_sum() < dealer_sum:
                bet = hand.amount_of_bet
                player.balance -= bet


            if hand.calculate_sum() > dealer_sum:
                bet = hand.amount_of_bet
                player.balance += bet


        player.new_round()
        self.new_round()


        # print(f"Player's balance after turn: {player.balance}")
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











    # hand1 = Hand(cards = cards, shoe= shoe)


    # Assume dealer's visible card is a '10 of Hearts'
    # dealer_card = Card('Hearts', '6')

    # # Run player's turn
    # results = player.player_turn(shoe, dealer_card)

    # # Print the results and player's balance after the turn
    # print("Results of the player's turn:")
    # for result in results:
    #     if isinstance(result, Hand):
    #         print(f"Hand with sum: {result.calculate_sum()}")
    #     else:
    #         print(result)
    # print(f"Player's balance after turn: {player.balance}")

    # result = player.play_with_hand(hand= hand1,dealer_card= dealer_card,shoe= shoe,results=[])

    # print(result)
    # print(f"Player's balance after turn: {player.balance}")