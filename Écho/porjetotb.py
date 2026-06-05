import discord
import random
# A variável intents armazena as permissões do bot
intents = discord.Intents.default()
# Ativar a permissão para ler o conteúdo das mensagens
intents.message_content = True
# Criar um bot e passar as permissões
client = discord.Client(intents=intents)

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
    flip = random.randint(0, 2)
    if flip == 0:
        return "cara"
    else:
        return "coroa"

@client.event
async def on_ready():
    print(f'Fizemos login como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send("Hello!")
    elif message.content.startswith('$bye'):
        await message.channel.send("\U0001f642")
    elif message.content.startswith('emoji'):
        await message.channel.send(gen_emodji())
    elif message.content.startswith('moeda'):
        await message.channel.send(flip_coin())
    elif message.content.startswith('senha'):
        await message.channel.send(gen_pass(10))
    elif message.content.startswith('d20'):
        resultado = random.randint(1, 20)
        await message.channel.send(resultado)
    elif message.content.startswith('d12'):
        resultado = random.randint(1, 12)
        await message.channel.send(resultado)
    elif message.content.startswith('d8'):
        resultado = random.randint(1, 8)
        await message.channel.send(resultado)
    elif message.content.startswith('d4'):
        resultado = random.randint(1, 4)
        await message.channel.send(resultado)
    else:
        await message.channel.send(message.content)

client.run("TOLKEN")