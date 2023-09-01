import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from Config import *
from db import  DbStruct,BotDb
from  icecream import  ic
session = BotDb().session

class Prompt_Submissions(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="submit_prompt")
    @app_commands.describe(prompt="idea to discuss", discussion_channel="which channel to discuss this idea on")
    async def submit_prompt(self,interaction:discord.Interaction,prompt:str,discussion_channel:discord.TextChannel):
        if interaction.channel.id != prompt_submission_channel:
            channel = self.bot.get_channel(prompt_submission_channel)
            await interaction.response.send_message(f"Wrong Channel,Check {channel.mention}",ephemeral=True)

        else:
            await interaction.response.send_message("Idea Submitted.waiting for admin approval", ephemeral=True)
            channel = self.bot.get_channel(admin_prompt_submission_channel)
            embed = discord.Embed(title="Discussion Idea Submission", color=discord.Color.random())
            embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)
            embed.add_field(name="Prompt", value=prompt, inline=False)
            embed.add_field(name="discuss it in", value=discussion_channel.mention, inline=False)
            await channel.send(embed=embed)

    @app_commands.command(name="accept_submission")
    @app_commands.describe(message_link="link to the submission")
    @commands.has_permissions(administrator=True)
    async def accept_submission(self,interaction:discord.Interaction,message_link:str):
        original_message = await interaction.channel.fetch_message(int(message_link.split("/")[-1]))
        if interaction.channel.id != admin_prompt_submission_channel:
            channel = self.bot.get_channel(admin_prompt_submission_channel)
            await interaction.response.send_message(f"Wrong Channel,Check {channel.mention}", ephemeral=True)
        else:
            if original_message.embeds:
                original_embed = original_message.embeds[0]  # Assuming there's only one embed
                new_embed = discord.Embed(title="Discussion Idea", color=original_embed.color)

                for field in original_embed.fields:
                    new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
                new_embed.set_footer(text="react to this message, upvote if you like the idea, downvote if you don't")
                embed_dict = new_embed.to_dict()
                for field in embed_dict.get("fields", []):
                    if field.get("name") == "Submitted by":
                        submitted_by = field.get("value")
                        break
                channel = self.bot.get_channel(prompt_submission_channel)
                message = await channel.send(embed=new_embed)
                await interaction.response.send_message(f"Successfuly Posted in {channel.mention}")

                submitted_by = str(submitted_by.removeprefix("<@").removesuffix(">"))
                submission_db = DbStruct.discussion_ideas(id=message.id,submitted_by=int(submitted_by))
                await message.add_reaction(upvote_reaction)
                await message.add_reaction(neutral_reaction)
                await message.add_reaction(downvote_reaction)
                session.add(submission_db)
                session.commit()


            else:
                await interaction.response.send_message("No embed found in the original message.", ephemeral=True)



async def setup(bot):
    await bot.add_cog(Prompt_Submissions(bot=bot))