import openai
import telebot
import telegram
import json
import os
from time import sleep

# Lendo os tokens dos arquivos JSON
with open('files/config_api.json', 'r') as f:
    openai_token = json.load(f)['api_key']

with open('files/config_bot.json', 'r') as f:
    telegram_token = json.load(f)['token']

# Autenticação da API do OpenAI
openai.api_key = openai_token

# Iniciando o bot
bot = None

# Tela de carregamento
print('Iniciando o bot...')
for i in range(5):
    print('.'*(i+1))
    sleep(1)

try:
    bot = telegram.Bot(token=telegram_token)
    print('Bot iniciado com sucesso!')
except telegram.TelegramError as e:
    print('Ocorreu um erro ao iniciar o bot:', e)

# Criação do bot do Telegram
tb = telebot.TeleBot(telegram_token)

# Comando para iniciar a conversa com o bot
@tb.message_handler(commands=['start'])
def send_welcome(message):
    tb.reply_to(message, "Olá! Eu sou um bot que responde perguntas. Pergunte-me algo!")

# Responder a mensagens de texto
@tb.message_handler(func=lambda message: True)
def answer_question(message):
    question = message.text.strip()
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Por favor, responda a esta pergunta em português:\n{question}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    tb.reply_to(message, answer)

tb.polling()
