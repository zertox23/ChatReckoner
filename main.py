import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from loguru import logger
from icecream import ic
from db import BotDb,DbStruct
from Exceptions import Chtrc_Error
from Config import Guild,tiers
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



class utils:
    def get_all_members() -> list:  # gets the necessary data to make a DbStruct.member object
        members_info = []
        for member in bot.get_all_members():
            roles = member.roles
            for role in roles:  
                if role.name in tiers:
                    rank = str(role.name)
                    ic(rank)
                    break
                else:
                    rank = "Not Applied"
            members_info.append({member.id: {"username": member.name, "rank": rank}})
        return members_info
    def update_members():
        for item in utils.get_all_members():
            discord_id = (list(item.keys()))[0]
            usermame = item[discord_id]["username"]
            role = item[discord_id]["rank"]
            member = DbStruct.member(int(discord_id), str(usermame), str(role), 0, 0)
            mem = session.query(DbStruct.member).filter(DbStruct.member.user_id == discord_id).first()

            if mem:
                ic(mem)
                if mem == member:
                    ic("mem = member")
                    pass
                else:
                    mem.username = usermame
                    mem.rank = role
                    session.commit()
            else:  # if the member isn't in the DB he will be inserted with 0 votes and 0 messages sent
                session.add(member)
                session.commit()

    def increment_messages(discord_id:int,n:int=1) -> bool:
        mem = session.query(DbStruct.member).filter(DbStruct.member.user_id == discord_id).first()  # Get the member object
        if mem:
            mem.messages_sent += n
            session.commit()
            return True
        else:
            logger.error(f"discord_id [{discord_id}] not found")
            return False

    def dec_increment_votes(discord_id:int,n:int,increment:bool) -> bool:
        mem = session.query(DbStruct.member).filter(DbStruct.member.user_id == discord_id).first()  # Get the member object
        if mem:
            if increment:
                mem.votes += n
            else:
                mem.votes -= n
            session.commit()
            return True
        else:
            logger.error(f"discord_id [{discord_id}] not found")
            return False





session = BotDb().session




@bot.event
async def on_ready():
    print("Bot is up and ready!")
    await bot.load_extension("background_tasks")
    await bot.load_extension("rankpoll")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command[s]")
    except Exception as e:
        logger.error(str(e))

@bot.event
async def on_message(message):
    utils.increment_messages(message.author.id)

@bot.tree.command(name="update_members")
async def update_members(interaction: discord.Interaction):
        try:
            utils.update_members()
        except Exception as e:
            logger.error(str(e))

@bot.tree.command(name="increment_votes")
@app_commands.describe(user="user to add votes to",n="how many votes to add")
@commands.has_permissions(administrator = True)
async def increment_votes(interaction: discord.Interaction,user:discord.Member,n:int):
    try:
        res = utils.dec_increment_votes(user.id,n,True)
        if res:
            await interaction.response.send_message(f"Success. Added {n} Votes to {user.mention}")
        else:
            await interaction.response.send_message(f"Failed.")
    except Exception as e:
        await interaction.response.send_message(f"Failed. {e}")

@bot.tree.command(name="decrement_votes")
@app_commands.describe(user="user to add votes to",n="how many votes to add")
@commands.has_permissions(administrator = True)
async def decrement_votes(interaction: discord.Interaction,user:discord.Member,n:int):
    try:
        res = utils.dec_increment_votes(user.id,n,False)
        if res:
            await interaction.response.send_message(f"Success. Removed {n} Votes to {user.mention}")
        else:
            await interaction.response.send_message(f"Failed.")
    except Exception as e:
        await interaction.response.send_message(f"Failed. {e}")




class Ranks:
    def __init__(self) -> None:
        pass


bot.run("MTE0NjY1MDQwNTQ2ODY0MzQyOA.GDUVOF.D7wScdQsucCtL5MxBBIo8LSxzaJZf5EH9pHOYA")
