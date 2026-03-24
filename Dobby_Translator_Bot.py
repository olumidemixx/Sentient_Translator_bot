import os
import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv

# --- Load .env safely, always from this file's directory ---
base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path)

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

FIREWORKS_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
MODEL_NAME = "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new"

intents = discord.Intents.default()
intents.message_content = True


class DobbyTranslator(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_text = None

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Logged in as {self.user}")


async def call_fireworks(prompt: str):
    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(FIREWORKS_URL, headers=headers, json=data) as resp:
            if resp.status != 200:
                return f"❌ Error: {resp.status} - {await resp.text()}"
            result = await resp.json()
            return result["choices"][0]["message"]["content"]


bot = DobbyTranslator()


@bot.tree.command(name="startbot", description="Start the bot and check if it's working")
async def startbot(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Dobby Translator Bot is online and ready!")


@bot.tree.command(name="identify_lang", description="Identify and store the language of the provided text")
async def identify_lang(interaction: discord.Interaction, text: str):
    bot.user_text = text
    await interaction.response.defer()
    result = await call_fireworks(
        f"Identify the language of the following text and respond with only the language name:\n\n{text}"
    )
    await interaction.followup.send(f"🌍 **Detected Language:** {result}\n\n✅ Text saved. Use a `/convert_to_...` command to translate.")


# --- Universal translate helper ---
async def translate_text(interaction: discord.Interaction, target_language: str):
    if not bot.user_text:
        await interaction.response.send_message("⚠️ No text saved yet. Use `/identify_lang` first.")
        return
    await interaction.response.defer()
    result = await call_fireworks(
        f"Translate the following text to {target_language}. "
        f"Preserve paragraph breaks, spacing, punctuation, and formatting exactly:\n\n{bot.user_text}"
    )
    await interaction.followup.send(f"📝 **Translated to {target_language.title()}:**\n{result}")


# --- Translation commands ---
@bot.tree.command(name="convert_to_english", description="Convert saved text to English")
async def convert_to_english(interaction: discord.Interaction):
    await translate_text(interaction, "English")

@bot.tree.command(name="convert_to_chinese", description="Convert saved text to Chinese")
async def convert_to_chinese(interaction: discord.Interaction):
    await translate_text(interaction, "Chinese")

@bot.tree.command(name="convert_to_vietnamese", description="Convert saved text to Vietnamese")
async def convert_to_vietnamese(interaction: discord.Interaction):
    await translate_text(interaction, "Vietnamese")

@bot.tree.command(name="convert_to_russian", description="Convert saved text to Russian")
async def convert_to_russian(interaction: discord.Interaction):
    await translate_text(interaction, "Russian")

@bot.tree.command(name="convert_to_spanish", description="Convert saved text to Spanish")
async def convert_to_spanish(interaction: discord.Interaction):
    await translate_text(interaction, "Spanish")

@bot.tree.command(name="convert_to_ukrainian", description="Convert saved text to Ukrainian")
async def convert_to_ukrainian(interaction: discord.Interaction):
    await translate_text(interaction, "Ukrainian")

@bot.tree.command(name="convert_to_turkish", description="Convert saved text to Turkish")
async def convert_to_turkish(interaction: discord.Interaction):
    await translate_text(interaction, "Turkish")

@bot.tree.command(name="convert_to_korean", description="Convert saved text to Korean")
async def convert_to_korean(interaction: discord.Interaction):
    await translate_text(interaction, "Korean")

@bot.tree.command(name="convert_to_hindi", description="Convert saved text to Hindi")
async def convert_to_hindi(interaction: discord.Interaction):
    await translate_text(interaction, "Hindi")

@bot.tree.command(name="convert_to_urdu", description="Convert saved text to Urdu")
async def convert_to_urdu(interaction: discord.Interaction):
    await translate_text(interaction, "Urdu")

@bot.tree.command(name="convert_to_bengali", description="Convert saved text to Bengali")
async def convert_to_bengali(interaction: discord.Interaction):
    await translate_text(interaction, "Bengali")

@bot.tree.command(name="convert_to_nepali", description="Convert saved text to Nepali")
async def convert_to_nepali(interaction: discord.Interaction):
    await translate_text(interaction, "Nepali")


@bot.tree.command(name="removeapi", description="Remove the API key from memory")
async def removeapi(interaction: discord.Interaction):
    global FIREWORKS_API_KEY
    FIREWORKS_API_KEY = None
    await interaction.response.send_message("🔒 API key removed from memory.")


bot.run(DISCORD_BOT_TOKEN)
