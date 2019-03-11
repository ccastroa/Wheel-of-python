#Carol Castro
#88710391

import json
import wof_computer
import random

NUM_HUMAN   = 1
NUM_PLAYERS = 3
VOWEL_COST  = 250
VOWELS = ['A', 'E', 'I', 'O', 'U']

# Load the wheel
wheelFile = open('wheel.json', 'r')
wheel = json.loads(wheelFile.read())
wheelFile.close()

# Load the phrase set
phraseFile = open('phrases.json', 'r')
phrases = json.loads(phraseFile.read())
phraseFile.close()
wof_computer.train(phrases)

# Uncomment these to see the structure of wheel and phrases

# print(json.dumps(wheel,indent=3))
# print(json.dumps(phrases,indent=3))

# Get a random item from wheel
def spinWheel():
    return random.choice(wheel)


# Get a random phrase and category
def getRandomCategoryAndPhrase():
    category = random.choice(list(phrases.keys()))
    phrase   = random.choice(phrases[category])
    return (category, phrase.upper())


def createPlayer(isComputer, player_num):
    if isComputer:
        name = 'Computer {}'.format(player_num)
    else:
        name = input('Enter your name: ')

    return WheelOfFortunePlayer(name, isComputer)


#####################################################
################ Do not change above ################
#####################################################


class WheelOfFortunePlayer():
    def __init__(self, name, isComputer):
        self.name       = name
        self.prizeMoney = 0
        self.prizes     = []
        if isComputer:
            self.computer = wof_computer.WOFComputer(difficulty = random.randint(1,9))
        else:
            self.computer = False


    def addMoney(self, amount):
        self.prizeMoney += amount

    def subtractMoney(self, amount):
        return self.addMoney(-amount)

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self, prize):
        self.prizes.append(prize)

    def getMove(self, *args, **kwargs):
        if(self.computer):
            return self.computer.getMove(*args, **kwargs)
            return ("{} guesses {}".format(self.name, guesses))
        else:
            return input('{}, Enter your guess: '.format(self.name)).upper()
    def __str__(self):
        return '{} (${})'.format(self.name, self.prizeMoney)

def completephrase(guessed, phrase):
    return all([(letter in guessed) or (not letter.isalnum()) for letter in phrase]) #checks to see if all values are true.

def obscurePhrase(phrase, guesses):
    word=''
    for m in phrase:
        if m.isalnum() == True and m not in guesses: #should underscore:
            word+= '_'
        else:
            word+=m

    return word

def letter_count(letter, phrase):
    let=0
    for x in phrase:
        if x == letter:
            let+=1
    return let

###############################################################
####################### write VOWEL_COST ######################
###############################################################

def buyvowel(player):
    player.subtractMoney(VOWEL_COST)
    return player.prizeMoney


def playround():
    for play in playGame:
        response= input('Play or Pass: ')
        if response=="Play":
            player.playGame()

# print('Random spin result:')
# wheelPrize = spinWheel()
# print(wheelPrize)
#
# category, phrase = getRandomCategoryAndPhrase()
# print('\nRandom Category: {}\nRandom Phrase:   {}'.format(category, phrase))
#
# # example code to illustrate how getMove works. You should delete this.
# comp_obscured_phrase = 'R___ ____AR'
# comp_obscured_category = 'Place'
#
# print('\n\nComputer guess for {} ({})'.format(comp_obscured_phrase, comp_obscured_category))
#
# computer_1 = wof_computer.WOFComputer(difficulty = random.randint(1,9))
# computerMove = computer_1.getMove(money=0, category=comp_obscured_category, obscuredPhrase = comp_obscured_phrase,
#                                     guessed=['P','N','X','R','A','Z','S'], wheelPrize=wheelPrize)
# print('Computer says: {}'.format(computerMove))

