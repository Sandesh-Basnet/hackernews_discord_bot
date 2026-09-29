import os
import re
import json
import html
import asyncio
import discord
import feedparser
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

FEED_URL = "https://feeds.feedburner.com/TheHackersNews"
NEWS_COUNT = 5
POSTED_FILE = BASE / "posted.json"

client = discord.Client(intents=discord.Intents.default())
started = False


def load_posted():
    try:
        return json.loads(POSTED_FILE.read_text())
    except Exception:
        return []


def save_posted(links):
    POSTED_FILE.write_text(json.dumps(links[-300:]))


def clean(text, limit=700):
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "..."
    return text


@client.event
async def on_ready():
    global started
    print(f"[+] Logged in as {client.user}")
    if started:
        return
    started = True

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("[-] Channel not found. Check CHANNEL_ID and bot permissions.")
        return

    feed = await asyncio.to_thread(feedparser.parse, FEED_URL)
    posted = load_posted()
    entries = [e for e in feed.entries if e.link not in posted][:NEWS_COUNT]

    if not entries:
        await channel.send("```ansi\n\u001b[1;33m[ NO NEW INTEL ] Nothing new since last sync.\u001b[0m\n```")
        print("[+] No new articles.")
        return

    await channel.send("```ansi\n\u001b[1;32m[ SYSTEM ONLINE ] Intercepting latest threat intel...\u001b[0m\n```")

    for n, entry in enumerate(entries, start=1):
        summary = clean(entry.get("summary", "No summary available."))
        embed = discord.Embed(
            title=f"[{n}/{len(entries)}] {entry.title}"[:256],
            url=entry.link,
            color=0x00FF41,
        )
        embed.add_field(name="> SUMMARY", value=f"```{summary}```"[:1024], inline=False)
        embed.add_field(name="> SOURCE", value=f"[Read full article]({entry.link})", inline=False)
        embed.set_footer(text="root@thehackernews:~# feed --latest")
        await channel.send(embed=embed)
        posted.append(entry.link)
        save_posted(posted)
        await asyncio.sleep(1)

    await channel.send("```ansi\n\u001b[1;32m[ END OF TRANSMISSION ]\u001b[0m\n```")
    print("[+] Posted news.")


client.run(TOKEN)
