"""Core processor for Instagram OSINT operations"""

import instaloader
import time
import os
from utils import print_info, print_warning, print_error, print_success, print_header, loading_animation
from analyzer import ProfileAnalytics, ComparativeAnalytics
from exporter import Exporter
from database import OsintDatabase

SESSION_FILE = "session-{username}"
DOWNLOAD_DIR = "downloads"  # Directory for Instagram content

class InstagramOSINT:
    """Main processor for Instagram OSINT"""
    
    def __init__(self, username=None, password=None, use_session=True, quiet=False):
        self.username = username
        self.password = password
        self.use_session = use_session
        self.quiet = quiet
        self.loader = instaloader.Instaloader(dirname_pattern=DOWNLOAD_DIR + "/{target}")
        self.is_logged_in = False
        
        # Create download directory if it doesn't exist
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    def load_session(self):
        """Load saved session if available"""
        if not self.use_session or not self.username:
            return False
        
        session_file = SESSION_FILE.format(username=self.username)
        try:
            self.loader.load_session_from_file(self.username, session_file)
            self.is_logged_in = True
            if not self.quiet:
                print_success("Session loaded successfully!")
            return True
        except FileNotFoundError:
            return False
    
    def login(self, username, password):
        """Handle login with 2FA support"""
        self.username = username
        self.password = password
        
        try:
            self.loader.login(username, password)
            self.is_logged_in = True
            self.save_session()
            if not self.quiet:
                print_success("Login successful!")
            return True
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            if not self.quiet:
                print_warning("Two-factor authentication required!")
            two_factor_code = input("Enter your 2FA code: ")
            self.loader.two_factor_login(two_factor_code)
            self.is_logged_in = True
            self.save_session()
            if not self.quiet:
                print_success("Login successful with 2FA!")
            return True
        except Exception as e:
            if not self.quiet:
                print_error(f"Login failed: {str(e)}")
            return False
    
    def save_session(self):
        """Save current session"""
        if self.username:
            session_file = SESSION_FILE.format(username=self.username)
            self.loader.save_session_to_file(session_file)
    
    def authenticate(self):
        """Authenticate using session or login"""
        if self.use_session and self.load_session():
            return True
        
        if self.username and self.password:
            return self.login(self.username, self.password)
        
        return False
    
    def fetch_profile(self, target_username):
        """Fetch profile data"""
        if not self.is_logged_in:
            print_error("Not logged in")
            return None
        
        try:
            profile = instaloader.Profile.from_username(self.loader.context, target_username)
            return profile
        except instaloader.exceptions.ProfileNotExistsException:
            print_error(f"Profile '{target_username}' does not exist")
            return None
        except Exception as e:
            print_error(f"Error fetching profile: {str(e)}")
            return None
    
    def fetch_followers(self, profile, limit=None):
        """Fetch followers list"""
        try:
            followers = []
            count = 0
            for follower in profile.get_followers():
                followers.append({
                    "username": follower.username,
                    "user_id": follower.userid,
                    "full_name": follower.full_name
                })
                count += 1
                if limit and count >= limit:
                    break
            
            if not self.quiet:
                print_success(f"Fetched {len(followers)} followers")
            return followers
        except Exception as e:
            print_error(f"Error fetching followers: {str(e)}")
            return []
    
    def fetch_following(self, profile, limit=None):
        """Fetch following list"""
        try:
            following = []
            count = 0
            for followee in profile.get_followees():
                following.append({
                    "username": followee.username,
                    "user_id": followee.userid,
                    "full_name": followee.full_name
                })
                count += 1
                if limit and count >= limit:
                    break
            
            if not self.quiet:
                print_success(f"Fetched {len(following)} following")
            return following
        except Exception as e:
            print_error(f"Error fetching following: {str(e)}")
            return []
    
    def download_posts(self, profile):
        """Download profile posts"""
        if not self.is_logged_in:
            return
        
        try:
            count = 0
            for post in profile.get_posts():
                self.loader.download_post(post, target=profile.username)
                count += 1
            
            if not self.quiet and count > 0:
                print_success(f"Downloaded {count} posts")
        except Exception as e:
            if not self.quiet:
                print_warning(f"Error downloading posts: {str(e)}")
    
    def download_highlights(self, profile):
        """Download profile highlights"""
        if not self.is_logged_in:
            return
        
        try:
            count = 0
            for highlight in self.loader.get_highlights(profile):
                for item in highlight.get_items():
                    self.loader.download_storyitem(item, target=profile.username)
                    count += 1
            
            if not self.quiet and count > 0:
                print_success(f"Downloaded {count} highlight items")
        except Exception as e:
            if not self.quiet:
                print_warning(f"Error downloading highlights: {str(e)}")
    
    def process_profile(self, target_username, options=None):
        """Complete profile processing pipeline"""
        options = options or {}
        
        if not self.quiet:
            print_header(f"PROCESSING {target_username}")
        
        # Fetch profile
        profile = self.fetch_profile(target_username)
        if not profile:
            return None
        
        if not self.quiet:
            print_info(f"Full Name: {profile.full_name}")
            print_info(f"ID: {profile.userid}")
            print_info(f"Followers: {profile.followers}")
            print_info(f"Following: {profile.followees}")
            print_info(f"Posts: {profile.mediacount}")
        
        # Fetch followers and following
        followers = self.fetch_followers(profile, options.get('limit_followers'))
        following = self.fetch_following(profile, options.get('limit_following'))
        
        # Calculate analytics
        analytics = None
        if options.get('analyze'):
            analytics = ProfileAnalytics(profile).get_analytics_summary()
            if not self.quiet and analytics:
                print_header("ANALYTICS")
                print_info(f"Profile Type: {analytics.get('profile_type')}")
                print_info(f"Engagement Rate: {analytics.get('engagement_rate')}")
                print_info(f"Follower Ratio: {analytics.get('follower_ratio')}")
                print_info(f"Risk Score: {analytics.get('risk_score')}/100")
        
        # Store in database
        if options.get('db'):
            db = OsintDatabase()
            db.save_profile(profile)
            db.save_followers(profile.username, followers)
            if analytics:
                db.save_analytics(profile.username, analytics)
            if not self.quiet:
                print_success("Data saved to database")
        
        # Download content
        if not options.get('no_download'):
            self.download_posts(profile)
            self.download_highlights(profile)
        
        # Export data
        results = {
            "profile": profile,
            "followers": followers,
            "following": following,
            "analytics": analytics
        }
        
        return results
    
    def batch_process(self, target_list, options=None):
        """Process multiple targets"""
        options = options or {}
        results = []
        
        for target in target_list:
            result = self.process_profile(target, options)
            if result:
                results.append(result)
            time.sleep(2)  # Rate limiting
        
        return results
    
    def export_results(self, results, target_username, formats='json'):
        """Export results in specified formats"""
        profile = results['profile']
        followers = results['followers']
        following = results['following']
        analytics = results['analytics']
        
        format_list = [f.strip().lower() for f in formats.split(',')]
        exported_files = []
        
        for fmt in format_list:
            try:
                if fmt == 'json':
                    file = Exporter.export_json(profile, followers, following, target_username, analytics)
                    exported_files.append(file)
                    if not self.quiet:
                        print_success(f"Exported to JSON: {file}")
                
                elif fmt == 'csv':
                    files = Exporter.export_csv(profile, followers, following, target_username)
                    exported_files.extend(files)
                    if not self.quiet:
                        for file in files:
                            print_success(f"Exported to CSV: {file}")
                
                elif fmt == 'html':
                    file = Exporter.export_html(profile, followers, following, target_username, analytics)
                    exported_files.append(file)
                    if not self.quiet:
                        print_success(f"Exported to HTML: {file}")
            except Exception as e:
                print_error(f"Error exporting to {fmt}: {str(e)}")
        
        return exported_files
