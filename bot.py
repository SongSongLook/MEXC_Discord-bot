import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from commands import fetch_price, start_updates, stop_updates
from commands import fetch_portfolio, start_portfolio_updates, stop_portfolio_updates

# 創建機器人實例
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} Woke up and connecting to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} comaands.")
    except Exception as e:
        print(f"Syncing commands error: {e}")

# 註冊Slash Commands
@bot.tree.command(name="price", description="查詢特定交易對的最新價格資訊")
async def price_command(interaction: discord.Interaction, symbol: str):
    await fetch_price(interaction, symbol)

@bot.tree.command(name="start_updates", description="開始定期更新預設交易對的價格")
async def start_updates_command(interaction: discord.Interaction):
    await start_updates(interaction)

@bot.tree.command(name="stop_updates", description="停止定期更新交易對的價格")
async def stop_updates_command(interaction: discord.Interaction):
    await stop_updates(interaction)

@bot.tree.command(name="start_portfolio_updates", description="開始 portfolio 定期更新")
async def start_portfolio_command(interaction: discord.Interaction):
    await start_portfolio_updates(interaction)

@bot.tree.command(name="stop_portfolio_updates", description="停止 portfolio 定期更新")
async def stop_portfolio_command(interaction: discord.Interaction):
    await stop_portfolio_updates(interaction)

# 啟動機器人
bot.run(DISCORD_TOKEN)
