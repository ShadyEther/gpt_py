import discord
import openai
from discord.ext import commands

# Set up your OpenAI API credentials
openai.api_key = "YOUR OPEN API KEY"

# Set up your Discord bot credentials
bot = commands.Bot(command_prefix='!')

# Set up your chat function using OpenAI's GPT-3
async def chat(ctx, *, message):
    response = openai.Completion.create(
        engine="davinci", prompt=message, max_tokens=1024, n=1, stop=None, temperature=0.7,
    )

    reply = response.choices[0].text
    await ctx.send(reply)

# Create a command for the bot to respond to a user's message with an AI-generated response
@bot.command()
async def talk(ctx, *, message):
    await chat(ctx, message=message)

# Start your Discord bot
bot.run('YOUR DISCORD BOT API KEY')