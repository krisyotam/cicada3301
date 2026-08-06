#!/usr/bin/env python3
from experiments import Experiments
import screen

def main():
    """
        Main routine.
    """

    # Shows all pages
    try:
        screen.clear()
        Experiments.show_all_sections(True)

    except (KeyboardInterrupt, EOFError):
        return

if __name__ == '__main__':
    main()
