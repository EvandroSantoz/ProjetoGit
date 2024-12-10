import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests  # Para buscar os links dos presentes

# Entrada de Dados
participantes = []

def adicionar_participante(nome, email, presentes):
    participantes.append({
        "nome": nome,
        "email": email,
        "presentes": presentes
    })

def buscar_links(presente):
    # Exemplo com Mercado Livre
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={presente}"
    response = requests.get(url)
    data = response.json()
    links = [item['permalink'] for item in data['results'][:3]]  # Pega os primeiros 3 resultados
    return links

def sorteio(participantes):
    nomes = [p['nome'] for p in participantes]
    random.shuffle(nomes)
    sorteados = {}
    for i, participante in enumerate(participantes):
        sorteado = nomes[i]
        while sorteado == participante['nome']:
            random.shuffle(nomes)
            sorteado = nomes[i]
        sorteados[participante['nome']] = sorteado
    return sorteados

def enviar_email(destinatario, amigo_secreto, presentes):
    remetente = "seu_email@gmail.com"
    senha = "sua_senha"
    subject = "Amigo Secreto 🎁"
    
    # Corpo do e-mail
    corpo = f"""
    Olá, {destinatario['nome']}!
    
    Seu amigo secreto é: {amigo_secreto}.
    
    Sugestões de presentes:
    1. {presentes[0]}
    2. {presentes[1]}
    3. {presentes[2]}
    
    Boa sorte e divirta-se! 🎉
    """
    
    # Configuração do e-mail
    message = MIMEMultipart()
    message['From'] = remetente
    message['To'] = destinatario['email']
    message['Subject'] = subject
    message.attach(MIMEText(corpo, 'plain'))
    
    # Enviar o e-mail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(message)

# Exemplo de Uso
adicionar_participante("Alice", "alice@email.com", ["Livro", "Caneca", "Chocolates"])
adicionar_participante("Bob", "bob@email.com", ["Jogo de Tabuleiro", "Fone de Ouvido", "Camisa"])
adicionar_participante("Carol", "carol@email.com", ["Perfume", "Bolsa", "Agenda"])

# Buscar Links dos Presentes
for participante in participantes:
    participante['links'] = [buscar_links(p) for p in participante['presentes']]

# Realizar Sorteio
sorteados = sorteio(participantes)

# Enviar E-mails
for participante in participantes:
    amigo = sorteados[participante['nome']]
    amigo_info = next(p for p in participantes if p['nome'] == amigo)
    enviar_email(participante, amigo_info['nome'], amigo_info['links'])
