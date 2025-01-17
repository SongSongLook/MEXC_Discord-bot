import discord
from config import MEXC_API_BASE, UPDATE_INTERVAL, UPDATE_INTERVAL_Pf, PORTFOLIO, BASE_PORTFOLIO_VALUE, SYMBOLS
import requests
import asyncio
from datetime import datetime

portfolio_message = None

# 儲存已發送消息的字典，用於編輯定期更新的消息
message_store = {}

async def fetch_price(interaction: discord.Interaction, symbol: str):
    """Slash Command: 查詢特定交易對的價格"""
    try:
        symbol = symbol.upper()
        url = f'{MEXC_API_BASE}/api/v3/ticker/24hr?symbol={symbol}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            content = (
                f"🔹 **{symbol} 最新價格資訊**\n"
                f"📈 價格: `{data['lastPrice']}`\n"
                f"⬆️ 24H 高: `{data['highPrice']}`\n"
                f"⬇️ 24H 低: `{data['lowPrice']}`\n"
                
            )
            await interaction.response.send_message(content)
        else:
            await interaction.response.send_message(f"⚠️ 無法獲取交易對 `{symbol}` 的數據。")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ 查詢價格時出現錯誤: {e}")

async def start_updates(interaction: discord.Interaction):
    """Slash Command: 開始定期更新預設交易對的價格"""
    if "price_update" in message_store:
        await interaction.response.send_message("✅ 定期更新已啟動，請勿重複啟動。")
        return

    initial_message = await interaction.channel.send("🔄 初始化交易對價格數據...")
    message_store["price_update"] = initial_message
    await interaction.response.send_message("✅ 已啟動定期(每十五秒)更新交易對價格！")
    asyncio.create_task(update_prices(initial_message))

async def stop_updates(interaction: discord.Interaction):
    """Slash Command: 停止定期更新價格"""
    if "price_update" in message_store:
        del message_store["price_update"]
        await interaction.response.send_message("🔚已停止定期更新交易對價格。")
    else:
        await interaction.response.send_message("❔未找到正在運行的定期更新任務。")

async def update_prices(message):
    """定期更新交易對價格，並編輯消息"""
    while "price_update" in message_store:
        try:
            price_data = []
            for symbol in SYMBOLS:
                url = f'{MEXC_API_BASE}/api/v3/ticker/24hr?symbol={symbol}'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    price_data.append(
                        f"🔹 **{symbol} 最新價格資訊**\n"
                        f"📈 價格: `{data['lastPrice']}`\n"
                        f"⬆️ 24H 高: `{data['highPrice']}`\n"
                        f"⬇️ 24H 低: `{data['lowPrice']}`\n"
                    )
                else:
                    price_data.append(f"⚠️ 無法獲取交易對 `{symbol}` 的數據。")

            last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = ">>> **💹 即時交易對價格更新**\n\n" + "\n".join(price_data) + "-# Source: MEXC" + "\n" +  "-# last update time:" + f" {last_update} "
            await message.edit(content=content)
        except Exception as e:
            await message.channel.send(f"⚠️ 更新價格時出現錯誤: {e}")

        await asyncio.sleep(UPDATE_INTERVAL)

async def fetch_portfolio(interaction=None):
    """計算 portfolio 資料"""
    try:
        total_value = 0
        portfolio_data = []
        
        # 查詢每個幣種的最新價格並計算價值
        for symbol, amount in PORTFOLIO.items():
            url = f'{MEXC_API_BASE}/api/v3/ticker/24hr?symbol={symbol}'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                price = float(data['lastPrice'])
                value = price * amount
                total_value += value
                portfolio_data.append({
                    "symbol": symbol,
                    "amount": amount,
                    "price": price,
                    "value": value
                })
            else:
                portfolio_data.append({
                    "symbol": symbol,
                    "amount": amount,
                    "price": None,
                    "value": None
                })
        
        # 計算價值百分比
        for item in portfolio_data:
            if item['value'] is not None:
                item['percentage'] = (item['value'] / total_value) * 100
            else:
                item['percentage'] = None
        
        # 計算總價值和增長百分比
        growth_percentage = ((total_value - BASE_PORTFOLIO_VALUE) / BASE_PORTFOLIO_VALUE) * 100
        return total_value, growth_percentage, portfolio_data
    except Exception as e:
        return None, None, f"⚠️獲取 portfolio 資料時出現錯誤: {e}"

async def start_portfolio_updates(interaction: discord.Interaction):
    """啟動 portfolio 定期更新"""
    global portfolio_message
    if portfolio_message:
        await interaction.response.send_message("✅ Portfolio 更新已啟動。若需重新啟動，請先停止。")
        return

    portfolio_message = await interaction.channel.send("🔄 初始化 portfolio 資料...")
    await interaction.response.send_message("✅ 已啟動 portfolio (每日)定期更新！")
    asyncio.create_task(update_portfolio(portfolio_message))

async def stop_portfolio_updates(interaction: discord.Interaction):
    """停止 portfolio 定期更新"""
    global portfolio_message
    if portfolio_message:
        portfolio_message = None
        await interaction.response.send_message("🔚 已停止 portfolio 定期更新。")
    else:
        await interaction.response.send_message("❔ 未找到正在運行的 portfolio 更新任務。")

async def update_portfolio(message):
    """定期更新 portfolio"""
    global portfolio_message
    while portfolio_message:
        total_value, growth_percentage, portfolio_data = await fetch_portfolio()
        if portfolio_data == "error":
            await message.edit(content="⚠️ 更新 portfolio 資料時出現錯誤。")
            continue
        
        # 組裝輸出
        content = ">>> **💹Portfolio** 資料:\n"
        for item in portfolio_data:
            if item['value'] is not None:
                content += (
                    f"🔹 **{item['symbol']}:**\n"
                    f"  數量: {item['amount']} "
                    f"  單價: {item['price']:.2f}\n "
                    f"  價值: {item['value']:.2f} "
                    f"  百分比: {item['percentage']:.2f}%\n"
                )
            else:
                content += f"{item['symbol']}: 無法獲取價格\n"
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content += (
            f"\n總價值: {total_value:.2f}\n"
            f"相較於基準增長: {growth_percentage:.2f}%\n"
            f"-# Source: MEXC \n"
            f"-# last update time: {last_update}"
        )
        await message.edit(content=content)
        await asyncio.sleep(UPDATE_INTERVAL_Pf)

