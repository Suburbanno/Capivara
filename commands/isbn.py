import discord
from discord import app_commands
from discord.ext import commands
import requests

class ISBNCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="isbn", description="Retorna informações de um livro pelo ISBN.")
    async def isbn(self, interaction: discord.Interaction, numero: str):
        isbn_number = ''.join(filter(str.isdigit, numero))
        isbn_url = f'https://brasilapi.com.br/api/isbn/v1/{isbn_number}'

        try:
            res = requests.get(isbn_url)
            if res.status_code == 200:
                data = res.json()
                embed = discord.Embed(title=f"Informações do Livro - ISBN {isbn_number}", color=discord.Color.blue())
                embed.add_field(name="Título", value=data.get('title') if data.get('title') else 'Não há informação', inline=False)
                embed.add_field(name="Subtítulo", value=data.get('subtitle') if data.get('subtitle') else 'Não há informação', inline=False)
                embed.add_field(name="Autores", value=", ".join(data.get('authors', ['Não há informação'])) if data.get('authors') else 'Não há informação', inline=False)
                embed.add_field(name="Editora", value=data.get('publisher') if data.get('publisher') else 'Não há informação', inline=False)
                embed.add_field(name="Sinopse", value=data.get('synopsis') if data.get('synopsis') else 'Não há informação', inline=False)
                embed.add_field(name="Ano", value=data.get('year') if data.get('year') else 'Não há informação', inline=True)
                embed.add_field(name="Formato", value=data.get('format') if data.get('format') else 'Não há informação', inline=True)
                embed.add_field(name="Número de Páginas", value=data.get('page_count') if data.get('page_count') else 'Não há informação', inline=True)
                embed.add_field(name="Localização", value=data.get('location') if data.get('location') else 'Não há informação', inline=False)
                
                dimensions = data.get('dimensions')
                if dimensions and isinstance(dimensions, dict):
                    width = dimensions.get('width', 'Não há informação')
                    height = dimensions.get('height', 'Não há informação')
                    unit = dimensions.get('unit', 'Não há informação')
                    embed.add_field(name="Dimensões", value=f"{width} x {height} {unit}" if all([width, height, unit]) else "Não há informação", inline=False)
                else:
                    embed.add_field(name="Dimensões", value="Não há informação", inline=False)

                await interaction.response.send_message(embed=embed)

            elif res.status_code == 400:
                await interaction.response.send_message("ISBN inválido.")
            elif res.status_code == 404:
                await interaction.response.send_message("ISBN não encontrado.")
            elif res.status_code == 500:
                await interaction.response.send_message("Erro no servidor. Todos os serviços ISBN retornaram erro.")
            else:
                await interaction.response.send_message("Erro ao consultar o ISBN.")

        except requests.exceptions.RequestException as e:
            await interaction.response.send_message("Erro ao consultar a API de ISBN.")
            print(f"Erro ao consultar API: {e}")

async def setup(bot):
    await bot.add_cog(ISBNCommand(bot))