import configparser

configurationFile = configparser.ConfigParser()
configurationFile.read("config.ini")
print(configurationFile.sections())
