import string
import random

chars = string.ascii_letters + string.digits


def generate_random_string(size: int):
    return ''.join(random.choice(chars) for _ in range(size))


print("Enter domain name:")
domain_name = input()

print("Enter your email:")
email = input()

db_user = "user_" + generate_random_string(5)
db_name = "db_" + generate_random_string(5)
db_password = generate_random_string(40)
db_root_password = generate_random_string(40)

secret_key = generate_random_string(50)

with open(".env", "w") as env:
    env.writelines([
        f"DOMAIN_NAME={domain_name}\n",
        f"CERTBOT_EMAIL={email}\n",
        f"MYSQL_DATABASE={db_name}\n",
        f"MYSQL_USER={db_user}\n",
        f"MYSQL_PASSWORD={db_password}\n",
        f"MYSQL_ROOT_PASSWORD={db_root_password}\n",
        f"WAIT_FOR_IT_TIME=60000\n",
        f"IS_DEBUG_VERSION=false\n"
        f"DEBUG=0\n"
        f"SECRET_KEY={secret_key}\n"
    ])
