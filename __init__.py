from otree.api import *
import random

class Constants(BaseConstants):
    name_in_url = 'hidden_ball_random'
    players_per_group = 3
    num_rounds = 1
    num_balls = 10

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    selected_player_id = models.IntegerField()  # Store the randomly selected player's ID
    sender_reported_number = models.IntegerField() 

class Player(BasePlayer):
    numbers = models.StringField()  # Store the random numbers
    observed_number = models.IntegerField(initial=0)
    reported_number = models.IntegerField(
        min=1,
        max=10,
        label="Enter your report (number between 1 and 10):",
        blank=True
    )
    clicked_ball_index = models.IntegerField(initial=-1)
    points_earned = models.FloatField(initial=0)  # Optional, for intermediate calculations
    player_role = models.StringField()  # Used for role assignment (Sender/Receiver)


def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=True)
    for player in subsession.get_players():
        numbers = list(range(1, Constants.num_balls + 1))
        random.shuffle(numbers)
        player.numbers = ','.join(map(str, numbers))

# PAGES
class Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'num_balls': Constants.num_balls,
            'players_per_group': Constants.players_per_group
        }

class BallGame(Page):
    form_model = 'player'
    form_fields = ['reported_number']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'ball_numbers': range(Constants.num_balls)
        }

    @staticmethod
    def live_method(player: Player, data):
        if 'clicked_index' in data:
            index = int(data['clicked_index'])
            numbers = [int(x) for x in player.numbers.split(',')]
            number = numbers[index]
            player.observed_number = number
            player.clicked_ball_index = index
            return {player.id_in_group: {'index': index, 'number': number}}
        return {player.id_in_group: {}}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.reported_number is not None:
            player.points_earned = player.reported_number

class RoleAssignment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        all_players = group.get_players()
        sender = next(p for p in all_players if p.player_role == 'Sender')  # Updated to player_role
        receivers = [p for p in all_players if p.player_role == 'Receiver']  # Updated to player_role
        
        return {
            'sender_id': sender.id_in_group,
            'receiver_ids': [p.id_in_group for p in receivers],
            'player_role': player.player_role,  # Updated to player_role
        }

class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # Randomly select a player to act as Sender
        group.selected_player_id = random.choice([p.id_in_group for p in group.get_players()])
        
        # Identify Sender and Receivers
        sender = next(p for p in group.get_players() if p.id_in_group == group.selected_player_id)
        receivers = [p for p in group.get_players() if p.id_in_group != group.selected_player_id]
        
        # Assign roles to players
        for player in group.get_players():
            if player == sender:
                player.player_role = 'Sender'
            else:
                player.player_role = 'Receiver'
        
        group.sender_reported_number = sender.reported_number 

        # Sender payoff: based on their reported number
        sender.payoff = sender.reported_number
        
        # Receivers payoff: Based on the Sender's report
        for receiver in receivers:
            receiver.payoff = 11 - sender.reported_number


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        selected_player = next(p for p in group.get_players() if p.id_in_group == group.selected_player_id)
        other_players = [p for p in group.get_players() if p.id_in_group != group.selected_player_id]

        return {
            'selected_player': {
                'id': selected_player.id_in_group,
                'observed_number': selected_player.observed_number,
                'points_earned': selected_player.points_earned,
                'reported_number': selected_player.reported_number,  # Add reported_number here
            },
            'other_players': [{
                'id': p.id_in_group,
                'points_earned': 11 - selected_player.reported_number,
                
            } for p in other_players],
            'is_selected_player': player.id_in_group == group.selected_player_id,
            'player_role': player.player_role  # Updated to player_role
        }

page_sequence = [Instructions, BallGame, ResultsWaitPage, RoleAssignment, Results]