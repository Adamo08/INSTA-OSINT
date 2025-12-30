"""Export functionality for multiple formats"""

import json
import csv
from datetime import datetime
from utils import Gr, Re, Wh, Ye

class Exporter:
    """Handle exports in multiple formats"""
    
    @staticmethod
    def export_json(profile, followers_list, followees_list, username, analytics=None):
        """Export to JSON format"""
        data = {
            "export_date": datetime.now().isoformat(),
            "profile": {
                "username": profile.username,
                "full_name": profile.full_name,
                "user_id": profile.userid,
                "biography": profile.biography,
                "external_url": profile.external_url,
                "is_private": profile.is_private,
                "is_business_account": profile.is_business_account,
                "business_category": profile.business_category_name,
                "followers_count": profile.followers,
                "following_count": profile.followees,
                "posts_count": profile.mediacount,
                "profile_pic_url": profile.profile_pic_url
            },
            "followers": followers_list,
            "following": followees_list
        }
        
        if analytics:
            data["analytics"] = analytics
        
        filename = f"{username}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    @staticmethod
    def export_csv(profile, followers_list, followees_list, username):
        """Export to CSV format"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Profile CSV
        profile_file = f"{username}_profile_{timestamp}.csv"
        with open(profile_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Username', profile.username])
            writer.writerow(['Full Name', profile.full_name])
            writer.writerow(['User ID', profile.userid])
            writer.writerow(['Biography', profile.biography])
            writer.writerow(['External URL', profile.external_url])
            writer.writerow(['Is Private', profile.is_private])
            writer.writerow(['Is Business', profile.is_business_account])
            writer.writerow(['Followers', profile.followers])
            writer.writerow(['Following', profile.followees])
            writer.writerow(['Posts', profile.mediacount])
        
        # Followers CSV
        followers_file = f"{username}_followers_{timestamp}.csv"
        with open(followers_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'user_id', 'full_name'])
            writer.writeheader()
            writer.writerows(followers_list)
        
        # Following CSV
        following_file = f"{username}_following_{timestamp}.csv"
        with open(following_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'user_id', 'full_name'])
            writer.writeheader()
            writer.writerows(followees_list)
        
        return profile_file, followers_file, following_file
    
    @staticmethod
    def export_html(profile, followers_list, followees_list, username, analytics=None):
        """Export to HTML report format"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{username}_report_{timestamp}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Instagram OSINT Report - {username}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; border-bottom: 2px solid #e1306c; padding-bottom: 10px; }}
                h2 {{ color: #555; margin-top: 30px; border-left: 4px solid #e1306c; padding-left: 10px; }}
                .profile-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .profile-item {{ background-color: #f9f9f9; padding: 10px; border-radius: 4px; }}
                .profile-item strong {{ color: #e1306c; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th {{ background-color: #e1306c; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .analytics {{ background-color: #f0f8ff; padding: 15px; border-radius: 4px; margin: 10px 0; }}
                .timestamp {{ color: #999; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Instagram OSINT Report</h1>
                
                <h2>Profile Information</h2>
                <div class="profile-section">
                    <div class="profile-item">
                        <strong>Username:</strong> {profile.username}
                    </div>
                    <div class="profile-item">
                        <strong>User ID:</strong> {profile.userid}
                    </div>
                    <div class="profile-item">
                        <strong>Full Name:</strong> {profile.full_name}
                    </div>
                    <div class="profile-item">
                        <strong>Followers:</strong> {profile.followers:,}
                    </div>
                    <div class="profile-item">
                        <strong>Following:</strong> {profile.followees:,}
                    </div>
                    <div class="profile-item">
                        <strong>Posts:</strong> {profile.mediacount}
                    </div>
                    <div class="profile-item">
                        <strong>Private:</strong> {"Yes" if profile.is_private else "No"}
                    </div>
                    <div class="profile-item">
                        <strong>Business Account:</strong> {"Yes" if profile.is_business_account else "No"}
                    </div>
                </div>
                
                <div class="profile-section">
                    <div class="profile-item">
                        <strong>Biography:</strong><br>{profile.biography or "N/A"}
                    </div>
                    <div class="profile-item">
                        <strong>External URL:</strong><br>{profile.external_url or "N/A"}
                    </div>
                </div>
        """
        
        if analytics:
            html_content += f"""
                <div class="analytics">
                    <h2>📈 Analytics</h2>
                    <div class="profile-section">
                        <div class="profile-item">
                            <strong>Engagement Rate:</strong> {analytics.get('engagement_rate', 'N/A')}
                        </div>
                        <div class="profile-item">
                            <strong>Follower Ratio:</strong> {analytics.get('follower_ratio', 'N/A')}
                        </div>
                        <div class="profile-item">
                            <strong>Profile Type:</strong> {analytics.get('profile_type', 'N/A')}
                        </div>
                        <div class="profile-item">
                            <strong>Risk Score:</strong> {analytics.get('risk_score', 'N/A')}/100
                        </div>
                    </div>
                </div>
            """
        
        html_content += f"""
                <h2>Followers ({len(followers_list)})</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>User ID</th>
                            <th>Full Name</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for follower in followers_list[:100]:  # Limit to first 100 for performance
            html_content += f"""
                        <tr>
                            <td>{follower.get('username', 'N/A')}</td>
                            <td>{follower.get('user_id', 'N/A')}</td>
                            <td>{follower.get('full_name', 'N/A')}</td>
                        </tr>
            """
        
        if len(followers_list) > 100:
            html_content += f"""
                        <tr>
                            <td colspan="3"><em>... and {len(followers_list) - 100} more followers</em></td>
                        </tr>
            """
        
        html_content += f"""
                    </tbody>
                </table>
                
                <h2>Following ({len(followees_list)})</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>User ID</th>
                            <th>Full Name</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for followee in followees_list[:100]:
            html_content += f"""
                        <tr>
                            <td>{followee.get('username', 'N/A')}</td>
                            <td>{followee.get('user_id', 'N/A')}</td>
                            <td>{followee.get('full_name', 'N/A')}</td>
                        </tr>
            """
        
        if len(followees_list) > 100:
            html_content += f"""
                        <tr>
                            <td colspan="3"><em>... and {len(followees_list) - 100} more following</em></td>
                        </tr>
            """
        
        html_content += f"""
                    </tbody>
                </table>
                
                <p class="timestamp">Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
