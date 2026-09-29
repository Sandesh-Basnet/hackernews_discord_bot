# Hacker News Discord Bot

A Discord bot that posts the latest cybersecurity news from [The Hacker News](https://thehackernews.com/) to a channel, with a summary for each article. It posts automatically when it comes online, has no commands, and never posts the same article twice.

## Features

- Posts 5 new articles per session, each with a summary and a link
- Skips articles it has already posted (tracked in `posted.json`)
- Posts only to one configured channel
- Hacker-style terminal look

## Setup

1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications) and invite it to your server with the View Channels, Send Messages and Embed Links permissions.
2. Clone the repo and create a virtual environment:

```
   git clone https://github.com/Sandesh-Basnet/hackernews_discord_bot.git
   cd hackernews_discord_bot
   python -m venv venv
   source venv/bin/activate
   pip install discord.py feedparser python-dotenv
```

3. Create a `.env` file in the project folder:

```
   DISCORD_TOKEN=your_bot_token
   CHANNEL_ID=your_channel_id
```

4. Run the bot:

```
   python bot.py
```

## Notes

- Never commit your `.env` file or share your bot token.
- Enable Developer Mode in Discord to copy the channel ID.
