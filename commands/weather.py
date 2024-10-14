import discord
from discord import app_commands
from discord.ext import commands
import requests

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clima", description="Mostra o clima atual em uma cidade específica.")
    @app_commands.describe(cidade="Nome da cidade")
    async def clima(self, interaction: discord.Interaction, cidade: str):
        try:
            headers = {
                'User-Agent': 'Telescope/1.0 (noxian.dev; eu@noxian.dev)'
            }
            
            geocoding_url = f"https://nominatim.openstreetmap.org/search?q={cidade}&format=json&limit=1"
            geocoding_response = requests.get(geocoding_url, headers=headers)

            if geocoding_response.status_code != 200:
                await interaction.response.send_message("Erro ao acessar a API de geocodificação.")
                return

            geocoding_data = geocoding_response.json()

            if not geocoding_data:
                await interaction.response.send_message("Cidade não encontrada. Por favor, verifique o nome e tente novamente.")
                return

            latitude = geocoding_data[0]['lat']
            longitude = geocoding_data[0]['lon']

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=America/Sao_Paulo"
            response = requests.get(weather_url)

            if response.status_code != 200:
                await interaction.response.send_message("Erro ao acessar a API de clima.")
                return

            data = response.json()

            if "current_weather" not in data:
                await interaction.response.send_message("Não foi possível obter as informações do clima para essa cidade.")
                return
            current_weather = data['current_weather']
            temperatura = current_weather['temperature']
            velocidade_vento = current_weather['windspeed']
            descricao = current_weather['weathercode']
            weather_descriptions = {
                0: "Céu claro 🌥️",
                1: "Principalmente claro 🌤️",
                2: "Parcialmente nublado ☁️",
                3: "Nublado ☁️",
                45: "Nevoeiro 🌫️",
                48: "Nevoeiro congelante 🌫️",
                51: "Chuva leve ☔",
                53: "Chuva moderada 🌧️",
                55: "Chuva intensa ⛈️",
                61: "Chuva leve ☔",
                63: "Chuva moderada 🌧️",
                65: "Chuva intensa ⛈️",
                80: "Chuva com pancadas ⛈️",
                81: "Chuva intensa com pancadas ⛈️",
                82: "Chuva torrencial ⛈️"
            }

            descricao_clima = weather_descriptions.get(descricao, "Condição desconhecida")

            embed = discord.Embed(title=f"Clima em {cidade.capitalize()}", color=discord.Color.blue())
            embed.add_field(name="Temperatura Atual 🌡️", value=f"{temperatura}°C", inline=True)
            embed.add_field(name="Velocidade do Vento 🍃", value=f"{velocidade_vento} km/h", inline=True)
            embed.add_field(name="Descrição ⛱️", value=descricao_clima, inline=False)
            embed.set_footer(text="Fonte: Open-Meteo")

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro ao buscar as informações: {str(e)}")

async def setup(bot):
    await bot.add_cog(Weather(bot))