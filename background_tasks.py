import discord
from discord.ext import commands, tasks
from db import DbStruct, BotDb
from Config import *

session = BotDb().session
from icecream import ic
import time


class BackgroundTasks(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.check_rank.start()
        self.check_polls.start()
        self.update_users_votes.start()
        self.update_members.start()
        self.check_discussion_submissions.start()
        self.db_backup.start()

    def cog_unload(self) -> None:
        self.check_rank.stop()
        self.check_polls.stop()
        self.update_users_votes.stop()
        self.update_members.stop()
        self.check_discussion_submissions.stop()
        self.db_backup.stop()

    @tasks.loop(seconds=2)
    async def check_rank(self):
        print("Started. loop")
        results = session.query(DbStruct.member).order_by(DbStruct.member.votes.desc())
        for member in results:
            # ["Tier 0","Tier F","Tier 1",'Tier 2','Tier 3']
            if member.votes >= rank_up_level:
                dis_member = self.bot.get_guild(Guild).get_member(member.user_id)
                roles = dis_member.roles
                for role in roles:
                    if role.name in tiers:
                        rank = str(role.name)
                        current_role_index = tiers.index(str(rank))
                        next_role_index = current_role_index + 1
                        if len(tiers) <= next_role_index:
                            pass
                        else:
                            await dis_member.add_roles(
                                discord.utils.get(
                                    self.bot.get_guild(Guild).roles,
                                    name=str(tiers[next_role_index]),
                                )
                            )  # Give Next Rank
                            await dis_member.remove_roles(
                                discord.utils.get(
                                    self.bot.get_guild(Guild).roles,
                                    name=str(tiers[current_role_index]),
                                )
                            )  # Remove last Rank
                            member.votes -= rank_up_level
                            member.rank = str(tiers[next_role_index])
                            session.commit()

                    else:
                        pass

                session.commit()
            elif member.votes <= -rank_up_level:
                dis_member = self.bot.get_guild(Guild).get_member(member.user_id)
                roles = dis_member.roles
                for role in roles:
                    if role.name in tiers:
                        rank = str(role.name)
                        current_role_index = tiers.index(str(rank))
                        next_role_index = current_role_index - 1
                        if next_role_index < 0:
                            pass
                        else:
                            await dis_member.add_roles(
                                discord.utils.get(
                                    self.bot.get_guild(Guild).roles,
                                    name=str(tiers[next_role_index]),
                                )
                            )  # Give lower Rank
                            await dis_member.remove_roles(
                                discord.utils.get(
                                    self.bot.get_guild(Guild).roles,
                                    name=str(tiers[current_role_index]),
                                )
                            )  # Remove last Rank
                            member.votes += rank_up_level
                            member.rank = str(tiers[next_role_index])
                            session.commit()

                    else:
                        pass

                session.commit()

    @tasks.loop(seconds=2)
    async def check_polls(self):
        # get all polls
        results = session.query(DbStruct.tierpolls).all()
        for poll in results:
            message = (
                await self.bot.get_guild(Guild)
                .get_channel(tier_submit_channel)
                .fetch_message(poll.id)
            )
            upvotes = 0
            downvotes = 0
            votes = 0
            for reaction in message.reactions:
                if reaction.emoji == upvote_reaction:
                    upvotes = reaction.count
                    votes += reaction.count
                elif reaction.emoji == downvote_reaction:
                    votes -= reaction.count
                    downvotes = reaction.count
                else:
                    pass
            poll.votes = votes
            poll.upvotes = upvotes
            poll.downvotes = downvotes
            session.commit()

    @tasks.loop(seconds=2)
    async def check_discussion_submissions(self):
        # get all polls
        results = session.query(DbStruct.discussion_ideas).all()
        for submission in results:
            message = (
                await self.bot.get_guild(Guild)
                .get_channel(prompt_submission_channel)
                .fetch_message(submission.id)
            )
            upvotes = 0
            downvotes = 0
            votes = 0
            for reaction in message.reactions:
                if reaction.emoji == upvote_reaction:
                    upvotes = reaction.count
                    votes += reaction.count
                elif reaction.emoji == downvote_reaction:
                    votes -= reaction.count
                    downvotes = reaction.count
                else:
                    pass
            submission.votes = votes
            submission.downvotes = downvotes
            submission.upvotes = upvotes
            session.commit()

    @tasks.loop(seconds=2)
    async def update_users_votes(self):
        results = session.query(DbStruct.tierpolls).all()
        for poll in results:
            member = (
                session.query(DbStruct.member)
                .filter(DbStruct.member.user_id == poll.voted_user)
                .first()
            )
            if member:
                member.votes -= poll.last_recorded
                member.votes += poll.votes
                poll.last_recorded = poll.votes
            session.commit()

    def get_all_members(self):
        members_info = []
        for member in self.bot.get_all_members():
            roles = member.roles
            for role in roles:
                if role.name in tiers:
                    rank = str(role.name)
                    break
                else:
                    rank = "Not Applied"
            members_info.append({member.id: {"username": member.name, "rank": rank}})
        return members_info

    @tasks.loop(seconds=1)
    async def update_members(self):
        for item in self.get_all_members():
            discord_id = (list(item.keys()))[0]
            usermame = item[discord_id]["username"]
            role = item[discord_id]["rank"]
            member = DbStruct.member(int(discord_id), str(usermame), str(role), 0, 0)
            mem = (
                session.query(DbStruct.member)
                .filter(DbStruct.member.user_id == discord_id)
                .first()
            )

            if mem:
                if mem == member:
                    pass
                else:
                    mem.username = usermame
                    mem.rank = role
                    session.commit()
            else:  # if the member isn't in the DB he will be inserted with 0 votes and 0 messages sent
                session.add(member)
                session.commit()

    @tasks.loop(seconds=720)
    async def db_backup(self):
        time.sleep(5)
        try:
            channel = self.bot.get_channel(db_backup_channel)
            await channel.send(file=discord.File("database.db"))
        except Exception as e:
            ic("Error uploading backup:", e)


async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))
