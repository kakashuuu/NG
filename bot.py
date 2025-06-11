import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename
from telethon.errors.rpcerrorlist import FloodWaitError

# Telegram API credentials
api_id = 28607488
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"

# Channel usernames or invite link
source_channel = "chicas_asiaticas_whaifus_y_mas"
destination_channel = "https://t.me/+40nUDiLxpG4wZGI0"

# Temporary download folder
download_dir = "temp_zips"
os.makedirs(download_dir, exist_ok=True)

async def transfer_all_zip_files():
    async with TelegramClient("session", api_id, api_hash) as client:
        await client.connect()

        if not await client.is_user_authorized():
            print("❌ Telegram client is not authorized. Please log in manually.")
            return

        print(f"✅ Connected. Fetching from @{source_channel}...")

        dest_entity = await client.get_entity(destination_channel)

        total_zips = 0
        async for msg in client.iter_messages(source_channel):
            if msg.file and msg.file.name and msg.file.name.lower().endswith(".zip"):
                try:
                    filename = msg.file.name
                    print(f"\n⬇️ Downloading: {filename}")
                    file_path = await msg.download_media(file=download_dir)
                    print(f"✅ Downloaded to: {file_path}")

                    print(f"📤 Sending to private channel...")
                    await client.send_file(dest_entity, file_path, caption=f"Forwarded: {filename}")
                    print(f"✅ Sent: {filename}")

                    os.remove(file_path)
                    print(f"🗑️ Deleted: {file_path}")

                    total_zips += 1

                except FloodWaitError as e:
                    print(f"⏳ FloodWait: Sleeping for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)

                except Exception as e:
                    print(f"⚠️ Error with message {msg.id}: {e}")

        print(f"\n🎉 Finished! {total_zips} ZIP files processed.")

# Run the script
asyncio.run(transfer_all_zip_files())
