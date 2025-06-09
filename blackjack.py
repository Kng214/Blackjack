import random
def createdeck():
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    cards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [(card, suit) for suit in suits for card in cards]
    #for suit in suits: #loop to make the numbers have all 4 suits
        #for num in numbers:
            #cards.append(f"{num} of {suit}")
    random.shuffle(deck)
    return deck

createdeck()

def card_values(card): #gets the values of every card
    if card[0] in ['J', 'Q', 'K']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])

def hand_value(hand): #reads aces in a players hand and the total value of their hand
    total = 0
    ace_count = 0
    for card in hand:
        value = card_values(card)
        total += value
        if card[0] == 'Ace':
            ace_count += 1
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total

def deal_card(deck): #deals a card from top of the deck
    return deck.pop()

def blackjack(): #bankroll for player, places bet, deals player 2 cards and shows value, deals dealers card and shows one
    player_bankroll = 100 #how much money player plays with
    deck = createdeck()
    while player_bankroll > 0:
        print(f"Current bankroll: ${player_bankroll}")
        try:
            bet = int(input("Place your bet: $"))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        if bet > player_bankroll:
                print("Not enough money! Bet Again!")
                continue
        if len(deck) < 15:
            print("Reshuffling deck...")
            deck = createdeck()
        
        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]
        
        print(f" Your hand is {player_hand[0]} and {player_hand[1]}, Your hand value is {hand_value(player_hand)}")
        print(f" Dealer has {dealer_hand[0]}")
        if hand_value(player_hand) == 21:
            player_bankroll += int(1.5 * bet)
            print("Blackjack! You win!")
            continue
        split_hand1 = None
        split_hand2 = None
        split_hand1_bust = False
        split_hand2_bust = False
        split_bet1 = bet  # Each split hand should have the same bet
        split_bet2 = bet
        total_bet = bet
        split_mode = False
        
        while True:
            if split_mode:
                break
            choice = input("Do you want to hit or stand or double or split (h/s/d/sp): ").lower() #implement double or splitting
            if choice == 'h':
                player_hand.append(deal_card(deck))
                print(f"Your hand value is {player_hand} and (Value: {hand_value(player_hand)})")
                print(f" Dealer has {dealer_hand[0]}")
                if hand_value(player_hand) > 21:
                    player_bankroll -= bet
                    print("You bust you lose!")
                    break  
            elif choice == 's':
                break  
            elif choice == 'd':
                if bet * 2 > player_bankroll:
                    print("You don't have enough money")
                    continue
                bet *= 2
                player_hand.append(deal_card(deck))
                print(f"Your hand value is {player_hand} and (Value: {hand_value(player_hand)})")
                if hand_value(player_hand) > 21:
                    player_bankroll -= bet
                    print("You bust you lose!")
                break  
            elif choice == 'sp': 
                if player_hand[0][0] != player_hand[1][0]: 
                    print("You cannot split different cards!")
                    continue
                if bet > player_bankroll:
                    print("Not enough money to split!")
                    continue

                split_mode = True
                split_hand1 = [player_hand[0], deal_card(deck)]
                split_hand2 = [player_hand[1], deal_card(deck)]

                print(f"Hand 1: {split_hand1}, Value: {hand_value(split_hand1)}")
                print(f"Hand 2: {split_hand2}, Value: {hand_value(split_hand2)}")

                # Aces Special Rule: Only One Card Per Hand
                if player_hand[0][0] == 'Ace':
                    print("Splitting Aces: You only get one more card per hand.")
                else:
                    print("Playing Hand 1:")
                    while True:
                        choice = input("Hit, stand, or double for Hand 1? (h/s/d): ").lower()
                        if choice == 'h':
                            split_hand1.append(deal_card(deck))
                            print(f"Hand 1: {split_hand1}, Value: {hand_value(split_hand1)}")
                            if hand_value(split_hand1) > 21:
                                print("You bust on Hand 1!")
                                break
                        elif choice == 's':
                            break
                        elif choice == 'd':
                            if split_bet1 > player_bankroll:
                                print("Not enough money to double down!")
                                continue
                            player_bankroll -= split_bet1  
                            split_bet1 *= 2  
                            split_hand1.append(deal_card(deck))
                            print(f"Final card for Hand 1: {split_hand1[-1]}, Value: {hand_value(split_hand1)}")
                            break

                    print("Playing Hand 2:")
                    while True:
                        choice = input("Hit, stand, or double for Hand 2? (h/s/d): ").lower()
                        if choice == 'h':
                            split_hand2.append(deal_card(deck))
                            print(f"Hand 2: {split_hand2}, Value: {hand_value(split_hand2)}")
                            if hand_value(split_hand2) > 21:
                                print("You bust on Hand 2!")
                                break
                        elif choice == 's':
                            break
                        elif choice == 'd':
                            if split_bet2 > player_bankroll:
                                print("Not enough money to double down!")
                                continue
                            player_bankroll -= split_bet2  
                            split_bet2 *= 2  
                            split_hand2.append(deal_card(deck))
                            print(f"Final card for Hand 2: {split_hand2[-1]}, Value: {hand_value(split_hand2)}")
                            break
                        else:
                            print("Invalid choice! Please enter 'h', 's', or 'd'.")

        print(f"Dealer's hand: {dealer_hand} (Value: {hand_value(dealer_hand)})")
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))
            print(f"Dealer draws... {dealer_hand} (Value: {hand_value(dealer_hand)})")

        dealer_total = hand_value(dealer_hand)
        
        if split_hand1 and split_hand2:
            for i, split_hand in enumerate([split_hand1, split_hand2]):
                player_total = hand_value(split_hand)
                if player_total > 21:  # Player busts, they lose immediately.
                    print(f"Hand {i+1} busts! You lose!")
                    player_bankroll -= bet
                elif player_total <=21 and dealer_total > 21:
                    print(f"Hand {i+1} wins! Dealer busts!")
                    player_bankroll += bet * 2
                elif dealer_total > player_total:
                    print(f"Dealer wins against Hand {i+1}!")
                    player_bankroll -= bet
                elif player_total > dealer_total:
                    print(f"Hand {i+1} wins!")
                    player_bankroll += bet * 2
                else:
                    print(f"Hand {i+1} is a push! No one wins.")
        else:
            player_total = hand_value(player_hand)
            if dealer_total > 21:
                print("You win! Dealer bust!")
                player_bankroll += bet
            elif dealer_total > player_total:
                print("Dealer wins!")
                player_bankroll -= bet
            elif player_total > dealer_total:
                print("Player wins!")
                player_bankroll += bet
            else:
                print("Push! No one wins!")

        split_hand1, split_hand2 = None, None  
    print("Game over! You've run out of money.")
            
blackjack()
    
            
    #need a user and a house
    #define a list of cards
    #numbers bust if over 21 unless it has an ace
    #house hits til soft 17
    #can do money in the game
    #10 jack queen king all 10
    #ace is 1 or 11 and chooses lower if goes over 21
    #user gets to stand or hit
    #two random cards are dealt to the user face up and the computer gets 1 card showing and 1 hidden