# Using python 2.7.10
import csv
from operator import itemgetter

def build_soccer_league():

    #create list of players
    players = get_players_from_file('soccer_players.csv')

    league = []
    teams = [
        {'name': 'sharks', 'attributes': {'experienced_players': 0, 'players': []}},
        {'name': 'dragons', 'attributes': {'experienced_players': 0, 'players': []}},
        {'name': 'raptors', 'attributes': {'experienced_players': 0, 'players': []}}
    ]

    #count total players
    total_players = len(players)
    #count total experienced players
    total_experienced_players = 0

    for player in players:
        if player['Soccer Experience'].lower() == "yes":
            total_experienced_players += 1

    #put players in height order
    sorted_players = sorted(players, key=itemgetter('Height (inches)'))

    #add players to team in order of height
    while len(sorted_players):
        for player in sorted_players:
            for team in teams:
                if len(team['attributes']['players']) < round(total_players / 3):
                    if player['Soccer Experience'].lower() == 'yes':
                        if team['attributes']['experienced_players'] >= round(total_experienced_players / 3):
                            #this team already has the maximum number of experienced players
                            #move on to the next team
                            continue
                        else:
                            team['attributes']['experienced_players'] += 1
                    add_player_to_team(player, team)
                    #delete the player from the list so they don't get added to another team
                    sorted_players.remove(player)
                    #move on to the next player
                    break
                else:
                    #this team was already full, move on to the next team
                    continue


    for team in teams:
        league.append([team['name'], team['attributes']['players']])

    return league


def add_player_to_team(player, team):

    team['attributes']['players'].append(player)

    return team

def get_players_from_file(file_name):

    with open(file_name) as file:
        csvlines = csv.DictReader(file)
        players = []
        for player in list(csvlines):
            players.append(player)

    return players

def write_letter(player, team):
    letter = '''\
Dear {guardians},

Your child, {name}, is on the {team} this year.
Their first team practice will be on August 1, 2016 at 5:30pm.
Please be sure to have {first_name} there on time.

Thank you,
Coach
'''.format(name=player['Name'], guardians=player['Guardian Name(s)'], team=team.capitalize(), first_name=player['Name'].split(' ')[0])
    filename = player['Name'].replace(' ', '_').lower() + '.txt'
    with open(filename, 'w') as file:
        file.write(letter)

def write_letters(league):
    for team, players in league:
        for player in players:
            write_letter(player, team)


if __name__ == '__main__':
    league = build_soccer_league()
    write_letters(league)

