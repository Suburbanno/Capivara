import discord
import asyncio
from discord import app_commands
from discord.ext import commands
import requests

class DDDCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ddd", description="Retorna informações sobre um DDD.")
    async def ddd(self, interaction: discord.Interaction, numero: str):

        numero = numero.lstrip('0')

        ddd_url = f'https://brasilapi.com.br/api/ddd/v1/{numero}'

        try:
            res = requests.get(ddd_url)
            if res.status_code == 200:
                data = res.json()
                cities = sorted(data['cities'])
                state = data['state']

                per_page = 16
                pages = [cities[i:i + per_page] for i in range(0, len(cities), per_page)]
                total_pages = len(pages)

                def create_embed(page_index):
                    embed = discord.Embed(title=f"Informações sobre o DDD {numero}", color=discord.Color.blue())
                    embed.add_field(name="Estado", value=state, inline=False)
                    embed.add_field(name="Cidades (Página {}/{})".format(page_index + 1, total_pages), 
                                    value="\n".join(pages[page_index]), inline=False)
                    return embed

                current_page = 0
                embed = create_embed(current_page)
                await interaction.response.send_message(embed=embed)
                message = await interaction.original_response()

                if total_pages > 1:
                    await message.add_reaction('⬅️')
                    await message.add_reaction('➡️')

                    def check(reaction, user):
                        return user == interaction.user and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == message.id

                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                            if str(reaction.emoji) == '⬅️' and current_page > 0:
                                current_page -= 1
                                embed = create_embed(current_page)
                                await message.edit(embed=embed)
                                await message.remove_reaction(reaction, user)

                            elif str(reaction.emoji) == '➡️' and current_page < total_pages - 1:
                                current_page += 1
                                embed = create_embed(current_page)
                                await message.edit(embed=embed)
                                await message.remove_reaction(reaction, user)

                        except asyncio.TimeoutError:
                            break

            elif res.status_code == 404:
                await interaction.response.send_message("DDD não encontrado. Verifique se o DDD está correto.")
            else:
                await interaction.response.send_message("Erro ao consultar o DDD. Tente novamente.")

        except requests.exceptions.RequestException as e:
            await interaction.response.send_message("Erro ao consultar o DDD.")
            print(f"Erro ao consultar API: {e}")

async def setup(bot):
    await bot.add_cog(DDDCommand(bot))
