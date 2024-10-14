import discord
from discord import app_commands
from discord.ext import commands
import requests

class BancoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="banco", description="Retorna informações de um determinado Banco.")
    async def banco(self, interaction: discord.Interaction, numero: str):
        bank_number = ''.join(filter(str.isdigit, numero))
        bank_url = f'https://brasilapi.com.br/api/banks/v1/{bank_number}'

        try:
            res = requests.get(bank_url)
            if res.status_code == 200:
                data = res.json()
                embed = discord.Embed(title=f"Informações do Banco {bank_number}", color=discord.Color.orange())
                embed.add_field(name="Nome", value=data['fullName'], inline=True)
                embed.add_field(name="Código", value=data['code'], inline=True)
                embed.add_field(name="ISPB", value=data['ispb'], inline=True)
                await interaction.response.send_message(embed=embed)
            elif res.status_code == 404:
                await interaction.response.send_message("Banco não encontrado ou inválido.")
            else:
                await interaction.response.send_message("Erro ao consultar o banco. Tente novamente.")
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message("Erro ao consultar o banco.")
            print(f"Erro ao consultar API: {e}")

async def setup(bot):
    await bot.add_cog(BancoCommand(bot))