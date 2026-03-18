import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>qazwsxedcrfvtgbyhnujmikolpç"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

def gen_emodji():
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emodji)

def flip_coin():
    flip = random.randint(0, 1)
    if flip == 0:
        return "cara"
    else:
        return "coroa"

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
    
@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! eu sou um bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def mult(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left * right)

@bot.command()
async def help(ctx):
    comandos = """
📜 **Comandos do Bot**

/hello → Cumprimenta o usuário  
/heh → Repete "he" várias vezes  
/add num1 num2 → Soma dois números  
/choose opção1 opção2 ... → Escolhe uma opção aleatória
/mult num1 num2 → Multiplica dois números 

🎲 **RPG**
d20, d12, d8, d6, d4 → Rola dados  

😂 **Diversos**
emoji → Envia um emoji aleatório  
senha → Gera uma senha  
moeda → Cara ou coroa
"""
    await ctx.send(comandos)

@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    if message.content.startswith('emoji'):
        await message.channel.send(gen_emodji())
    elif message.content.startswith('senha'):
        await message.channel.send(gen_pass(10))
    elif message.content.startswith('moeda'):
        await message.channel.send(flip_coin())
    elif message.content.startswith('d20'):
        resultado = random.randint(1, 20)
        await message.channel.send(resultado)
    elif message.content.startswith('d12'):
        resultado = random.randint(1, 12)
        await message.channel.send(resultado)
    elif message.content.startswith('d8'):
        resultado = random.randint(1, 8)
        await message.channel.send(resultado)
    elif message.content.startswith('d6'):
        resultado = random.randint(1, 6)
        await message.channel.send(resultado)
    elif message.content.startswith('d4'):
        resultado = random.randint(1, 4)
        await message.channel.send(resultado)
    await bot.process_commands(message)

bot.run("MTQ3ODE1MDE3NDI2OTUwOTgzNg.Gdj_XE.9DRc3dlCy0bgqowMU8UldNdBV2ydFSmx5jceL0")
