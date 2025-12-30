"""Interactive menu system for Instagram OSINT"""

from utils import print_header, print_info, print_success, print_error, print_warning, Wh, Gr, Ye, Cy, Re

def display_main_menu():
    """Display main menu options"""
    print_header("MAIN MENU")
    print(f"""
       {Wh}[{Gr}1{Wh}] {Cy}Single Profile Analysis
       {Wh}[{Gr}2{Wh}] {Cy}Batch Profile Analysis (Multiple Targets)
       {Wh}[{Gr}3{Wh}] {Cy}Compare Profiles
       {Wh}[{Gr}4{Wh}] {Cy}View Database History
       {Wh}[{Gr}5{Wh}] {Re}Exit
    """)

def get_menu_choice(prompt, valid_choices):
    """Get user menu choice with validation"""
    while True:
        choice = input(f"\n       {Wh}[{Gr}?{Wh}] {prompt}: {Ye}").strip()
        if choice in valid_choices:
            return choice
        print_error(f"Invalid choice. Please select from {', '.join(valid_choices)}")

def display_features_menu():
    """Display features configuration menu"""
    print_header("FEATURES CONFIGURATION")
    print(f"""
       {Wh}Select features to enable:
       
       {Wh}[{Gr}1{Wh}] {Cy}Download Posts & Highlights {Ye}(may take time)
       {Wh}[{Gr}2{Wh}] {Cy}Run Analytics {Ye}(engagement, risk scoring)
       {Wh}[{Gr}3{Wh}] {Cy}Save to Database {Ye}(historical tracking)
       {Wh}[{Gr}4{Wh}] {Cy}All Features
       {Wh}[{Gr}5{Wh}] {Cy}None (Quick mode - basic info only)
    """)

def get_features_config():
    """Get features configuration from user"""
    display_features_menu()  # Show the menu before asking
    choice = get_menu_choice("Choose features option", ['1', '2', '3', '4', '5'])
    
    config = {
        'download': False,
        'analyze': False,
        'db': False,
        'no_download': True
    }
    
    if choice == '1':
        config['download'] = True
        config['no_download'] = False
    elif choice == '2':
        config['analyze'] = True
    elif choice == '3':
        config['db'] = True
    elif choice == '4':
        config['download'] = True
        config['analyze'] = True
        config['db'] = True
        config['no_download'] = False
    # Choice 5 keeps defaults (quick mode)
    
    return config

def display_export_menu():
    """Display export format menu"""
    print_header("EXPORT FORMATS")
    print(f"""
       {Wh}Select export format(s):
       
       {Wh}[{Gr}1{Wh}] {Cy}JSON only {Ye}(structured data)
       {Wh}[{Gr}2{Wh}] {Cy}CSV only {Ye}(spreadsheet format)
       {Wh}[{Gr}3{Wh}] {Cy}HTML only {Ye}(visual report)
       {Wh}[{Gr}4{Wh}] {Cy}JSON + CSV
       {Wh}[{Gr}5{Wh}] {Cy}JSON + HTML
       {Wh}[{Gr}6{Wh}] {Cy}All formats {Ye}(JSON + CSV + HTML)
    """)

def get_export_format():
    """Get export format choice from user"""
    display_export_menu()  # Show the menu before asking
    choice = get_menu_choice("Choose export format", ['1', '2', '3', '4', '5', '6'])
    
    format_map = {
        '1': 'json',
        '2': 'csv',
        '3': 'html',
        '4': 'json,csv',
        '5': 'json,html',
        '6': 'json,csv,html'
    }
    
    return format_map[choice]

def get_target_input():
    """Get single target username from user"""
    print_info("Enter target username to analyze")
    target = input(f"\n       {Wh}[{Gr}>{Wh}] {Cy}Target username: {Ye}").strip()
    return target

def get_multiple_targets():
    """Get multiple target usernames from user"""
    print_info("Enter target usernames (one per line, empty line to finish)")
    targets = []
    count = 1
    
    while True:
        target = input(f"       {Wh}[{Gr}{count}{Wh}] {Cy}Target: {Ye}").strip()
        if not target:
            break
        targets.append(target)
        count += 1
    
    return targets

def get_limit_options():
    """Get follower/following limit options"""
    print_header("DATA LIMITS")
    print(f"""
       {Wh}Set data fetching limits (for performance):
       
       {Wh}[{Gr}1{Wh}] {Cy}No limits {Ye}(fetch all - may be slow)
       {Wh}[{Gr}2{Wh}] {Cy}Limit to 100 each
       {Wh}[{Gr}3{Wh}] {Cy}Limit to 500 each
       {Wh}[{Gr}4{Wh}] {Cy}Limit to 1000 each
       {Wh}[{Gr}5{Wh}] {Cy}Custom limits
    """)
    
    choice = get_menu_choice("Choose limit option", ['1', '2', '3', '4', '5'])
    
    if choice == '1':
        return None, None
    elif choice == '2':
        return 100, 100
    elif choice == '3':
        return 500, 500
    elif choice == '4':
        return 1000, 1000
    elif choice == '5':
        try:
            followers = int(input(f"       {Wh}[{Gr}?{Wh}] {Cy}Followers limit: {Ye}"))
            following = int(input(f"       {Wh}[{Gr}?{Wh}] {Cy}Following limit: {Ye}"))
            return followers, following
        except ValueError:
            print_warning("Invalid number, using no limits")
            return None, None

def confirm_action(message):
    """Ask user to confirm action"""
    response = input(f"\n       {Wh}[{Ye}?{Wh}] {message} {Ye}(y/n): {Wh}").strip().lower()
    return response in ['y', 'yes']

def display_summary(config):
    """Display configuration summary before processing"""
    print_header("CONFIGURATION SUMMARY")
    print(f"\n       {Cy}Features:")
    print(f"       {Wh}• Download Posts: {Gr if config.get('download') else Re}{'Yes' if config.get('download') else 'No'}")
    print(f"       {Wh}• Run Analytics: {Gr if config.get('analyze') else Re}{'Yes' if config.get('analyze') else 'No'}")
    print(f"       {Wh}• Save to Database: {Gr if config.get('db') else Re}{'Yes' if config.get('db') else 'No'}")
    
    if config.get('limit_followers') or config.get('limit_following'):
        print(f"\n       {Cy}Limits:")
        print(f"       {Wh}• Followers: {Ye}{config.get('limit_followers', 'All')}")
        print(f"       {Wh}• Following: {Ye}{config.get('limit_following', 'All')}")
    
    print(f"\n       {Cy}Export Format: {Ye}{config.get('export_format', 'json')}")
    print()
