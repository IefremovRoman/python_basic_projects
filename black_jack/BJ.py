from random import shuffle
import time
import os
import sys
from collections import namedtuple

# Greetings
def greetings(player_name=''):
  with open('welcome_text.txt', 'r', encoding='utf-8') as file:
      print(file.read())
  # Naming
  if player_name:
    print('Type your name: {}'.format(player_name))
  else:
    player_name = input('Type your name: ')
  
  return player_name
  
def initial_values():
  # Number of decks
  player_name = ''
  while True:
    try:
      player_name = greetings(player_name)
      decks = int(input('Type number of decks you want to play with. You can only choose numbers of 1, 2, 4, 6 or 8 decks: '))
      if decks in [1,2,4,6,8]:
        time.sleep(0.1)
        break
      else:
        raise ValueError
    except ValueError:
      os.system('cls' if os.name == 'nt' else 'clear')
  
  return player_name, decks

def int_checked_input(prompt):
    while True:
      try:
        return int(input(prompt))
                
      except ValueError:
        os.system('clear')
        continue

PLAYER_NAME, NUM_OF_DECKS = initial_values()

time.sleep(2)
os.system('clear')
print(
  "Hello, {}! For welcome game our casino gave you $100.0 cash. You can only play with whis sum, no turning back. So let's play!".format(PLAYER_NAME)
  )

Card = namedtuple('Card', 'value, color')
colors = ['H', 'D', 'S', 'C']
card_values = {
          'A': 11,  # value of the ace is high until it needs to be low
          '2': 2,
          '3': 3,
          '4': 4,
          '5': 5,
          '6': 6,
          '7': 7,
          '8': 8,
          '9': 9,
          '10': 10,
          'J': 10,
          'Q': 10,
          'K': 10
      }

def define_new_deck():
  return [Card(v, c) for v in card_values for c in colors] * NUM_OF_DECKS

def card_display(card):
  suits = {'H': '♥',
           'D': '♦',
           'S': '♠',
           'C': '♣'}
  return suits[card.color] + card.value

#def hand_state_display(hand):

#score = lambda hand: sum([card_values[card.value] for card in hand])
def score(hand):
  hand_score = sum([card_values[card.value] for card in hand])  
  aces = [card for card in hand if card.value == 'A']
  if aces and hand_score > 21:
    if len(aces) == len(hand):
      hand_score -= (10 * (len(aces) - 1))
    else:
      hand_score -= 10 * len(aces)
  return hand_score

display_hand = lambda cards: [card_display(card) for card in cards]

MONEY = 100

Deck = []

def distribution_of_cards():
    global Deck
    Deck = define_new_deck()
    shuffle(Deck)
    Deck = [card for card in Deck if card not in player_hand + croupier_hand]
    print('New deck given...')

while MONEY > 0:
  time.sleep(2)
  os.system('cls' if os.name == 'nt' else 'clear')
  
  if len(Deck) == 0:
    Deck = define_new_deck()
    shuffle(Deck)

  player_hand = []
  croupier_hand = []

  print('Your current money: {}$'.format(int(MONEY)))

  # Betting
  while True:
    bet = int_checked_input('Place your bet: ')
    if bet > MONEY:
      print('You cannot bet more than you have!')
      continue
    
    else:
      MONEY -= bet
      break
  
  while True:
    try:
      player_hand.append(Deck.pop()) if len(player_hand) == 0 else player_hand
      croupier_hand.append(Deck.pop()) if len(croupier_hand) == 0 else croupier_hand
      player_hand.append(Deck.pop()) if len(player_hand) == 1 else player_hand
      croupier_hand.append(Deck.pop()) if len(croupier_hand) == 1 else croupier_hand
      break
    except IndexError:
      distribution_of_cards()
      continue

  #distribution_of_cards()
  LOOSER_FLAG, PLAYER_BJ, CROUPIER_BJ, CROUPIER_BUSTS = False, False, False, False
  
  loop_counter = 0

  while not LOOSER_FLAG or score(player_hand) <= 21:
   
    print("Player's hand:", *display_hand(player_hand), "Player's score:", score(player_hand))
    print("Croupier's hand:", card_display(croupier_hand[0]), 'XX')

    if score(player_hand) < 21:
      move = input("Do you need more cards? Type 'Hit' to give you 1 more card, or 'Stand' to transfer the move to croupier. Your answer: ")

      loop_counter += 1
      
      if move == 'h': 
        try:
          player_hand.append(Deck.pop())
        except IndexError:
          distribution_of_cards()
          player_hand.append(Deck.pop())
          
        PLAYER_BJ = False; continue
        
      elif move == 's': break
        
      # Here must be another functions as 'Double', 'Split', 'Surrender', 'Incurance'
      else: continue
         
    elif score(player_hand) == 21: 
      if not loop_counter:
          PLAYER_BJ = True
      break
      
    else: print('You loose!'); LOOSER_FLAG = True; break
    
  else: print('You loose!'); continue

  if LOOSER_FLAG:
    continue

  else:
    while score(croupier_hand) < 16 and not PLAYER_BJ:
      time.sleep(1.2)
      CROUPIER_BJ = False
      print("Croupier's hand:", *display_hand(croupier_hand), "Croupier's score:", score(croupier_hand))
      print('Croupier hits...')
      try:
        croupier_hand.append(Deck.pop())
      except IndexError:
        distribution_of_cards()
        croupier_hand.append(Deck.pop())
      time.sleep(0.5)
    
    # Croupier stands
    else:
      print("Croupier's hand:", *display_hand(croupier_hand), "Croupier's score:", score(croupier_hand))
      #CROUPIER_BJ = True if score(croupier_hand)

      if score(croupier_hand) > 21:
        CROUPIER_BUSTS, CROUPIER_BJ = True, False
        print('Croupier busts!')
      else:
        print('Croupier stands.')

    time.sleep(1.2)
    # BJ winner
    if PLAYER_BJ and not CROUPIER_BJ:
      MONEY += (1 + 1.5) * bet
      #MONEY = int(MONEY)
      print('You win with BJ!')
      print(f"You've got {(1 + 1.5) * bet}$")
      time.sleep(2)
      continue

    # 21 winner
    elif (not PLAYER_BJ and not CROUPIER_BJ and score(player_hand) > score(croupier_hand)) or CROUPIER_BUSTS:
      MONEY += bet * 2
      print('You win!')
      print(f"You've got {bet * 2}$")
      time.sleep(2)
      continue
    
    # Draw game
    elif score(croupier_hand) == score(player_hand):
      MONEY += bet
      #print("Croupier's hand:", *display_hand(croupier_hand), "Croupier's score:", score(croupier_hand))
      print('Draw!')
      print(f"You've got your bet ({bet}$) back!")
      time.sleep(2)
      continue

    # Croupier wins
    elif (score(player_hand) < score(croupier_hand) <= 21) or (CROUPIER_BJ and not PLAYER_BJ):
      #print("Croupier's hand:", *display_hand(croupier_hand), "Croupier's score:", score(croupier_hand))
      print('Croupier wins - you loose!')
      time.sleep(2)
      continue

    # Test logic case
    else:
      print('Else test winner case')
      time.sleep(2)
      continue   

#end
else:
  print('You lost all you money in this game. Get more money and come back!')
  print(sys.exit('Code stopped here: row 250'))
