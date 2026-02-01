#!/usr/bin/env python3

# Read the content of index.html
with open('index.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Fix the header to be sticky on all screen sizes
content = content.replace('md:static md:relative', '')

# Write the modified content back to the file
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(content)

print("L'en-tête est maintenant fixe sur tous les écrans!")