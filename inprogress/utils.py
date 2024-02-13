import time
import matplotlib.pyplot as plt
import IPython.display as display
import random
import numpy as np
from queue import PriorityQueue
from typing import List, Tuple

N_ARR = np.array([0, 1])
S_ARR = np.array([0, -1])
W_ARR = np.array([-1, 0])
E_ARR = np.array([1, 0])
NE_ARR = N_ARR + E_ARR
SE_ARR = S_ARR + E_ARR
SW_ARR = S_ARR + W_ARR
NW_ARR = N_ARR + W_ARR
MOVES = [N_ARR, E_ARR, S_ARR, W_ARR, NE_ARR, SE_ARR, SW_ARR, NW_ARR]

N = 0
E = 1
S = 2
W = 3
NE = 3 + N + E
SE = 2 + S + E
SW = 1 + S + W
NW = 4 + N + W
ACTIONS = [N, E, S, W, NE, SE, SW, NW]
DIAGONAL_ACTIONS = [NE, SE, SW, NW]

ACTION_NAMES = ['N', 'E', 'S', 'W', 'NE', 'SE', 'SW', 'NW']


def move_to_action(move: np.ndarray[int]) -> List[int]:
    if np.array_equal(move, N_ARR):
        return N
    elif np.array_equal(move, S_ARR):
        return S
    elif np.array_equal(move, W_ARR):
        return W
    elif np.array_equal(move, E_ARR):
        return E
    elif np.array_equal(move, NE_ARR):
        return NE
    elif np.array_equal(move, SE_ARR):
        return SE
    elif np.array_equal(move, NW_ARR):
        return NW
    elif np.array_equal(move, SW_ARR):
        return SW


def action_to_move(action: int) -> np.ndarray[int]:
    if action == N:
        return N_ARR
    elif action == S:
        return S_ARR
    elif action == W:
        return W_ARR
    elif action == E:
        return E_ARR
    elif action == NE:
        return NE_ARR
    elif action == SE:
        return SE_ARR
    elif action == NW:
        return NW_ARR
    elif action == SW:
        return SW_ARR


def action_to_string(action: int) -> str:
    return ACTION_NAMES[action]


def show_episode(states: dict, clear_output: bool = True) -> None:
    image = plt.imshow(states[0]['pixel'][100:300, 500:750])
    for state in states[1:]:
        display.display(plt.gcf())
        if clear_output:
            display.clear_output(wait=True)
        image.set_data(np.array(state['pixel'])[100:300, 500:750])
        time.sleep(0.3)


def allowed_moves(width: int, height: int, agent_coord: Tuple[int, int], to_avoid: Tuple[int, int] = None) -> List[np.ndarray[int]]:
    x, y = agent_coord
    n = 0b1000
    s = 0b0100
    w = 0b0010
    e = 0b0001
    b = 0b0000
    nw = n | w
    ne = n | e
    sw = s | w
    se = s | e
    moves = []
    if x-1 >= 0:
        b |= w
        moves.append(W_ARR)
    if x+1 < height:
        b |= e
        moves.append(E_ARR)
    if y-1 >= 0:
        b |= s
        moves.append(S_ARR)
    if y+1 < width:
        b |= n
        moves.append(N_ARR)
    if b & (n | w) == nw:
        moves.append(NW_ARR)
    if b & (n | e) == ne:
        moves.append(NE_ARR)
    if b & (s | w) == sw:
        moves.append(SW_ARR)
    if b & (s | e) == se:
        moves.append(SE_ARR)
    moves = [m for m in moves if tuple(np.array(agent_coord) + m) != to_avoid]

    return moves


def is_composite(move: np.ndarray[int]) -> bool:
    for m in MOVES:
        if np.array_equal(move, m):
            return False
    return True