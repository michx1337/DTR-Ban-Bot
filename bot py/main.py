from discord.ext import commands
from robloxpy import User, Group, Game
from pymongo import MongoClient
import pymongo
import discord
import robloxpy
import random
import asyncio
import requests
import json

with open('config.json', 'r') as c:
    config = json.load(c)
    TOKEN = config["TOKEN"]
    PREFIX = config["PREFIX"]
    MONGO_URL = config["MONGO_URL"]
    LOG_CHANNEL = config["LOG_CHANNEL"]

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

mongo_url = MONGO_URL
cluster = MongoClient(mongo_url)
db = cluster['database name'] #database name
collectionban = db['ban collection name'] #ban collection name
collectionkick = db['kick collection name'] #kick collection name

# put ur own user ids or usernames here
reserved = ["anyidhere", "anyusernamehere"]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    streaming = discord.Streaming(name="heal <3", url="https://www.twitch.tv/heal")
    await bot.change_presence(activity=streaming)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
         embed = discord.Embed(color=0x1a1a1a)
         embed.title = f"Slow down! You are on cooldown for {error.retry_after:.2f}s"
         await ctx.send(embed=embed)


@bot.remove_command("help")

#help menu
@bot.command()
@commands.cooldown(1, 2.5, commands.BucketType.user)
async def help(ctx):
    em = discord.Embed(color=0x1a1a1a)
    em.title = "Help Menu"
    em.description = f"```ini\n[help]: Shows this menu\n[!lookup <username>]: Looksup user on roblox\n[!ban <userid or username]: Bans a user in game\n[!unban <userid or username>]: Unbans a user in game\n[!banlist]: Shows the ban list in game```"
    await ctx.send(embed=em)

#ban
@bot.command()
@commands.cooldown(1, 2.5, commands.BucketType.user)
async def ban(ctx, user):
    if user.isnumeric():
        info = requests.get(f'https://users.roblox.com/v1/users/{user}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl']
        display = info['displayName']
        name = info['name']

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Banning {user}..."
        msg = await ctx.send(embed=em)
        
        for i in collectionban.find():
            if user in i.values():
                em = discord.Embed(color=0x1a1a1a)
                em.title = f"This user is already banned!"
                await msg.edit(embed=em)
                return 0

        if user in reserved:
            em = discord.Embed(color=0x1a1a1a)
            em.title = f"This user is blacklisted!"
            await msg.edit(embed=em)
            return 0

        collectionban.insert_one({"id": user})
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} has been banned!"
        em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {user}```"
        em.set_footer(text=f"Banned by {ctx.author}")
        em.set_thumbnail(url=image)
        await msg.edit(embed=em)
        
        # sends to log channel to log the ban
        channel = bot.get_channel(LOG_CHANNEL) 
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{name} has been banned"
        em.description = f"Banned by {ctx.author}!"
        em.set_thumbnail(url=image)
        await channel.send(embed=em)
    else:
        userId = requests.get(f'https://api.roblox.com/users/get-by-username?username={user}').json()['Id']
        info = requests.get(f'https://users.roblox.com/v1/users/{userId}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl'] 
        display = info['displayName']
        name = info['name']
        
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Banning {user}..."
        msg = await ctx.send(embed=em)
        
        for i in collectionban.find():
            if str(userId) in i.values():
                em = discord.Embed(color=0x1a1a1a)
                em.title = f"This user is already banned!"
                await msg.edit(embed=em)
                return 0

        if user in reserved:
            em = discord.Embed(color=0x1a1a1a)
            em.title = f"This user is blacklisted!"
            await msg.edit(embed=em)
            return 0

        collectionban.insert_one({"id": str(userId)})
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} has been banned!"
        em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {userId}```"
        em.set_footer(text=f"Banned by {ctx.author}")
        em.set_thumbnail(url=image)
        await msg.edit(embed=em)

        # sends to log channel to log the ban
        channel = bot.get_channel(LOG_CHANNEL) 
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} has been banned"
        em.description = f"Banned by {ctx.author}!"
        em.set_thumbnail(url=image)
        await channel.send(embed=em)

