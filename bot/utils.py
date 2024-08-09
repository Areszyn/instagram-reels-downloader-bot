from pyrogram import Client, filters

# Check if the user is an admin
async def is_admin(client, user_id):
    return user_id in [123456789, 987654321]  # Replace with actual admin user IDs

# Add user to the database
async def add_user(db, user_id):
    db.users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
