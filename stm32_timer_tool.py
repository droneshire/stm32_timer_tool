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
    for i in range(3):
        fclk = fclk / (i**2 + 1)
        for prescalar in range(2**16 - 1):
            reload_val = int(float(fclk) / float(prescalar + 1) / args.target - 1)
            if reload_val >= 2**16 or reload_val <=10:
                continue
            if reload_val > max_reload:
                max_reload = reload_val
                best_prescalar = prescalar
                div = i + 1

    print('CLKDIV: {} ARR: {} PRE: {}'.format(div, max_reload, best_prescalar))