#unban
@bot.command()
@commands.cooldown(1, 2.5, commands.BucketType.user)
async def unban(ctx, user):
    if user.isnumeric():
        info = requests.get(f'https://users.roblox.com/v1/users/{user}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl']
        display = info['displayName']
        name = info['name']

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Unbanning {user}..."
        msg = await ctx.send(embed=em)
        
        for i in collectionban.find():
            if user in i.values():
                collectionban.delete_one({"id": user})
                
                em = discord.Embed(color=0x1a1a1a)
                em.title = f"{display} has been unbanned!"
                em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {user}```"
                em.set_footer(text=f"Unbanned by {ctx.author}")
                em.set_thumbnail(url=image)
                await msg.edit(embed=em)
                return 0

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"This user is not banned!"
        await msg.edit(embed=em)
    else:
        userId = requests.get(f'https://api.roblox.com/users/get-by-username?username={user}').json()['Id']
        info = requests.get(f'https://users.roblox.com/v1/users/{userId}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl'] 
        display = info['displayName']
        name = info['name']

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Unbanning {user}..."
        msg = await ctx.send(embed=em)

        for i in collectionban.find():
            if str(userId) in i.values():
                collectionban.delete_one({"id": str(userId)})
                
                em = discord.Embed(color=0x1a1a1a)
                em.title = f"{display} has been unbanned!"
                em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {userId}```"
                em.set_footer(text=f"Unbanned by {ctx.author}")
                em.set_thumbnail(url=image)
                await msg.edit(embed=em)
                return 0

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"This user is not banned!"
        await msg.edit(embed=em)


#check
@bot.command()
@commands.cooldown(1, 2.5, commands.BucketType.user)
async def check(ctx, user):
    if user.isnumeric():
        info = requests.get(f'https://users.roblox.com/v1/users/{user}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl']
        display = info['displayName']
        name = info['name']

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Fetching {name}..."
        msg = await ctx.send(embed=em)

        for i in collectionban.find():
            if user in i.values():
                em = discord.Embed(color=0x1a1a1a)
                em.title = f"{name} is banned!"
                em.set_thumbnail(url=image)
                await msg.edit(embed=em)
                return 0

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{name} is not banned!"
        em.set_thumbnail(url=image)
        await msg.edit(embed=em)
    else:
        userId = requests.get(f'https://api.roblox.com/users/get-by-username?username={user}').json()['Id']
        info = requests.get(f'https://users.roblox.com/v1/users/{userId}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl'] 
        display = info['displayName']
        name = info['name']

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Fetching {name}..."
        msg = await ctx.send(embed=em)

        for i in collectionban.find():
            if str(userId) in i.values():
                em = discord.Embed(color=0x1a1a1a)
                em.title = f"{display} is banned!"
                em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {userId}```"
                em.set_thumbnail(url=image)
                await msg.edit(embed=em)
                return 0

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} is not banned!"
        em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {userId}```"
        em.set_thumbnail(url=image)
        await msg.edit(embed=em)


#banlist
@bot.command()
@commands.cooldown(1, 2.5, commands.BucketType.user)
async def banlist(ctx):

    if collectionban.count_documents({}) == 0:
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"API Banlist Not Found!"
        await ctx.send(embed=em)
        return 0

    r = requests.get(f'https://scripts.slave.rip/api/list').json()
    r = str(r)
    r = r.replace("[", "")
    r = r.replace("]", "")
    r = r.replace("'", "")
    r = r.replace(",", "\n\n")
    r = r.replace("ids:", "")
    r = r.replace("{", "")
    r = r.replace("}", "")
    r = r.replace(" ", "")

    em = discord.Embed(color=0x1a1a1a)
    em.title = f"API Banlist"
    em.description = f"```ini\n{r}```"
    await ctx.send(embed=em)


