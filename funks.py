#random functions used in more than one file
import discord

from Config import  *
def create_ratio_string(upvotes :int ,downvotes :int ,upchar:str = upvotes_char ,downchar:str = downvotes_char):
    winratio = (upvotes /(upvotes +downvotes))
    win_string = (upchar * int((10  * winratio)))
    win_string = win_string + (downchar * (10 - len(win_string)))
    return f"approval rate:{win_string} ({round((winratio * 100),2)}%)"


def create_embed(title:str,content:str,color:discord.Color):
    embed = discord.Embed(title=title,color=color)
    embed.add_field(name=content,value="")
    print(type(embed))
    return embed