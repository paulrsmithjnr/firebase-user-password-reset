#!/usr/bin/env python3
"""
Firebase User Password Reset Script

This script resets a Firebase user's password to a default value using the Firebase Admin SDK.
"""

import argparse
import sys
from pathlib import Path

import firebase_admin
from firebase_admin import auth, credentials


def initialize_firebase(credentials_path: str) -> None:
    """
    Initialize Firebase Admin SDK with service account credentials.
    
    Args:
        credentials_path (str): Path to the Firebase service account JSON file
    """
    try:
        # Check if credentials file exists
        if not Path(credentials_path).exists():
            raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
        
        # Initialize the Firebase Admin SDK
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred)
        print(f"✅ Firebase Admin SDK initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        sys.exit(1)


def reset_user_password(user_id: str, new_password: str = "password123") -> bool:
    """
    Reset a Firebase user's password.
    
    Args:
        user_id (str): The UID of the user whose password should be reset
        new_password (str): The new password to set (default: "password123")
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Update the user's password
        auth.update_user(user_id, password=new_password)
        print(f"✅ Password successfully reset for user: {user_id}")
        return True
        
    except auth.UserNotFoundError:
        print(f"❌ User not found: {user_id}")
        return False
    except Exception as e:
        print(f"❌ Error resetting password for user {user_id}: {e}")
        return False


def get_user_info(user_id: str) -> dict:
    """
    Get basic information about a Firebase user.
    
    Args:
        user_id (str): The UID of the user
    
    Returns:
        dict: User information or None if user not found
    """
    try:
        user = auth.get_user(user_id)
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "disabled": user.disabled,
            "email_verified": user.email_verified
        }
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        print(f"❌ Error getting user info: {e}")
        return None


def main():
    """Main function to handle command line arguments and execute password reset."""
    parser = argparse.ArgumentParser(
        description="Reset Firebase user password to default value",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reset_password.py -u user123 -c firebase-credentials.json
  python reset_password.py --user-id user123 --credentials ./config/firebase-key.json --password newpass123
        """
    )
    
    parser.add_argument(
        "-u", "--user-id",
        required=True,
        help="Firebase user UID whose password should be reset"
    )
    
    parser.add_argument(
        "-c", "--credentials",
        required=True,
        help="Path to Firebase service account credentials JSON file"
    )
    
    parser.add_argument(
        "-p", "--password",
        default="password123",
        help="New password to set (default: password123)"
    )
    
    parser.add_argument(
        "--show-user-info",
        action="store_true",
        help="Display user information before resetting password"
    )
    
    args = parser.parse_args()
    
    print("🔥 Firebase Password Reset Tool")
    print("=" * 40)
    
    # Initialize Firebase
    initialize_firebase(args.credentials)
    
    # Show user info if requested
    if args.show_user_info:
        print(f"\n📋 Getting user information for: {args.user_id}")
        user_info = get_user_info(args.user_id)
        if user_info:
            print(f"  Email: {user_info['email']}")
            print(f"  Display Name: {user_info['display_name']}")
            print(f"  Email Verified: {user_info['email_verified']}")
            print(f"  Account Disabled: {user_info['disabled']}")
        else:
            print(f"❌ User {args.user_id} not found")
            sys.exit(1)
    
    # Reset password
    print(f"\n🔐 Resetting password for user: {args.user_id}")
    success = reset_user_password(args.user_id, args.password)
    
    if success:
        print(f"✅ Password reset completed successfully!")
        print(f"   New password: {args.password}")
    else:
        print("❌ Password reset failed")
        sys.exit(1)


if __name__ == "__main__":
    main() 