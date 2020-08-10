# Version 3: Includes aces being worth 11 points or 1 if they are over 21 (with ace counter instead of boolean)

# Player class:
class Player():

    def __init__(self, name='NA', bankroll=0):
        self.name = name
        self.bankroll = bankroll

    def check_roll(self):
        return self.bankroll

    def add_money(self, amount=0):
        self.bankroll += amount

    def check_bet_amount(self, amount):
        if amount <= self.bankroll:
            return True
        else:
            return False

    def remove_money(self, amount):
        if amount <= self.bankroll:
            self.bankroll -= amount
        else:
            print("Error. Withdrawal is too large.")


# Deck class:
import random


class Deck():
    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    numbers = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace')
    values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    def __init__(self):
        self.deck = []
        for suit in self.suits:
            for num in self.numbers:
                self.deck.append((suit, num))

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return self.deck

    def print_deck(self):
        print(self.deck)

    def get_deck(self):
        return self.deck


# Hand class:

class Hand():

    def __init__(self):
        self.used_cards = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_card_sum = 0
        self.dealer_card_sum = 0
        self.stand = False

    def clear_hand(self):
        self.used_cards.clear()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.player_card_sum = 0
        self.dealer_card_sum = 0
        self.stand = False

    def create_hand(self):
        self.used_cards.clear()
        dealing = True

        while True:
            while True:
                card_num = random.randint(0, 51)
                if card_num not in self.used_cards:
                    break
                else:
                    continue

            if len(self.player_hand) < 2:
                self.player_hand.append(card_num)
                self.used_cards.append(card_num)
            elif len(self.dealer_hand) < 2:
                self.dealer_hand.append(card_num)
                self.used_cards.append(card_num)
            else:
                break

        return [self.player_hand, self.dealer_hand]

    def does_player_move(self):
        while True:
            player_choice = input("Would you like to hit or stand? ")
            if player_choice.lower() == 'hit':
                return True
            elif player_choice.lower() == 'stand':
                return False
            else:
                print("Please type hit or stand.")

    def return_dealer_values(self, game_deck, values):
        card_sum = 0
        ace_count = 0

        for card in self.dealer_hand:
            card_type = game_deck[card][1]
            if card_type == 'Ace':
                ace_count += 1
            card_sum += values[card_type]

        for ace in range(0, ace_count):
            if card_sum > 21:
                card_sum -= 10

        self.dealer_card_sum = card_sum
        return card_sum

    def return_player_values(self, game_deck, values,):
        card_sum = 0
        ace_count = 0

        for card in self.player_hand:
            card_type = game_deck[card][1]
            if card_type == 'Ace':
                ace_count += 1
            card_sum += values[card_type]

        for ace in range(0, ace_count):
            if card_sum > 21:
                card_sum -= 10

        self.player_card_sum = card_sum
        return card_sum

    def print_dealer_hand(self, game_deck, player_stood):
        print('Dealer hand: ')
        if player_stood:
            for index, card in enumerate(self.dealer_hand):
                print(f'Card {index + 1}: {game_deck[card][1]} of {game_deck[card][0]}')
        else:
            print('First dealer card is hidden.')
            for index, card in enumerate(self.dealer_hand):
                if index == 0:
                    continue
                print(f'Card {index + 1}: {game_deck[card][1]} of {game_deck[card][0]}')

    def print_player_hand(self, game_deck):
        print('Player hand: ')
        for index, card in enumerate(self.player_hand):
            print(f'Card {index + 1}: {game_deck[card][1]} of {game_deck[card][0]}')

    def check_player_hand(self):
        if self.player_card_sum > 21:
            return 'BUST!'
        elif self.player_card_sum == 21:
            return '21'
        else:
            return 'Under 21'

    def check_dealer_hand(self):
        if self.dealer_card_sum > 21:
            return 'Dealer has busted.'
        elif self.dealer_card_sum == 21:
            return 'Dealer has blackjack.'
        else:
            return 'Dealer is under 21.'

    def deal_another_card(self, player_or_dealer):
        while True:
            card_num = random.randint(0, 51)
            if card_num not in self.used_cards:
                break
            else:
                continue

        if player_or_dealer.lower() == 'player':
            self.player_hand.append(card_num)
            self.used_cards.append(card_num)
        else:
            self.dealer_hand.append(card_num)
            self.used_cards.append(card_num)


# Actual game:
# Initialize items:
player = Player("John", 500)
deck = Deck()
hand = Hand()

print('Welcome to Blackjack!')

while True:

    continue_playing = input("Would you like to play? (Type no to quit) ")
    if continue_playing.lower() == 'no':
        break

    incorrect_bet = True

    while incorrect_bet:
        bet_amount = int(input('How much would you like to bet? '))

        if player.check_bet_amount(bet_amount):
            incorrect_bet = False
            player.remove_money(bet_amount)
        else:
            print('Please choose an appropriately sized bet.')

    game_deck = deck.shuffle_deck()
    card_vals = deck.values

    hand.clear_hand()
    current_hands = hand.create_hand()

    dealer_values = hand.return_dealer_values(game_deck, card_vals)
    player_values = hand.return_player_values(game_deck, card_vals)

    player_stood = False

    print()
    hand.print_dealer_hand(game_deck, player_stood)
    print()
    hand.print_player_hand(game_deck)
    print(f'Player sum: {player_values}')
    print()

    # Check for blackjack here and if they have it continue to the top of the loop.
    if player_values == 21:
        print("Blackjack! Congratulations!")
        print(f"You win {bet_amount * 2}.")
        player.add_money(bet_amount * 2)
        continue

    continue_betting = hand.does_player_move()

    player_busted = False

    # Make it so that as long as the user keeps betting (or until they bust) the loop continues
    # Once they stand start going up in dealer cards until they bust or win
    while continue_betting:
        hand.deal_another_card('player')
        player_values = hand.return_player_values(game_deck, card_vals)

        print()
        hand.print_dealer_hand(game_deck, player_stood)
        print()
        hand.print_player_hand(game_deck)
        print(f'Player sum: {player_values}')
        print()

        player_status = hand.check_player_hand()
        print(player_status)
        print()
        if player_status == 'BUST!':
            print('Dealer wins.')
            print()
            player_busted = True
            break

        continue_betting = hand.does_player_move()

    if player_busted:
        continue

    player_stood = True

    hand.print_dealer_hand(game_deck, player_stood)
    print(f'Dealer sum: {dealer_values}\n')

    # Now dealer is dealt cards until they reach 17 or bust:
    while dealer_values < 17:
        hand.deal_another_card('dealer')
        dealer_values = hand.return_dealer_values(game_deck, card_vals)
        hand.print_dealer_hand(game_deck, player_stood)
        print(f'Dealer sum: {dealer_values}\n')

    # Now check how dealer did compared to you:
    if dealer_values > 21:
        print('Dealer busted!')
        print(f"You win {bet_amount}.")
        player.add_money(bet_amount * 2)
        continue
    elif player_values < dealer_values < 22:
        print('The dealer won.')
        print(f"You lost {bet_amount}.")
    elif dealer_values == player_values:
        print('The dealer and player have the same hand. The pot is split.')
        print(f"Your original bet ({bet_amount}) has been returned.")
        player.add_money(bet_amount)
    else:
        print('You won!')
        print(f"You win {bet_amount}.")
        player.add_money(bet_amount * 2)


# After player stop playing:
print(f'Your bankroll is now: {player.check_roll()}')
print('Thank you for playing!')
