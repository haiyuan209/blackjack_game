# used for shuffling deck before dealing cards
import random

# used for pausing print statements to make program more user-friendly
import time

# variables to store type of cards
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
          'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

# Boolean to control flow of game
playing = True


class Card:
    '''
    Class used to handle suit, rank, and value of cards
    Attributes:
        Suit (str): suit of the card
        Rank (str): rank of the card
        Value (int): int value of the card
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    '''
    Class for storing all 52 card objects
    Attributes:
        deck (list): A deck of 52 card objects
    '''

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                # create Card object and add to deck
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_output = ''  # start as empty string

        for card in self.deck:
            deck_output += '\n' + card.__str__()  # add each Card object print string

        return 'Deck contains: \n' + deck_output

    def shuffle(self):
        '''
        Method for shuffling cards in deck
        '''

        random.shuffle(self.deck)

    def deal(self):
        '''
        Method for dealing a card
        Returns:
            str: Rank and suit of card
        '''

        dealt_card = self.deck.pop()
        return dealt_card


class Hand:
    '''
    Class to calculate values of cards dealt to each player
    Attributes:
        cards (list): cards in hand
        value (int): total value of cards in hand
        aces (int): amount of aces in hand
    '''

    def __init__(self):
        self.cards = []         # start with an empty list as we did in the Deck class
        self.value = 0          # start with zero value
        self.aces = 0           # add an attribute to keep track of aces

    def add_card(self, card):
        '''
        Method to add card and its value to hand
        '''

        self.cards.append(card)  # add card to hand
        self.value += values[card.rank]  # add value of card to hand

        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        '''
        Method to adjust value of cards in hand if there is an ace
        '''

        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    '''
    Class to keep track of Player's chips, bets, and winnings
    Attributes:
        total (int): total chips that the player has
        bet (int): bet placed for amount of chips
    '''

    def __init__(self):
        self.total = 100  # Starting amount of chips
        self.bet = 0

    def win_bet(self):
        '''
        Player wins bet. Total amount increases.
        '''

        self.total += self.bet

    def lose_bet(self):
        '''
        Player loses bet. Total amount decreases.
        '''
        self.total -= self.bet


def take_bet(chips):
    '''
    Ask user to place amount to bet.
    Parameters:
        chips (int): Amount of chips the player has
    '''

    while True:
        try:
            chips.bet = int(input("Enter the amount you would like to bet: "))
        except:
            print("Invalid input.")
        else:
            if chips.bet <= 0:
                print("You must enter an amount greater than 0.")
            elif chips.bet > chips.total:
                print("Your bet cannot exceed " + str(chips.total) + ".")
                continue
            else:
                print("\nYou bet " + str(chips.bet) + " chips.")
                print("Chips remaining: ", + (chips.total - chips.bet))
                print("===================================")
                time.sleep(3)
                break


def hit(deck, hand):
    '''
    Handles hits whenever player requests a hit or Dealer's hand is less than 17
    Parameters:
        deck (list): Cards in deck
        hand (list): Cards in hand
    '''

    hand.add_card(deck.deal())  # take card from deck and add to hand
    hand.adjust_for_ace()  # adjust value if there is an ace


def hit_or_stand(deck, hand):
    '''
    Determine if game continues based on whether player hits or stands
    Parameters:
        deck (list): Cards in deck
        hand (list): Cards in hand
    '''

    global playing  # to control an upcoming while loop

    while True:
        if player_hand.value == 21:
            print("BLACKJACK!")
            time.sleep(3)
            print("===================================")
            playing = False
            break

        x = input("Would you like to hit or stand? ")

        if x.lower() == 'hit':
            print("===================================\n")
            time.sleep(1)
            hit(deck, hand)  # hit() function defined above

        elif x.lower() == 'stand':
            print("Player stands. Dealer is playing.")
            print("===================================\n")
            time.sleep(3)
            playing = False

        else:
            print("Invalid input.")
            continue
        break


def show_some(player, dealer):
    '''
    Show one of the dealer's hidden card, and all of player's card
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
    '''

    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print('Total: ' + str(player.value) + '\n')


def show_all(player, dealer):
    '''
    Show all of dealer's cards, and all of player's cards
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
    '''

    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    '''
    Player busts and loses chips
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
        chips (int): Amount of chips that player has
    '''

    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    '''
    Players wins and earns chips
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
        chips (int): Amount of chips that player has
    '''

    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    '''
    Dealer busts and player earns chips
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
        chips (int): Amount of chips that player has
    '''

    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    '''
    Dealer wins and players loses chips
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
        chips (int): Amount of chips that player has
    '''

    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    '''
    Dealer and player ties, and player's chips are unaffected
    Parameters:
        player (list): Cards in player's hand
        dealer (list): Cards in dealer's hand
        chips (int): Amount of chips that player has
    '''

    print("Dealer and Player tie! It's a push.")

# GAMEPLAY


# Print an opening statement
print('Welcome to BlackJack! Get as close to 21 without going over.\n\
Dealer hits until he reaches 17 or over.\n')

# Print amount of chips the player starts with
print('You will start with 100 chips.\n')

time.sleep(3)

player_chips = Chips()

while True:
    print('Chips remaining: ' + str(player_chips.total))

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            show_all(player_hand, dealer_hand)
            player_busts(player_hand, dealer_hand, player_chips)
            break

        # If player's hand is 21, break out of loop
        if player_hand.value == 21:
            break

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips total
    print("\nPlayer's winnings:", player_chips.total)

    # Player has 0 chips remaining, ask to play again
    if player_chips.total == 0:
        print("You ran out of chips!")

        new_game = input(
            "Would you like to start over and play again (yes or no)? ")

        # Ask to play again
        if new_game.lower() == 'yes':
            player_chips.total = 100

            print("Restarting game...\n")
            time.sleep(3)
            continue
        elif new_game.lower() == 'no':
            print("Thanks for playing!")
            break
        else:
            print("Invalid input.")
            break

    # Player has more than 0 chips remaining, ask to play again
    new_game = input("Would you like to play again? (yes or no) ")

    if new_game.lower() == 'yes':
        playing = True
        continue
    elif new_game.lower() == 'no':
        print("Thanks for playing!")
        break
    else:
        print("Invalid input.")
