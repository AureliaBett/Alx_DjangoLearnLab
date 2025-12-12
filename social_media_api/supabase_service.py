"""
Supabase integration service for Django
Handles Supabase client initialization and interactions
"""
import os
from typing import Optional
from supabase import create_client, Client


class SupabaseService:
    """
    Singleton service for Supabase client management
    Usage: supabase = SupabaseService.get_client()
    """
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """
        Get or create the Supabase client instance
        
        Returns:
            Client: Supabase client instance
            
        Raises:
            ValueError: If SUPABASE_URL or SUPABASE_KEY not in environment
        """
        if cls._instance is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_KEY environment variables must be set. "
                    "See SUPABASE_SETUP_GUIDE.md for instructions."
                )
            
            cls._instance = create_client(url, key)
        
        return cls._instance
    
    @classmethod
    def reset_client(cls):
        """Reset the client instance (useful for testing)"""
        cls._instance = None


# Quick access
def get_supabase() -> Client:
    """Convenience function to get Supabase client"""
    return SupabaseService.get_client()


# Example usage in views:
# from social_media_api.supabase_service import get_supabase
# supabase = get_supabase()
# response = supabase.table('posts_post').select('*').execute()
