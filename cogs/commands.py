import asyncio
import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(
        title="My Github Source Code Woohoo", 
        description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)", 
        color=var.CTEAL
        ).set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/shift-logotypes/32/Github-512.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
        title="My invite link!",
        description="[Invite me from here](https://discord.com/api/oauth2/authorize?client_id=843484459113775114&permissions=8&scope=bot)",
        color=var.CBLUE
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def suggest(self, ctx, *, desc=None):
        if desc is not None:
            channel = self.bot.get_channel(843548616505294848) #Support server suggestion channel id

            embed = discord.Embed(
            title=f"{ctx.author}'s idea", 
            description=f"This idea came from a server named **{ctx.guild.name}**!", 
            color=var.CBLUE
            ).add_field(name="Suggestion", value=desc
            )
            msg = await channel.send(embed=embed)
            await msg.add_reaction(var.ACCEPT)
            await msg.add_reaction(var.DECLINE)
            await ctx.send("Suggestion sent to the support server!")
        else:
            await ctx.send(f"You need to describe your idea too! This is the format\n```{getprefix(ctx)} <description of your idea>```\nDon't forget the space after prefix :D")


    @commands.command()
    async def about(self, ctx):
        guildcount = 0
        membercount = 0
        ping = f"{round(self.bot.latency*1000)}ms"
        for guild in self.bot.guilds:
            guildcount +=1
            membercount += guild.member_count

        embed = discord.Embed(
        title="Some information about me :flushed:",
        color=var.CMAIN
        ).add_field(name="Server Count", value=guildcount, inline=False
        ).add_field(name="Members", value=membercount, inline=False
        ).add_field(name="Ping", value=ping, inline=False
        ).add_field(name="Made by", value="Bolt#8905", inline=False
        ).set_footer(text="I was born on 16 May, 2021"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def embed(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:

            embed = discord.Embed(
            title="Create an embed",
            description=f"React to the emojis below to choose your color! When you are done press the {var.CONTINUE} emoji to continue editing",
            color=var.CMAIN
            ).set_footer(text="This message will become the live preview of the embed you are creating!"
            )
            preview = await ctx.send(embed=embed)
            emojis = [var.ERED,var.EPINK,var.EGREEN,var.EBLUE,var.EORANGE,var.EYELLOW]
            colors = [0xFF0000, 0xFF58BC, 0x24FF00, 0x00E0FF, 0xFF5C00, 0xFFC700]

            for i in emojis:
                await preview.add_reaction(i)
            await preview.add_reaction(var.CONTINUE)
            
            def previewreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == preview
            
            def msgcheck(message):
                return message.author == ctx.author and message.channel.id == ctx.channel.id

            try:
                while True:
                    reaction, user = await self.bot.wait_for('reaction_add', check=previewreactioncheck, timeout=30.0)
                    if str(reaction.emoji) == var.CONTINUE:
                        break

                    index = emojis.index(str(reaction))
                    embed.color=colors[index]
                    await preview.remove_reaction(emojis[index], ctx.author)
                    await preview.edit(embed=embed)
                
                await preview.clear_reactions()    
                titlebotmsg = await ctx.send(embed=discord.Embed(
                title="Title",
                description=f"Now send a message to make it the title of the [embed](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})",
                color=var.CBLUE)
                )
                usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=30.0)
                embed.title = usermsg.content
                await preview.edit(embed=embed)
                await titlebotmsg.delete()

                descbotmsg = await ctx.send(embed=discord.Embed(
                title="Description",
                description=f"Now send a message to make it the description of the [embed](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})",
                color=var.CBLUE
                ).add_field(name="** **", value="Type `skip` if you don't want to set this")
                )
                usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=30.0)
                if usermsg.content == "skip" or usermsg.content == "`skip`":
                    embed.description = None
                    await preview.edit(embed=embed)
                    await descbotmsg.delete()
                else:
                    embed.description = usermsg.content
                    await preview.edit(embed=embed)
                    await descbotmsg.delete()

                thumbnailbotmsg = await ctx.send(embed=discord.Embed(
                title="Thumbnail",
                description=f"Now send a message to make it the description of the [embed](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})",
                color=var.CBLUE
                ).add_field(name="** **", value="Type `skip` if you don't want to set this")
                )
                usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=20.0)
                if usermsg.attachments:
                    embed.set_thumbnail(url=usermsg.attachments[0].url)
                    await preview.edit(embed=embed)
                    await thumbnailbotmsg.delete()
                elif usermsg.content == "skip" or usermsg.content == "`skip`":
                    await thumbnailbotmsg.delete()
                else:
                    embed.set_thumbnail(url=usermsg.content)
                    await preview.edit(embed=embed)
                    await thumbnailbotmsg.delete()
                
                await preview.add_reaction(var.ACCEPT)
                edit = await ctx.send(embed=discord.Embed(
                            description=f"React to the {var.ACCEPT} emoji in the original [preview](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id}) to send your embed! To edit more react to the respective emojis below",
                            color=var.CBLUE
                ).add_field(name="Add field", value="React to 🇦", inline=False
                ).add_field(name="Footer", value="React to 🇫", inline=False
                ).add_field(name="Image", value="React to 🇮", inline=False
                ).add_field(name="Set Author (yourself)", value="React to 🇺", inline=False)
                )
                def editreactioncheck(reaction, user):
                    return user == ctx.author and reaction.message == edit or reaction.message == preview
                editemojis = ["🇦", "🇫", "🇮", "🇺"]
                for i in editemojis:
                    await edit.add_reaction(i)

                while True:
                    reaction, user = await self.bot.wait_for('reaction_add', check=editreactioncheck, timeout=30.0)
                    if str(reaction.emoji) == var.ACCEPT:
                        await channel.send(embed=embed)
                        await ctx.send("Embed sent in "+channel.mention+" !")
                        break
                    if str(reaction.emoji) == "🇦":
                        fieldbotmsg = await ctx.send("Send a message and seperate your **Field name and value** with `|`\nFor example: This is my field name | This is the field value!")
                        usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=120.0)
                        fieldlist = usermsg.content.split("|")
                        embed.add_field(name=fieldlist[0], value=fieldlist[1], inline=False)
                        await preview.edit(embed=embed)
                        await fieldbotmsg.delete()
                        await edit.remove_reaction("🇦", ctx.author)

                    if str(reaction.emoji) == "🇫":
                        footerbotmsg = await ctx.send("Send a message to make it the **Footer**!")
                        usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=50.0)
                        embed.set_footer(text=usermsg.content)
                        await preview.edit(embed=embed)
                        await footerbotmsg.delete()
                        await edit.clear_reaction("🇫")

                    if str(reaction.emoji) == "🇮":
                        imagebotmsg = await ctx.send("Now send an image or link to add that **Image** to the embed!")
                        usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=30.0)   
                        try:   
                            if usermsg.attachments:
                                embed.set_image(url=usermsg.attachments[0].url)
                                await preview.edit(embed=embed)
                                await thumbnailbotmsg.delete()
                                edit.clear_reaction("🇮")
                            else:
                                embed.set_image(url=usermsg.content)
                                await preview.edit(embed=embed)
                                await imagebotmsg.delete()
                                await edit.clear_reaction("🇮")
                        except:
                            await ctx.send("Invalid image, either use a url or send the image")
                            await edit.remove_reaction("🇮", ctx.author)

                    if str(reaction.emoji) == "🇺":
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        await preview.edit(embed=embed)
                        await edit.clear_reaction("🇺")

            except asyncio.TimeoutError:
                    await preview.clear_reactions()
                    await ctx.send("You took too long ;-;")
        else:
            await ctx.send(f"You also need to define the channel too! Format:\n```{getprefix(ctx)}embed <#channel>```\nDon't worry, the embed won't be sent right away to the channel :D")

        
def setup(bot):
    bot.add_cog(Commands(bot))