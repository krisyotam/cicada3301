#!/usr/bin/env python3
from experiments import Experiments
import screen

import logging

def main():
    """
        Main routine.
    """

    # Logging capability
    logging.basicConfig(filename='CicadaUtils.log', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # List all static methods in Experiments 
    exprs = [ (k, v) for (k, v) in Experiments.__dict__.items() if isinstance(v, staticmethod) ]
    menu_items = [ (k.replace('_', ' ').title(), v.__func__.__doc__.strip().split('\n')[0]) for (k, v) in exprs ]

    # Run forever
    while True:

        # Run menu
        choice = None
        try:
            choice = screen.run_menu('== METHODS AVAILABLE ==', menu_items)

            # Handle quitting
            if choice is None:
                return

            # Handle a valid choice
            logger.info(f'Starting: {menu_items[choice][0]}')
            screen.clear()
            screen.print_yellow(f'== {menu_items[choice][0]} ==\n')
            exprs[choice][1].__func__()
            logger.info(f'Finished: {menu_items[choice][0]}')
            screen.print_green('\n\nEXECUTION COMPLETE\n')
            screen.press_enter()

        except (KeyboardInterrupt, EOFError):
            if choice is not None:
                logger.info(f'Stopped: {menu_items[choice][0]}')
                screen.print_red('\n\nSTOPPED BY USER\n')
                screen.press_enter()
                continue

if __name__ == '__main__':
    main()
    
