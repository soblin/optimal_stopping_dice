#!/usr/bin/env python3

from copy import deepcopy
import numpy as np

class TrialNode:
    def __init__(self, index):
        self.index = index # the # of drawings so far
        self.opt_stop_index = -1 # when this trial stopped
        self.opt_stop_value = -1
        self.prob = 0.0
        self.nexts = []

def is_optimal(remaining, dice):
    if remaining == 1:
        return True

    if remaining == 2:
        if dice >= 4:
            return True
        else:
            return False

    if remaining == 3 or \
       remaining == 4 or \
       remaining == 5:
        if dice >= 5:
            return True
        else:
            return False

    if remaining >= 6:
        if dice == 6:
            return True
        else:
            return False

def run_trial(root, N, n_remaining_before_draw, results):
    # for the trial in trials, continue dicing if not it was not stopped,
    # and then optimally stop if the new dice is optimal
    dices = [1, 2, 3, 4, 5, 6]

    new_trials = []
    for i in dices:
        # NOTE: if n_remaining_before_draw == 1, optimal, terminate here
        if is_optimal(n_remaining_before_draw, i):
            trial = TrialNode(root.index + 1)
            trial.opt_stop_time = root.index + 1
            trial.opt_value = i
            trial.prob = root.prob / 6.0
            root.nexts.append(trial)
            assert root.index + n_remaining_before_draw == N
            results.append(trial)
        else:
            trial = TrialNode(root.index + 1)
            trial.prob = root.prob / 6.0
            root.nexts.append(trial)
            new_trials.append(trial)

    for new_trial in new_trials:
        run_trial(new_trial, N, n_remaining_before_draw - 1, results)

def main():
    N = 10 # the # of drawings

    root = TrialNode(0)  # []TrialNode
    root.prob = 1.0
    results = []
    run_trial(root, N, N, results)
    print(len(results))

if __name__  == '__main__':
    main()
