import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Baca file .env (kalau ada) dan masukkan isinya ke environment variable
load_dotenv()

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


WELCOME_CHANNEL_NAME = os.getenv("selamat-datang", "general")


@bot.event
async def on_member_join(member):
    """Dipanggil otomatis saat ada member baru join server."""
    # Cari channel khusus welcome dulu, kalau nggak ada pakai system channel bawaan server
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL_NAME)
    if channel is None:
        channel = member.guild.system_channel

    if channel is None:
        return  # nggak ada channel yang bisa dipakai, skip

    embed = discord.Embed(
        title="Welcome Aboard! 🎉",
        description=(
            f"H-hi {member.mention}, welcome to **{member.guild.name}**!\n"
            f"We h-have **{member.guild.member_count}** member(s). h-hope you have a great stay! 👋"
        ),
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Bergabung pada {member.joined_at.strftime('%d %B %Y')}")

    await channel.send(embed=embed)


@bot.command(name="hello")
async def hello(ctx):
    """Command manual: ketik !hello di chat untuk disapa bot."""
    await ctx.send(f"Halo {ctx.author.mention}! Senang ketemu kamu 😄")


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN belum diset atau kosong. Cek file .env kamu, "
            "pastikan formatnya: DISCORD_BOT_TOKEN=isi_token (tanpa spasi/kutip)."
        )
    bot.run(TOKEN)
