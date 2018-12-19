# -*- coding:utf-8 -*-
import itertools
import random
from functools import reduce
from collections import defaultdict

# team ratings
COUNTRY_18 = {
    5.0: ['Brazil', 'Italy', 'Spain', 'France', 'Germany', 'Argentina', 'Portugal', 'Belgium'], 
    4.5: ['England', 'Uruguay', 'Netherlands', 'Colombia'], 
    4.0: ['Turkey', 'Denmark', 'Russia', 'Mexico', 'Greece', 'Switzerland', 'Sweden', 'Republic of Ireland', 'United States', 'Poland', 'Scotland', 'Austria', 'Wales', 'Slovenia', "Côte d'Ivoire", 'Chile'], 
    3.5: ['Cameroon', 'Australia', 'Norway', 'Paraguay', 'Romania', 'Ecuador', 'Northern Ireland', 'Hungary', 'Czech Republic', 'South Africa', 'Peru', 'Egypt', 'Venezuela', 'Saudi Arabia', 'Iceland'], 
    3.0: ['Bulgaria', 'Finland', 'China PR'], 
    2.5: ['New Zealand', 'Bolivia', 'Canada'], 
    1.0: ['India']
}
COUNTRY_19 = {
    5.0: ['Italy', 'Spain', 'France', 'Germany', 'Belgium'],
    4.5: ['Brazil', 'England', 'Argentina', 'Portugal', 'Uruguay', 'Croatia', 'Netherlands'], 
    4.0: ['Turkey', 'Nigeria', 'Denmark', 'Russia', 'Mexico', 'Greece', 'Cameroon', 'Serbia', 'Switzerland', 'Sweden', 'Norway', 'Poland', 'Scotland', 'Austria', 'Wales', 'Slovenia', 'Czech Republic', "Côte d'Ivoire", 'Chile', 'Colombia', 'Morocco', 'Senegal', 'Japan'], 
    3.5: ['Australia', 'Republic of Ireland', 'Korea Republic', 'United States', 'Paraguay', 'Romania', 'Ecuador', 'Tunisia', 'Northern Ireland', 'Hungary', 'South Africa', 'Peru', 'Egypt', 'Venezuela', 'Saudi Arabia', 'Iceland', 'Iran', 'Costa Rica'], 
    3.0: ['Finland', 'China PR', 'Canada', 'Panama'],
    2.5: ['Bulgaria', 'Bolivia'], 
    2.0: ['New Zealand'], 
    1.0: ['India']
}
LEAGUE = {
    5.0: ['Man United', 'Man City', 'Chelsea', 'Atlético Madrid', 'PSG', 'Juventus', 'Dortmund', 'Real Madrid', 'Barcelona', 'Bayern'],
    4.5: ['Arsenal', 'Everton', 'Liverpool', 'Spurs', 'AS Monaco', 'Real Sociedad', 'Valencia CF', 'Fiorentina', 'Milan', 'Napoli', 'Inter', 'Lazio', 'Roma', 'FC Porto', 'SL Benfica', 'Zenit', 'CSKA', 'Bayer 04', 'FC Shalke 04', 'VfL Wolfsburg', 'Newcastle United', 'Galatasaray'],
    4.0: ['West Ham', 'Stoke City', 'Southhampton', 'Norwich City', 'Sevilla', 'Real Betis', 'Lyon', 'Lille', 'Udinese', 'Ajax', 'Saint-Etienne', 'Sporting CP', 'Spartak', '1899 Hoffenheim', 'Borussia Monchengladbach', 'Hamburger SV', 'Hannover 96', 'VfB Stuttgart', 'Sao Paulo', 'Levante UD', 'Minerio', 'Cruzeiro', 'Shaktar', 'Torino', 'Marseille', 'Atlanta', 'Stade Rennais', 'Genoa', 'Parma', 'Sunderland', 'West Brom', 'West Ham', 'Swansea City', 'Aston Villa', 'PSV', 'Lokomotiv', 'Montpellier HSC', 'Dinamo Moskva', 'Getafe', 'Malaga', 'Atletic Bilbao', 'Frankfurt', 'QPR', 'Olympiakos']
}


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [0] * 5  # starting hand is 5 stars
        self.deck = []
        self.discard = []

    def star(self):
        return float(sum([v == 0 for v in self.hand]))

    def score(self):
        return sum(self.hand + self.deck + self.discard)

    def gain_and_draw(self, value=None):
        """
        Gain a value and redraw hand

        :param value: either a star (0) or a score e.g. (1, 3, 6)
        """
        if value is not None:
            self.hand.append(value)  # gain a value
        self.discard += self.hand
        if len(self.deck) < 5:  # need to reshuffle discard pile into deck
            random.shuffle(self.discard)
            self.deck += self.discard
            self.discard = []
        self.hand = self.deck[:5]  # draw 5 cards from deck
        self.deck = self.deck[5:]  # remove 5 cards
        if self.star() == 0:  # no star, gain a curse :)
            print(f'{self.name} gains a curse!')
            self.gain_and_draw(-1)

    def print_state(self):
        print(f'{self.name}: Score:{self.score()} Hand:{self.hand} Deck:{self.deck} Discard:{self.discard}')


