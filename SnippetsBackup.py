"""
GitHub companion module for SnippetsBackup
Author: LEE WEI HAO JONATHAN (buildevol)
"""

import GitHub

# Show main menu
display_main_menu = True
while display_main_menu:
    print("""Main Menu
=========
1. Backup a single GitHub Gist.
2. Backup all snippets from a GitHub username.""")

    user_input = input("Enter a valid option (for example: 1): ")
    if user_input == '1':
        GitHub.backup_single_github_gist()
        break
    elif user_input == '2':
        GitHub.backup_gist_from_username()
        break
    else:
        print("Invalid Input.\n")
        continue
