#!/usr/bin/python
import curses
from curses import wrapper
import random

dice_displays = {
   1: ['│       │','│   o   │','│       │'],
   2: ['│ o     │','│       │','│     o │'],
   3: ['│ o     │','│   o   │','│     o │'],
   4: ['│ o   o │','│       │','│ o   o │'],
   5: ['│ o   o │','│   o   │','│ o   o │'],
   6: ['│ o   o │','│ o   o │','│ o   o │']
}

board_offset_y = 1
board_offset_x = 1

board_display = [
   "╔══════════════════════════════════════════════════════╗",
   "║             Command Line Casino Craps                ║",
   "╚══════════════════════════════════════════════════════╝",
   "│ BETS                                          STATUS │",
   "├────────────┬────────────┬────────────────────────────┤",
   "│ PASS       │ DON'T PASS │       COME OUT ROLL        │",
   "│ $          │ $          ├────────────────────────────┤",
   "├────────────┴────────────┤                            │",
   "│ Types of bets:          │                            │",
   "│ [P]ass                  │                            │",
   "│ [D]on't Pass            │                            │",
   "│ [N]one                  │                            │",
   "│                         ├────────────────────────────┤",
   "│                         │   YOUR MONEY: $            │",
   "└─────────────────────────┴────────────────────────────┘",
]

'''
RULES OF CRAPS:
   Based on https://en.wikipedia.org/wiki/Craps
   Bets Possible:
      Pass: 
         Pays even money (1:1, double your money)
         Contract Bet (cannot be taken down once a point is established)
      Don't Pass: 
         Pays even money (1:1, double your money)
         No-contract Bet (Can be taken down once a point is established because the odds are in the player's favor)
      Point Number Bet:
         Can be placed at anytime

   Phases:
      Come Out
      Point

   Come Out:
      Roll Outputs:
         2, 3, 12:
            CRAPS!
               "Pass" bets LOSE
               "Don't Pass" bets 
                  WIN on 2,3
                  TIE on 12
         7, 11:
            NATURAL
               "Pass" bets WIN
               "Don't Pass" bets LOSE
         4,5,6,8,9,10:
            POINT established
   Point:
      Point must be rolled again before a 7
      Roll Output:
         7:
            "Pass" LOSES
            "Don't Pass" WINS
         Point:
            "Pass" WINS
            "Don't Pass" LOSES
      
            

'''

game_state = {
   'phase': 'BETTING',
   'money': 1000,
   'bets': {
      "pass": 0,
      "dontPass": 0
   },
   'dice': []
}

def get_die_string_array(die1, die2):
   output_array = ['┌───────┐     ┌───────┐']
   total = die1 + die2
   
   for i in range(3):
      total_string = '     '
      if i == 1:
         total_string = str(total).center(5)
      output_array.append(f"{dice_displays[die1][i]}{total_string}{dice_displays[die2][i]}")
   
      
   output_array.append('└───────┘     └───────┘')
   return output_array

def print_dice(stdscr, die1, die2):
   die_string_array = get_die_string_array(die1, die2)
   count = 0
   for line in die_string_array:
      stdscr.addstr(board_offset_y + 7 + count, board_offset_x + 29, line, curses.color_pair(227))
      count += 1
   
   stdscr.refresh()




def rollDie():
   return random.randint(1, 6)

def get_input(stdscr, row, col, prompt_string):
   stdscr.move(board_offset_y + 15 + row, board_offset_x + 1)
   # Delete the line
   stdscr.deleteln()
   curses.echo() 
   stdscr.addstr(board_offset_y + row + 15, board_offset_x + col + 1, prompt_string)
   stdscr.refresh()
   input = stdscr.getstr(board_offset_y + row + 15, board_offset_x + col + 1 + len(prompt_string), 20)
   return input

