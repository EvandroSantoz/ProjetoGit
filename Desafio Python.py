import tkinter as tk
from tkinter import messagebox
import random
import os

# Lista de participantess
participantes = []

# Função para adicionar participante
def adicionar_participante():
    nome = entry_nome.get()
    presentes = [entry_presente1.get(), entry_presente2.get(), entry_presente3.get()]
    
    if nome and all(presentes):
        participantes.append({"nome": nome, "presentes": presentes})
        listbox_participantes.insert(tk.END, nome)
        entry_nome.delete(0, tk.END)
        entry_presente1.delete(0, tk.END)
        entry_presente2.delete(0, tk.END)
        entry_presente3.delete(0, tk.END)
        verificar_participantes()
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

# Função para realizar o sorteio
def sorteio():
    if len(participantes) < 2:
        messagebox.showwarning("Erro", "Adicione pelo menos dois participantes!")
        return
    
    nomes = [p["nome"] for p in participantes]
    random.shuffle(nomes)
    sorteados = {}
    for i, participante in enumerate(participantes):
        sorteado = nomes[i]
        while sorteado == participante["nome"]:
            random.shuffle(nomes)
            sorteado = nomes[i]
        sorteados[participante["nome"]] = sorteado

    salvar_em_arquivo(sorteados)
    messagebox.showinfo("Sucesso", "Sorteio realizado! Arquivos gerados na pasta 'resultados'.")

# Função para salvar resultados em arquivos
def salvar_em_arquivo(sorteados):
    # Cria a pasta "resultados" caso não exista
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
    
    for tirou, tirado in sorteados.items():
        # Encontra os presentes sugeridos pela pessoa sorteada
        presente_sorteado = next(p for p in participantes if p["nome"] == tirado)
        presentes_texto = "\n".join([f"- {presente}" for presente in presente_sorteado["presentes"]])
        
        # Salva o arquivo na pasta "resultados"
        nome_arquivo = os.path.join("resultados", f"{tirou}.txt")
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Você tirou: {tirado}\n")
            arquivo.write("\nSugestões de presentes:\n")
            arquivo.write(presentes_texto)
    print("Arquivos salvos na pasta 'resultados'.")

# Função para verificar se o botão "Sortear" deve ser exibido
def verificar_participantes():
    if len(participantes) >= 2:
        botao_sortear.grid(row=4, column=1, padx=5, pady=10)

# Configuração da Janela Principal
root = tk.Tk()
root.title("Amigo Secreto 🎅")
root.geometry("600x500")
root.configure(bg=BG_COLOR)

# Frame para Adicionar Participantes
frame_adicionar = tk.Frame(root, bg=BG_COLOR)
frame_adicionar.pack(pady=20)

tk.Label(frame_adicionar, text="Nome:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_adicionar, font=("Arial", 14), width=25)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_adicionar, text="Presente 1:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=5, pady=5)
entry_presente1 = tk.Entry(frame_adicionar, font=("Arial", 14), width=25)
entry_presente1.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_adicionar, text="Presente 2:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=5, pady=5)
entry_presente2 = tk.Entry(frame_adicionar, font=("Arial", 14), width=25)
entry_presente2.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_adicionar, text="Presente 3:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, padx=5, pady=5)
entry_presente3 = tk.Entry(frame_adicionar, font=("Arial", 14), width=25)
entry_presente3.grid(row=3, column=1, padx=5, pady=5)

botao_adicionar = tk.Button(frame_adicionar, text="Adicionar", font=("Arial", 14), bg=BTN_PRIMARY, fg=BG_COLOR, command=adicionar_participante)
botao_adicionar.grid(row=4, column=0, padx=5, pady=10)

# O botão "Sortear" é criado, mas inicialmente não é exibido
botao_sortear = tk.Button(frame_adicionar, text="Sortear", font=("Arial", 14), bg=BTN_SECONDARY, fg=BG_COLOR, command=sorteio)

# Frame para Exibir Participantes
frame_lista = tk.Frame(root, bg=BG_COLOR)
frame_lista.pack(pady=20)

tk.Label(frame_lista, text="Participantes:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
listbox_participantes = tk.Listbox(frame_lista, font=("Arial", 14), width=50, height=10, bg=LIST_BG, fg=LIST_FG)
listbox_participantes.pack(pady=5)

# Loop Principal
root.mainloop()
