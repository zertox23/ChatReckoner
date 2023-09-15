import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from loguru import logger
from icecream import ic
from db import BotDb,DbStruct
from Exceptions import Chtrc_Error
from Config import Guild,tiers
from funks import create_embed
import asyncio
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())









session = BotDb().session


class utils:
    @staticmethod
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

    @staticmethod
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
                ic(f"{mem}, Inceremented {n} votes")
            else:
                mem.votes -= n
                ic(f"{mem}, decremented {n} votes")
            session.commit()
            return True
        else:
            logger.error(f"discord_id [{discord_id}] not found")
            return False


@bot.event
async def on_ready():
    print("Bot is up and ready!")
    await bot.load_extension("background_tasks")
    await bot.load_extension("rankpoll")
    await bot.load_extension("discussions")
    await bot.load_extension("administration")
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
            await interaction.response.defer()
            await interaction.followup.send(embed=create_embed(" ","Success server status updated",color=discord.Color.green()))
        except Exception as e:
            logger.error(str(e))

@bot.tree.command(name="increment_votes")
@app_commands.describe(user="user to add votes to",n="how many votes to add")
@commands.has_permissions(administrator = True)
async def increment_votes(interaction: discord.Interaction, user: discord.Member, n: int):
        try:
            res = utils.dec_increment_votes(user.id, n, True)
            if res:
                await interaction.response.defer()
                await interaction.followup.send(embed=create_embed(" ", f"Success. Added {n} Votes to {user.mention}",
                                                                   color=discord.Color.green()))
            else:
                await interaction.response.defer()
                await interaction.followup.send(embed=create_embed("Error", "Failed.", color=discord.Color.red()))
        except Exception as e:
            await interaction.response.defer()
            await interaction.followup.send(embed=create_embed("Error", f"Failed,{str(e)}", color=discord.Color.red()))
@bot.tree.command(name="decrement_votes")
@app_commands.describe(user="user to add votes to",n="how many votes to add")
@commands.has_permissions(administrator = True)
async def decrement_votes(interaction: discord.Interaction,user:discord.Member,n:int):
    try:
        res = utils.dec_increment_votes(user.id,n,False)
        if res:
            await interaction.response.defer()
            await interaction.followup.send(embed=create_embed(" ",f"Success. Removed {n} Votes to {user.mention}",color=discord.Color.green()))
        else:
            await interaction.response.defer()
            await interaction.followup.send(embed=create_embed("Error","Failed.",color=discord.Color.red()))
    except Exception as e:
        await interaction.response.defer()
        await interaction.followup.send(embed=create_embed("Error", f"Failed,{str(e)}", color=discord.Color.red()))


@bot.tree.command(name="derank")
@app_commands.describe(user="user to derank")
@commands.has_permissions(administrator=True)
async def derank(interaction:discord.Interaction,user:discord.Member):
    dis_member = bot.get_guild(Guild).get_member(user.id)
    roles = dis_member.roles
    for role in roles:
        if role.name in tiers:
            rank = str(role.name)
            current_role_index = tiers.index(str(rank))
            next_role_index = current_role_index - 1
            if next_role_index < 0:
                pass
            else:
                await dis_member.add_roles(discord.utils.get(bot.get_guild(Guild).roles, name=str(
                    tiers[next_role_index])))  # Give lower Rank
                await dis_member.remove_roles(discord.utils.get(bot.get_guild(Guild).roles, name=str(
                    tiers[current_role_index])))  # Remove last Rank
                await interaction.response.defer()
                await interaction.followup.send(embed=create_embed(" ",f"Deranked {user.mention} successfully",color=discord.Color.green()))


@bot.tree.command(name="uprank")
@app_commands.describe(user="user to uprank")
@commands.has_permissions(administrator=True)
async  def uprank(interaction:discord.Interaction,user:discord.Member):
    dis_member = bot.get_guild(Guild).get_member(user.id)
    roles = dis_member.roles
    for role in roles:
        if role.name in tiers:
            rank = str(role.name)
            current_role_index = tiers.index(str(rank))
            next_role_index = current_role_index + 1
            if len(tiers) <= next_role_index:
                pass
            else:
                await dis_member.add_roles(discord.utils.get(bot.get_guild(Guild).roles,
                                                             name=str(tiers[next_role_index])))  # Give Next Rank
                await dis_member.remove_roles(discord.utils.get(bot.get_guild(Guild).roles, name=str(
                    tiers[current_role_index])))  # Remove last Rank
                await interaction.response.defer()
                await interaction.followup.send(embed=create_embed(" ", f"upranked {user.mention} successfully",color=discord.Color.green()))

@bot.tree.command(name="show_user_info")
@app_commands.describe(user="user to display info of")
async def show_user_info(interaction:discord.Interaction,user:discord.Member):
    member = session.query(DbStruct.member).filter(DbStruct.member.user_id == user.id).first()
    if member:
        embed = discord.Embed(title="User Info Request",color= discord.Color.random())
        embed.add_field(name="User Id",value=str(member.user_id), inline=False)
        embed.add_field(name="Username",value=str(member.username), inline=False)
        embed.add_field(name="Rank",value=str(member.rank), inline=False)
        embed.add_field(name="Current Votes",value=str(member.votes), inline=False)
        embed.add_field(name="messages Sent",value=str(member.messages_sent), inline=False)
        await interaction.response.defer()
        #asyncio.sleep()
        await interaction.followup.send(embed=embed)
    else:
        await interaction.response.defer()
        await interaction.followup.send(f"User Not Found 404")





class Ranks:
    def __init__(self) -> None:
        pass


bot.run("MTE0NjY1MDQwNTQ2ODY0MzQyOA.GPM6H9._fS2VDBPqLDFuNQyXtRJMSLtrRKgc07rwveKdQ")
