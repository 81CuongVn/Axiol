import random
import discord
import math
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix, getxprange


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def cog_check(self, ctx):
        GuildDoc = var.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Leveling") == True:
            return ctx.guild.id



    @commands.command()
    async def rank(self, ctx, rankuser:discord.Member=None):
        if rankuser is None:
            user = ctx.author
        else:
            user = rankuser

        GuildCol = var.LEVELDATABASE[str(ctx.guild.id)]
        userdata = GuildCol.find_one({"_id": user.id})
        if userdata is None:
                await ctx.send("The user does not have any rank yet...")
        else:
            xp = userdata["xp"]
            level = int(1 + math.sqrt(1+10 * xp/120 )/2)
            rankings = GuildCol.find().sort("xp", -1)
            rank = 0
            for i in rankings:
                rank += 1
                if userdata["_id"] == i["_id"]:
                    break

            embed = discord.Embed(
            title=f"Level stats for {user.name}",
            color=var.CTEAL
            ).add_field(name="Rank", value=f"{rank}/{GuildCol.estimated_document_count()-1}", inline=True
            ).add_field(name="XP", value=f"{xp}/{int(200*((1/2)*level))}", inline=True
            ).add_field(name="Level", value=level, inline=True
            ).set_thumbnail(url=user.avatar_url
            )
            if var.LEVELDATABASE[str(ctx.guild.id)].find_one({"_id":0}).get("status") == False:
                embed.set_footer(text="Leveling for this server is disabled this means the xp is still there but members won't gain any new xp")
            await ctx.channel.send(embed=embed)



    @commands.command()
    async def leaderboard(self, ctx):
        GuildCol = var.LEVELDATABASE[str(ctx.guild.id)]
        rankings = GuildCol.find({ "_id": { "$ne": 0 } }  ).sort("xp") #All documents (users) excluding document with id 0 (Configuration)
        embed = discord.Embed(
        title=f"Leaderboard", 
        color=var.CBLUE
        )
        rankcount = 0
        for i in rankings:
            rankcount += 1
            user = await ctx.guild.fetch_member(i.get("_id"))
            xp = i.get("xp")
            embed.add_field(name=f"{rankcount}: {user.name}", value=f"Total XP: {xp}", inline=False)
            if rankcount > 15:
                break
        await ctx.send(embed=embed)



    @commands.command()
    async def givexp(self, ctx, user:discord.Member=None, amount:int=None):
        if user and amount is not None:
            GuildCol = var.LEVELDATABASE[str(ctx.guild.id)]
            data = GuildCol.find_one({"_id": user.id})

            newdata = {"$set":{
                        "xp": data.get("xp") + amount
                    }}
            GuildCol.update_one(data, newdata)
            await ctx.send(f"Successfully awarded {user} with {amount} xp!")
        else:
            await ctx.send(f"You need to define the user and amount both, follow this format\n```{getprefix(ctx)}givexp <user> <amount>```\nFor user either user can be mentioned or ID can be used.")


    @commands.command()
    async def removexp(self, ctx, user:discord.Member=None, amount:int=None):
        if user and amount is not None:
            GuildCol = var.LEVELDATABASE[str(ctx.guild.id)]
            data = GuildCol.find_one({"_id": user.id})

            newdata = {"$set":{
                        "xp": data.get("xp") - amount
                    }}
            GuildCol.update_one(data, newdata)
            await ctx.send(f"Successfully removed {amount} xp from {user}!")
        else:
            await ctx.send(f"You need to define the user and amount both, follow this format\n```{getprefix(ctx)}removexp <user> <amount>```\nFor user either user can be mentioned or ID can be used.")


#Leveling Configs
    @commands.command()
    async def blacklist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = var.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newsettings = settings.get("blacklistedchannels").copy()
            newsettings.append(channel.id)
            newdata = {"$set":{
                "blacklistedchannels": newsettings
                }}
            GuildCol.update_one(settings, newdata)

            await ctx.send(embed=discord.Embed(
                        description=f"{channel.mention} has been blacklisted, hence users won't gain any xp in that channel.",
                        color=var.CGREEN)
                        )
        else:
            await ctx.send(f"Looks like you forgot to mention the channel, follow this format\n```{getprefix(ctx)}blacklist <#channel>```")

    @commands.command()
    async def whitelist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = var.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newsettings = settings.get("blacklistedchannels").copy()
            if channel.id in newsettings:
                newsettings.remove(channel.id)
            else:
                await ctx.send(f"{channel.mention} was not blacklisted")
            newdata = {"$set":{
                "blacklistedchannels": newsettings
                }}
            GuildCol.update_one(settings, newdata)

            await ctx.send(embed=discord.Embed(
                        description=f"{channel.mention} has been removed from blacklist, hence users will be able to gain xp again in that channel.",
                        color=var.CGREEN)
                        )
        else:
            await ctx.send(f"Looks like you forgot to mention the channel, follow this format\n```{getprefix(ctx)}blacklist <#channel>```")


    @commands.command()
    async def alertchannel(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = var.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newdata = {"$set":{
                "alertchannel": channel.id
                }}
            GuildCol.update_one(settings, newdata)
            await ctx.send(embed=discord.Embed(
                        description=f"{channel.mention} has been marked as the alert channel, hence users who will level up will get mentioned here!",
                        color=var.CGREEN)
                        )
        else:
            await ctx.send(f"Looks like you forgot to mention the channel, follow this format\n```{getprefix(ctx)}blacklist <#channel>```")

    @commands.command()
    async def xprange(self, ctx, minval:int=None, maxval:int=None):
        if minval and maxval is not None:
            GuildCol = var.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newdata = {"$set":{
                "xprange": [minval, maxval]
            }}
            GuildCol.update_one(settings, newdata)
            await ctx.send(embed=discord.Embed(
                        description=f"New xp range is now {minval} - {maxval}!",
                        color=var.CGREEN)
            )
        else:
            await ctx.send(f"Looks like you forgot to enter both minimum and maximum xp values, follow this format\n```{getprefix(ctx)}xprange <minxp> <maxxp>```")


    def cog_check(self, ctx):
        servers = []
        for i in var.PLUGINS.find({"Leveling": True}):
            servers.append(i.get("_id"))
            if ctx.guild.id in servers:
                return ctx.guild.id



    @commands.Cog.listener()
    async def on_message(self, message):
        GuildDoc = var.PLUGINS.find_one({"_id": message.guild.id})
        if GuildDoc.get("Leveling") == True:

            if not message.channel.id in var.LEVELDATABASE[str(message.guild.id)].find_one({"_id":0}).get("blacklistedchannels"):
                GuildDoc = var.LEVELDATABASE[str(message.guild.id)]
                userdata = GuildDoc.find_one({"_id": message.author.id})

                if userdata is None:
                    GuildDoc.insert_one({"_id": message.author.id, "xp": 0})
                else:
                    xp = userdata["xp"]
                    initlvl = int(1 + math.sqrt(1+10 * xp/120 )/2)
                    xp = userdata["xp"] + random.randint(getxprange(message)[0], getxprange(message)[1])
                    GuildDoc.update_one(userdata, {"$set": {"xp": xp}})
                    levelnow = int(1 + math.sqrt(1+10 * xp/120 )/2)
                    if levelnow > initlvl:
                        ch = self.bot.get_channel(GuildDoc.find_one({"_id":0}).get("alertchannel"))
                        if ch is not None:
                            await ch.send(f"{message.author.mention} you leveled up to level {levelnow}!")
                        else:
                            await message.channel.send(f"{message.author.mention} you leveled up to level {levelnow}!")



def setup(bot):
    bot.add_cog(Leveling(bot))