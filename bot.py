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


WELCOME_CHANNEL_NAME = os.getenv("WELCOME_CHANNEL_NAME", "general")
WELCOME_IMAGE_PATH = os.getenv("WELCOME_IMAGE_PATH", "welcome.png")


@bot.event
async def on_member_join(member):
    """Dipanggil otomatis saat ada member baru join server."""
    # Cari channel khusus welcome dulu, kalau nggak ada pakai system channel bawaan server
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL_NAME)
    if channel is None:
        channel = member.guild.system_channel

    if channel is None:
        return  # nggak ada channel yang bisa dipakai, skip

    pesan = (
        f"Halo {member.mention}, selamat datang di **{member.guild.name}**! 🎉\n"
        f"Sekarang kita ada **{member.guild.member_count}** member. Semoga betah ya! 👋"
    )

    # Kalau ada file gambar lokal untuk welcome, kirim bareng sebagai attachment
    if os.path.isfile(WELCOME_IMAGE_PATH):
        file = discord.File(WELCOME_IMAGE_PATH, filename="welcome.png")
        await channel.send(content=pesan, file=file)
    else:
        await channel.send(content=pesan)


LEAVE_CHANNEL_NAME = os.getenv("LEAVE_CHANNEL_NAME", WELCOME_CHANNEL_NAME)
LEAVE_IMAGE_PATH = os.getenv("LEAVE_IMAGE_PATH", "goodbye.png")


@bot.event
async def on_member_remove(member):
    """Dipanggil otomatis saat ada member yang keluar/di-kick dari server."""
    channel = discord.utils.get(member.guild.text_channels, name=LEAVE_CHANNEL_NAME)
    if channel is None:
        channel = member.guild.system_channel

    if channel is None:
        return  # nggak ada channel yang bisa dipakai, skip

    pesan = (
        f"**{member.name}** baru aja meninggalkan server. 👋\n"
        f"Sekarang tersisa **{member.guild.member_count}** member."
    )

    # Kalau ada file gambar lokal untuk goodbye, kirim bareng sebagai attachment
    if os.path.isfile(LEAVE_IMAGE_PATH):
        file = discord.File(LEAVE_IMAGE_PATH, filename="goodbye.png")
        await channel.send(content=pesan, file=file)
    else:
        await channel.send(content=pesan)


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