#lookup
@bot.command()
@commands.cooldown(1, 1.5, commands.BucketType.user)
async def lookup(ctx, username):
    em = discord.Embed(color=0x1a1a1a)
    em.title = f"Looking up {username}..."
    msg = await ctx.send(embed=em)

    if username in reserved:
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"This username is blacklisted!"
        await msg.edit(embed=em)
        return 0

    userId = requests.get(f'https://api.roblox.com/users/get-by-username?username={username}').json()

    if userId == {"success":False,"errorMessage":"User not found"}:
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{username} does not exist or has been terminated!"
        await msg.edit(embed=em)
        return 0
    else:
        userId = userId['Id']

    r = requests.get(f'https://users.roblox.com/v1/users/{userId}').json()
    display = r['displayName']
    description = r['description']
    idd = r['id']
    isBanned = r['isBanned']

    friend_count = requests.get(f'https://friends.roblox.com/v1/users/{userId}/friends/count').json()['count']
    follow_count = requests.get(f'https://friends.roblox.com/v1/users/{userId}/followers/count').json()['count']
    following = requests.get(f'https://friends.roblox.com/v1/users/{userId}/followings/count').json()['count']
    image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl']

    rap = robloxpy.User.External.GetRAP(userId)
    creation = robloxpy.User.External.CreationDate(userId)
    age = robloxpy.User.External.GetAge(userId)
    usernamehistory = robloxpy.User.External.UsernameHistory(userId)


    usernamehistory = str(usernamehistory)
    usernamehistory = usernamehistory.replace("[", "")
    usernamehistory = usernamehistory.replace("]", "")
    usernamehistory = usernamehistory.replace("'", "")

    if usernamehistory == len(usernamehistory) > 0:
        usernamehistory = "No Username History"


    if rap == 0:
        rap = "Private or No RAP"

    if description == len(description) > 20:
        description = "Too Long"

    if description == "":
        description = "No Description"
                

    em = discord.Embed(color=0x1a1a1a)
    em.title = f"{display}'s Profile"
    em.url = f"https://www.roblox.com/users/{userId}/profile"
    em.description = f"**User Info**```ini\n[Display Name]: {display}\n[User ID]: {idd}\n[Description]: {description}\n[Account Age]: {age}\n[Creation]: {creation}\n[Terminated]: {isBanned}```\n\n**Social**```ini\n[Friends]: {friend_count}\n[Followers]: {follow_count}\n[Following]: {following}```\n\n**Roblox Info**```ini\n[RAP]: {rap}\n[Username History]: {usernamehistory}```"
    em.set_thumbnail(url=image)
    await msg.edit(embed=em)



#kick
@bot.command()
@commands.cooldown(1, 1.5, commands.BucketType.user)
async def kick(ctx, user):
    if user.isnumeric():
        info = requests.get(f'https://users.roblox.com/v1/users/{user}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl']
        display = info['displayName']
        name = info['name']

        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Kicking {user}..."
        msg = await ctx.send(embed=em)

        if user in reserved:
            em = discord.Embed(color=0x1a1a1a)
            em.title = f"This user is blacklisted!"
            await msg.edit(embed=em)
            return 0

        collectionkick.insert_one({"id": str(userId)})
        asyncio.sleep(0.5)
        collectionkick.delete_one({"id": str(userId)})
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} has been kicked!"
        em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {user}```"
        em.set_footer(text=f"Kicked by {ctx.author}")
        em.set_thumbnail(url=image)
        await msg.edit(embed=em)
        
        # sends to log channel to log the kick
        channel = bot.get_channel(LOG_CHANNEL) 
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{name} has been kicked!"
        em.description = f"Banned by {ctx.author}!"
        em.set_thumbnail(url=image)
        await channel.send(embed=em)
    else:
        userId = requests.get(f'https://api.roblox.com/users/get-by-username?username={user}').json()['Id']
        info = requests.get(f'https://users.roblox.com/v1/users/{userId}').json()
        image = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userId}&size=420x420&format=Png&isCircular=false').json()['data'][0]['imageUrl'] 
        display = info['displayName']
        name = info['name']
        
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"Kicking {user}..."
        msg = await ctx.send(embed=em)

        if user in reserved:
            em = discord.Embed(color=0x1a1a1a)
            em.title = f"This user is blacklisted!"
            await msg.edit(embed=em)
            return 0

        collectionkick.insert_one({"id": str(userId)})
        asyncio.sleep(0.5)
        collectionkick.delete_one({"id": str(userId)})
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} has been kicked!"
        em.description = f"**User Info**```ini\n[Display Name]: {display}\n[Username]: {name}\n[User ID]: {userId}```"
        em.set_footer(text=f"Kicked by {ctx.author}")
        em.set_thumbnail(url=image)
        await msg.edit(embed=em)

        # sends to log channel to log the kick
        channel = bot.get_channel(LOG_CHANNEL) 
        em = discord.Embed(color=0x1a1a1a)
        em.title = f"{display} has been kicked"
        em.description = f"Kicked by {ctx.author}!"
        em.set_thumbnail(url=image)
        await channel.send(embed=em)

bot.run(TOKEN)
