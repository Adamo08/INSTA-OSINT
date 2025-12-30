"""Analytics engine for Instagram profiles"""

class ProfileAnalytics:
    """Analyze Instagram profile metrics"""
    
    def __init__(self, profile):
        self.profile = profile
    
    def get_engagement_rate(self):
        """Calculate estimated engagement rate (followers / posts)"""
        if self.profile.mediacount == 0:
            return 0
        return round(self.profile.followers / self.profile.mediacount, 2)
    
    def get_follower_following_ratio(self):
        """Calculate follower to following ratio"""
        if self.profile.followees == 0:
            return self.profile.followers
        return round(self.profile.followers / self.profile.followees, 2)
    
    def get_profile_risk_score(self):
        """Calculate risk score (higher = more suspicious)
        Based on: low engagement, many following, few followers, no posts"""
        risk = 0
        
        # High following, low followers = risky
        if self.profile.followees > self.profile.followers * 2:
            risk += 30
        
        # No posts but many followers = suspicious
        if self.profile.mediacount == 0 and self.profile.followers > 100:
            risk += 25
        
        # Low engagement
        if self.profile.mediacount > 0:
            engagement = self.get_engagement_rate()
            if engagement < 1:
                risk += 20
        
        # Likely bot indicators
        if self.profile.is_private == False and self.profile.is_business_account == False and self.profile.followers > 1000:
            if self.profile.mediacount == 0:
                risk += 25
        
        return min(risk, 100)
    
    def get_profile_type(self):
        """Classify profile type"""
        if self.profile.is_business_account:
            return "Business Account"
        if self.profile.is_private:
            return "Private Account"
        if self.profile.followers > 10000:
            return "Influencer"
        if self.profile.mediacount == 0:
            return "Inactive/Potential Bot"
        return "Regular Account"
    
    def get_analytics_summary(self):
        """Get complete analytics summary"""
        return {
            "engagement_rate": self.get_engagement_rate(),
            "follower_ratio": self.get_follower_following_ratio(),
            "risk_score": self.get_profile_risk_score(),
            "profile_type": self.get_profile_type(),
            "posts_per_follower": round(self.profile.mediacount / max(self.profile.followers, 1), 4),
            "following_percentage": round((self.profile.followees / max(self.profile.followers, 1)) * 100, 2) if self.profile.followers > 0 else 0
        }


class ComparativeAnalytics:
    """Compare multiple profiles"""
    
    @staticmethod
    def compare_profiles(profile_list):
        """Compare multiple profiles and return insights"""
        if not profile_list:
            return {}
        
        analytics_list = [ProfileAnalytics(p) for p in profile_list]
        
        total_followers = sum(p.profile.followers for p in profile_list)
        total_following = sum(p.profile.followees for p in profile_list)
        total_posts = sum(p.profile.mediacount for p in profile_list)
        
        return {
            "profile_count": len(profile_list),
            "total_followers": total_followers,
            "total_following": total_following,
            "total_posts": total_posts,
            "avg_followers": round(total_followers / len(profile_list), 0),
            "avg_following": round(total_following / len(profile_list), 0),
            "avg_posts": round(total_posts / len(profile_list), 0),
            "profiles": [a.get_analytics_summary() for a in analytics_list]
        }
    
    @staticmethod
    def find_mutual_followers(followers_list1, followers_list2):
        """Find mutual followers between two follower lists"""
        usernames1 = {f["username"] for f in followers_list1}
        usernames2 = {f["username"] for f in followers_list2}
        
        mutual = usernames1.intersection(usernames2)
        
        # Reconstruct mutual follower objects
        mutual_followers = [f for f in followers_list1 if f["username"] in mutual]
        
        return {
            "mutual_count": len(mutual),
            "mutual_followers": mutual_followers,
            "percentage_of_first": round((len(mutual) / len(followers_list1)) * 100, 2) if followers_list1 else 0,
            "percentage_of_second": round((len(mutual) / len(followers_list2)) * 100, 2) if followers_list2 else 0
        }
