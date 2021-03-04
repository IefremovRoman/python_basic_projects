from random import choice
from os import system, name
from time import sleep
from collections import Iterable
# Greetings
print(
  """
  Welcome to roulette! This is European type roulette with almost real rules!
  Just bet, spin a roulette and have fun!

  You have $1000 start money. Bet by your system wisely!
  """
)

sleep(2)

# Initials
MONEY = 1000

def range_to_str_set(*args):
  return set(map(str, range(*args)))

# Numbers
_FIELD = set(map(str, range(37)))
_HALF1, _HALF2 = set(map(str, range(1, 19))), set(map(str, range(19, 37)))
_EVENS = set(map(str, range(2, 37, 2)))
_ODDS = _FIELD - _EVENS
_DOZEN1, _DOZEN2, _DOZEN3 = range_to_str_set(1, 13), range_to_str_set(13, 25), range_to_str_set(25, 37)
_COLUMN1, _COLUMN2, _COLUMN3 = range_to_str_set(1,37,3), range_to_str_set(2,37,3), range_to_str_set(3,37,3)
_REDS = {'1','3','5','9','12','14','16','18','19','21','23','25','27','30','32','34','36'}
_BLACKS = _FIELD - _REDS - {'0'}
_LAYERS = [_HALF1, _HALF2, _EVENS, _ODDS, _DOZEN1, _DOZEN2, _DOZEN3, _COLUMN1, _COLUMN2, _COLUMN3, _REDS, _BLACKS]

## Service functions

# Clear function
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

field_types = 'half1, half2, evens, odds, dozen1, dozen2, dozen3, column1, column2, column3, reds, blacks'.split(", ")
numbers_rewards = {str(v): 36 for v in range(37)}

section_rewards = {
  'half1': 2,
  'half2': 2,
  'evens': 2,
  'odds': 2,
  'dozen1': 3,
  'dozen2': 3,
  'dozen3': 3,
  'column1': 3,
  'column2': 3,
  'column3': 3,
  'reds': 2,
  'blacks': 2,
}

reward_system = dict(**section_rewards, **numbers_rewards)

_number_cells = _FIELD

def validate_bet_item(bet_item):
  if not (bet_item in set(field_types) | _number_cells):
    raise ValidationError(
              f'No such type of bet! Only the following instructions are supported: {field_types} or 0 to 36. Please bet again correctly!')
  return bet_item

def validate_bet_value(bet_value):
  try:
    bet_value = int(bet_value)
  except ValueError:
    raise ValidationError('Money value must be only integer!')
  else:
    if bet_value > MONEY:
      raise ValidationError('Check your available cash amount: you cannot place more than you have!')

    elif bet_value <= 0:
      raise ValidationError('Bet should be real positive integer number!')
    
    return bet_value

def validate_actchoice(actchoice):
  if not actchoice in ['s', 'u']:
    raise ValidationError('Bad answer! Try again!')
  return actchoice

def input_and_clean(prompt_msg, validator):
  while True:
    value = input(prompt_msg)
    
    try:
      if isinstance(validator, Iterable):
        if value not in validator:
          raise ValidationError(f'Value should be one of {validator}')
      else:
        value = validator(value)
      return value
    except ValidationError as e:
      print(e.msg)

## Bet system
def betting():
  global MONEY
  bet_pack = dict()

  clear()
  print(
    """
    Bet by your system! First should be number or part of field, like half1 (1-18), half2 (19-36), evens, odds, dozen1 (1-12), dozen2 (13-24), dozen3 (25-36), column1, column2, column3, reds, blacks. Second should be bet equivalent in $.
    """
    )
  
  count = 0
  while True and MONEY:
    
    if bet_pack:
      for k, v in bet_pack.items():
        print(f'{k}: ${v}', sep='\n')
      print('\n')

    if count:
      bet_answer = input('Do you need more bet? ')
    else:
      bet_answer = 'y'

    
    if bet_answer == 'y' and MONEY:
      print(f'You still have ${MONEY} left. How much will you put?')
    
      # Validation and forming bet_pack
      bet_item = input_and_clean("Input your bet item: ", validate_bet_item)
      print('Bet item:', bet_item)
      bet_value = input_and_clean("Input your bet value: ", validate_bet_value)
      
      MONEY -= bet_value
      
      if bet_item in bet_pack:
        print('What do we need to do with your previous bet? Sum or upgrade?')
        
        
        actchoice = input_and_clean("Press 's' for sum or 'u' for upgrade: ", ['s', 'u'])
          
        if actchoice == 's':
          bet_pack[bet_item] += bet_value
          
        elif actchoice == 'u':
          MONEY += bet_pack[bet_item] - bet_value
          bet_pack[bet_item] = bet_value

      else: 
        bet_pack[bet_item] = bet_value

      count += 1
      continue
        

    elif bet_answer == 'n':
      break
    
    elif not MONEY:
      print('Not enough to make more bet pack!')
      break
  
  return bet_pack

## Rewarding system counting the reward sum
def rewarding(number, bet_pack):
  reward = 0

  for layer, key in zip(_LAYERS, field_types):

    if number in layer and key in bet_pack.keys():
      reward += bet_pack[key] * reward_system[key]

  if number in bet_pack.keys():
    reward += bet_pack[number] * 36

  return reward

## Game engine
while MONEY:
  bet = betting()
  print('Spinning...')
  sleep(3)
  lucky_number = choice(list(_FIELD))
  print(f' It is: {lucky_number}!')
  reward = rewarding(lucky_number, bet)
  print(f'You have got ${reward}!')
  MONEY += reward
  input('Lets try again! Just press "Enter"')

else:
  print('You lost all your money in this tricky game! Get more money and come back!')
