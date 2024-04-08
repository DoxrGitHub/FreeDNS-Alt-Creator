import freedns
import getpass
import requests
import re
import os
import time # Import time module for sleep
from wonderwords import RandomWord
import random
import string
import json # Make sure to import json to parse JSON responses

r = RandomWord()

### --- sharkmail! ----
def hexstr(length):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))

def createsession():
    response = requests.get('https://www.sharklasers.com/ajax.php?f=get_email_address')
    data = response.text
    return data

headers = {
    'authority': 'www.sharklasers.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'ApiToken {hexstr(64)}',
    'cookie': '', # This will be set dynamically in the loop
    'referer': 'https://www.sharklasers.com/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Chrome OS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def check_email(session, headers):
  ses = json.loads(session)
  # Extract the first part of the email
  email_first_part = ses.get('email', '').split('@')[0]

  # Update the cookie in headers with the session ID
  headers['cookie'] = f'PHPSESSID={ses["sid_token"]}'

  # Use the extracted email part as the value for the 'in' parameter
  response = requests.get(f'https://www.sharklasers.com/ajax.php?f=check_email&seq=1&site=sharklasers.com&in={email_first_part}&_=1712514193424', headers=headers)
  data = response.json()
  return data

client = freedns.Client()

while True:
    print('\033[1;31mFreeDNS Alt Generator!\033[0m')

    print("Starting TempMail generation...")
    email = createsession() # Use the createsession function to get the email
    firstname = r.word(word_min_length=5, word_max_length=10)
    print('Generated Firstname: ' + firstname)
    lastname = r.word(word_min_length=4, word_max_length=8)
    print('Generated Lastname: ' + lastname)

    username = r.word(word_min_length=1, word_max_length=7) + r.word(word_min_length=1, word_max_length=7)
    if len(username) > 16:
        print("ERR: username must be under 16 characters.")
        continue
    print('Generated Username: ' + username)

    password = r.word(word_min_length=4, word_max_length=16)
    if len(password) < 4 or len(password) > 16:
        print("ERR: Password must be between 4 and 16 characters long.")
        continue
    print(f'Generated Password: {password}')

    print("Requesting Captcha...")
    captcha = client.get_captcha()
    print('We got a captcha! It\'s stored at /tmp/captcha.png, see image file if necessary.')
    with open("/tmp/captcha.png", "wb") as f:
        f.write(captcha)
    os.system("viu /tmp/captcha.png -h 18")
    captcha_code = input("Enter captcha (if you get this wrong, re-run this script): ")

    print("Creating account...")
    # Fetch email status before using it
    email_status = check_email(email, headers)
    client.create_account(captcha_code, firstname, lastname, username, password, email_status['email'])
    print("Activation email sent to TempMail - program waiting 25 seconds to recieve the email...")
    # Wait for 10 seconds before checking the email status
    time.sleep(25)
    email_status = check_email(email, headers)
    email_data = email_status['list']
    activation_url_pattern = r'http://freedns\.afraid\.org/signup/activate\.php\?([\w]+)'

    email_first_part = email_status['email'].split('@')[0]
    # Assuming email_status['list'] is the list of emails and email_first_part is already defined

    # Define the regex pattern for the activation URL
    activation_url_pattern = r'http://freedns\.afraid\.org/signup/activate\.php\?([\w]+)'
# replit is so fuck
    # Assuming `data` contains the email content
    for email_item in email_status['list']:
      mail_id = email_item.get('mail_id') # Adjust the key name as per the actual structure
      if mail_id:
          print(f'Extracted mail_id: {mail_id}')
          # Construct the URL for the new request
          url = f"https://www.sharklasers.com/ajax.php?f=fetch_email&email_id=mr_{mail_id}&site=sharklasers.com&in={email_first_part}&_=1712526343051"
          # Make the new request
          response = requests.get(url, headers=headers)
          data = response.json()

          # Extract the activation code from the email content
          activation_match = re.search(activation_url_pattern, data.get('mail_body', ''))
          if activation_match:
              activation_code = activation_match.group(1) # The first group is the activation code
              print(f'Activation code: {activation_code}')
              client.activate_account(activation_code)
          else:
              print("Activation code not found in the email content.")
    print("Account activated, creation finished.")

    with open("accounts.txt", "a") as f:
        print(email)
        f.write(f"Email: {email_status['email']}\nFirstname: {firstname}\nLastname: {lastname}\nUsername: {username}\nPassword: {password}\n\n")

    again = input("Do you want to enter another account? (y/n): ")
    if again.lower() != "y":
        break
