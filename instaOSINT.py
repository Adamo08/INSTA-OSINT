#!/usr/bin/python
# << CODE BY HUNX04
# << MAU RECODE ??? IZIN DULU LAH , MINIMAL TAG AKUN GITHUB MIMIN YANG MENGARAH KE AKUN INI, LEBIH ENAKNYA SIH FORK 
# << KALAU DI ATAS TIDAK DI IKUTI MAKA AKAN MENDAPATKAN DOSA KARENA MIMIN GAK IKHLAS DUNIA AKHIRAT SAMPAI 7 TURUNAN
# "Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil," (QS. An Nisaa': 29). Rasulullah SAW juga melarang umatnya untuk mengambil hak orang lain tanpa izin.

import sys
import os
import time
import getpass
from cli import get_args, validate_args
from processor import InstagramOSINT
from utils import print_logo, print_info, print_warning, print_error, print_success, print_header, Wh, Gr, Ye, Cy
from menu import (display_main_menu, get_menu_choice, display_features_menu, 
                  get_features_config, display_export_menu, get_export_format,
                  get_target_input, get_multiple_targets, get_limit_options,
                  confirm_action, display_summary)
from database import OsintDatabase

def interactive_mode():
    """Interactive CLI mode with menu system"""
    print_logo()
    print_header("AUTHENTICATION")
    
    # Get credentials
    username = input(f"\n       {Wh}[{Gr}>{Wh}] {Cy}Instagram username: {Ye}")
    password = getpass.getpass(f"       {Wh}[{Gr}>{Wh}] {Cy}Instagram password: {Ye}")
    
    os.system('clear')
    print_logo()
    
    # Initialize OSINT processor
    osint = InstagramOSINT(username, password)
    
    # Authenticate
    print_info("Authenticating...")
    if not osint.authenticate():
        print_error("Authentication failed!")
        sys.exit(1)
    
    print_success("Authentication successful!")
    time.sleep(1)
    
    # Main menu loop
    while True:
        os.system('clear')
        print_logo()
        display_main_menu()
        
        choice = get_menu_choice("Select an option", ['1', '2', '3', '4', '5'])
        
        if choice == '5':
            print_success("Goodbye!")
            sys.exit(0)
        
        elif choice == '1':
            # Single profile analysis
            handle_single_profile(osint)
        
        elif choice == '2':
            # Batch analysis
            handle_batch_profiles(osint)
        
        elif choice == '3':
            # Compare profiles
            handle_compare_profiles(osint)
        
        elif choice == '4':
            # View database
            handle_view_database()
        
        # Ask if user wants to continue
        if not confirm_action("Continue with another operation?"):
            print_success("Goodbye!")
            sys.exit(0)

def handle_single_profile(osint):
    """Handle single profile analysis"""
    os.system('clear')
    print_logo()
    
    # Get target
    target = get_target_input()
    
    # Get features configuration
    features_config = get_features_config()
    
    # Get export format
    export_format = get_export_format()
    
    # Get limits
    follower_limit, following_limit = get_limit_options()
    
    # Build options
    options = {
        'analyze': features_config['analyze'],
        'db': features_config['db'],
        'no_download': features_config['no_download'],
        'limit_followers': follower_limit,
        'limit_following': following_limit
    }
    
    # Show summary
    config_summary = {**options, 'export_format': export_format, 'download': features_config['download']}
    display_summary(config_summary)
    
    if not confirm_action("Proceed with analysis?"):
        print_warning("Analysis cancelled")
        return
    
    # Process
    print_header("PROCESSING")
    print_info(f"Analyzing profile: {target}")
    
    results = osint.process_profile(target, options)
    
    if results:
        # Export results
        print_info("Exporting results...")
        exported = osint.export_results(results, target, export_format)
        print_success(f"✓ Exported {len(exported)} file(s)")
        for file in exported:
            print(f"       {Wh}• {Gr}{file}")
    else:
        print_error("Failed to process target")

def handle_batch_profiles(osint):
    """Handle batch profile analysis"""
    os.system('clear')
    print_logo()
    
    # Get targets
    targets = get_multiple_targets()
    
    if not targets:
        print_warning("No targets provided")
        return
    
    print_info(f"Total targets: {len(targets)}")
    
    # Get features configuration
    features_config = get_features_config()
    
    # Get export format
    export_format = get_export_format()
    
    # Get limits
    follower_limit, following_limit = get_limit_options()
    
    # Build options
    options = {
        'analyze': features_config['analyze'],
        'db': features_config['db'],
        'no_download': features_config['no_download'],
        'limit_followers': follower_limit,
        'limit_following': following_limit
    }
    
    # Show summary
    config_summary = {**options, 'export_format': export_format, 'download': features_config['download']}
    display_summary(config_summary)
    
    if not confirm_action(f"Proceed with {len(targets)} profiles?"):
        print_warning("Analysis cancelled")
        return
    
    # Process batch
    print_header("BATCH PROCESSING")
    
    for idx, target in enumerate(targets, 1):
        print_info(f"Processing [{idx}/{len(targets)}]: {target}")
        
        results = osint.process_profile(target, options)
        
        if results:
            exported = osint.export_results(results, target, export_format)
            print_success(f"✓ Completed {target}")
        else:
            print_error(f"✗ Failed {target}")
        
        if idx < len(targets):
            time.sleep(2)  # Rate limiting
    
    print_success(f"✓ Batch processing complete! Processed {len(targets)} profiles")

