import discord
from discord import app_commands
from discord.ext import commands
import requests

class CepCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cep", description="Retorna informações de um determinado CEP.")
    async def cep(self, interaction: discord.Interaction, numero: str):
        cep_number = ''.join(filter(str.isdigit, numero))
        cep_url = f'https://brasilapi.com.br/api/cep/v2/{cep_number}'

        try:
            res = requests.get(cep_url)
            if res.status_code == 200:
                data = res.json()
                embed = discord.Embed(title=f"Informações do CEP {cep_number}", color=discord.Color.blue())
                embed.add_field(name="Estado", value=data['state'], inline=True)
                embed.add_field(name="Cidade", value=data['city'], inline=True)
                embed.add_field(name="Bairro", value=data['neighborhood'], inline=True)
                embed.add_field(name="Rua", value=data['street'], inline=True)
                await interaction.response.send_message(embed=embed)
            elif res.status_code == 404:
                await interaction.response.send_message("CEP não existe ou não foi encontrado.")
            else:
                await interaction.response.send_message("Erro ao consultar o CEP. Tente novamente.")
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message("Erro ao consultar o CEP.")
            print(f"Erro ao consultar API: {e}")

async def setup(bot):
    await bot.add_cog(CepCommand(bot))