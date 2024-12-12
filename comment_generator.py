# def generate_comment(game_situation):
#     comments = []
#
#     # Assuming game_situation is a list of events
#     for event in game_situation:
#         if isinstance(event, dict):
#             # Generate comment based on event type
#             if 'goal' in event:
#                 comment = f"What a fantastic goal by {event.get('player', 'an unknown player')}!"
#             elif 'foul' in event:
#                 comment = f"Foul! A player has committed a foul against {event.get('opponent', 'an unknown opponent')}."
#             # Add more event-based comments here
#             comments.append(comment)
#         else:
#             comments.append("Event data is not in the expected format.")
#
#     return comments
#
def generate_comment(event):
    """
    Generates a comment based on the game event.
    """
    comments = {
        "goal": "What a fantastic goal!",
        "penalty": "A penalty kick is coming up!",
        "assist": "An amazing assist!",
        "whistle": "The game is paused!",
        "applause": "The crowd is going wild!"
    }
    return comments.get(event["type"], "An exciting moment in the game!")
