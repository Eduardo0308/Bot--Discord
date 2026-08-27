import discord
import random
import os
import requests
from discord.ext import commands
from comandos import get_class
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from deep_translator import GoogleTranslator



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
async def d20(ctx):
    resultado = random.randint(1, 20)
    await ctx.send(resultado)

@bot.command()
async def d12(ctx):
    resultado = random.randint(1, 12)
    await ctx.send(resultado)

@bot.command()
async def d8(ctx):
    resultado = random.randint(1, 8)
    await ctx.send(resultado)

@bot.command()
async def d6(ctx):
    resultado = random.randint(1, 6)
    await ctx.send(resultado)

@bot.command()
async def d4(ctx):
    resultado = random.randint(1, 4)
    await ctx.send(resultado)

@bot.command()
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)

@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    if membro is None:
        membro = ctx.author
    
    await ctx.send(membro.avatar.url)

    

@bot.command()
async def m_ambiente(ctx):
    ideias = [
        "Reaproveitar potes de vidro e embalagens",
        "Usar folhas de papel frente e verso",
        "Transformar roupas velhas em panos de limpeza",
        "Utilizar sacolas reutilizáveis",
        "Evitar copos e talheres descartáveis", 
        "Usar garrafas reutilizáveis",
        "Separar papel, plástico, vidro e metal para reciclagem",
        "Não misturar lixo orgânico com reciclável",
        "Levar pilhas e eletrônicos a pontos de coleta",
        "Usar transporte sustentável"
    ]
    await ctx.send(random.sample(ideias, 3))

@bot.command()
async def r_desperdicio(ctx):
    praticas = [
        "Planejar as refeições antes de fazer compras",
        "Aproveitar sobras em novas receitas", 
        "Fazer compostagem com restos de alimentos",
        "Fechar a torneira ao usar",
        "Verificar vazamentos regularmente",
        "Usar lâmpadas LED(gastam menos energia)",
        "Aproveitar a luz natural",
        "Desligar aparelhos que não estão sendo usados"
    ]
    await ctx.send(random.sample(praticas, 3))

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! eu sou {bot.user}!')

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
/meme → Gera um meme aleatório
/salvar → Salva qualuqer imagem que você mandar
/duck → Gera uma imagem de patos
/indent → Indentifica se a imagem é real ou feita por IA

🎲 **RPG**
d20, d12, d8, d6, d4 → Rola dados  

😂 **Diversos**
emoji → Envia um emoji aleatório  
senha → Gera uma senha  
moeda → Cara ou coroa
"""
    await ctx.send(comandos)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)


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
    await bot.process_commands(message)

@bot.command()
async def meme(ctx):
    lista = os.listdir("images")

    imagem_selecionada = random.choice(lista)


    with open(f'images/{imagem_selecionada}', 'rb') as f:
        #Vamos armazenar o arquivo convertido da biblioteca do Discord nesta variável!
        picture = discord.File(f)
    # Podemos então enviar esse arquivo como um parâmetro
    await ctx.send(file=picture)

@bot.command()
async def salvar(ctx):
    lista = ctx.message.attachments
    for attachment in lista:
        await attachment.save(f"images/{attachment.filename}")
    await ctx.send(f"Imagem(ns):{attachment.filename} foi(ram) salva(s) com sucesso!")

@bot.command()
async def indent(ctx):
    anexo = ctx.message.attachments[0]
    caminho_imagem = f"images/{anexo.filename}"
    await anexo.save(caminho_imagem)

    classe = get_class("keras_model.h5",
                        "labels.txt",
                        caminho_imagem)
    if not ctx.message.attachments:
        await ctx.send("Envie uma imagem junto com o comando!")
        return
    if classe.strip() == "IA images":
        await ctx.send("Essa imagem é feita por IA")
    elif classe.strip() == "Real images":
        await ctx.send("Essa imagem é real")

@bot.tree.command(name="traduzir", description="Traduz um texto")
async def traduzir(interaction: discord.Interaction, texto: str, idioma: str = "en"):
    try:
        traducao = GoogleTranslator(source="auto", target=idioma).translate(texto)
        await interaction.response.send_message(f"**Tradução ({idioma}):**\n{traducao}")
    except Exception as e:
        await interaction.response.send_message(f"Erro ao traduzir: {e}")


bot.run("MTQ3ODE1MDE3NDI2OTUwOTgzNg.GyrIVU.xl9hosYHvxwvgxmIIMQB6dOD21r7ceC73woWSM")