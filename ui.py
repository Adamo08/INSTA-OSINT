"""Advanced terminal UI components"""

import time
import getpass
from typing import List, Dict, Tuple
from utils import (
    Cy, Gr, Re, Ye, Wh, BrGr, BrCy, BrYe, BrRe,
    Bold, Underline, Dim, Reset, CHECK, CROSS, INFO, ARROW
)

class TerminalUI:
    """Advanced terminal UI components"""
    
    @staticmethod
    def print_header_banner(title, subtitle=""):
        """Print an impressive header banner"""
        width = 80
        print(f"\n{Cy}{Bold}{'█' * width}{Reset}")
        print(f"{Cy}█{Reset} {BrCy}{Bold}{title.center(width - 4)}{Reset} {Cy}█{Reset}")
        
        if subtitle:
            print(f"{Cy}█{Reset} {Dim}{subtitle.center(width - 4)}{Reset} {Cy}█{Reset}")
        
        print(f"{Cy}{Bold}{'█' * width}{Reset}\n")
    
    @staticmethod
    def print_profile_table(profile_data: Dict):
        """Print profile data in a nice table format"""
        print(f"\n{BrCy}{Bold}  📊 PROFILE DATA{Reset}\n")
        
        display_order = [
            ("Username", "username"),
            ("Full Name", "full_name"),
            ("User ID", "userid"),
            ("Bio", "biography"),
            ("Followers", "followers"),
            ("Following", "followees"),
            ("Posts", "mediacount"),
            ("Private", "is_private"),
            ("Business", "is_business_account"),
        ]
        
        for label, key in display_order:
            value = profile_data.get(key, "N/A")
            
            # Format value
            if isinstance(value, bool):
                value_str = f"{BrGr}Yes{Reset}" if value else f"{Re}No{Reset}"
            elif isinstance(value, int) and key in ["followers", "followees", "mediacount"]:
                value_str = f"{BrCy}{value:,}{Reset}"
            else:
                value_str = str(value) if value else f"{Dim}N/A{Reset}"
            
            label_width = 20
            print(f"  {ARROW} {label:<{label_width}} {Wh}{value_str}{Reset}")
    
    @staticmethod
    def print_stats_grid(stats: Dict[str, Tuple[str, str]]):
        """Print statistics in a grid layout
        
        stats = {
            "Engagement": ("2.5", "posts/follower"),
            "Follower Ratio": ("1.5", "followers/following")
        }
        """
        print(f"\n{BrCy}{Bold}  📈 ANALYTICS{Reset}\n")
        
        for label, (value, unit) in stats.items():
            print(f"  {CHECK} {Bold}{label:<25}{Reset} {BrGr}{value:>12}{Reset} {Dim}{unit}{Reset}")
    
    @staticmethod
    def print_followers_table(followers: List[Dict], limit=20):
        """Print followers in a formatted table"""
        print(f"\n{BrCy}{Bold}  👥 FOLLOWERS ({len(followers)}){Reset}\n")
        
        # Header
        header = ["#", "Username", "User ID", "Full Name"]
        col_widths = [4, 20, 12, 25]
        
        header_line = "  " + " │ ".join(f"{h:^{w}}" for h, w in zip(header, col_widths))
        print(f"{BrCy}{Bold}{header_line}{Reset}")
        
        sep = "  " + "─┼─".join("─" * w for w in col_widths)
        print(f"{Cy}{sep}{Reset}")
        
        # Data rows
        for i, follower in enumerate(followers[:limit], 1):
            row_data = [
                str(i),
                follower.get("username", "N/A")[:20],
                str(follower.get("user_id", ""))[:12],
                follower.get("full_name", "N/A")[:25]
            ]
            row_line = "  " + " │ ".join(f"{d:<{w}}" for d, w in zip(row_data, col_widths))
            print(f"{Wh}{row_line}{Reset}")
        
        if len(followers) > limit:
            remaining = len(followers) - limit
            print(f"{Dim}  ... and {remaining} more followers{Reset}\n")
        else:
            print()
    
    @staticmethod
    def print_risk_assessment(risk_score: int, profile_type: str):
        """Print risk assessment with color coding"""
        print(f"\n{BrCy}{Bold}  ⚠️  RISK ASSESSMENT{Reset}\n")
        
        # Risk level
        if risk_score < 25:
            risk_color = BrGr
            risk_level = "LOW RISK"
        elif risk_score < 50:
            risk_color = BrYe
            risk_level = "MEDIUM RISK"
        elif risk_score < 75:
            risk_color = Ye
            risk_level = "HIGH RISK"
        else:
            risk_color = BrRe
            risk_level = "CRITICAL RISK"
        
        # Risk bar
        filled = int(risk_score / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        print(f"  Risk Score: {risk_color}{bar}{Reset} {risk_score}/100")
        print(f"  Level: {risk_color}{Bold}{risk_level}{Reset}")
        print(f"  Type: {BrCy}{profile_type}{Reset}\n")
    
    @staticmethod
    def print_comparison(profile1: Dict, profile2: Dict):
        """Print side-by-side profile comparison"""
        print(f"\n{BrCy}{Bold}  🔄 PROFILE COMPARISON{Reset}\n")
        
        keys = ["followers", "followees", "mediacount"]
        
        for key in keys:
            label = key.replace("_", " ").title()
            val1 = profile1.get(key, 0)
            val2 = profile2.get(key, 0)
            
            val1_str = f"{val1:,}" if isinstance(val1, int) else str(val1)
            val2_str = f"{val2:,}" if isinstance(val2, int) else str(val2)
            
            # Determine which is larger
            if isinstance(val1, int) and isinstance(val2, int):
                diff = val1 - val2
                if diff > 0:
                    diff_str = f"{BrGr}+{diff:,}{Reset}"
                elif diff < 0:
                    diff_str = f"{BrRe}{diff:,}{Reset}"
                else:
                    diff_str = f"{Dim}Equal{Reset}"
            else:
                diff_str = ""
            
            print(f"  {label:<15} {BrCy}{val1_str:>12}{Reset}  vs  {BrCy}{val2_str:>12}{Reset}  {diff_str}")
        
        print()
    
    @staticmethod
    def print_step_progress(current: int, total: int, label: str):
        """Print step-by-step progress"""
        bar = "▰" * current + "▱" * (total - current)
        percent = int((current / total) * 100)
        
        print(f"  {BrCy}{bar}{Reset} {BrGr}{percent:>3}%{Reset} - {label}")
    
    @staticmethod
    def print_export_summary(exports: List[Tuple[str, str]]):
        """Print export file summary"""
        print(f"\n{BrGr}{Bold}  ✓ EXPORT COMPLETE{Reset}\n")
        
        for file_type, filename in exports:
            icon = "📄" if file_type == "JSON" else ("📊" if file_type == "CSV" else "🌐")
            print(f"  {icon} {Bold}{file_type:<8}{Reset} {Cy}{filename}{Reset}")
        
        print()
    
    @staticmethod
    def print_database_summary(profile_count: int, follower_count: int):
        """Print database operation summary"""
        print(f"\n{BrGr}{Bold}  ✓ DATABASE SAVED{Reset}\n")
        print(f"  {CHECK} Stored {BrCy}{profile_count}{Reset} profile snapshot(s)")
        print(f"  {CHECK} Stored {BrCy}{follower_count:,}{Reset} follower record(s)")
        print()
    
    @staticmethod
    def print_loading_phase(phase: int, total_phases: int, phase_name: str):
        """Print loading phase with animation"""
        bar = "▰" * phase + "▱" * (total_phases - phase)
        print(f"\r  {Cy}{bar}{Reset} {BrCy}[{phase}/{total_phases}]{Reset} {phase_name:<40}", end="", flush=True)
    
    @staticmethod
    def print_success_box(message: str):
        """Print success in a box"""
        width = 78
        print(f"\n  {BrGr}╔{'═' * width}╗{Reset}")
        print(f"  {BrGr}║{Reset} {BrGr}{Bold}{message.center(width)}{Reset} {BrGr}║{Reset}")
        print(f"  {BrGr}╚{'═' * width}╝{Reset}\n")
    
    @staticmethod
    def print_error_box(message: str):
        """Print error in a box"""
        width = 78
        print(f"\n  {BrRe}╔{'═' * width}╗{Reset}")
        print(f"  {BrRe}║{Reset} {BrRe}{Bold}{message.center(width)}{Reset} {BrRe}║{Reset}")
        print(f"  {BrRe}╚{'═' * width}╝{Reset}\n")

class InteractivePrompt:
    """Interactive command-line prompts"""
    
    @staticmethod
    def get_credentials():
        """Get credentials with styling - password hidden for security"""
        print(f"\n{BrCy}{Bold}  🔐 INSTAGRAM CREDENTIALS{Reset}\n")
        
        username = input(f"  {ARROW} Username: {BrCy}")
        print(Reset, end="")
        
        # Use getpass to hide password input
        password = getpass.getpass(f"  {ARROW} Password: {BrCy}")
        print(Reset, end="")
        
        return username, password
    
    @staticmethod
    def get_target():
        """Get target username"""
        print(f"\n{BrCy}{Bold}  🎯 TARGET SELECTION{Reset}\n")
        target = input(f"  {ARROW} Target username: {BrCy}")
        print(Reset, end="")
        return target
    
    @staticmethod
    def confirm(message: str) -> bool:
        """Get confirmation"""
        response = input(f"  {ARROW} {message} {BrCy}(y/n): {Reset}").lower().strip()
        return response in ['y', 'yes']
    
    @staticmethod
    def select_options(options: List[str], title: str = "Select options") -> List[bool]:
        """Multi-select options"""
        print(f"\n{BrCy}{Bold}  ⚙️  {title}{Reset}\n")
        
        selections = []
        for i, option in enumerate(options, 1):
            response = input(f"  {i}. {option}? {BrCy}(y/n): {Reset}").lower().strip()
            selections.append(response in ['y', 'yes'])
        
        return selections
