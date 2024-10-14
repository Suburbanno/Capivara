import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import requests

class DominioCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="registrobr", description="Retorna informações sobre um domínio.")
    async def dominio(self, interaction: discord.Interaction, dominio: str):
        dominio_url = f'https://brasilapi.com.br/api/registrobr/v1/{dominio}'

        try:
            res = requests.get(dominio_url)
            if res.status_code == 200:
                data = res.json()

                if not data:
                    await interaction.response.send_message("Nenhuma informação encontrada para o domínio.")
                    return

                embed = discord.Embed(title=f"Informações sobre o domínio {dominio}", color=discord.Color.blue())
                embed.add_field(name="Domínio", value=data.get('fqdn', 'Não disponível'), inline=False)
                embed.add_field(name="Status", value=data.get('status', 'Não disponível'), inline=False)
                expires_at = data.get('expires-at', 'Não disponível')
                if expires_at != 'Não disponível':
                    expires_at = datetime.fromisoformat(expires_at[:-6]).strftime("%d/%m/%Y %H:%M")
                embed.add_field(name="Data de Expiração", value=expires_at, inline=False)

                hosts = data.get('hosts', [])
                if hosts:
                    embed.add_field(name="Servidores DNS", value=", ".join(hosts), inline=False)
                else:
                    embed.add_field(name="Servidores DNS", value="Não disponível", inline=False)

                await interaction.response.send_message(embed=embed)

            elif res.status_code == 404:
                await interaction.response.send_message("Domínio digitado errado ou não tem um registro .br.")
            else:
                await interaction.response.send_message("Erro ao consultar o domínio. Tente novamente.")

        except requests.exceptions.RequestException as e:
            await interaction.response.send_message("Erro ao consultar a API.")
            print(f"Erro ao consultar API: {e}")

async def setup(bot):
    await bot.add_cog(DominioCommand(bot))