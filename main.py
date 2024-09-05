import os
import discord
import google.generativeai as genai

import openai


from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()


DISCORD_TOKEN  = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')



openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# for gemini
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}




intents = discord.Intents.default()
intents.message_content = True 


bot = commands.Bot(command_prefix='!',intents=intents)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')





@bot.command()
async def sup(ctx):
    await ctx.send(f'sup {ctx.author.mention}..👋')



@bot.command()
async def helppls(ctx):
    await ctx.send('''---Help page---
1. List of Commands: !sup !gpt !gemmy !help
2. About: a simple bot which takes your question and answers them using gpt
''')





@bot.command()
async def gpt(ctx, *, query: str):
    try:
        await ctx.send("Gpt is Thinking... 🤔")

        
        response = openai.Completion.create(
            engine="gpt-4o-mini",  
            prompt=query,
            max_tokens=150
        )

        
        answer = response.choices[0].text.strip()

        
        await ctx.send(answer)

    except Exception as e:
        await ctx.send(f"Error occured: {e}")





model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )


chat_session = model.start_chat(
  history=[
  ]
)




@bot.command()
async def gemmy(ctx, *, query: str):
    try:
        await ctx.send("Gemini is Thinking... 🤔")

        
        

        # response = model.generate_content("what is a cat?")

        response = chat_session.send_message(query)
        answer=response.text
        
        await ctx.send(answer)

    except Exception as e:
        await ctx.send(f"Error occured: {e}")



bot.run(DISCORD_TOKEN)

