import discord
from discord import app_commands
from discord.ext import commands

class helpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ajuda", description="Lista os comandos disponíveis.")
    async def ajuda(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Comandos Disponíveis", color=discord.Color.blue())
        embed.add_field(name="`/ddd` <número>", value="Retorna informações sobre um DDD.", inline=False)
        embed.add_field(name="`/bank` <número>", value="Retorna informações sobre o banco pelo código.", inline=False)
        embed.add_field(name="`/cep` <número>", value="Retorna informações de um determinado CEP.", inline=False)
        embed.add_field(name="`/banco` <número>", value="Retorna informações de um determinado Banco.", inline=False)
        embed.add_field(name="`/isbn` <número>", value="Retorna informações de um livro pelo ISBN.", inline=False)
        embed.add_field(name="`/cnpj` <número>", value="Retorna informações de um determinado CNPJ.", inline=False)
        embed.add_field(name="`/registrobr` <número>", value="Retorna informações dominios .br.", inline=False)
        embed.add_field(name="`/info`", value="Retorna informações sobre o bot.", inline=False)
        embed.add_field(name="`/ajuda`", value="Lista os comandos disponíveis.", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(helpCommand(bot))