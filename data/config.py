from environs import Env


env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
admins = env.list("ADMINS")  # admins
ADMINS = [int(admin) for admin in admins]


