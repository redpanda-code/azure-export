import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.secret"),
    **os.environ,
}


def main():
    print("Hello from azure-export!", config["CLIENT_ID"])


if __name__ == "__main__":
    main()
