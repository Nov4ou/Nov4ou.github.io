#!/bin/bash

# Change to the blog root directory
cd _site

# Add all changed files to the staging area
git add --all

# Commit the changes with a short commit message
git commit -m "Updated blog content"

# Push the local repository to the remote repository
git push -u origin main --force

# Print a success message
echo "Blog deployed successfully!"
