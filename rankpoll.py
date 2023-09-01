import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from Config import *
from db import  DbStruct,BotDb
from  icecream import  ic
session = BotDb().session
class RankPoll(commands.Cog):
    def __init__(self,bot:discord.Client):
        self.bot = bot
    @app_commands.command(name="submit_poll")
    @app_commands.describe(user="user to make the poll on",conclusion="Upvote/Downvote",reason="why did you choose to upvote/downvote the user")
    @app_commands.choices(conclusion=[
        app_commands.Choice(name="Upvote",value=1),
        app_commands.Choice(name="Downvote",value=1)
    ])
    async def pollsubmit (self,interaction: discord.Interaction,user:discord.Member,conclusion:app_commands.Choice[int],reason:str):
        if interaction.channel.id != tier_submit_channel:
            channel = self.bot.get_channel(tier_submit_channel)
            await interaction.response.send_message(f"Wrong Channel,Check {channel.mention}",ephemeral=True)

        elif interaction.user.id == user.id:
            dm = await interaction.user.create_dm()
            await dm.send("You Cant make a poll about yourself")

        else:
            channel = self.bot.get_channel(admin_tier_submit)
            embed = discord.Embed(title="Rank Poll Submission", color=discord.Color.random())
            embed.add_field(name="Poll Submitted by", value=interaction.user.mention, inline=False)
            embed.add_field(name="Poll For", value=user.mention, inline=False)
            embed.add_field(name="Opinion", value=conclusion.name, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await channel.send(embed=embed)

    @app_commands.command(name="accept_poll")
    @app_commands.describe(message_link="link to the poll")
    @commands.has_permissions(administrator=True)
    async def accept_poll(self,interaction:discord.Interaction,message_link:str):
            original_message = await interaction.channel.fetch_message(int(message_link.split("/")[-1]))
            if interaction.channel.id != admin_tier_submit:
                channel = self.bot.get_channel(admin_tier_submit)
                await interaction.response.send_message(f"Wrong Channel,Check {channel.mention}", ephemeral=True)
            else:
                if original_message.embeds:
                    original_embed = original_message.embeds[0]  # Assuming there's only one embed
                    new_embed = discord.Embed(title="Rank Poll", color=original_embed.color)

                    for field in original_embed.fields:
                        new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
                    new_embed.set_footer(text="please provide your opinion using the reactions below")
                    channel = self.bot.get_channel(tier_submit_channel)
                    message = await channel.send(embed=new_embed)

                    embed_dict = new_embed.to_dict()
                    for field in embed_dict.get("fields", []):
                        if field.get("name") == "Poll For":
                            poll_for_value = field.get("value")
                            break
                    poll_for_user_id = str(poll_for_value.removeprefix("<@").removesuffix(">"))

                    ic(poll_for_value)
                    poll_db = DbStruct.tierpolls(message_id=message.id,voted_user=poll_for_user_id)
                    await message.add_reaction(upvote_reaction)
                    await message.add_reaction(neutral_reaction)
                    await message.add_reaction(downvote_reaction)
                    session.add(poll_db)
                    session.commit()

                else:
                    await interaction.response.send_mesasge("No embed found in the original message.",ephemeral=True)



async def setup(bot):
    await bot.add_cog(RankPoll(bot=bot))






    