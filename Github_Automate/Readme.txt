Generate token from github with classic all changes possible command. 

It should help you  with login. 

You can save it in your mac keychain and later reterieve it via command 
security find-generic-password -a your_github_username -s github_pat -w

# How to generate and save a GitHub Personal Access Token (PAT)

1. Go to https://github.com/settings/tokens and generate a new classic token with all necessary scopes.

2. Save your token securely in macOS keychain by running:

```bash
security add-generic-password -a your_github_username -s github_pat -w YOUR_TOKEN_HERE

3.     To retrieve the token later, run:

security find-generic-password -a your_github_username -s github_pat -w


---

