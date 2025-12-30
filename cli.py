"""CLI argument parser and configuration"""

import argparse

def get_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Instagram OSINT Tool - Gather intelligence on Instagram profiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python instaOSINT.py
  
  # Specify account and target
  python instaOSINT.py -u myusername -p mypassword -t targetusername
  
  # Batch mode with multiple targets
  python instaOSINT.py -u myusername -p mypassword -f targets.txt
  
  # Export to specific format
  python instaOSINT.py -u myusername -p mypassword -t targetusername -o html,json,csv
  
  # Store data in database and analyze
  python instaOSINT.py -u myusername -p mypassword -t targetusername --db --analyze
        """
    )
    
    # Authentication arguments
    auth_group = parser.add_argument_group('Authentication')
    auth_group.add_argument('-u', '--username', help='Instagram username')
    auth_group.add_argument('-p', '--password', help='Instagram password')
    auth_group.add_argument('--no-session', action='store_true', help='Do not use saved session')
    
    # Target arguments
    target_group = parser.add_argument_group('Target')
    target_group.add_argument('-t', '--target', help='Single target username')
    target_group.add_argument('-f', '--file', help='File with list of target usernames (one per line)')
    
    # Output arguments
    output_group = parser.add_argument_group('Output')
    output_group.add_argument('-o', '--output', default='json', 
                             help='Export format(s): json, csv, html (comma-separated, default: json)')
    output_group.add_argument('-d', '--dir', default='.', help='Output directory (default: current)')
    
    # Feature arguments
    feature_group = parser.add_argument_group('Features')
    feature_group.add_argument('--db', action='store_true', help='Store data in database')
    feature_group.add_argument('--analyze', action='store_true', help='Run analytics and calculate metrics')
    feature_group.add_argument('--compare', action='store_true', help='Compare multiple profiles')
    feature_group.add_argument('--no-download', action='store_true', help='Skip downloading posts/highlights')
    
    # Performance arguments
    perf_group = parser.add_argument_group('Performance')
    perf_group.add_argument('--limit-followers', type=int, help='Limit followers to fetch (default: all)')
    perf_group.add_argument('--limit-following', type=int, help='Limit following to fetch (default: all)')
    perf_group.add_argument('--quiet', action='store_true', help='Minimize console output')
    
    return parser.parse_args()

def validate_args(args):
    """Validate parsed arguments"""
    errors = []
    
    if not args.target and not args.file:
        errors.append("Either --target or --file must be specified")
    
    if args.target and args.file:
        errors.append("Cannot specify both --target and --file")
    
    valid_formats = ['json', 'csv', 'html']
    formats = [f.strip().lower() for f in args.output.split(',')]
    invalid = [f for f in formats if f not in valid_formats]
    if invalid:
        errors.append(f"Invalid output format(s): {', '.join(invalid)}")
    
    if errors:
        for error in errors:
            print(f"Error: {error}")
        return False
    
    return True
