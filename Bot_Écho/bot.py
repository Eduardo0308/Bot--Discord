import discord
import random
import os
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from comandos import get_class
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from deep_translator import GoogleTranslator
import pyttsx3


# Carrega as variáveis do arquivo .env (onde fica o token)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Permissões do bot (precisa ler o conteúdo das mensagens)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)


# ===================================================
# FUNÇÕES AUXILIARES
# ===================================================

def gen_pass(pass_length):
    """Gera uma senha aleatória com o tamanho informado."""
    elements = "+-/*!&$#?=@<>qazwsxedcrfvtgbyhnujmikolpç"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password


def gen_emodji():
    """Escolhe um emoji aleatório da lista."""
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emodji)


def flip_coin():
    """Joga uma moeda e retorna 'cara' ou 'coroa'."""
    flip = random.randint(0, 1)
    if flip == 0:
        return "cara"
    else:
        return "coroa"


def get_duck_image_url():
    """Busca o link de uma imagem aleatória de pato na API."""
    url = 'https://random-d.uk/api/random'
    res = requests.get(url, timeout=10)
    data = res.json()
    return data['url']


# ===================================================
# EVENTOS
# ===================================================

@bot.event
async def on_ready():
    """Executa quando o bot conecta ao Discord."""
    print(f'Estamos logados como {bot.user}')
    # Registra os comandos de barra (/traduzir e /resumir) no Discord
    await bot.tree.sync()
    print("Slash commands sincronizados!")


@bot.event
async def on_message(message):
    """Responde a palavras-chave enviadas no chat."""
    # Ignora as mensagens do próprio bot
    if message.author == bot.user:
        return

    if message.content.startswith('emoji'):
        await message.channel.send(gen_emodji())
    elif message.content.startswith('senha'):
        await message.channel.send(gen_pass(10))
    elif message.content.startswith('moeda'):
        await message.channel.send(flip_coin())

    # Necessário para os comandos com "/" continuarem funcionando
    await bot.process_commands(message)


# ===================================================
# COMANDOS GERAIS
# ===================================================

@bot.command()
async def help(ctx):
    """Mostra a lista de comandos do bot."""
    comandos = """
📜 **Comandos do Bot**

/start → Apresentação do Écho
/hello → Cumprimenta o usuário
/heh → Repete "he" várias vezes
/choose opção1 opção2 ... → Escolhe uma opção aleatória
/magic_ball pergunta → Responde sua pergunta como uma bola 8 mágica
/avatar [@membro] → Mostra o avatar seu ou de outro membro
/limpar quantidade → Apaga mensagens do canal (precisa de permissão)

🧮 **Matemática**
/add num1 num2 → Soma dois números
/sub num1 num2 → Subtrai dois números
/mult num1 num2 → Multiplica dois números

🖼️ **Imagens**
/meme → Envia um meme aleatório
/salvar → Salva as imagens que você mandar junto com o comando
/duck → Envia uma imagem de pato
/identificar_imagem → Identifica se a imagem é real ou feita por IA

🌍 **Tradução e Texto**
/traduzir texto idioma → Traduz um texto para o idioma escolhido
/resumir texto frases → Resume um texto longo

🌦️ **Clima**
/tempo_hj cidade → Mostra o clima real da cidade
/temperatura → Sorteia uma temperatura (só de brincadeira!)

🌱 **Sustentabilidade**
/m_ambiente → Dá dicas de sustentabilidade
/r_desperdicio → Dá dicas para reduzir desperdício

🎲 **RPG**
/dado lados → Rola um dado (ex: /dado 20)

😂 **Diversos**
emoji → Envia um emoji aleatório
senha → Gera uma senha
moeda → Cara ou coroa

⚠️ *Os comandos /traduzir e /resumir usam o menu de barra "/" do Discord — digite "/" e escolha na lista, em vez de digitar o comando inteiro como texto.*
"""
    await ctx.send(comandos)


@bot.command()
async def start(ctx):
    """Apresentação do bot."""
    await ctx.send("Olá! Eu sou o Écho! O que vamos fazer hoje? Digite /help para ver meus comandos.")


@bot.command()
async def hello(ctx):
    """Cumprimenta o usuário."""
    await ctx.send(f'Olá! Eu sou {bot.user}!')


