import configparser
import os
import time

#path = fr'{os.path.abspath(__file__)[:-17]}\config\config.ini'
path = 'config.ini'

def create_config():

    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "bot_token", "1650826029:AAF0PKdJJK4dWvD9j13hRpYfkMomY1FskOs")
    config.set("Settings", "admin_group", "-773430667")
    config.set("Settings", "admin_id", "373668569")
    config.set("Settings", "qiwi_number", "+79398013229")
    config.set("Settings", "qiwi_token", "4b5d4b6ecbdd05e53ba522f536633b0d")
    config.set("Settings", "coder_link", "end_soft")
    config.set("Settings", "proxy_api", "mttx15ewy3hsxhcgae97426ajiv1gp50ls9bloic")
    config.set("Settings", "vds_api", "0")
    config.set("Settings", "cheating_api", "f1c562a878da0ecc6c28c9c961ef3dc1")
    config.set("Settings", "proxy_percent", "11000")
    config.set("Settings", "ref_percent", "5")


    
    with open(path, "w") as config_file:
        config.write(config_file)


def check_config_file():
    if not os.path.exists(path):
        create_config()
        
        print('Config created')
        time.sleep(3)
        exit(0)


def config(what):
    src = None
    config = configparser.ConfigParser()
    config.read(f'config.ini')

    if what != "qiwi_token" and what != "qiwi_number":
        src = 'config'
        value = config.get("Settings", what)
    else:
        import sqlite3

        path1 = './data/database.db'
        connect = sqlite3.connect(path1)
        cur = connect.cursor()
        cur.execute(f"SELECT {what} FROM qiwi_data")
        value = cur.fetchone()[0]
        src = 'db'

    print(f'[CONFIG]: {what} = {value} | SOURCE: {src}')
    return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path)

    config.set("Settings", setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)

check_config_file()



