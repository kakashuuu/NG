import os
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import Document

# Telegram API credentials
api_id = 28607488
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"

# Channels
source_channel = "chicas_asiaticas_whaifus_y_mas"
destination_channel = "https://t.me/+40nUDiLxpG4wZGI0"

# Create temp dir
download_dir = "temp_zips"
os.makedirs(download_dir, exist_ok=True)

async def fetch_and_forward_all_zips():
    async with TelegramClient("session", api_id, api_hash) as client:
        await client.connect()
        if not await client.is_user_authorized():
            print("❌ Login required.")
            return

        dest = await client.get_entity(destination_channel)
        total = 0

        print("🚀 Starting full scan of channel...")
        async for message in client.iter_messages(source_channel, reverse=True):  # reverse = oldest to newest
            if (
                message.file 
                and isinstance(message.file, Document)
                and message.file.name 
                and message.file.name.lower().endswith(".zip")
            ):
                try:
                    filename = message.file.name
                    print(f"\n📩 Message ID: {message.id} | Downloading {filename}")
                    filepath = await message.download_media(file=download_dir)
                    print(f"✅ Downloaded to: {filepath}")

                    await client.send_file(dest, filepath, caption=f"Forwarded: {filename}")
                    print("📤 Sent to private channel")

                    os.remove(filepath)
                    print("🗑️ Deleted from disk")
                    total += 1

                except FloodWaitError as e:
                    print(f"⏳ Flood wait: sleeping for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)

                except Exception as e:
                    print(f"❌ Error at message {message.id}: {e}")

        print(f"\n🎉 Done. Total ZIP files transferred: {total}")

# Run it
asyncio.run(fetch_and_forward_all_zips())