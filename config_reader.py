import yaml

with open('config.yml') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

