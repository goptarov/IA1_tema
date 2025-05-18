""" Data model for user accounts """

ACCOUNTS = {
    "user@example.com": "coolpass",
}


def check_login(email, password):
    if password == ACCOUNTS[email]:
        return True
    return False
