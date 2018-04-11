#!/usr/bin/env python

"""
Calculate the auto reload value and prescalar for timers, maximizing for
best resolution
"""
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clock', type=int, default=int(84e6), help='timer clock frequency')
    parser.add_argument('-t', '--target', type=int, required=True, help='target frequency')
    args = parser.parse_args()

    max_reload = 0
    best_prescalar = 0
    fclk = args.clock
    div = 1
    for i in range(3):
        clk_div = (i**2 + 1)
        fclk = fclk / clk_div
        for prescalar in range(2**16 - 1):
            reload_val = int(float(fclk) / float(prescalar + 1) / args.target - 1)
            if reload_val >= 2**16 or reload_val <= 0.0:
                continue
            if reload_val > max_reload:
                max_reload = reload_val
                best_prescalar = prescalar
                div = clk_div

    print('CLKDIV: {} ARR: {} PRE: {}'.format(div, max_reload, best_prescalar))
    actual =  args.clock / div / (best_prescalar + 1) / (max_reload  + 1)
    print('Desired: {} Actual: {} Error: {}%'.format(args.target, actual, float(actual - args.target) * 100.0 / float(args.target)))
    if actual != args.target:
        print('WARNING: Can\'t achieve desired frequecy with current timer clock frequency!')
