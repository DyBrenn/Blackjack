import random
class deck:
    def __init__(self, funds = None):
        #initiallize deck class
        self._funds = funds if funds is not None else 0
        self._bet = 0
        self._cards = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
        self._suits = ['Diamond', 'Spade', 'Club', 'Heart']
        self._deck = []
        self._total = 0
        #creates a full deck of cards
        for i in self._cards:
            for j in self._suits:
                self._deck.append((j,i))
        self._hand = []
        self._dealer = []
        self._dealertot = 0

    def deal(self):
        #Always deals a random card from a full deck
        num = random.randint(0,51)
        card = self._deck[num]
        return card

    def changefunds(self, amount):
        self._funds += amount

    def showfunds(self):
        print(self._funds)
    
    def _clearhand(self):
        self._hand = []

class blackjack(deck):
    def __init__(self, funds = None):
        print('Use bj.bet() to bet money from your funds (bet will remain same if you don\'t change it in between rounds), use bj.start() to start a new game, bj.hit() to be given a card (always draws from a full deck), bj.hold() to hold onto your cards, bj.double() to double down (can only do this directly after bj.start (only have 2 cards). Can\'t hit after doubling down). To add funds use bj.changefunds(amount) and use bj.showfunds() to see your funds. Dealer must hit on 16. Enjoy and may the odds be ever random!')
        deck.__init__(self, funds)
        #Initialize blackjack class
        self._start = False
        #Tracks if ace has been used as 11 so if bust it can be changed to a 1 for both dealer and player
        self._ace = 0
        self._ace2 = 0
        #Tracks if player has doubled down
        self._double = False
        
    def bet(self, amount):
        #Bets constrained by 0<bet<=self._funds
        if amount > 0 and self._funds >= amount:
            self._bet = amount
        else:
            print("Please enter a positive amount to bet")

    def hit(self):
        #Ensures bj.start() was used to begin new game
        if self._start == True:
            initial = self._total
            i = self.deal()
            self._hand.append(i)
            #Handles face cards
            if i[1] in ['K', 'Q', 'J']:
                #Track hand value with self._total
                self._total += 10
            #Handles aces
            if i[1] == 'A':
                if self._total < 11:
                    self._total += 11
                    self._ace += 1
                else:
                    self._total += 1
            #Catches any non-face cards
            if isinstance(i[1], int):
                self._total += i[1]
            if initial == self._total:
                self._total += 10
            if self._total > 21:
                if self._ace > 0:
                    self._ace -= 1
                    self._total -= 10
                else:
                    self._funds -= self._bet
                    print("Oops, you busted. hand:",self._hand ,"total:", self._total)
                    self._start = False
            if self._total == 21:
                print("Blackjack! You win! hand:", self._hand, "total:", self._total)
                self._funds += self._bet
                self._start = False
            if self._start == True:
                print('Hand:', self._hand, ', total:', self._total)
        else:
            print("Please use .start() to begin a game.")
    def hold(self):
        if self._start == True:
            #dealer keeps track of dealer hand value
            self._dealertot += self._dealer[1]
            while self._dealertot < 17:
                num = self.deal()[1]
                if num in ['K', 'Q', 'J']:
                    self._dealertot += 10
                if num == 'A':
                    if self._dealertot < 11:
                        self._dealertot += 11
                        self._ace2 += 1
                    else:
                        self._dealertot += 1
                if isinstance(num, int):
                    self._dealertot += num
            #Handle who wins
            if self._dealertot > 21:
                if self._ace2 > 0:
                    self._ace2 -= 1
                    self._dealertot -= 10
                    self.hold()
                else:
                    print("You win, dealer busted! you:", self._total,'dealer:', self._dealertot)
                    if self._double:
                        self._funds += (2*self._bet)
                    else:
                        self._funds += self._bet
            else:
                if self._dealertot > self._total:
                    self._funds -= self._bet
                    print("Sorry, dealer's got you beat. you:", self._total,'dealer:', self._dealertot)
                    if self._double:
                    	self._funds -= 2*self._bet
                    else:
                    	self._funds -= self._bet
                if self._dealertot == self._total:
                    print("You push. you:", self._total,'dealer:', self._dealertot)
                if self._total > self._dealertot:
                    print("Winner, winner, chicken dinner! you:", self._total,'dealer:', self._dealertot)
                    if self._double:
                    	self._funds += 2*self._bet
                    else:
                    	self._funds += self._bet
            self._start = False
        else:
            print("Please use .start() to begin a game.")
    def start(self):
        #Initialize all variables clean states
        self._start = True
        self._total = 0
        self._hand = []
        self._dealer = []
        self._double = False
        self._dealertot = 0
        self._ace = 0
        self._ace2 = 0
        self._hand.append(self.deal())
        self._hand.append(self.deal())
        self._dealer.append(self.deal())
        for i in self._hand:
                if i[1] in ['K', 'Q', 'J']:
                    self._total += 10
                if i[1] == 'A':
                    if self._total < 11:
                        self._total += 11
                        self._ace += 1
                    else:
                        self._total += 1
                if isinstance(i[1], int):
                    self._total += i[1]
        for i in self._dealer:
                if i[1] in ['K', 'Q', 'J']:
                    self._dealer.append(10)
                if i[1] == 'A':
                    self._ace2 += 1
                    self._dealer.append(11)
                if isinstance(i[1], int):
                    self._dealer.append(i[1])
                break
        if self._total == 21:
            print("Blackjack! 2x winnings! hand:", self._hand,"total:", self._total)
            self._start = False
            self._funds += 2*self._bet
        else:
            print("Your hand is:", self._hand,'total:', self._total, '\n' 'dealers card:', self._dealer[0])

    def double(self):
        #Double your bet and draw once card
        if self._start == True and len(self._hand) == 2:
            #Used to pay or take double
            self._double = True
            card = self.deal()
            self._hand.append(card)
            if card[1] in ['K', 'Q', 'J']:
                self._total += 10
            if card[1] == 'A':
                if self._total < 11:
                    self._total += 11
                else:
                    self._total += 1
            if isinstance(card[1], int):
                self._total += card[1]
            if self._total > 21:
                print("Whoops, looks like you busted. total:", self._total)
                self._funds -= 2*self._bet
                self._start = False
            else:
                self.hold()

if __name__ == "__main__":
	cash = input("How much money would you like to start with? ")
	bj = blackjack(int(cash))
