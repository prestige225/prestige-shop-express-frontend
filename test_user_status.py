import requests
import json

# Test the API endpoint to see what it returns for users
try:
    response = requests.get("http://localhost:5000/api/users")
    if response.status_code == 200:
        data = response.json()
        print("API Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Check if we have users data
        if data.get('success') and 'users' in data:
            users = data['users']
            print(f"\nFound {len(users)} users:")
            for user in users:
                print(f"- ID: {user['id']}, Name: {user.get('nom_complet', 'N/A')}, Email: {user['email']}")
                print(f"  Status: {user['statut']}, Connection Status: {user['statut_connexion']}")
                print(f"  Last Connection: {user.get('derniere_connexion', 'N/A')}")
                print()
        else:
            print("No users data found in response")
    else:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error connecting to API: {e}")