@bot.command()
async def heh(ctx, count_heh: int = 5):
    """Repete 'he' a quantidade de vezes informada."""
    await ctx.send("he" * count_heh)


@bot.command()
async def choose(ctx, *choices: str):
    """Escolhe uma opção aleatória entre as informadas."""
    # Verifica se o usuário mandou pelo menos uma opção
    if not choices:
        await ctx.send("Informe as opções! Exemplo: /choose pizza hambúrguer sushi")
        return
    await ctx.send(random.choice(choices))


@bot.command()
async def magic_ball(ctx, *, pergunta: str = None):
    """Responde a pergunta do usuário como uma bola 8 mágica."""
    if pergunta is None:
        await ctx.send("Faça uma pergunta! Exemplo: /magic_ball Vou passar na prova?")
        return

    respostas = [
        "🎱 Com certeza!",
        "🎱 Provavelmente sim.",
        "🎱 Não conte com isso.",
        "🎱 Acho que não.",
        "🎱 Talvez...",
        "🎱 Definitivamente não.",
        "🎱 As estrelas dizem que sim!",
        "🎱 Melhor perguntar novamente."
    ]
    resposta = random.choice(respostas)
    await ctx.send(f"❓ **{pergunta}**\n{resposta}")


@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    """Mostra o avatar do membro (ou de quem usou o comando)."""
    if membro is None:
        membro = ctx.author
    # display_avatar funciona mesmo se a pessoa não tiver foto personalizada
    await ctx.send(membro.display_avatar.url)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    """Apaga mensagens do canal (só para quem pode gerenciar mensagens)."""
    # +1 para apagar também a mensagem do comando
    await ctx.channel.purge(limit=quantidade + 1)


# ===================================================
# COMANDOS DE MATEMÁTICA
# ===================================================

@bot.command()
async def add(ctx, left: int, right: int):
    """Soma dois números."""
    await ctx.send(left + right)


@bot.command()
async def sub(ctx, left: int, right: int):
    """Subtrai dois números."""
    await ctx.send(left - right)


@bot.command()
async def mult(ctx, left: int, right: int):
    """Multiplica dois números."""
    await ctx.send(left * right)


# ===================================================
# COMANDOS DE RPG
# ===================================================

@bot.command()
async def dado(ctx, lados: int = 6):
    """Rola um dado com a quantidade de lados informada."""
    if lados < 2:
        await ctx.send("O dado precisa ter pelo menos 2 lados!")
        return
    resultado = random.randint(1, lados)
    await ctx.send(f"🎲 d{lados}: {resultado}")


# ===================================================
# COMANDOS DE CLIMA
# ===================================================

@bot.command()
async def tempo_hj(ctx, *, cidade: str = None):
    """Mostra o clima real da cidade usando a API do wttr.in."""
    if cidade is None:
        await ctx.send("Informe a cidade! Exemplo: /tempo_hj São Paulo")
        return

    url = f"https://wttr.in/{cidade}?format=%C+%h+%w+%l"

    # try/except evita que o bot quebre se a internet ou a API falharem
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            await ctx.send(f"🌦️ {resposta.text}")
        else:
            await ctx.send("Conexão mal sucedida. Tente novamente mais tarde.")
    except requests.RequestException:
        await ctx.send("Não consegui acessar o serviço de clima agora.")

@bot.command()
async def fatos(ctx):
    motor = pyttsx3.init()
# Criando um dicionário de exemplo

    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        await ctx.send(resposta.json())
        motor.say(resposta.json())
        motor.runAndWait()
        motor.stop()
    else:
        await ctx.send("Conexão falhou.")

@bot.command()
async def temperatura(ctx):
    """Sorteia uma temperatura aleatória (não é um dado real)."""
    temp = random.randint(-10, 40)
    await ctx.send(f"🌡️ Temperatura sorteada: **{temp}°C**! (Para o clima real, use /tempo_hj cidade)")


# ===================================================
# COMANDOS DE SUSTENTABILIDADE
# ===================================================

@bot.command()
async def m_ambiente(ctx):
    """Envia 3 ideias para ajudar o meio ambiente."""
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
    escolhidas = random.sample(ideias, 3)
    # Mostra uma ideia por linha, em vez da lista com colchetes
    await ctx.send("🌱 " + "\n🌱 ".join(escolhidas))


