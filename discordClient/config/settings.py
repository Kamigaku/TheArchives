import configparser
from discordClient.dal import dbContext

def saveConfig():
    with open("config.ini", "w") as f:
        configurationFile.write(f)

def registerCogChannel(cog_name: str, channel_id: str):
    configurationFile.set("COGS_CONFIGURATION", cog_name, channel_id)
    saveConfig()

def loadConfig():
    tempConfiguration = configparser.ConfigParser()
    tempConfiguration.read("config.ini")
    return tempConfiguration


configurationFile = loadConfig()
dbContext = dbContext.DbContext()
print(configurationFile.sections())
