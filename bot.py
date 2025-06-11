import os
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import Document

# Telegram API credentials
api_id = 28607488
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"

source_channel = "chicas_asiaticas_whaifus_y_mas"
destination_channel = "https://t.me/+40nUDiLxpG4wZGI0"

download_dir = "temp_zips"
os.makedirs(download_dir, exist_ok=True)

# MIME types to match ZIPs
zip_mime_types = {
    "application/zip",
    "application/x-zip-compressed",
    "application/octet-stream",  # fallback generic
}

async def fetch_all_possible_zips():
    async with TelegramClient("session", api_id, api_hash) as client:
        await client.connect()
        if not await client.is_user_authorized():
            print("❌ Please login to Telegram")
            return

        dest = await client.get_entity(destination_channel)
        total = 0

        print("🚀 Scanning all messages for ZIP-like files...")

        async for msg in client.iter_messages(source_channel, reverse=True):  # oldest to newest
            if msg.file and isinstance(msg.file, Document):
                mime = msg.file.mime_type
                fname = msg.file.name or f"unknown_{msg.id}.zip"

                if mime in zip_mime_types or fname.lower().endswith(".zip"):
                    try:
                        print(f"\n📦 Downloading {fname} (MIME: {mime})")
                        filepath = await msg.download_media(file=os.path.join(download_dir, fname))
                        print(f"✅ Downloaded: {filepath}")

                        await client.send_file(dest, filepath, caption=f"Forwarded: {fname}")
                        print(f"📤 Sent to private channel")

                        os.remove(filepath)
                        print("🗑️ Deleted from disk")
                        total += 1

                    except FloodWaitError as e:
                        print(f"⏳ Flood wait: sleeping {e.seconds}s")
                        await asyncio.sleep(e.seconds)

                    except Exception as e:
                        print(f"❌ Error at msg {msg.id}: {e}")

        print(f"\n🎉 Done! {total} files transferred.")

# Run it
asyncio.run(fetch_all_possible_zips())