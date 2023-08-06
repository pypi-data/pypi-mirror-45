class Player(object):

    def __init__(self,
                 name,
                 position,
                 age,
                 team,
                 games,
                 games_started,
                 minutes_played,
                 field_goals,
                 field_goal_attempts,
                 field_goal_percentage,
                 three_pointers,
                 three_pointer_attempts,
                 three_pointer_percentage,
                 free_throws,
                 free_throw_attempts,
                 free_throw_percentage,
                 offensive_rebounds,
                 defensive_rebounds,
                 total_rebounds,
                 assists,
                 steals,
                 blocks,
                 turn_overs,
                 personal_fouls,
                 points,):
        self._name = name,
        self._position = position,
        self._age = age,
        self._team = team,
        self._games = games,
        self._games_started = games_started
        self._minutes_played = minutes_played
        self._field_goals = field_goals
        self._field_goal_attempts = field_goal_attempts
        self._field_goal_percentage = field_goal_percentage
        self._three_pointers = three_pointers
        self._three_pointer_attempts = three_pointer_attempts
        self._three_pointer_percentage = three_pointer_percentage
        self._free_throws = free_throws
        self._free_throw_attempts = free_throw_attempts
        self._free_throw_percentage = free_throw_percentage
        self._offensive_rebounds = offensive_rebounds
        self._defensive_rebounds = defensive_rebounds
        self._total_rebounds = total_rebounds
        self._assists = assists
        self._steals = steals
        self._blocks = blocks
        self._turn_overs = turn_overs
        self._personal_fouls = personal_fouls
        self._points = points

    def __repr__(self):
        return "Player: {0}\nPosition: {1}\nTeam: {2}\n".format(str(self._name).strip('r\'(,)r\''), str(self._position).strip('r\'(,)r\''), str(self._team).strip('r\'(,)r\''))

    def __str__(self):
        return self.__repr__()

    def get_name(self):
        return str(self._name)

    def get_position(self):
        return str(self._position)

    def get_age(self):
        return str(self._age)

    def get_team(self):
        return str(self._team)

    def get_games(self):
        return str(self._games)

    def get_games_started(self):
        return str(self._games_started)

    def get_minutes_played(self):
        return str(self._minutes_played)

    def get_field_goals(self):
        return str(self._field_goals)

    def get_field_goal_attempts(self):
        return str(self._field_goal_attempts)

    def get_field_goal_percentage(self):
        return str(self._field_goal_percentage)

    def get_three_pointers(self):
        return str(self._three_pointers)

    def get_three_pointer_attempts(self):
        return str(self._three_pointer_attempts)

    def get_three_pointer_percentage(self):
        return str(self._three_pointer_percentage)

    def get_free_throws(self):
        return str(self._free_throws)

    def get_free_throw_attempts(self):
        return str(self._free_throw_attempts)

    def get_free_throw_percentage(self):
        return str(self._free_throw_percentage)

    def get_offensive_rebounds(self):
        return str(self._offensive_rebounds)

    def get_defensive_rebounds(self):
        return str(self._defensive_rebounds)

    def get_total_rebounds(self):
        return str(self._total_rebounds)

    def get_assists(self):
        return str(self._assists)

    def get_steals(self):
        return str(self._steals)

    def get_blocks(self):
        return str(self._blocks)

    def get_turn_overs(self):
        return str(self._turn_overs)

    def get_personal_fouls(self):
        return str(self._personal_fouls)

    def get_points(self):
        return str(self._points)
