from pyrogram import Client, filters
import instaloader

# Start command handler
async def start(client, message):
    await message.reply("Hello! Send me an Instagram reel link to download.")

# Download reel command handler
async def download_reel(client, message, db):
    link = message.text.split(maxsplit=1)[1]  # Get link from the message
    try:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, link.split('/')[-2])
        video_url = post.video_url
        await message.reply_video(video_url)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

    # Log download
    db.download_logs.insert_one({"user_id": message.from_user.id, "link": link, "status": "success"})

# Broadcast message handler
async def broadcast_message(client, message, db):
    text = message.text.split(maxsplit=1)[1]
    users = db.users.find()
    for user in users:
        try:
            await client.send_message(user["user_id"], text)
        except Exception as e:
            print(f"Failed to send to {user['user_id']}: {str(e)}")