def all_partitions(a, b):
    """
    Generate all possible binary partitions of [0, 1, ..., a+b-1] of size a and b
    """
    population = set(range(a + b))
    result = []
    for item in itertools.combinations(population, a):
        pairs = (item, tuple(population-set(item)))
        if pairs not in result and pairs[::-1] not in result:
            result.append(pairs)
    return result

def init():
    pool = defaultdict(list)
    for k, v in itertools.chain(COUNTRY_18.items(), LEAGUE.items()):
        pool[k] += v
    return pool

def gd_to_score(gd):
    gd = abs(gd)
    if gd == 1:
        return 1
    elif gd == 2:
        return 3
    elif gd >= 3:
        return 6

def play(pool):
    player_input = input('Player Names (space separated): ')
    players = [Player(name) for name in player_input.split(' ')]
    n_players = len(players)
    game_round = 1
    while True:
        mode = input(f'Round {game_round}! Which mode? (2v2, 1v3, etc.): ')
        matching_indices = all_partitions(*map(int, mode.split('v')))
        for team_index in matching_indices:
            total_players_this_turn = sum([len(_) for _ in team_index])
            for player_this_turn in itertools.combinations(players, total_players_this_turn):
                for p in players:
                    p.print_state()
                team1 = [player_this_turn[index] for index in team_index[0]]
                team2 = [player_this_turn[index] for index in team_index[1]]
                star_team1 = reduce(lambda x, y: x + y, [p.star() for p in team1]) / len(team1)
                star_team2 = reduce(lambda x, y: x + y, [p.star() for p in team2]) / len(team2)
                name_team1 = ','.join([p.name for p in team1])
                name_team2 = ','.join([p.name for p in team2])
                print(name_team1 + ' (' + str(star_team1) + ' star) vs. ' + name_team2 + ' (' + str(star_team2) + ' star)')
                selected = False
                while not selected:
                    selected1 = 'null' if star_team1 not in pool else random.choice(pool[star_team1])
                    selected2 = 'null' if star_team2 not in pool else random.choice(pool[star_team2])
                    response = input(f'selected teams: {selected1} vs. {selected2}, ok? (y/n) ')
                    if response != 'n':
                        selected = True
                score_team1, score_team2 = map(int, input(f'Play the game! Final score (space separated): ').split(' '))
                gd = score_team1 - score_team2
                if gd > 0:  # team 1 win
                    winner_team, loser_team = team1, team2
                elif gd < 0:  # team 2 win
                    winner_team, loser_team = team2, team1
                else:  # draw
                    continue
                for p in winner_team:
                    p.gain_and_draw(gd_to_score(gd))
                for p in loser_team:
                    p.gain_and_draw(0)

        game_round += 1


if __name__ == "__main__":
    pool = init()
    play(pool)
