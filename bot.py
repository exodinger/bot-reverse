import os
import discord
from discord.ext import commands

# Ambil token dari environment variable (JANGAN hardcode token di sini!)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Setup intents (izin akses event tertentu)
intents = discord.Intents.default()
intents.members = True          # perlu untuk event on_member_join
intents.message_content = True  # perlu untuk membaca isi pesan (command !hello)

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")


@bot.event
async def on_member_join(member):
    """Dipanggil otomatis saat ada member baru join server."""
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(
            f"Halo {member.mention}, selamat datang di **{member.guild.name}**! 👋"
        )


@bot.command(name="hello")
async def hello(ctx):
    """Command manual: ketik !hello di chat untuk disapa bot."""
    await ctx.send(f"Halo {ctx.author.mention}! Senang ketemu kamu 😄")


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN belum diset. Set environment variable dulu sebelum jalankan bot."
        )
    bot.run(TOKEN)
