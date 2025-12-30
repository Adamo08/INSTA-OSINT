"""Utility functions for Instagram OSINT"""

import sys
import time
from typing import List

# Color variables
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'

# Reset color
Reset = '\033[0m'

# Bright colors
BrRe = '\033[91m'
BrGr = '\033[92m'
BrYe = '\033[93m'
BrBlu = '\033[94m'
BrMa = '\033[95m'
BrCy = '\033[96m'

# Background colors
BgGr = '\033[42m'
BgRe = '\033[41m'
BgYe = '\033[43m'
BgBlu = '\033[44m'

# Formatting
Bold = '\033[1m'
Dim = '\033[2m'
Italic = '\033[3m'
Underline = '\033[4m'

# Symbols
CHECK = f"{Gr}✓{Reset}"
CROSS = f"{Re}✗{Reset}"
INFO = f"{Blu}ℹ{Reset}"
WARN = f"{Ye}⚠{Reset}"
STAR = f"{Ye}★{Reset}"
ARROW = f"{Cy}→{Reset}"
BULLET = f"{Gr}●{Reset}"
LINE = "─" * 80

def print_logo():
    """Print the application logo"""
    logo = f"""{Gr} 

        {Gr}██╗███╗   ██╗███████╗████████╗ █████╗        {Re}██████╗ ███████╗██╗███╗   ██╗████████╗
        {Gr}██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗      {Re}██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
        {Gr}██║██╔██╗ ██║███████╗   ██║   ███████║{Wh}█████╗{Re}██║   ██║███████╗██║██╔██╗ ██║   ██║   
        {Gr}██║██║╚██╗██║╚════██║   ██║   ██╔══██║{Wh}╚════╝{Re}██║   ██║╚════██║██║██║╚██╗██║   ██║   
        {Gr}██║██║ ╚████║███████║   ██║   ██║  ██║      {Re}╚██████╔╝███████║██║██║ ╚████║   ██║   
        {Gr}╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝       {Re}╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
        
        {Wh}{Bold}INSTAGRAM OSINT INTELLIGENCE GATHERING TOOL{Reset}
        {Cy}{Dim}Advanced Profile Analysis & Data Collection{Reset}
    """
    print(logo)

def print_section(title, subtitle=""):
    """Print a formatted section header"""
    print(f"\n{Cy}{Bold}{LINE}{Reset}")
    print(f"{Cy}{Bold}  {title.upper()}{Reset}")
    if subtitle:
        print(f"{Dim}{Cy}  {subtitle}{Reset}")
    print(f"{Cy}{Bold}{LINE}{Reset}\n")

def print_info(message, prefix=""):
    """Print info message"""
    icon = INFO if not prefix else prefix
    print(f"  {icon} {Wh}{message}{Reset}")

def print_success(message, prefix=""):
    """Print success message"""
    icon = CHECK if not prefix else prefix
    print(f"  {icon} {BrGr}{message}{Reset}")

def print_warning(message, prefix=""):
    """Print warning message"""
    icon = WARN if not prefix else prefix
    print(f"  {icon} {BrYe}{message}{Reset}")

def print_error(message, prefix=""):
    """Print error message"""
    icon = CROSS if not prefix else prefix
    print(f"  {icon} {BrRe}{message}{Reset}")

def print_highlight(message):
    """Print highlighted message"""
    print(f"  {STAR} {Bold}{BrCy}{message}{Reset}")

def print_header(title):
    """Print section header"""
    print(f"\n{BgBlu}{Wh}{Bold} {title.upper()} {Reset}\n")

def print_subheader(title):
    """Print subsection header"""
    print(f"\n{Cy}{Underline}{title}{Reset}\n")

def print_data(key, value, color=Wh):
    """Print key-value pair"""
    print(f"  {ARROW} {Cyan}{Bold}{key}{Reset}: {color}{value}{Reset}")

def print_table_row(columns: List[str], widths: List[int], is_header=False, color=Wh):
    """Print a formatted table row"""
    row = " │ ".join(
        f"{col:<{width}}" if i == 0 else f"{col:^{width}}" 
        for i, (col, width) in enumerate(zip(columns, widths))
    )
    
    if is_header:
        print(f"  {BgBlu}{Wh}{Bold}{row}{Reset}")
        separator = " ├─" + "─┼─".join("─" * w for w in widths) + "─┤"
        print(f"  {Cy}{separator}{Reset}")
    else:
        print(f"  {color}{row}{Reset}")

