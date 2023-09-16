import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from Config import *
from db import DbStruct, BotDb
from icecream import ic
from funks import create_ratio_string, create_embed

session = BotDb().session


class Administration(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="clear")
    @app_commands.describe(n="how many messages to clear -1 = max")
    @commands.has_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction, n: int):
        channel = interaction.channel
        if n == -1:
            await channel.purge(limit=100)
            await interaction.channel.send(
                embed=create_embed(
                    "Success",
                    f"Purged 100 messages in {channel.mention} ✅",
                    color=discord.Color.green(),
                )
            )
        elif n > 100:
            n = 100
            await channel.purge(limit=int(n))
            await interaction.channel.send(
                embed=create_embed(
                    "Success",
                    f"Purged {n} messages in {channel.mention} ✅",
                    color=discord.Color.green(),
                )
            )
        else:
            await channel.purge(limit=int(n))
            await interaction.channel.send(
                embed=create_embed(
                    "Success",
                    f"Purged {n} messages in {channel.mention} ✅",
                    color=discord.Color.green(),
                )
            )

    @app_commands.command(name="ban")
    @app_commands.describe(
        user="Which user to ban", reason="why did you choose to ban the nig?"
    )
    @commands.has_permissions(administrator=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: str = "administrator rights",
    ):
        if interaction.user.id == user.id:
            await interaction.channel.send(
                embed=create_embed(
                    "Error",
                    "you can't ban yourself STUPEEED",
                    color=discord.Color.red(),
                )
            )
        else:
            try:
                await self.bot.get_guild(Guild).ban(user, reason=reason)
                await interaction.channel.send(
                    embed=create_embed(
                        "Success",
                        f"{user.mention} Banned ✅",
                        color=discord.Color.green(),
                    )
                )
                channel = await self.bot.create_dm(user)
                await channel.send(
                    f"you were banned in {self.bot.get_guild(Guild).name} Reason:{reason}"
                )
            except Exception as e:
                await interaction.channel.send(
                    embed=create_embed("Error", f"{str(e)}", color=discord.Color.red())
                )

    @app_commands.command(name="clear_votes")
    @app_commands.describe(
        user="Which user to clear his votes", reason="why did you choose to clear the votes of the nig?"
    )
    @commands.has_permissions(administrator=True)
    async def clear_votes(self, interaction: discord.Interaction,user:discord.User,reason:str):
        if interaction.user.id == user.id:
            await interaction.channel.send(
                embed=create_embed(
                    "Error",
                    "you can't clear the votes of yourself",
                    color=discord.Color.red(),
                )
            )
        else:
            try:
                member = session.query(DbStruct.member).filter(DbStruct.member.user_id == user.id).first()
                member.votes = 0
                session.commit()
                await interaction.channel.send(
                    embed=create_embed(
                        "Success",
                        f"{user.mention} cleared ✅",
                        color=discord.Color.green(),
                    )
                )
                channel = await self.bot.create_dm(user)
                await channel.send(
                    f"you'r votes were cleared and back to 0 in {self.bot.get_guild(Guild).name} Reason:{reason}"
                )
            except Exception as e:
                await interaction.channel.send(
                    embed=create_embed("Error", f"{str(e)}", color=discord.Color.red())
                )


async def setup(bot):
    await bot.add_cog(Administration(bot=bot))
