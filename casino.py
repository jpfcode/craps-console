#!/usr/bin/python

import random

diceDisplays = {
   1: ['│       │','│   o   │','│       │'],
   2: ['│ o     │','│       │','│     o │'],
   3: ['│ o     │','│   o   │','│     o │'],
   4: ['│ o   o │','│       │','│ o   o │'],
   5: ['│ o   o │','│   o   │','│ o   o │'],
   6: ['│ o   o │','│ o   o │','│ o   o │']
}


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
def getDieString(die1, die2):
   outputArray = ['┌───────┐   ┌───────┐\n']
   for i in range(3):
      total = die1 + die2
      totalString = ''
      if i == 1:
         totalString = ' = ' + str(total)
      outputArray.append(f"{diceDisplays[die1][i]}   {diceDisplays[die2][i]}{totalString}\n")
      
   outputArray.append('└───────┘   └───────┘\n')
   return ''.join(outputArray)
def printDie(die1, die2):
   print(getDieString(die1, die2))

def rollDie():
   return random.randint(1, 6)

def monify(amt):
   return f"${amt}"

def printBets(bets):
   print("\n-------------- BETS --------------")
   for bet in bets:
      print(f"{bets[bet]['name']} : {monify(bets[bet]['value'])}")
   print('')

def printMoney(money):
   print('┌────────┐')
   print(f"│$ {str(money).rjust(5, ' ')} │")
   print('└────────┘')

print("Welcome to Craps at the Command-Line Casino!\n")

money = 1000

# print(getDieString(rollDie(),rollDie()))
# for _ in range(10):
#    print(getDieString(rollDie(),rollDie()))

endOfGame = False

while not endOfGame:
   bets = {
      "pass": {
         "name": "Pass Bet      ",
         "value": 0,
      },
      "dontPass": {
         "name": "Don't Pass Bet",
         "value": 0
      }
   }
   
   print(f"You have {monify(money)} to spend.\n")
   doneBetting = False
   
   while not doneBetting:
      printMoney(money)
      printBets(bets)
      print ("\nWhich type of bet would you like to add?")
      betType = 'nothing'
      betAmt = 0
      while betType == 'nothing':
         betType = input ("\n[P]ass, [D]on't Pass, [N]one: ")
         betType = betType.lower()
         
         if len(betType) > 0 and betType not in ['p', 'd', 'n']:
            betType = 'nothing'
      
      if betType in ['p', 'd']:
         while betAmt < 1:
            betAmt = input("\nHow much would you like to wager: ")
            if not betAmt.isdigit():
               betAmt = 0
            else:
               betAmt = int(betAmt)

            if betAmt > money:
               print(f"\nSorry, you do not have that much money! You only have {monify(money)}\n")
         
         if betType == 'd':
            betType = 'dontPass'
         else:
            betType = 'pass'
         
         bets[betType]['value'] += betAmt
         money -= betAmt

      elif betType == None or betType == '' or betType == 'n':
         doneBetting = True
   
   printMoney(money)
   printBets(bets)
   print("Bets are closed!\n")

   print("========================================")
   print("             COME-OUT ROLL")
   print("========================================\n")

   die1 = rollDie()
   die2 = rollDie()
   total = die1 + die2
   printDie(die1, die2)

   if total in [2, 3, 12]:
      print("!!!!! CRAPS !!!!\n")
      print("Pass bets lose!")
      if total in [2,3]:
         print("Don't pass bets win!\n")
      else:
         print("Don't pass bets push (tie)!\n")

      if (bets['pass']['value'] > 0):
         print(f"You lost {monify(bets['pass']['value'])} on your Pass bet!")
      if bets['dontPass']['value'] > 0 and total is not 12:
         print(f"You WON {monify(bets['dontPass']['value'])} on your Don't Pass bet!")
         money += bets['dontPass']['value'] * 2
      print('')
   elif total in [7,11]:
      print("******* NATURAL *******\n")
      print("Pass bets win")
      print("Don't Pass bets lose\n")
      if (bets['pass']['value'] > 0):
         print(f"You WON {monify(bets['pass']['value'])} on your Pass bet!")
         money += bets['pass']['value'] * 2
      if bets['dontPass']['value'] > 0 and total is not 12:
         print(f"You lost {monify(bets['dontPass']['value'])} on your Don't Pass bet!")
      print('')
   else:
      cover = total
      print(f"COVER: {cover}")
      endOfRound = False
      while not endOfRound:
         input("Press the < enter > key to roll again")

         die1 = rollDie()
         die2 = rollDie()
         total = die1 + die2
         printDie(die1, die2)

         if cover == total:
            print("******* COVER PASSED *******\n")
            print("Pass bets win")
            print("Don't Pass bets lose\n")
            if (bets['pass']['value'] > 0):
               print(f"You WON {monify(bets['pass']['value'])} on your Pass bet!")
               money += bets['pass']['value'] * 2
            if bets['dontPass']['value'] > 0 and total is not 12:
               print(f"You lost {monify(bets['dontPass']['value'])} on your Don't Pass bet!")
            print("")
            endOfRound = True
         elif total == 7:
            print("!!!!! SEVEN OUT !!!!\n")
            print("Pass bets lose!")
            print("Don't pass bets win!\n")
            if (bets['pass']['value'] > 0):
               print(f"You lost {monify(bets['pass']['value'])} on your Pass bet!")
            if bets['dontPass']['value'] > 0 and total is not 12:
               print(f"You WON {monify(bets['dontPass']['value'])} on your Don't Pass bet!")
               money += bets['dontPass']['value'] * 2
            print('')
            endOfRound = True
   
   print("Round is over")
   print("\n Your Money:")
   printMoney(money)

   if money > 0:
      play_again = input("\nWould you like to play again? (Y/n): ")
      if play_again is None or play_again.lower() in ['y', 'yes', '']:
         endOfGame = False
      else:
         endOfGame = True   
   else:
      print("\n Sorry, you are out of money. Goodbye.")

print("\n\nThank you for playing at the Console Casino!")
 
   
