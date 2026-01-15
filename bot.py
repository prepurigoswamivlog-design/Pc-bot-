import discord
from discord.ext import commands
import json, os, random, time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="owo ",
    intents=intents,
    help_command=None
)

DATA_FILE = "data.json"

# ---------- DATA ----------
def load():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(data, uid):
    if uid not in data:
        data[uid] = {
            "coins": 0,
            "last_daily": 0,
            "xp": 0,
            "level": 1,
            "animals": []
        }
    for k, v in {
        "coins": 0, "last_daily": 0,
        "xp": 0, "level": 1, "animals": []
    }.items():
        if k not in data[uid]:
            data[uid][k] = v
    return data[uid]

# ---------- EVENTS ----------
@bot.event
async def on_ready():
    print("OWO BOT ALL COMMANDS ONLINE")

# ---------- BASIC ----------
@bot.command()
async def hi(ctx):
    await ctx.send("OwO hi 😸")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency*1000)}ms")

# ---------- ECONOMY ----------
@bot.command()
async def balance(ctx):
    data = load()
    u = get_user(data, str(ctx.author.id))
    await ctx.send(f"{ctx.author.mention} 💰 Coins: {u['coins']}")

@bot.command()
async def daily(ctx):
    data = load()
    u = get_user(data, str(ctx.author.id))
    now = int(time.time())
    if now - u["last_daily"] < 86400:
        await ctx.send("⏳ Daily already liya hai")
        return
    u["coins"] += 500
    u["last_daily"] = now
    save(data)
    await ctx.send("🎁 Daily reward: 💰 500 coins")

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    data = load()
    s = get_user(data, str(ctx.author.id))
    r = get_user(data, str(member.id))
    if amount <= 0 or s["coins"] < amount:
        await ctx.send("❌ Coins insufficient")
        return
    s["coins"] -= amount
    r["coins"] += amount
    save(data)
    await ctx.send(f"✅ {member.mention} ko {amount} coins diye")

# ---------- HUNT / ANIMALS ----------
animals_list = [
    ("🐶 Dog", 20), ("🐱 Cat", 30), ("🦊 Fox", 50),
    ("🐻 Bear", 80), ("🐉 Dragon", 150)
]

@bot.command()
async def hunt(ctx):
    data = load()
    u = get_user(data, str(ctx.author.id))
    animal, reward = random.choice(animals_list)
    u["coins"] += reward
    u["xp"] += reward
    u["animals"].append(animal)
    if u["xp"] >= u["level"] * 500:
        u["level"] += 1
        await ctx.send(f"⬆️ LEVEL UP! Level {u['level']}")
    save(data)
    await ctx.send(f"{ctx.author.mention} hunted {animal} 💰 {reward} coins")

@bot.command()
async def inv(ctx):
    data = load()
    u = get_user(data, str(ctx.author.id))
    if not u["animals"]:
        await ctx.send("📦 Inventory khali hai")
        return
    await ctx.send("📦 Animals:\n" + ", ".join(u["animals"]))

# ---------- GAMBLE ----------
@bot.command()
async def cf(ctx, amount: str):
    data = load()
    u = get_user(data, str(ctx.author.id))

    if amount.lower() == "all":
        amount = u["coins"]
    elif amount.isdigit():
        amount = int(amount)
    else:
        await ctx.send("❌ Number ya all likho")
        return

    if amount <= 0 or u["coins"] < amount:
        await ctx.send("❌ Coins insufficient")
        return

    if random.choice([True, False]):
        u["coins"] += amount
        msg = f"🎉 Jeet! +{amount}"
    else:
        u["coins"] -= amount
        msg = f"💀 Haar! -{amount}"

    save(data)
    await ctx.send(msg)

# ---------- FUN ----------
@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 You rolled: {random.randint(1,6)}")

@bot.command()
async def slap(ctx, member: discord.Member):
    await ctx.send(f"😾 {ctx.author.mention} slapped {member.mention}")

# ---------- INFO ----------
@bot.command()
async def profile(ctx):
    data = load()
    u = get_user(data, str(ctx.author.id))
    await ctx.send(
        f"👤 {ctx.author.name}\n"
        f"💰 Coins: {u['coins']}\n"
        f"⭐ Level: {u['level']}\n"
        f"⚡ XP: {u['xp']}\n"
        f"🐾 Animals: {len(u['animals'])}"
    )

@bot.command()
async def help(ctx):
    await ctx.send(
        "**OwO ALL COMMANDS**\n"
        "`owo hi`\n"
        "`owo ping`\n"
        "`owo hunt`\n"
        "`owo inv`\n"
        "`owo balance`\n"
        "`owo daily`\n"
        "`owo cf <amount/all>`\n"
        "`owo give @user amount`\n"
        "`owo roll`\n"
        "`owo slap @user`\n"
        "`owo profile`"
    )

# ---------- RUN ----------
import os
bot.run(os.environ["MTQ2MDk4MTQ0Njk1NjAyNDAwMA.GMWaOG.3BNC7JES0EPaXik8dSQ4xpy2_TZD8RJnOAd8fg"])
