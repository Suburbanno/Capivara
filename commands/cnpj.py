import discord
from discord import app_commands
from discord.ext import commands
import requests

class CnpjCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cnpj", description="Retorna informações de um determinado CNPJ.")
    async def cnpj(self, interaction: discord.Interaction, numero: str):
        cnpj_number = ''.join(filter(str.isdigit, numero))
        cnpj_url = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj_number}'

        try:
            res = requests.get(cnpj_url)
            if res.status_code == 200:
                data = res.json()
                embed = discord.Embed(title=f"Informações do CNPJ {cnpj_number}", color=discord.Color.green())
                embed.add_field(name="Razão Social", value=data['razao_social'], inline=True)
                embed.add_field(name="Nome Fantasia", value=data['nome_fantasia'], inline=True)
                embed.add_field(name="Situação Cadastral", value=data['situacao_cadastral'], inline=True)
                await interaction.response.send_message(embed=embed)
            elif res.status_code == 404:
                await interaction.response.send_message("CNPJ digitado errado ou não tem registro.")
            else:
                await interaction.response.send_message("Erro ao consultar o CNPJ. Tente novamente.")
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message("Erro ao consultar o CNPJ.")
            print(f"Erro ao consultar API: {e}")

async def setup(bot):
    await bot.add_cog(CnpjCommand(bot))