def playGame():
    players = [createPlayer(player_num>=NUM_HUMAN, player_num+1) for player_num in range(NUM_PLAYERS)]
    guessed = []
    category, phrase = getRandomCategoryAndPhrase()
    playerIndex = 0
    while True:
        player = players[playerIndex]


        wheelPrize = spinWheel()
        print("\n...{} spins...".format(player.name))

        if wheelPrize['type'] == 'cash':
            obscuredPhrase = obscurePhrase(phrase, guessed)
            print('\nGuessed: {}'.format(','.join(guessed)))
            print('\nCategory is {}: '.format(category))
            print(obscuredPhrase)

            if wheelPrize['prize']!= False:
                print('Spin: {} and {}'.format(wheelPrize['text'], wheelPrize['prize']))

            else:
                print('Spin: {}'.format(wheelPrize['text']))


            print(player)
            print('='*40)


            while True:

                guess= player.getMove(player.prizeMoney, category, obscuredPhrase, guessed, wheelPrize)



                if guess in guessed:
                    print("{} was already guessed. Guess again!".format(guess))
                    continue


                if guess.isalnum()==True and len(guess)==1:
                    if guess in VOWELS:
                        if player.prizeMoney>=250:
                            buyvowel(player)
                            print("{} bought a vowel for $250".format(player.name))


                        else:
                            print("Not enough money to buy a vowel. Guess again.")
                            continue


                    num_inst=0
                    if len(guess)==1:
                        for char in phrase:
                            if guess ==char:
                                num_inst+=1

                    if player.computer == False:

                        if num_inst==0:
                            print("...There are 0 {}'s\n".format(guess))
                        elif num_inst==1:
                            print("...There is 1 {}\n".format(guess))
                        else:
                            print("...There are {} {}'s\n".format(num_inst, guess))
                    else:
                        print("{} guesses {}".format(player.name, guess))

                        if num_inst==0:
                            print("...There are 0 {}'s\n".format(guess))
                        elif num_inst==1:
                            print("...There is 1 {}\n".format(guess))
                        else:
                            print("...There are {} {}'s\n".format(num_inst, guess))




                    if guess in phrase:
                        if wheelPrize['type']=='cash':
                            player.addMoney(wheelPrize['value']* letter_count(guess, phrase))
                        if wheelPrize["prize"]!=False:
                            player.addPrize(wheelPrize['prize'])
                        guessed.append(guess)

                        if completephrase(guessed, phrase)==True:
                            print("Correct! The phrase was {}".format(phrase))
                            if player.prizes==[]:
                                print("Congratulations! {} wins ${}".format(player.name, player.prizeMoney))
                            else:
                                print("Congratulations! {} wins ${} and {}".format(player.name, player.prizeMoney, ','.join(player.prizes)))
                            return None

                        print ('{} was in the phrase! Guess again!'.format(guess))

                        print('\nGuessed: {}'.format(','.join(guessed)))
                        print('\nCategory is {}: '.format(category))
                        obscuredPhrase=obscurePhrase(phrase, guessed)
                        print(obscuredPhrase)

                        wheelPrize = spinWheel()
                        if wheelPrize['type']=='cash':

                            print("\n...{} spins...".format(player.name))
                            if wheelPrize['prize']!= False:
                                print('Spin: {} and {}'.format(wheelPrize['text'], wheelPrize['prize']))

                            else:
                                print('Spin: {}'.format(wheelPrize['text']))

                            print(player)
                            print('='*40)
                            continue
                        elif wheelPrize['type'] == 'bankrupt': #bankrupt
                            print ('\n{} has gone Bankrupt!'.format(player.name))
                            player.goBankrupt()
                            #print ('='*40)
                            pass

                        elif wheelPrize['type'] == 'loseturn':
                            print ('\n{} Lost a turn!'.format(player.name))
                            player.addMoney(0)
                            #print ('='*40)
                            pass



                    guessed.append(guess)
                    break

                if guess.isalnum()==False and len(guess)==1:
                    print("guess is invalid")
                    print("Guess again")
                    continue


                elif len(guess)>1:
                    if guess == phrase:
                        player.addMoney(wheelPrize['value'])
                        if wheelPrize["prize"]!=False:
                            player.addPrize(wheelPrize['prize'])

                        print("{} guessed {}".format(player.name, guess))
                        print("Correct! Phrase was {}".format(guess))
                        if player.prizes==[]:
                            print("Congratulations! {} wins ${}".format(player.name, player.prizeMoney))
                        else:
                            print("Congratulations, {} wins ${} and {}".format(player.name, player.prizeMoney, ','.join(player.prizes)))
                        return None
                    elif guess=="PASS":
                        print("{} passed their turn".format(player.name))
                        break
                    else:
                        print("Phrase {} is incorrect".format(guess))
                        break
                elif guess.isalnum() ==False and len(guess)==1:
                    print('Your guess {} was invalid. Guess again.'.format(guess))
                    continue




        elif wheelPrize['type'] == 'bankrupt': #bankrupt
            print ('\n{} has gone Bankrupt!\n'.format(player.name))
            player.goBankrupt()
            print ('='*40)
            pass

        elif wheelPrize['type'] == 'loseturn':
            print ('\n{} Lost a turn!\n'.format(player.name))
            print ('='*40)
            pass


        playerIndex += 1
        playerIndex = playerIndex%len(players)

playGame()
