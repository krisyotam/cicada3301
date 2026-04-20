#!/usr/bin/env python3
from core import RuneUtils

import os
import sys
import string
import base64

# Colors
RED, GREEN, BLUE, WHITE, YELLOW, RESET_COLORS = '', '', '', '', '', ''
try:
    import colorama
    colorama.init()
    RED = colorama.Fore.RED + colorama.Style.BRIGHT
    GREEN = colorama.Fore.GREEN + colorama.Style.BRIGHT
    BLUE = colorama.Fore.LIGHTBLUE_EX + colorama.Style.BRIGHT
    WHITE = colorama.Fore.WHITE + colorama.Style.BRIGHT
    YELLOW = colorama.Fore.YELLOW
    RESET_COLORS = colorama.Style.RESET_ALL
except Exception:
    pass

# Logo
LOGO = base64.b64decode(b'CgogICAgICAsKysrNzc3NzcrKz06LCAgICAgICAgICAgICAgICAgICAgKz0gICAgICAgICAgICAgICAgICAgICAgLCwrKz03Kys9LCwgICAgICAgICAgICAgIOKWhOKWhMK3IOKWqiAgIOKWhOKWhMK3ICDiloTiloTiloTCtyDCt+KWhOKWhOKWhOKWhCAgIOKWhOKWhOKWhMK3ICAgICDiloTiloTiloTiloTiloQgICAgICAgICAgICDiloTiloTilowgIC7iloTiloQgwrcgCiAgICA3fj83ICAgKzdJNzcgOixJNzc3ICBJICAgICAgICAgIDc3IDcrNzcgNzogICAgICAgICw/Nzc3Nzc3Pz9+LD0rPX5JNz8sPTc3IEkgICAgICAgICDilpDilogg4paM4paq4paI4paIIOKWkOKWiCDilozilqrilpDilogg4paA4paIIOKWiOKWiMK3IOKWiOKWiCDilpDilogg4paA4paIICAgICDigKLilojiloggIOKWqiAgICAg4paqICAgICDilojilojigKIgIOKWkOKWiCDiloAuIAo9N0k3SX43ICAsNzc6ICsrOn4rNyA3Nz03Nzc3IDcgICAgICs3Nz03ID03STcgICAgICxJNzc3PSA3Nyw6fjcgKz83LCB+NyAgIH4gNzc3PyAgICAgICAg4paI4paIIOKWhOKWhOKWkOKWiMK34paI4paIIOKWhOKWhOKWhOKWiOKWgOKWgOKWiCDilpDilojilqog4paQ4paI4paM4paE4paI4paA4paA4paIICAgICAg4paQ4paILuKWqiDiloTilojiloDiloQgIOKWhOKWiOKWgOKWhCDilojilojilqogIOKWhOKWgOKWgOKWgOKWiOKWhAo3Nys3SSA3Nzd+LCw9N34gICw6Ojc9NzogNyA3NyAgIDc3OiA3IDcgKzc3LDcgSTc3N34rNzc3ST0gICA9Oiw3Nyw3NyAgNzcgNyw3NzcsICAgICAgICAg4paQ4paI4paI4paI4paM4paQ4paI4paM4paQ4paI4paI4paI4paM4paQ4paI4paqIOKWkOKWjOKWiOKWiC4g4paI4paIIOKWkOKWiOKWqiDilpDilowgICAgIOKWkOKWiOKWjMK34paQ4paI4paMLuKWkOKWjOKWkOKWiOKWjC7ilpDilozilpDilojilozilpDilozilpDilojiloTilqrilpDilogKICA9IDcgID83ICwgN34sfiAgKyA3NyA/OiA6Pzc3NyArfjc3IDc3PyBJNzc3N0k3STcgNzc3Kzc3ICAgPTosID83ICAgKzcgNzc3PyAgICAgICAgICAgIMK34paA4paA4paAIOKWgOKWgOKWgMK34paA4paA4paAICDiloAgIOKWgCDiloDiloDiloDiloDiloDigKIgIOKWgCAg4paAICAgICAg4paA4paA4paAICDiloDilojiloTiloDilqog4paA4paI4paE4paA4paqLuKWgOKWgOKWgCAg4paA4paA4paA4paAIAogICAgICA3NyB+SSA9PSB+Nzc9ICs3NzcgNzc3fjogSSwrNzc/ICA3ICA3Oj83PyA/NyA3IDcgNzcgfkkgICA3SSwsPzcgSTc3fgogICAgICAgSSA3PTc3fis3Nys/PTpJK343Nz8gICAgICwgSSA3PyA3NyA3ICAgNzc3fiArNyBJKz83ICArN34/Nzc3LDc3SSAgICAgICAgICAgICAgICAgICAgICAgICAgIFV0aWxpdGllcyBmb3IgQ2ljYWRhIDMzMDEgcmVzZWFyY2gKICAgICAgICAgPTc3IDc3PSArNyA3Nzc3ICAgICAgICAgLDcgNz83Oiw/PzcgICAgICs3ICAgIDcgICA3Nz8/KyA3Nzc3LCAgICAgICAgICAgICAgICAgICAgICAgICAgSm9uYXRoYW4gQmFyIE9yICgiSkJPIiksIEB5b195b195b19qYm8KICAgICAgICAgICAgID1JLCBJIDcrOjc3PyAgICAgICAgICs3STc/Nzc3NyA6ICAgICAgICAgICAgIDo3IDcgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBbIGh0dHBzOi8veW8teW8teW8tamJvLmdpdGh1Yi5pbyBdCiAgICAgICAgICAgICAgICA3STdJPzc3IH4gICAgICAgICArNzo3NywgICAgIH4gICAgICAgICArNyw6OjcgICA3CiAgICAgICAgICAgICAgICw3fjc3Pzc/ID86ICAgICAgICAgNys6Nzc3NzcsICAgICAgICAgICA3NyA6Nzc3Nz0KICAgICAgICAgICAgICAgID83NyArSTcrLDcgICAgICAgICA3fiAgNywrNyAgLD8gICAgICAgPzc/fj83Nzc6CiAgICAgICAgICAgICAgICAgICBJNzc3PTc3NzcgfiAgICAgNzcgOiAgNzcgPTcrLCAgICBJNzcgIDc3NwogICAgICAgICAgICAgICAgICAgICArICAgICAgfj8gICAgICwgKyA3ICAgICwsIH5JLCAgPSA/ICwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgNzc6SSsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLDcKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDo3NwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgOgo=').decode() 

