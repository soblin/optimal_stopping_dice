#!/usr/bin/env python3

from copy import deepcopy
import numpy as np

class TrialNode:
    def __init__(self, history):
        self.history = deepcopy(history)
        self.opt_stop_time = -1 # when this trial stopped
        self.opt_value = -1
        self.prob = 0.0

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

def run_trial(trials, N):
    # for the trial in trials, continue dicing if not it was not stopped,
    # and then optimally stop if the new dice is optimal

    dices = [1, 2, 3, 4, 5, 6]
    if len(trials) == 0:
        for i in dices:
            trial = TrialNode([i])
            remaining = N - 1
            if is_optimal(remaining, i):
                trial.opt_stop_time = 1
                trial.opt_value = i

            trial.prob = 1.0 / 6.0
            trials.append(trial)
        return trials

    new_trials = []
    for trial in trials:
        if trial.opt_stop_time != -1:
            # this trial was already optimally stopped
            new_trials.append(trial)
            continue
        
        cur_history = trial.history
        for i in dices:
            remaining = N - len(cur_history)
            new_history = cur_history + [i]
            new_trial = TrialNode(new_history)
            if is_optimal(remaining, i):
                # optimal stopping
                new_trial.opt_stop_time = len(new_history)
                new_trial.opt_value = i

            new_trials.append(new_trial)

    return new_trials

def main():
    N = 10 # the # of drawings

    trials = []  # []TrialNode
    for i in range(N):
        print("drawing {}-th dice".format(i+1))
        trials = run_trial(trials, N)
    
    print("There are {} trials".format(len(trials)))

    results = {}
    values = []
    for trial in trials:
        # if trial.opt_stop_time == -1, then it terminated without chances of optimal stopping :)
        n_drawing = len(trial.history)
        last_dice = trial.opt_value
        results.setdefault(n_drawing, {})[last_dice] = results.get(n_drawing, {}).get(last_dice, 0) + 1
        values.append(trial.opt_value)

    print("----------- stat -----------")
    print("{0:7} {1:8} {2:10}".format("#drawings", "last_dice", "#cases"))
    for n_drawing, result in results.items():
        for last_dice, n_cases in result.items():
            print("{0:7} {1:8} {2:10}".format(n_drawing, last_dice, n_cases))

if __name__  == '__main__':
    main()
