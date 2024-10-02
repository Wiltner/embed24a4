import telepot
import requests
import os

# Substitua pelos seus tokens
TELEGRAM_BOT_TOKEN = '7913426910:AAFY9Q0KcQ36k9594OPG-6ESAsxZ66PKUWw'
REMOVE_BG_API_KEY = 'DNf4ZJi7Rs2smHgReTgjJcBf'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'photo':
        # Obter o maior tamanho de foto disponível
        file_id = msg['photo'][-1]['file_id']
        file_path = bot.getFile(file_id)['file_path']
        file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
        
        # Baixar a imagem
        response = requests.get(file_url)
        image_path = 'temp_image.png'
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        # Enviar a imagem para a API remove.bg
        with open(image_path, 'rb') as f:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': f},
                data={'size': 'auto'},
                headers={'X-Api-Key': REMOVE_BG_API_KEY}
            )
        
        # Verificar se a API remove.bg retornou a imagem processada
        if response.status_code == requests.codes.ok:
            with open('no_bg_image.png', 'wb') as out:
                out.write(response.content)
            
            # Enviar a imagem processada de volta ao usuário
            bot.sendPhoto(chat_id, photo=open('no_bg_image.png', 'rb'))
        else:
            bot.sendMessage(chat_id, 'Erro ao processar a imagem.')
        
        # Remover arquivos temporários
        os.remove(image_path)
        os.remove('no_bg_image.png')
    else:
        bot.sendMessage(chat_id, 'Por favor, envie uma imagem.')

# Inicializar o bot
bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
bot.message_loop(handle)

# Manter o programa rodando
print('Bot está funcionando...')
while True:
    pass