from requests import get
from requests.exceptions import RequestException
from contextlib2 import closing
from bs4 import BeautifulSoup
import operator

from Player import Player


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def sort_dict(dict):
    sorted_dict = sorted(dict.items(), key = operator.itemgetter(1), reverse = True)
    return sorted_dict



class Scraper:

    def __init__(self):
        self.player_list = []
        url = "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html"
        page = self.simple_get(url)
        soup = BeautifulSoup(page, 'html.parser')

        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        headers = headers[1:]

        rows = soup.findAll('tr')[1:]
        stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

        for player in stats:
            if player:
                p_name = player[0]
                p_position = player[1]
                p_age = player[2]
                p_team = player[3]
                p_games = player[4]
                p_games_started = player[5]
                p_minutes_played = player[6]
                p_field_goals = player[7]
                p_field_goal_attempts = player[8]
                p_field_goal_percentage = player[9]
                p_three_pointers = player[10]
                p_three_point_attempts = player[11]
                p_three_point_percentage = player[12]
                p_free_throws = player[17]
                p_free_throw_attempts = player[18]
                p_free_throw_percentage = player[19]
                p_offensive_rebounds = player[20]
                p_defensive_rebounds = player[21]
                p_total_rebounds = player[22]
                p_assists = player[23]
                p_steals = player[24]
                p_blocks = player[25]
                p_turn_overs = player[26]
                p_personal_fouls = player[27]
                p_points = player[28]

                new_player = Player(p_name,
                                    p_position,
                                    p_age,
                                    p_team,
                                    p_games,
                                    p_games_started,
                                    p_minutes_played,
                                    p_field_goals,
                                    p_field_goal_attempts,
                                    p_field_goal_percentage,
                                    p_three_pointers,
                                    p_three_point_attempts,
                                    p_three_point_percentage,
                                    p_free_throws,
                                    p_free_throw_attempts,
                                    p_free_throw_percentage,
                                    p_offensive_rebounds,
                                    p_defensive_rebounds,
                                    p_total_rebounds,
                                    p_assists,
                                    p_steals,
                                    p_blocks,
                                    p_turn_overs,
                                    p_personal_fouls,
                                    p_points,)

                self.player_list.append(new_player)

    def simple_get(self, url):
        try:
            with closing(get(url, stream=True)) as resp:
                if is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            print('Error during request to {0} : {1}'.format(url, str(e)))
            return None

    def find_player_by_name(self, name):
        result = []
        if self.player_list:
            for player in self.player_list:
                comparing_name: str = player.get_name().strip('r\'(,)r\'')
                if comparing_name == name:
                    result.append(player)
            return result

    def sort_by_points(self, *argv):
        result = {}
        if argv:
            # search by position
            for arg in argv:
                for player in self.player_list:
                    if(player.get_position().strip('r\'(,)r\'') == arg):
                        player_points: float = float(player.get_points())
                        result.update({player: player_points})
        else:
            for player in self.player_list:
                player_points: float = float(player.get_points())
                result.update({player: player_points})
        ret = sort_dict(result)
        return ret

    def sort_by_assists(self, *argv):
        result = {}
        if argv:
            # search by position
            for arg in argv:
                for player in self.player_list:
                    if(player.get_position().strip('r\'(,)r\'') == arg):
                        player_assists: float = float(player.get_assists())
                        result.update({player: player_assists})
        else:
            for player in self.player_list:
                player_assists: float = float(player.get_assists())
                result.update({player: player_assists})
        ret = sort_dict(result)
        return ret

    def sort_by_rebounds(self, *argv):
        result = {}
        if argv:
            # search by position
            for arg in argv:
                for player in self.player_list:
                    if (player.get_position().strip('r\'(,)r\'') == arg):
                        player_rebounds: float = float(player.get_total_rebounds())
                        result.update({player: player_rebounds})
        else:
            for player in self.player_list:
                player_rebounds: float = float(player.get_total_rebounds())
                result.update({player: player_rebounds})
        ret = sort_dict(result)
        return ret
