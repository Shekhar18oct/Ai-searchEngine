import os
import webbrowser

def setup_api_keys():
    print("Welcome to the API Keys Setup Wizard!")
    print("This script will help you set up your API keys for various services.")
    print("\n" + "="*50 + "\n")

    # Check if .env file exists
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('# API Keys Configuration\n\n')

    # YouTube API Setup
    print("1. YouTube API Setup:")
    print("   a. Go to https://console.cloud.google.com/")
    print("   b. Create a new project")
    print("   c. Enable YouTube Data API v3")
    print("   d. Create credentials (API key)")
    input("\nPress Enter to open Google Cloud Console...")
    webbrowser.open('https://console.cloud.google.com/')
    youtube_key = input("Enter your YouTube API Key (or press Enter to skip): ").strip()

    # GitHub API Setup
    print("\n2. GitHub API Setup:")
    print("   a. Go to https://github.com/settings/tokens")
    print("   b. Click 'Generate new token (classic)'")
    print("   c. Select scopes: public_repo, read:repo_hook")
    print("   d. Generate and copy the token")
    input("\nPress Enter to open GitHub Token settings...")
    webbrowser.open('https://github.com/settings/tokens')
    github_token = input("Enter your GitHub Token (or press Enter to skip): ").strip()

    # Stack Overflow API Setup
    print("\n3. Stack Overflow API Setup:")
    print("   a. Go to https://stackapps.com/apps/oauth/register")
    print("   b. Register your application")
    print("   c. Get your API key")
    input("\nPress Enter to open Stack Apps registration...")
    webbrowser.open('https://stackapps.com/apps/oauth/register')
    stackoverflow_key = input("Enter your Stack Overflow API Key (or press Enter to skip): ").strip()

    # Google Custom Search Setup
    print("\n4. Google Custom Search Setup (Optional):")
    print("   a. Go to https://programmablesearchengine.google.com/")
    print("   b. Create a new search engine")
    print("   c. Get your Search Engine ID and API key")
    google_search_key = input("Enter your Google Search API Key (or press Enter to skip): ").strip()
    google_search_id = input("Enter your Google Search Engine ID (or press Enter to skip): ").strip()

    # Update .env file
    env_content = []
    with open('.env', 'r') as f:
        env_content = f.readlines()

    # Function to update or add environment variable
    def update_env_var(content, var_name, var_value):
        if not var_value:
            return content
        
        var_line = f"{var_name}={var_value}\n"
        for i, line in enumerate(content):
            if line.startswith(f"{var_name}="):
                content[i] = var_line
                return content
        content.append(var_line)
        return content

    # Update all environment variables
    if youtube_key:
        env_content = update_env_var(env_content, "YOUTUBE_API_KEY", youtube_key)
    if github_token:
        env_content = update_env_var(env_content, "GITHUB_TOKEN", github_token)
    if stackoverflow_key:
        env_content = update_env_var(env_content, "STACKOVERFLOW_KEY", stackoverflow_key)
    if google_search_key:
        env_content = update_env_var(env_content, "GOOGLE_SEARCH_API_KEY", google_search_key)
    if google_search_id:
        env_content = update_env_var(env_content, "GOOGLE_SEARCH_ENGINE_ID", google_search_id)

    # Write updated content back to .env file
    with open('.env', 'w') as f:
        f.writelines(env_content)

    print("\nAPI keys have been updated successfully!")
    print("You can now restart your application to use the new API keys.")

if __name__ == "__main__":
    setup_api_keys()
