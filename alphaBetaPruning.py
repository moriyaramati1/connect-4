import copy

import game

DEPTH = 5


def go(s):
    if game.is_human_turn(s):
        return abmin(s, DEPTH, game.Status.LOSS - 1, game.Status.VICTORY + 1)[1]
    else:
        return abmax(s, DEPTH, game.Status.LOSS - 1, game.Status.VICTORY + 1)[1]


def abmax(s, d, a, b):
    """
    :param s: the state (max's turn)
    :param d: max. depth of search
    :param a: alpha
    :param b: beta
    :return: returns [v, ns]: v = state s's value. ns = the state after recommended move.
            if s is a terminal state ns=0.
    """
    if d == 0 or game.is_finished(s):
        return [game.value(s), 0]
    v = float("-inf")
    ns = game.get_next(s)
    best_move = 0
    for i in ns:
        tmp = abmin(copy.deepcopy(i), d - 1, a, b)
        if tmp[0] > v:
            v = tmp[0]
            best_move = i
        if v >= b:
            return [v, i]
        if v > a:
            a = v
    return [v, best_move]


def abmin(s, d, a, b):
    """
    :param s: the state (min's turn)
    :param d: max. depth of search
    :param a: alpha
    :param b: beta
    :return: [v, ns]: v = state s's value. ns = the state after recommended move.
             if s is a terminal state ns=0.
    """

    if d == 0 or game.is_finished(s):
        return [game.value(s), 0]
    v = float("inf")
    ns = game.get_next(s)
    best_move = 0
    for i in ns:
        tmp = abmax(copy.deepcopy(i), d - 1, a, b)
        if tmp[0] < v:
            v = tmp[0]
            best_move = i
        if v <= a:
            return [v, i]
        if v < b:
            b = v
    return [v, best_move]
