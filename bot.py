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
    bot.add_view(RoleButtonView())  # daftarkan ulang view supaya tombol lama tetap berfungsi
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

    embed = discord.Embed(
        title="Selamat Datang! 🎉",
        description=(
            f"Halo {member.mention}, selamat datang di **{member.guild.name}**!\n"
            f"Sekarang kita ada **{member.guild.member_count}** member. Semoga betah ya! 👋"
        ),
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Bergabung pada {member.joined_at.strftime('%d %B %Y')}")

    if os.path.isfile(WELCOME_IMAGE_PATH):
        file = discord.File(WELCOME_IMAGE_PATH, filename="welcome.png")
        embed.set_image(url="attachment://welcome.png")
        await channel.send(embed=embed, file=file)
    else:
        await channel.send(embed=embed)


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

    embed = discord.Embed(
        title="Sampai Jumpa 👋",
        description=(
            f"**{member.name}** baru aja meninggalkan server.\n"
            f"Sekarang tersisa **{member.guild.member_count}** member."
        ),
        color=discord.Color.red(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    if os.path.isfile(LEAVE_IMAGE_PATH):
        file = discord.File(LEAVE_IMAGE_PATH, filename="goodbye.png")
        embed.set_image(url="attachment://goodbye.png")
        await channel.send(embed=embed, file=file)
    else:
        await channel.send(embed=embed)


@bot.command(name="hello")
async def hello(ctx):
    """Command manual: ketik !hello di chat untuk disapa bot."""
    await ctx.send(f"Halo {ctx.author.mention}! Senang ketemu kamu 😄")


# ====== FITUR BUTTON ROLE ======
# Nama role yang mau dikasih pas tombol diklik. Bisa diganti lewat .env.
BUTTON_ROLE_NAME = os.getenv("BUTTON_ROLE_NAME", "Member")


class RoleButtonView(discord.ui.View):
    """View persistent supaya tombol tetap berfungsi walau bot restart."""

    def __init__(self):
        super().__init__(timeout=None)  # timeout=None wajib untuk persistent view

    @discord.ui.button(
        label="Ambil Role",
        style=discord.ButtonStyle.green,
        emoji="✅",
        custom_id="button_role:ambil",  # custom_id WAJIB unik & tetap sama tiap restart
    )
    async def ambil_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name=BUTTON_ROLE_NAME)
        if role is None:
            await interaction.response.send_message(
                f"Role **{BUTTON_ROLE_NAME}** belum dibuat di server ini. Hubungi admin ya.",
                ephemeral=True,
            )
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"Role **{role.name}** dilepas dari kamu.", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"Role **{role.name}** berhasil ditambahkan ke kamu! 🎉", ephemeral=True
            )


@bot.command(name="setuprole")
@commands.has_permissions(manage_roles=True)
async def setuprole(ctx):
    """Command admin: kirim pesan dengan tombol untuk ambil/lepas role."""
    embed = discord.Embed(
        title="Ambil Role di Sini!",
        description=f"Klik tombol di bawah untuk mendapatkan role **{BUTTON_ROLE_NAME}**.",
        color=discord.Color.blurple(),
    )
    await ctx.send(embed=embed, view=RoleButtonView())


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN belum diset atau kosong. Cek file .env kamu, "
            "pastikan formatnya: DISCORD_BOT_TOKEN=isi_token (tanpa spasi/kutip)."
        )
    bot.run(TOKEN)