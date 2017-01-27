#to-do: finish fixing bets and write comments
import random
class deck:
    def __init__(self, funds = None):
        self._funds = funds if funds is not None else 0
        self._bet = 0
        self._cards = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
        self._suits = ['Diamond', 'Spade', 'Club', 'Heart']
        self._deck = []
        self._total = 0
        for i in self._cards:
            for j in self._suits:
                self._deck.append((j,i))
        self._hand = []
        self._dealer = []

    def deal(self):
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
        print('Use .bet() to bet money from your funds (bet will remain same if you don\'t change it in between rounds), use .start() to start a game, .hit() to be given a card (always draws from a full deck), .hold() to hold onto your cards, .double() to double down (only do this after .start (2 cards) and you are given only 1 card and can no longer hit). To add funds use .changefunds(amount) and use .showfunds() to see your funds. Dealer must hit on 16. Enjoy!')
        deck.__init__(self, funds)
        self._start = False
        #Tracks if ace has been used as 11 so if bust it can be changed to a 1 for both dealer and player
        self._ace = 0
        self._ace2 = 0
        
    def bet(self, amount):
        if amount > 0 and self._funds >= amount:
            self._bet = amount
        else:
            print("Please enter a positive amount to bet")

    def hit(self):
        if self._start == True:
            i = self.deal()
            self._hand.append(i)
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
            if self._total > 21:
                if self._ace > 0:
                    self._ace -= 1
                    self._total -= 10
                else:
                    self._funds -= self._bet
                    print("Oops, you busted. hand:",self._hand ,"total:", self._total)
                    self._start = False
                    self._total = 0
                    self._hand = []
                    self._dealer = []
            if self._total == 21:
                print("Blackjack! 2x winnings! hand:", self._hand, "total:", self._total)
                self._funds += (2*self._bet)
                self._start = False
                self._total = 0
                self._hand = []
                self._dealer = []
            if self._start == True:
                print('Hand:', self._hand, ', total:', self._total)
        else:
            print("Please use .start() to begin a game.")
    def hold(self):
        if self._start == True:
            dealer = self._dealer[1]
            while dealer < 17:
                num = self.deal()[1]
                if num in ['K', 'Q', 'J']:
                    dealer += 10
                if num == 'A':
                    if dealer < 11:
                        dealer += 11
                        self._ace2 += 1
                    else:
                        dealer += 1
                if isinstance(num, int):
                    dealer += num
            if dealer > 21:
                if self._ace2 > 0:
                    self._ace2 -= 1
                    dealer -= 10
                else:
                    print("You win, dealer busted! you:", self._total,'dealer:', dealer)
                    self._funds += self._bet
                    self._bet = 0
            else:
                if dealer > self._total:
                    self._funds -= self._bet
                    print("Sorry, dealer's got you beat. you:", self._total,'dealer:', dealer)
                if dealer == self._total:
                    print("You push. you:", self._total,'dealer:', dealer)
                if self._total > dealer:
                    print("Winner, winner, chicken dinner! you:", self._total,'dealer:', dealer)
                    self._funds += self._bet
            self._start = False
            self._total = 0
            self._hand = []
            self._dealer = []
        else:
            print("Please use .start() to begin a game.")
    def start(self):
        self._start = True
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
            self._total = 0
            self._hand = []
            self._dealer = []
        else:
            print("Your hand is:", self._hand,'total:', self._total, '\n' 'dealers card:', self._dealer[0])

    def double(self):
        if self._start == True and len(self._hand) == 2:
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
                self._start = False
                self._total = 0
                self._hand = []
                self._dealer = []
            else:
                self.hold()