def loading_animation(message="", duration=3):
    """Show loading animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start = time.time()
    
    while time.time() - start < duration:
        for frame in frames:
            sys.stdout.write(f"\r  {Cy}{frame}{Reset} {message}")
            sys.stdout.flush()
            time.sleep(0.08)

def progress_bar(current, total, width=50, label="", color=Gr):
    """Display a progress bar"""
    if total == 0:
        return
    
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    
    percentage = f"{int(percent * 100):>3}%"
    count_str = f"[{current}/{total}]"
    
    if label:
        print(f"  {label}")
    
    print(f"  {color}{bar}{Reset} {percentage} {count_str}")

def spinner(duration=3, label=""):
    """Show a spinner"""
    frames = ["◐", "◓", "◑", "◒"]
    start = time.time()
    frame_idx = 0
    
    while time.time() - start < duration:
        sys.stdout.write(f"\r  {Cy}{frames[frame_idx % len(frames)]}{Reset} {label}")
        sys.stdout.flush()
        time.sleep(0.2)
        frame_idx += 1
    
    sys.stdout.write(f"\r  {CHECK} {label}\n")
    sys.stdout.flush()

def print_box(title, content, color=Cy):
    """Print content in a box"""
    border_top = f"  {color}╔════════════════════════════════════════════════════════════════════════════════╗{Reset}"
    border_mid = f"  {color}║{Reset}"
    border_bot = f"  {color}╚════════════════════════════════════════════════════════════════════════════════╝{Reset}"
    
    print(border_top)
    if title:
        title_str = f" {Bold}{title}{Reset} "
        print(f"{border_mid} {title_str:<78} {border_mid}")
        print(f"  {color}╠════════════════════════════════════════════════════════════════════════════════╣{Reset}")
    
    for line in content.split('\n'):
        padding = 78 - len(line)
        print(f"{border_mid} {line:<{padding}} {border_mid}")
    
    print(border_bot)

def print_stat(label, value, unit="", color=BrCy):
    """Print a statistic with formatting"""
    print(f"  {BULLET} {Bold}{label}{Reset}: {color}{value:,}{Reset} {Dim}{unit}{Reset}")

def print_menu(options: List[str], title="Select an option"):
    """Print an interactive menu"""
    print(f"\n{Cy}{Bold}{title}{Reset}")
    for i, option in enumerate(options, 1):
        print(f"  {BrCy}{i}{Reset} {Wh}{option}{Reset}")
    
    while True:
        try:
            choice = input(f"\n  {Gr}Enter your choice (1-{len(options)}): {Reset}")
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            else:
                print_warning("Invalid choice. Please try again.")
        except ValueError:
            print_warning("Please enter a valid number.")

def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('clear' if sys.platform != 'win32' else 'cls')

def print_divider(char="=", length=80):
    """Print a divider line"""
    print(f"  {Cy}{char * length}{Reset}")

def print_profile_card(profile_data: dict):
    """Print a formatted profile card"""
    print(f"\n{BgBlu}{Wh}{Bold} PROFILE INFORMATION {Reset}\n")
    
    for key, value in profile_data.items():
        key_display = key.replace('_', ' ').title()
        if isinstance(value, bool):
            value = f"{BrGr}Yes{Reset}" if value else f"{Re}No{Reset}"
        else:
            value = str(value) if value else f"{Dim}N/A{Reset}"
        print(f"  {Cy}▸{Reset} {Bold}{key_display:<25}{Reset} {Wh}{value}{Reset}")

def print_comparison_header(title1, title2):
    """Print header for comparison"""
    print(f"\n{Cy}{Bold}{LINE}{Reset}")
    print(f"  {BrCy}{title1:<35}{Reset} │ {BrCy}{title2:<35}{Reset}")
    print(f"{Cy}{Bold}{LINE}{Reset}\n")

def format_large_number(num):
    """Format large numbers for display"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

