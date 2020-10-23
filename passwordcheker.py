#password checker. This is hashing the password and  using the Have I been Pwned API v2 to check how many times it has been exposed to data breaches.

import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error fetching: {res.status_code} , check API and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def check_pwned_api(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = check_pwned_api(password)
        if count:
            print(f'{password} was found {count} times')
        else:
            print(f'{password} was not found')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

