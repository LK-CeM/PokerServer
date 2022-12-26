import random
import requests
import json
import time



class Card:
    rank = 2 
    color = 0 

    def __init__(self, rank, color):
        self.rank = rank;
        self.color = color;

    def __str__(self):
        ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        colors = ["D","C","H","S"]
        return ranks[self.rank-2] + colors[self.color]
    
    def __repr__(self):
        return str(self)
class Player:
    socket = None
    hand = Card(2,3),Card(3,3)
    money = 100

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
      return str(self.cards)

    
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

    def wait_for_player_action(self, gamestate):
        #do stuff and communicate 2 players
        pass

def wait_for_players():
    #open soket connection 2 players
    #return player
    return [Player(),Player()]
    
class Gamestate:
    p1 = Player()
    p2 = Player()
    p1_is_big_blind = False
      
    def __init__(self, p1,p2):
        self.p1 = p1
        self.p2 = p2
    
    def has_no_winner(self):
        if (self.p1.money == 0 or self.p2.money == 0):
            return False
        return True
            
    def royal_flush(hand):
        return False 
    
    def flush(self, hand):
        hand.sort(key = lambda c: c.color)
        same_color_max = 0
        same_color_c = 0
        color = hand[0].color

        for i in range (6):
            if (hand[i].color == hand[i+1].color):
                same_color_c += 1
            else:
                if (same_color_max < same_color_c):
                    same_color_max = same_color_c
                same_color_c = 0
        if (same_color_c == 4 or same_color_max == 4):
            return True
        return False 
        
    
    def four_of_a_kind(self, hand):
        hand.sort(key = lambda c: c.rank)
        same_rank_max = 0
        same_rank_c = 0
        rank = hand[0].rank

        for i in range (6):
            if (hand[i].rank == hand[i+1].rank):
                same_rank_c += 1
            else:
                if (same_rank_max < same_rank_c):
                    same_rank_max = same_rank_c
                same_rank_c = 0
        if (same_rank_c == 3 or same_rank_max == 3):
            return True
        return False 

    def tree_of_a_kind(self, hand):
        hand.sort(key = lambda c: c.rank)
        same_rank_max = 0
        same_rank_c = 0
        rank = hand[0].rank

        for i in range (6):
            if (hand[i].rank == hand[i+1].rank):
                same_rank_c += 1
            else:
                if (same_rank_max < same_rank_c):
                    same_rank_max = same_rank_c
                same_rank_c = 0
        if (same_rank_c == 2 or same_rank_max == 2):
            return True
        return False 
    
    def pair(self, hand):
        hand.sort(key = lambda c: c.rank)
        same_rank_max = 0
        same_rank_c = 0
        rank = hand[0].rank

        for i in range (6):
            if (hand[i].rank == hand[i+1].rank):
                same_rank_c += 1
            else:
                if (same_rank_max < same_rank_c):
                    same_rank_max = same_rank_c
                same_rank_c = 0
        if (same_rank_c == 1 or same_rank_max == 1):
            return True
        return False

    def two_pair(self, hand):
        hand.sort(key = lambda c: c.rank)
        same_rank_max = 0
        same_rank_c = 0
        rank = hand[0].rank
        first_pair = False
        ranked_changed = False

        for i in range (6):
            if (hand[i].rank == hand[i+1].rank):
                same_rank_c += 1
                if (same_rank_c >= 1):
                    first_pair = True
                if (ranked_changed):
                    return True
            else:
                if (first_pair):
                    ranked_changed = True
        return False
    
    def straight(self, hand):
        hand.sort(key = lambda c: c.rank)
        seq_rank_max = 0
        seq_rank_c = 0
        rank = hand[0].rank

        for i in range (6):
            if (hand[i].rank == hand[i+1].rank + 1):
                seq_rank_c += 1
            else:
                if (seq_rank_max < seq_rank_c):
                    seq_rank_max = seq_rank_c
                seq_rank_c = 0
        if (seq_rank_c >= 4 or seq_rank_max >= 4):
            return True
        return False 
    
    def high_card(self, hand):
        hand.sort(key = lambda c: c.rank)
        return hand[-1]
    
    def rank_hand(self, hand):
        score = 0
        high_card = self.high_card(hand)
        score = high_card.rank
        if self.pair(hand):
            score = 100
        if self.two_pair(hand):
            score = 200
        if self.tree_of_a_kind(hand):
            score = 300
        if self.straight(hand):
            score = 400
        if self.flush(hand):
            score = 500
        # self.fullhouse

        if self.four_of_a_kind(hand):
            score = 600
        #straightFlush
        #royalFlush
        return score
    
    def winning_hand(self, faceupCards, h1, h2):
        pool1 = h1.copy()
        pool2 = h2.copy()
        for card in faceupCards:
            pool1.append(card)
            pool2.append(card)
        s1 = self.rank_hand(pool1)
        s2 = self.rank_hand(pool2)
        if (s1 < s2):
            return (h2),s2,h1,s1,faceupCards
        else:
            return (h1),s1,h2,s2,faceupCards

    




def poker (p1,p2):
    dealer = Dealer()
    p1.hand = dealer.deal_hand()
    p2.hand = dealer.deal_hand()
    gamestate = Gamestate(p1, p2)
    dealer.deal_flop()
    dealer.deal_turn()
    dealer.deal_river()
    return gamestate.winning_hand(dealer.faceUpCards, p1.hand, p2.hand)
    

    while (gamestate.has_no_winner()):
        p1.hand = dealer.deal_hand()
        p2.hand = dealer.deal_hand()
        gamestate = Gamestate(p1, p2)
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
    

def api_shit(h1,h2,FU):
    url = 'https://api.pokerapi.dev/v1/winner/texas_holdem?cc=AC,KD,QH,JS,7C&pc[]=10S,8C&pc[]=3S,2C'
    url = 'https://api.pokerapi.dev/v1/winner/texas_holdem?cc=' + str(FU[0]) + ','+ str(FU[1]) + ','+ str(FU[2]) + ','+ str(FU[3]) + ','+ str(FU[4])
    url += '&pc[]=' + str(h1[0]) + ','+ str(h1[1])
    url += '&pc[]=' + str(h2[0]) + ','+ str(h2[1])
    response = requests.get(url = url)
    data = response.json()
    json_formatted_str = json.dumps(data, indent=2)
    text_file = open("data.txt", "a")
    text_file.write(json_formatted_str)
    text_file.close()
    if 'winners' in response.json():
        data = response.json()["winners"][0]["cards"]
    else:
        data = "no winna"
    print(str(data))
    return str(data)

def main():
    p1,p2 = wait_for_players();
    logs = open("log.txt", "w")
    logs.write("Yes\n")
    logs.close()
    logs = open("log.txt", "a")
    correct = 0
    fail = 0
    testcounter = 10
    for _ in range(testcounter):
        time.sleep(1)
        hand1,score1,hand2,score2,faceupCards = poker(p1,p2);
        
        my_ret = str(hand1[0])+","+ str(hand1[1])
        faceupCards.sort(key = lambda c: c.rank, reverse= True)
        print(hand1, score1,hand2,score2, faceupCards)
        api_ret = api_shit(hand1,hand2,faceupCards)
        if (my_ret == api_ret):
            print("vibin... ")
            correct +=1
        else:
            if (api_ret =="no winna"):
                fail +=1
            print("incorrect")
            print(my_ret, api_ret)
    print(correct/(testcounter-fail)*100, " Prozent der Loesungen waren richtig, nice")

main()


