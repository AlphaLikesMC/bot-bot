import discord
from discord.ext import commands
import random

class eightball(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8b'])
    async def eightball(self, ctx, *, question):
        """ Gives a random yes/no reply to your question. """
        responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


async def setup(client):
    await client.add_cog(eightball(client))    