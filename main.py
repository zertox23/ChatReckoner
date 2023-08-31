import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from loguru import logger
import time
#from db import DbStruct,BotDb

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
Guild = 1146654542713331773
tiers = ['Tier 3','Tier 2',"Tier 1","Tier 0","Tier F"]
class utils:
    def get_all_members() -> list: #gets the necessary data to make a DbStruct.member object
        members_info = []
        for member in bot.get_all_members():
            roles = member.roles 
            for role in roles:
                if role in tiers:
                    role = roles
                    break
                else:
                    role = "Not Applied"
            members_info.append({member.id:{"username":member.name,"rank":role}})
        return members_info

class Ranks:    
    def __init__(self) -> None:
        pass
    
@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command[s]")
    except Exception as e:
        logger.error(str(e))


@bot.tree.command(name="get_members")
async def get_members(interaction: discord.Interaction):
    for item in utils.get_all_members():
        print(list(item.keys())[0])

bot.run("MTE0NjY1MDQwNTQ2ODY0MzQyOA.GqWqxn.7CYtsm1pDto_5MSNJpPJTSqUj7kyD11zRGlmBE")