def refresh_board(stdscr):
   row = board_offset_y
   col = board_offset_x
   for line in board_display:
      stdscr.addstr(row, col, line)
      row += 1
   
   # Print status
   stdscr.addstr(board_offset_y + 5, board_offset_x + 28, game_state['phase'].center(27), curses.color_pair(124))

   # Print bets
   stdscr.addstr(board_offset_y + 6, board_offset_x + 4, str(game_state['bets']['pass']).rjust(4, ' '))
   stdscr.addstr(board_offset_y + 6, board_offset_x + 17, str(game_state['bets']['dontPass']).rjust(4, ' '))
   
   # Print player money
   stdscr.addstr(board_offset_y + 13, board_offset_x + 45, str(game_state['money']).rjust(5, " "))
   
   # Print die
   if len(game_state['dice']) > 0:
      print_dice(stdscr, game_state['dice'][0], game_state['dice'][1])

   stdscr.refresh()

def print_msg(stdscr, text, line=0):
   # Move the cursor to the outputString line
   stdscr.move(board_offset_y + 15 + line, board_offset_x + 1)
   # Delete the line
   stdscr.deleteln()
   # Print the new line
   stdscr.addstr(board_offset_y + 15 + line, board_offset_x + 1, text)
   stdscr.refresh()

text_obj = {
   "text": '',
   "color": curses.COLOR_WHITE
}

def print_multicolor_message(stdscr, text_obj_array, line = 0):
   # Move the cursor to the outputString line
   stdscr.move(board_offset_y + 15 + line, board_offset_x + 1)
   # Delete the line
   stdscr.deleteln()

   # Print the new lines
   for text_o in text_obj_array:
      if type(text_o) is str:
         stdscr.addstr(text_o)
      else:
         stdscr.addstr(text_o['text'], text_o['color'])
   
   stdscr.refresh()

def print_lost_msg(stdscr, amount, bet_type, message_line = 0):
   print_multicolor_message(stdscr, [ "You ", {"text": "LOST", "color": curses.color_pair(197) }, f" $ {amount} on your {bet_type} bet!"], message_line)
 
def print_won_msg(stdscr, amount, bet_type, message_line = 0):
   print_multicolor_message(stdscr, [ "You ", {"text": "WON", "color": curses.color_pair(48) }, f" $ {amount} on your {bet_type} bet!"], message_line)
 
def clear_dice():
   game_state['dice'] = []

