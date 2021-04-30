import discord
from discordClient import puppet


def mainProcess():
    bot = puppet.Puppet("ODIyNzY1NzQzMTkxODgzNzc2.YFXCTw.EUaNzgH1sU3YPOXFX9ycmMnFeOE")
    bot.connectToServer()


if __name__ == '__main__':
    mainProcess()
