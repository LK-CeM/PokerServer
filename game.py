import random
import math

class Card:
    rank = 2 
    color = 0 
    def __init__(self, rank, color):
        self.rank = rank;
        self.color = color;
    def __str__(self):
        ranks = ["2","3","4","5","6","7","8","9","10","B","Q","K","A"]
        colors = ["H","T","C","P"]
        return ranks[self.rank-2] + "-" + colors[self.color]
    
    
class Deck:
    cards = []
    size = 0
    def __init__(self):
        for i in range (2, 15):
            for j in range (0,4):
                self.cards.append(Card(i,j));
                self.size += 1;
        

    def draw(self, amount):
        if amount < 1:
            return None
        if amount == 1:
            ret = self.cards.pop()
            return ret
            
        else:
            drawn_cards = []
            while (amount >= 1):
                drawn_cards.append(self.cards.pop())
                amount -= 1
            return drawn_cards

    def __str__(self):
        ret = ""
        for card in self.cards:
            ret += card.__str__() + " "
        return ret
    

class Dealer:
    deck = None
    faceUpCards = []
    def __init__(self):
        self.shuffel()

    def deal_hand(self):
        return self.deck.draw(2)
    
    def deal_flop(self):
        self.faceUpCards = self.deck.draw(3)

    def deal_turn(self):
        self.faceUpCards.append(self.deck.draw(1))
    
    def deal_river(self):
        self.faceUpCards.append(self.deck.draw(1))
    
    def shuffel(self):
        self.deck = Deck()
        random.shuffle(self.deck.cards)
        

        

class Player:
    socket = None
    hand = []
    money = 100

def wait_for_players():
    #open soket connection 2 players
    #return player
    return [Player(),Player()]


def poker (p1,p2):
    p1_is_big_blind = False
    dealer = Dealer()
    gamestate = [p1,p2,p1_is_big_blind]
    p1.hand = dealer.deal_hand()
    p2.hand = dealer.deal_hand()

    print(dealer.deck)
    print(p1.hand[0],p1.hand[1])
    print(p2.hand[0],p2.hand[1])
    return
    while (gamestate[0].money > 0 and gamestate[1].money > 0):
        p1.hand = dealer.deal_hand()
        p2.hand = dealer.deal_hand()
        gamestate = dealer.wait_for_player_action(gamestate)
        dealer.deal_flop()
        gamestate = dealer.wait_for_player_action(gamestate)
        dealer.deal_turn()
        gamestate = dealer.wait_for_player_action(gamestate)
        dealer.deal_river()
        gamestate = dealer.wait_for_player_action(gamestate)
        gamestate[-1] = not gamestate[-1];
        dealer.shuffel();
    
    print(dealer.deck)
    
    

def main():
    p1,p2 = wait_for_players();
    poker(p1,p2);

main()
