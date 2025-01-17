# Discord Crypto Porfolio Bot

A Discord bot for tracking cryptocurrencies and managing a real-time portfolio using MEXC API. The bot support periodic updates and interactive Slash Commands.

---

## Features

###1. Trading Updates
- Periodically fetches and updates prices for fetching for predefined  

###2. Portfolio Tracking 
-Monitors predefined assets and quantities:
  - **BTCUSDT**: 1
  - **ETHUSDT**: 1
  - etc, you can add whatever you want in the form at ```config.py```: XXXUSDT

###3. Slash Commands
- `/price <symbol>`: Fetch the latest price for a trading pair.
- `/start_updates`: Start periodic updates for trading pairs.
- `/stop_updates`: Stop periodic updates.
- `/portfolio`: Show current portfolio data.
- `/start_portfolio_updates`: Start periodic portfolio updates.
- `/stop_portfolio_updates`: Stop periodic portfolio updates.

---

## Setup

### Prerequisites
- Python 3.8+
- Discord bot token

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/discord-crypto-portfolio-bot.git
   cd discord-crypto-portfolio-bot
   ```

2. Install dependencies:
   ```bash
   pip install discord.py uiohttp requests
   ```

3. Configure the bot:
   - Edit `config.py` to set:
     - `DISCORD_TOKEN`: Your Discord bot token.
     - `PORTFOLIO`: Portfolio assets and quantities.

4. Run the bot:
   ```bash
   python3 bot.py
   ```

---

## Usage

### Commands
- **Slash Commands**:
  - `/price <symbol>`: Query a trading pair's price.
  - `/start_updates`: Start periodic updates for trading pairs.
  - `/stop_updates`: Stop periodic updates.
  - `/portfolio`: Display current portfolio data.
  - `/start_portfolio_updates`: Start portfolio updates.
  - `/stop_portfolio_updates`: Stop portfolio updates.

### Example Output
#### Portfolio Data
```
Portfolio Data:
BTCUSDT:
  Amount: 0.01
  Price: 50000.00
  Value: 500.00
  Percentage: 50.00%

ETHUSDT:
  Amount: 0.05
  Price: 4000.00
  Value: 200.00
  Percentage: 20.00%

...

Total Value: 700.00
Growth Compared to Baseline: 159.26%
```

---

## Acknowledgments
- [MEXC API Documentation](https://mexcdevelop.github.io/apidocs/spot_v3_en/#introduction)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)

    
