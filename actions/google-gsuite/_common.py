import random
import string

body_template = """

Hello,

You have a new Google Account with the Sema4.ai organization.

Sign in to your Google Account to access the Google services your organization provides. For your security, the reset password link expires after 48 hours. After that, please contact your nea@sema4.ai for your password.

Your username: EMAIL_REPLACE
Password: PASSWORD_REPLACE
Note! You need to change your password after you sign in for the first time. After that, the given password will no longer work.


Click here to sign in https://accounts.google.com/


If you have any questions, feel free to reach out! 

Best,
Nea"""


def create_body_message(primary_email: str, password: str):
    body = body_template.replace("EMAIL_REPLACE", primary_email).replace(
        "PASSWORD_REPLACE", password
    )
    # template_body_file = (
    #     Path(__file__).absolute().parent / "body_message.txt"
    # )
    # with open(template_body_file,"w") as fout:
    #     fout.write(body)
    return body


def generate_password(length=12):
    if length < 12:
        raise ValueError("Password length must be at least 12 characters.")

    characters = string.ascii_letters + string.digits
    symbol = random.choice(string.punctuation)
    password = "".join(random.choice(characters) for i in range(length - 1)) + symbol
    password_list = list(password)
    random.shuffle(password_list)

    return "".join(password_list)
