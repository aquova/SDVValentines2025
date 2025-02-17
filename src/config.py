import yaml

_CONFIG_PATH = "./private/config.yaml"
with open(_CONFIG_PATH, 'r') as config_file:
    cfg = yaml.safe_load(config_file)

TMP_PATH = "./private/tmp"

DISCORD_KEY = cfg['discord']
ADMIN_ROLES = cfg['roles']['admin']
EVENT_ROLES = cfg['roles']['event']
REDIRECT_CHANNELS = cfg['channels']['redirect']
JUDGE_CHANNELS = cfg['channels']['judge']