def handle_compare_profiles(osint):
    """Handle profile comparison"""
    os.system('clear')
    print_logo()
    
    print_info("Profile comparison requires at least 2 profiles")
    targets = get_multiple_targets()
    
    if len(targets) < 2:
        print_warning("Need at least 2 profiles to compare")
        return
    
    print_info(f"Comparing {len(targets)} profiles")
    
    # Get options
    options = {
        'analyze': True,
        'db': True,
        'no_download': True,
        'limit_followers': 100,  # Limit for comparison
        'limit_following': 100
    }
    
    if not confirm_action(f"Compare {len(targets)} profiles?"):
        print_warning("Comparison cancelled")
        return
    
    # Process all profiles
    print_header("COMPARING PROFILES")
    all_results = []
    
    for idx, target in enumerate(targets, 1):
        print_info(f"Fetching [{idx}/{len(targets)}]: {target}")
        results = osint.process_profile(target, options)
        if results:
            all_results.append(results)
    
    if len(all_results) >= 2:
        print_header("COMPARISON RESULTS")
        
        # Display comparison
        for result in all_results:
            profile = result['profile']
            analytics = result.get('analytics', {})
            
            print(f"\n       {Cy}Profile: {Gr}{profile.username}")
            print(f"       {Wh}├─ Followers: {Ye}{profile.followers:,}")
            print(f"       {Wh}├─ Following: {Ye}{profile.followees:,}")
            print(f"       {Wh}├─ Posts: {Ye}{profile.mediacount}")
            
            if analytics:
                print(f"       {Wh}├─ Engagement Rate: {Ye}{analytics.get('engagement_rate', 0)}")
                print(f"       {Wh}├─ Follower Ratio: {Ye}{analytics.get('follower_ratio', 0)}")
                print(f"       {Wh}└─ Risk Score: {Ye}{analytics.get('risk_score', 0)}/100")
        
        print_success(f"\n✓ Comparison complete!")
    else:
        print_error("Failed to fetch enough profiles for comparison")

def handle_view_database():
    """View database statistics"""
    os.system('clear')
    print_logo()
    print_header("DATABASE VIEWER")
    
    db = OsintDatabase()
    profiles = db.get_all_profiles()
    
    if not profiles:
        print_warning("No profiles in database yet")
        return
    
    print_info(f"Total profiles stored: {len(profiles)}")
    print()
    
    for profile in profiles[:10]:  # Show first 10
        print(f"       {Wh}• {Gr}{profile}")
        
        # Try to get history
        history = db.get_profile_history(profile)
        if len(history) > 1:
            growth = db.get_growth_stats(profile)
            if growth:
                print(f"         {Wh}├─ Data points: {Ye}{growth['data_points']}")
                print(f"         {Wh}├─ Follower change: {Ye}{growth['followers_change']:+,}")
                print(f"         {Wh}└─ Following change: {Ye}{growth['following_change']:+,}")
    
    if len(profiles) > 10:
        print(f"\n       {Wh}... and {Ye}{len(profiles) - 10}{Wh} more profiles")
    
    print()


def cli_mode(args):
    """Command-line argument mode"""
    # Prepare options
    options = {
        'analyze': args.analyze,
        'db': args.db,
        'no_download': args.no_download,
        'limit_followers': args.limit_followers,
        'limit_following': args.limit_following
    }
    
    # Initialize OSINT processor
    osint = InstagramOSINT(
        args.username,
        args.password,
        use_session=not args.no_session,
        quiet=args.quiet
    )
    
    # Authenticate
    if not osint.authenticate():
        if not args.quiet:
            print_error("Authentication failed!")
        sys.exit(1)
    
    # Get target list
    targets = []
    if args.target:
        targets = [args.target]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                targets = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            if not args.quiet:
                print_error(f"File not found: {args.file}")
            sys.exit(1)
    
    # Process targets
    if args.compare and len(targets) > 1:
        # Comparison mode
        all_results = osint.batch_process(targets, options)
        
        if all_results:
            # Export each profile
            for result in all_results:
                profile = result['profile']
                osint.export_results(result, profile.username, args.output)
    else:
        # Single or batch mode
        for target in targets:
            result = osint.process_profile(target, options)
            if result:
                osint.export_results(result, target, args.output)
            time.sleep(2)  # Rate limiting


def main():
    """Main entry point"""
    try:
        # Check if arguments provided
        if len(sys.argv) > 1:
            args = get_args()
            
            if not validate_args(args):
                sys.exit(1)
            
            cli_mode(args)
        else:
            interactive_mode()
    
    except KeyboardInterrupt:
        print(f"\n[!] Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
