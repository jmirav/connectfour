from enum import Enum


class Action(Enum):
    """An action that occurs in the game.

    These are the actions that the model publishes and which the views
    may subscribe to.
    """
    player_added = 0
    round_started = 1
    next_player = 2
    try_again = 3
    disc_played = 4
    round_won = 5
    round_draw = 6


# Master dictionary to store all subscribed callbacks, keyed on Action
subscriptions = {}


def subscribe(action, callback):
    """Subscribe so that callback is called when action occurs."""
    if action not in subscriptions:
        subscriptions[action] = []

    subscriptions[action].append(callback)


def publish(action, *args, **kwargs):
    """Publish that an action occurred.

    Any *args and **kwargs are passed along to all subscribed
    callbacks for this action.
    """
    if action not in subscriptions:
        return

    for callback in subscriptions[action]:
        callback(*args, **kwargs)