def print_logo():
    """
        Prints out the logo.
    """

    # White if possible
    print(f'{WHITE}{LOGO}{RESET_COLORS}')

def print_blue(msg, end='\n'):
    """
        Prints a blue message.
    """

    # Blue if possible
    print(f'{BLUE}{msg}{RESET_COLORS}', end=end)

def print_green(msg, end='\n'):
    """
        Prints a green message.
    """

    # Green if possible
    print(f'{GREEN}{msg}{RESET_COLORS}', end=end)

def print_red(msg, end='\n'):
    """
        Prints a red message.
    """

    # Red if possible
    print(f'{RED}{msg}{RESET_COLORS}', end=end)

def print_yellow(msg, end='\n'):
    """
        Prints a yellow message.
    """

    # Yellow if possible
    print(f'{YELLOW}{msg}{RESET_COLORS}', end=end)

def clear():
    """
        Clears the screen.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    # Print the logo as a header
    print_logo()

def press_enter(clear_screen=True):
    """
        Waits for an ENTER keypress.
    """

    # Get input and clear the screen
    print('Press ', end='')
    print_yellow('ENTER', end='')
    _ = input(' to continue.')
    if clear_screen:
        clear()

def print_solved_text(text):
    """
        Prettifies and prints solved text.
    """

    # Color lowercase
    s = text
    for c in string.ascii_lowercase:
        s = s.replace(c, f'[!!!BLUE!!!]{c}[!!!RESET_COLORS!!!]')
    s = s.replace('[!!!RESET_COLORS!!!]', RESET_COLORS).replace('[!!!BLUE!!!]', BLUE)

    # Color titles
    s = s.replace('<', RED).replace('>', RESET_COLORS)

    # Print
    print(s)

def run_menu(title, menu_items_list):
    """
        Runs a menu. The given menu items argument must be a list that maps keys to values.
    """

    # Run forever
    last_error = None
    while True:

        # Print title
        clear()
        if last_error is not None:
            print_red(f'{last_error}\n')
            last_error = None
        print_yellow(title)

        # Print menu item
        dots_max_len = len(str(len(menu_items_list))) + 3 + max([ len(item[0]) for item in menu_items_list ])
        index = 0
        for k, v in menu_items_list:
            index += 1
            print_blue(f'{index}.', end=' ')
            dots = '.' * (dots_max_len - (len(k) + len(str(index))))
            print(f'{k} {dots} {v}')

        # Get user choice
        print('\nChoose ', end='')
        print_yellow('Q', end='')
        print(' to quit, or ', end='')
        print_yellow('CTRL+C', end='')
        print(' (or ', end='')
        print_yellow('CTRL+D', end='')
        print(') to get back to main menu.\n')

        # Get choice and return it
        choice = input('Enter your choice: ').strip()
        if choice in ('q', 'Q'):
            return None
        if choice == '':
            continue
        if not choice.isdigit():
            last_error = 'Invalid choice'
            continue
        menu_index = int(choice)
        if menu_index <= 0 or menu_index > len(menu_items_list):
            last_error = 'Invalid choice'
            continue
        return menu_index - 1

