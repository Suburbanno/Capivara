import discord
import asyncio
import os
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

perm = discord.Intents.default()
perm.message_content = True
perm.members = True

bot = commands.Bot(command_prefix=".", intents=perm)

async def load_cogs():
    for file in os.listdir('commands'):
        if file.endswith('.py'):
            await bot.load_extension(f'commands.{file[:-3]}')

@bot.command()
async def reload(ctx: commands.Context):
    if ctx.author.id == xxxx:
        sincs = await bot.tree.sync()
        await ctx.reply(f'{len(sincs)} Comandos sincronizados 🔄')
    else:
        await ctx.reply('Você não pode usar esse comando!')

@bot.event
async def on_ready():
    await load_cogs()
    status_task.start()
    print(f'Logged in as {bot.user}')
    print('--------------------------')

@tasks.loop()
async def status_task() -> None:
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("BrasilAPI ⚡"))
    await asyncio.sleep(60)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Lo-fi 🎧"))
    await asyncio.sleep(60)
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="`/ajuda`"))
    await asyncio.sleep(60)

bot.run(token)