def main(stdscr):
   curses.start_color()
   curses.use_default_colors()
   for i in range(0, curses.COLORS):
      curses.init_pair(i + 1, i, -1)
   
   clear_dice()
   refresh_board(stdscr)
   game_state['money'] = 1000

   end_of_game = False

   while not end_of_game:
      game_state['bets'] = {
         "pass": 0,
         "dontPass": 0
      }
      
      doneBetting = False
      
      while not doneBetting:
         refresh_board(stdscr)
         print_msg(stdscr, "Add a bet? [P]ass, [D]on't Pass, [N]one: ")
         betType = 'nothing'
         while betType == 'nothing':
            betType = stdscr.getch()
            #print_msg(stdscr, "Yup " + str(chr(betType)))
            betType = str(chr(betType)).lower()
            
            if len(betType) > 0 and betType not in ['p', 'd', 'n']:
               betType = 'nothing'
         
         betAmt = 0
         if betType in ['p', 'd']:
            while betAmt < 1:
               betAmt = get_input(stdscr, 0, 0, "How much would you like to wager: $ ")
               #betAmt = 100 #input("\nHow much would you like to wager: ")
               if not betAmt.isdigit():
                  betAmt = 0
               else:
                  betAmt = int(betAmt)

               if betAmt > game_state['money']:
                  print_msg(stdscr, f"Sorry, you do not have that much money!", 1)
            
            if betType == 'd':
               betType = 'dontPass'
            else:
               betType = 'pass'
            
            game_state['bets'][betType] += betAmt
            game_state['money'] -= betAmt

         elif betType == None or betType == '' or betType == 'n':
            doneBetting = True
      
      ####################################################
      # COME-OUT PHASE
      game_state['phase'] = 'COME-OUT ROLL'
      refresh_board(stdscr)
      
      clear_dice()
      die1 = rollDie()
      die2 = rollDie()
      game_state['dice'].append(die1)
      game_state['dice'].append(die2)
      total = die1 + die2
      message_line = 0

      if total in [2, 3, 12]:
         game_state['phase'] = "!!!!! CRAPS !!!!!"
         refresh_board(stdscr)
         #print("Pass bets lose!")
         #if total in [2,3]:
         #   print("Don't pass bets win!\n")
         #else:
         #   print("Don't pass bets push (tie)!\n")

         if (game_state['bets']['pass'] > 0):
            print_lost_msg(stdscr, game_state['bets']['pass'], "Pass", message_line)
            message_line += 1
            
         if game_state['bets']['dontPass'] > 0 and total is not 12:
            print_won_msg(stdscr, game_state['bets']['dontPass'], "Don't Pass", message_line)
            message_line += 1
            game_state['money'] += game_state['bets']['dontPass'] * 2
      elif total in [7,11]:
         game_state['phase'] = "*** NATURAL ***"
         # print("Pass bets win")
         # print("Don't Pass bets lose\n")
         if (game_state['bets']['pass'] > 0):
            print_won_msg(stdscr, game_state['bets']['pass'], "Pass", message_line)
            message_line += 1
            game_state['money'] += game_state['bets']['pass'] * 2
         if game_state['bets']['dontPass'] > 0 and total is not 12:
            print_lost_msg(stdscr, game_state['bets']['dontPass'], "Don't Pass", message_line)
            message_line += 1
         refresh_board(stdscr)
      else:
         cover = total
         game_state['phase'] = f"COVER: {cover}"
         refresh_board(stdscr)
         endOfRound = False
         while not endOfRound:
            print_msg(stdscr, "Press the < enter > key to roll again")
            _ = stdscr.getch()

            clear_dice()
            die1 = rollDie()
            die2 = rollDie()
            game_state['dice'].append(die1)
            game_state['dice'].append(die2)
            total = die1 + die2
            print_dice(stdscr, die1, die2)

            if cover == total:
               game_state['phase'] = "*** COVER PASSED ***"
               # print("Pass bets win")
               # print("Don't Pass bets lose\n")
               if (game_state['bets']['pass'] > 0):
                  print_won_msg(stdscr, game_state['bets']['pass'], "Pass", message_line)
                  message_line += 1
                  game_state['money'] += game_state['bets']['pass'] * 2
               if game_state['bets']['dontPass'] > 0 and total is not 12:
                  print_lost_msg(stdscr, game_state['bets']['dontPass'], "Don't Pass", message_line)
                  message_line += 1

               refresh_board(stdscr)

               endOfRound = True
            elif total == 7:
               game_state['phase'] = "!!! SEVEN OUT !!!"
               # print("Pass bets lose!")
               # print("Don't pass bets win!\n")
               if (game_state['bets']['pass'] > 0):
                  print_lost_msg(stdscr, game_state['bets']['pass'], "Pass", message_line)
                  message_line += 1
               if game_state['bets']['dontPass'] > 0 and total is not 12:
                  print_won_msg(stdscr, game_state['bets']['dontPass'], "Don't Pass", message_line)
                  message_line += 1
                  game_state['money'] += game_state['bets']['dontPass'] * 2
               endOfRound = True
               refresh_board(stdscr)
      
      if int(game_state['money']) > 0:
         print_msg(stdscr, "Would you like to play again? (Y/n): ", message_line)
         message_line += 1

         play_again = stdscr.getch()
         play_again = str(chr(play_again)).lower()
         while play_again not in ['y', 'n']:
            play_again = stdscr.getch()
            play_again = str(chr(play_again)).lower()
         
         if play_again is None or play_again.lower() in ['y', 'yes', '']:
            end_of_game = False
         else:
            end_of_game = True   
      else:
         print_msg(stdscr, "Sorry, you are out of money. Goodbye.", message_line)
         message_line += 1
         end_of_game = True

   print_msg(stdscr, "Thank you for playing at the Console Casino!", message_line)
   _ = stdscr.getch()

# Wrapper is a curses wrapper that sets up the console screen and restores
# it when completed or errored out
wrapper(main)
      
