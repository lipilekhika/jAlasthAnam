import dotenv, os, requests, shubhlipi as sh
from getpass import getpass
from cryptography.fernet import InvalidToken

dotenv.load_dotenv(".env.development")
KEY_NAME = "CLOUDFARE_DEPLOY_HOOK"
HOOK = os.getenv(KEY_NAME)
if HOOK:
    key = getpass("key: ")
    try:
        HOOK = sh.decrypt_text(HOOK, key)
        if input("Are you sure to deploy ? ") not in ("astu", "yes"):
            exit(-1)
        rq = requests.post(HOOK)
        print(sh.dump_json(rq.json()))
    except InvalidToken:
        print("Invalid Key")
else:
    print("DEPLOY_HOOK not found")
