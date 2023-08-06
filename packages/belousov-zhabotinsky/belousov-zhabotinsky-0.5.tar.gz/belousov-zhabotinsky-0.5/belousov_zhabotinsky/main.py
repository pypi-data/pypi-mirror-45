#!/usr/bin/python

import curses, argparse

import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import laplace
from scipy.ndimage.interpolation import rotate


def average_rotate(array, degree):

    array = np.mean(
        [
            rotate(array, (360 / degree) * i, reshape=False, mode='wrap')
            for i in range(degree)
        ],
        axis=0,
    )

    return array


def update_bz(p, array, coefficients, height, width):

    q = int(not p)
    p = int(p)

    alpha, beta, gamma = coefficients
    # Count the average amount of each species in the 9 cells around each cell
    s = np.zeros((3, height, width))
    m = np.ones((3, 3)) / 9
    for k in range(3):
        s[k] = convolve2d(array[p, k], m, mode="same", boundary="wrap")
    # Apply the reaction equations
    array[q, 0] = s[0] + s[0] * (alpha * s[1] - gamma * s[2])
    array[q, 1] = s[1] + s[1] * (beta * s[2] - alpha * s[0])
    array[q, 2] = s[2] + s[2] * (gamma * s[0] - beta * s[1])
    # Ensure the species concentrations are kept within [0,1].
    np.clip(array[q], 0, 0.99, array[q])

    return array


def update_turing(p, array, coefficients):

    q = int(not p)
    p = int(p)

    DT, DA, DB = 0.0005, 1, 100
    alpha, beta, _ = coefficients
    # Apply the reaction equations
    array[q, 0] = array[p, 0] + DT * (
        DA * laplace(array[p, 0], mode='wrap')
        + array[p, 0]
        - array[p, 0] ** 3
        - array[p, 1]
        + alpha
    )
    array[q, 1] = array[p, 1] + DT * (
        DB * laplace(array[p, 1], mode='wrap') + (array[p, 0] - array[p, 1]) * beta
    )
    # Ensure the species concentrations are kept within [0,1].
    np.clip(array[q], 0, 0.99, array[q])

    return array


def render(args):

    args.ascii = np.array(args.ascii)

    screen = curses.initscr()
    height, width = screen.getmaxyx()

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, 1, args.background)
    curses.init_pair(2, 2, args.background)
    curses.init_pair(3, 3, args.background)
    curses.init_pair(4, 4, args.background)
    curses.init_pair(5, 5, args.background)
    curses.init_pair(6, 6, args.background)
    curses.init_pair(7, 7, args.background)
    screen.clear

    # Initialize the array
    array = np.array(
        [
            average_rotate(np.random.random(size=(height, width)), args.symmetry)
            for _ in range(6)
        ]
    ).reshape((2, 3, height, width))

    phase = True
    while True:
        phase = not phase
        if args.turing:
            for _ in range(20):
                array = update_turing(phase, array, args.coefficients)
                phase = not phase
        else:
            array = update_bz(phase, array, args.coefficients, height, width)

        if args.fast:
            values = (array[int(phase), 0] * 10).astype('int8')
            for line in range(height - 1):
                screen.addstr(
                    line,
                    0,
                    ''.join(args.ascii[values[line]]),
                    curses.color_pair(7) | curses.A_BOLD,
                )
        else:
            for line in range(height - 1):
                for column in range(width - 1):
                    value = (array[int(phase), 0, line, column] * 10).astype("int8")
                    screen.addstr(
                        line,
                        column,
                        args.ascii[value],
                        curses.color_pair(args.color[value]) | curses.A_BOLD,
                    )
        screen.refresh()
        screen.timeout(30)
        if screen.getch() != -1:
            break
    curses.endwin()


def main():

    # Default parameters
    coefficients = 1.0, 1.0, 1.0
    asciis = np.array((" ", ".", " ", ":", "*", "*", "#", "#", "@", "@"))
    colors = (1, 1, 2, 2, 2, 3, 3, 3, 7, 7)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-t', '--turing', action='store_true', default=False, help='TURING PATTERN MODE'
    )
    parser.add_argument(
        '-a',
        '--ascii',
        action='store',
        default=asciis,
        nargs=10,
        help='10 ASCII characters to be use in the rendering. Each point in the screen has a value between 0 and 1, and each ASCII character used as an input represents a range of values (e.g. 0.0-0.1, 0.1-0.2 etc)',
    )
    parser.add_argument(
        '-c',
        '--color',
        action='store',
        default=colors,
        nargs=10,
        type=int,
        help='10 numbers in the [0-7] range for mapping colors to the ASCII characters. 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white',
    )
    parser.add_argument(
        '-coef',
        '--coefficients',
        action='store',
        default=coefficients,
        nargs=3,
        type=float,
        help="Values for alpha, beta and gamma -- changes the reaction's behaviour. Default is alpha=1.0, beta=1.0, gamma=1.0",
    )
    parser.add_argument(
        '-b',
        '--background',
        action='store',
        default=1,
        type=int,
        help='Background color [int 0-7]. 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white',
    )
    parser.add_argument(
        '-s',
        '--symmetry',
        action='store',
        default=1,
        type=int,
        help='Symmetric mode, generates a n-fold symmetric grid',
    )
    parser.add_argument(
        '-f',
        '--fast',
        action='store_true',
        default=False,
        help='One color mode. Recommended for faster rendering in big terminal windows',
    )
    parser.add_argument(
        '-n', '--number', action='store_true', default=False, help='Show grid values'
    )

    args = parser.parse_args()

    if args.turing:
        args.coefficients = -0.005, 10, 0
        args.ascii = np.array((".", "*", "#", ":", "*", "#", "*", ";", "*", "#"))
        args.color = (1, 2, 4, 1, 2, 4, 1, 2, 4, 1)
        args.background = 0
    if args.number:
        args.ascii = np.array(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))

    render(args)


if __name__ == "__main__":
    main()
