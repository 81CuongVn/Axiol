"""Custom cog for Logically Answered discord server."""

import discord
from discord.ext import commands, tasks
import string
from functions import get_randomtext
import variables as var


class LogicallyAnswered(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """Simple check this custom cog only runs on this server"""
        return ctx.guild.id == 751491708465840159

    @commands.command()
    async def poll(self, ctx, *, msg: str = None):
        role = discord.utils.find(
            lambda r: r.name == 'Level 30+',
            ctx.message.guild.roles
        )

        if msg != None and role in ctx.author.roles:
            # Polls channel
            channel = self.bot.get_channel(789214004950204416)

            embed = discord.Embed(
                title=f"{ctx.author.name} asks:",
                description=msg,
                color=discord.Colour.green()
            )

            msg = await channel.send(
                content='<@&789216491090346025>',
                embed=embed
            )

            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            await msg.add_reaction("🤷‍♂️")

        elif msg == None and not role in ctx.author.roles:
            await ctx.send(
                "You neither specified your message nor you are level 30+,"
                " sorry you can't use the command right now."
            )

        elif msg == None:
            await ctx.send(
                "__You need to specify the message to start a poll!__\n"
                " Format: ```!poll <yourmessage>```"
            )

        elif not role in ctx.author.roles:
            await ctx.send(
                "You don't have level 30+ role yet, "
                "you can't use the command right now."
            )

    @commands.group(pass_context=True, invoke_without_command=True)
    async def ows(self, ctx):
        status = one_word_story.is_running()
        seconds = one_word_story.seconds
        minutes = one_word_story.minutes
        hours = one_word_story.hours
        await ctx.send(
            f"```css\n.Running? [{status}]\n."
            f"StopWhen? [{hours}h {minutes}h {seconds}s]```"
        )

    @ows.command()
    async def start(self, ctx):
        one_word_story.start(self, ctx)
        await ctx.send(
            f"{var.E_ENABLE} Started the background process for one word story"
        )

    @ows.command()
    async def stop(self, ctx):
        one_word_story.stop()
        await ctx.send(
            f"{var.E_DISABLE} Stopped the background process for one word story"
        )

    # Soon gonna add auto reactions too
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        def message_check(msg):
            allowed = list(string.ascii_lowercase + string.digits)
            return msg <= allowed

        if message.guild.id == 751491708465840159:

            if str(message.channel) == '💡〢suggestions':
                await message.add_reaction('<:upvote:776831295946620948>')
                await message.add_reaction('<:downvote:776831143453786164>')

            if str(message.channel) == '✋〢video-requests':
                await message.add_reaction('👍')
                await message.add_reaction('👎')

            if str(message.channel) == '👋〢welcome':
                await message.add_reaction('<:elonwave:806962782330552340>')

            if str(message.channel) == '🗳〢vote':
                await message.add_reaction('✅')
                await message.add_reaction('❌')

            if (str(message.channel) == '📝〢one-word-story' and
                    message.author.bot == False):

                last_message = await message.channel.history(limit=2).flatten()
                last_message_author = last_message[1].author
                if last_message_author == message.author:
                    await message.channel.send(
                        (
                            f"{message.author.mention} "
                            "You can't send two messages in a row! "
                            "Wait for someone else to send a message first"
                        ),
                        delete_after=3
                    )

                    try:
                        await message.delete()

                    except:
                        pass

                if (
                    " " in list(message.content)
                    or "-" in list(message.content)
                    or "_" in list(message.content)
                    or "." in list(message.content)
                        or "+" in list(message.content)
                ):
                    try:
                        await message.delete()

                    except:
                        pass

            if (
                str(message.channel) == "💯〢counting-to-420k"
                and message.author.bot == False
            ):

                fetch = await message.channel.history(limit=2).flatten()
                last_message = fetch[1].content

                increment = int(last_message) + 1

                if message.content != str(increment):
                    await message.delete()
                    await message.channel.send(
                        (
                            f"{message.author.mention}"
                            " The number you sent is not the correct"
                            " increment of previous one!"
                        ),
                        delete_after=2
                    )


@tasks.loop(hours=12)
async def one_word_story(self, _ctx):
    channel = self.bot.get_channel(803308171577393172)
    bot_msg = await channel.history().find(lambda m: m.author == self.bot.user)

    bot_embeds = [embed.to_dict() for embed in bot_msg.embeds]

    first_word = bot_embeds[0]["fields"][0]["value"]
    messages = await channel.history(after=bot_msg).flatten()
    previous_story = " ".join([msg.content for msg in messages])

    new_word = await get_randomtext(0).strip(".")

    embed = discord.Embed(
        title=f"Create a new story!",
        description=f">>> **Previous story**\n{first_word} {previous_story}",
        color=var.C_MAIN
    ).add_field(name="New word", value=new_word)

    await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(LogicallyAnswered(bot))
