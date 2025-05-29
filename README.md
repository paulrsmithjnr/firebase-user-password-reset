# Firebase Password Reset Tool

A Python script that uses the Firebase Admin SDK to reset user passwords to a default value.

## Features

- Reset any Firebase user's password using their UID
- Customizable default password (defaults to "password123")
- User information display option
- Comprehensive error handling
- Command-line interface with helpful arguments

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Firebase project** with Authentication enabled
3. **Firebase service account credentials** (JSON file)

## Setup

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd firebase-password-reset

# Or download the files directly
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Firebase Service Account Credentials

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Navigate to **Project Settings** (gear icon) → **Service Accounts**
4. Click **Generate New Private Key**
5. Save the downloaded JSON file securely (e.g., `firebase-credentials.json`)

⚠️ **Important**: Never commit this credentials file to version control!

## Usage

### Basic Usage
```bash
python reset_password.py -u USER_UID -c path/to/firebase-credentials.json
```

### With Custom Password
```bash
python reset_password.py -u USER_UID -c firebase-credentials.json -p "mynewpassword"
```

### Show User Information First
```bash
python reset_password.py -u USER_UID -c firebase-credentials.json --show-user-info
```

### Command Line Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `--user-id` | `-u` | ✅ | Firebase user UID to reset password for |
| `--credentials` | `-c` | ✅ | Path to Firebase service account JSON file |
| `--password` | `-p` | ❌ | New password (default: "password123") |
| `--show-user-info` | | ❌ | Display user info before password reset |

### Examples

1. **Basic password reset:**
   ```bash
   python reset_password.py -u "abc123def456" -c "./firebase-key.json"
   ```

2. **Custom password:**
   ```bash
   python reset_password.py -u "abc123def456" -c "./firebase-key.json" -p "tempPassword2024"
   ```

3. **With user info display:**
   ```bash
   python reset_password.py -u "abc123def456" -c "./firebase-key.json" --show-user-info
   ```

## Finding User UIDs

To find a user's UID, you can:

1. **Firebase Console**: Go to Authentication → Users tab
2. **Firebase Admin SDK**: Use `auth.get_user_by_email()` 
3. **Client SDK**: Access `user.uid` property after authentication

## Error Handling

The script handles common errors:

- ❌ **User not found**: Invalid or non-existent user UID
- ❌ **Credentials error**: Invalid or missing service account file
- ❌ **Permission denied**: Insufficient Firebase Admin privileges
- ❌ **Network issues**: Connection problems with Firebase

## Troubleshooting

### "User not found" Error
- Verify the user UID is correct
- Check that the user exists in your Firebase project
- Ensure you're using the correct Firebase project credentials

### "Permission denied" Error
- Verify your service account has proper permissions
- Check that Firebase Authentication is enabled in your project
- Ensure the service account key is valid and not expired

### Import Errors
- Confirm Python 3.7+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Try using `python3` instead of `python`