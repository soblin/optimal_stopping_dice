#!/usr/bin/env python3

from copy import deepcopy
import numpy as np
import argparse

class TrialNode:
    def __init__(self, index):
        self.index = index  # first trial is 1
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
            trial.opt_stop_value = i
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

def main(N):
    root = TrialNode(0)  # []TrialNode
    root.prob = 1.0
    results = []
    run_trial(root, N, N, results)

    stats = {}  # mapping [n_drawing][last_dice] --> n_case
    probs = {}  # mapping [n_drawing][last_dice] --> prob
    values = []
    weights = []
    for result in results:
        n_drawing = result.opt_stop_time
        last_dice = result.opt_stop_value
        stats.setdefault(n_drawing, {})[last_dice] = stats.setdefault(n_drawing, {}).get(last_dice, 0) + 1
        probs.setdefault(n_drawing, {})[last_dice] = probs.setdefault(n_drawing, {}).get(last_dice, 0.0) + result.prob
        values.append(result.opt_stop_value)
        weights.append(result.prob)

    print("------------------------- stat -------------------------")
    print("{0:7}   {1:8}   {2:10}   {3:10}".format("#drawings", "last_dice", "#cases", "prob"))
    for n_drawing, result in stats.items():
        for last_dice, n_cases in result.items():
            prob = probs[n_drawing][last_dice]
            print("{0:7}   {1:8}   {2:10}   {3:10}".format(n_drawing, last_dice, n_cases, prob))

    values = np.array(values)
    weights = np.array(weights)
    print("")
    print("expectation of last_dice is {}".format(np.average(values, weights=weights)))
    print("sum of prob = {}".format(np.sum(weights)))

if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('N', help='number of trials')
    args = parser.parse_args()

    N = int(args.N)
    main(N)