@bot.command()
async def r_desperdicio(ctx):
    """Envia 3 dicas para reduzir o desperdício."""
    praticas = [
        "Planejar as refeições antes de fazer compras",
        "Aproveitar sobras em novas receitas",
        "Fazer compostagem com restos de alimentos",
        "Fechar a torneira ao usar",
        "Verificar vazamentos regularmente",
        "Usar lâmpadas LED (gastam menos energia)",
        "Aproveitar a luz natural",
        "Desligar aparelhos que não estão sendo usados"
    ]
    escolhidas = random.sample(praticas, 3)
    await ctx.send("♻️ " + "\n♻️ ".join(escolhidas))


# ===================================================
# COMANDOS DE IMAGEM
# ===================================================

@bot.command()
async def duck(ctx):
    """Envia uma imagem aleatória de pato."""
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command()
async def meme(ctx):
    """Envia um meme aleatório da pasta images."""
    lista = os.listdir("images")

    if not lista:
        await ctx.send("Ainda não tem nenhuma imagem salva!")
        return

    imagem_selecionada = random.choice(lista)

    with open(f'images/{imagem_selecionada}', 'rb') as f:
        # Converte o arquivo para o formato que o Discord aceita
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command()
async def salvar(ctx):
    """Salva na pasta images as imagens enviadas junto com o comando."""
    lista = ctx.message.attachments

    # Verifica se a pessoa mandou algum arquivo
    if not lista:
        await ctx.send("Envie uma imagem junto com o comando!")
        return

    nomes = []
    for attachment in lista:
        await attachment.save(f"images/{attachment.filename}")
        nomes.append(attachment.filename)

    await ctx.send(f"Imagem(ns) salva(s) com sucesso: {', '.join(nomes)}")


@bot.command()
async def identificar_imagem(ctx):
    """Identifica se a imagem enviada é real ou feita por IA."""
    # Verifica ANTES de acessar o anexo, para não dar erro
    if not ctx.message.attachments:
        await ctx.send("Envie uma imagem junto com o comando!")
        return

    anexo = ctx.message.attachments[0]
    caminho_imagem = f"images/{anexo.filename}"
    await anexo.save(caminho_imagem)

    classe = get_class("keras_model.h5", "labels.txt", caminho_imagem)

    if classe.strip() == "IA images":
        await ctx.send("Essa imagem é feita por IA")
    elif classe.strip() == "Real images":
        await ctx.send("Essa imagem é real")
    else:
        await ctx.send("Não consegui identificar essa imagem.")


# ===================================================
# COMANDOS DE BARRA (SLASH COMMANDS)
# ===================================================

@bot.tree.command(name="traduzir", description="Traduz um texto")
@app_commands.choices(idioma=[
    app_commands.Choice(name="Inglês", value="en"),
    app_commands.Choice(name="Espanhol", value="es"),
    app_commands.Choice(name="Francês", value="fr"),
    app_commands.Choice(name="Italiano", value="it"),
    app_commands.Choice(name="Alemão", value="de"),
    app_commands.Choice(name="Japonês", value="ja"),
    app_commands.Choice(name="Chinês", value="zh-CN"),
    app_commands.Choice(name="Russo", value="ru"),
    app_commands.Choice(name="Português", value="pt"),
])
async def traduzir(interaction: discord.Interaction, texto: str, idioma: app_commands.Choice[str]):
    """Traduz o texto para o idioma escolhido no menu."""
    try:
        traducao = GoogleTranslator(source="auto", target=idioma.value).translate(texto)
        await interaction.response.send_message(f"**Tradução ({idioma.name}):**\n{traducao}")
    except Exception as e:
        await interaction.response.send_message(f"Erro ao traduzir: {e}")


@bot.tree.command(name="resumir", description="Resume um texto longo")
async def resumir(interaction: discord.Interaction, texto: str, frases: int = 3):
    """Resume o texto usando a quantidade de frases escolhida."""
    try:
        parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
        summarizer = LexRankSummarizer()
        resumo = summarizer(parser.document, frases)
        resultado = " ".join(str(frase) for frase in resumo)
        await interaction.response.send_message(f"**Resumo:**\n{resultado}")
    except Exception as e:
        await interaction.response.send_message(f"Erro ao resumir: {e}")


# ===================================================
# INICIAR O BOT
# ===================================================

bot.run(TOLKEN)
