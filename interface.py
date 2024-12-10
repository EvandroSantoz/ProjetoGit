import tkinter as tk

# Criando a janela principal
root = tk.Tk()
root.title("Interface Básica com Tkinter 🖥️")
root.geometry("400x300")
root.configure(bg="lightblue")

# Adicionando um Label (Rótulo)
label = tk.Label(root, text="Digite seu nome:", font=("Arial", 14), bg="lightblue")
label.pack(pady=10)  # Adicionando espaçamento vertical

# Adicionando um Entry (Caixa de Texto)
entrada = tk.Entry(root, font=("Arial", 14))
entrada.pack(pady=10)

# Função para capturar e exibir o texto
def exibir_texto():
    texto = entrada.get()  # Obtendo o texto do Entry
    print(f"Você digitou: {texto} 🎉")

# Função para limpar o texto do Entry
def limpar_texto():
    entrada.delete(0, tk.END)  # Apaga o conteúdo do Entry

# Funções para efeitos nos botões
def ao_passar_mouse(event):
    event.widget.configure(bg="yellow", fg="black")  # Muda a cor ao passar o mouse

def ao_sair_mouse(event):
    if event.widget["text"] == "Enviar":
        event.widget.configure(bg="green", fg="white")  # Restaura a cor original do botão "Enviar"
    elif event.widget["text"] == "Limpar":
        event.widget.configure(bg="red", fg="white")  # Restaura a cor original do botão "Limpar"

# Criando um Frame para organizar os botões adicionais
frame_botoes = tk.Frame(root, bg="lightblue")
frame_botoes.pack(pady=10)

# Adicionando botões ao Frame
botao_enviar = tk.Button(frame_botoes, text="Enviar", font=("Arial", 14), bg="green", fg="white", command=exibir_texto)
botao_enviar.pack(side=tk.LEFT, padx=5)

botao_limpar = tk.Button(frame_botoes, text="Limpar", font=("Arial", 14), bg="red", fg="white", command=limpar_texto)
botao_limpar.pack(side=tk.LEFT, padx=5)

# Adicionando os eventos de passar e sair do mouse aos botões
botao_enviar.bind("<Enter>", ao_passar_mouse)  # Evento ao passar o mouse sobre o botão "Enviar"
botao_enviar.bind("<Leave>", ao_sair_mouse)    # Evento ao sair do mouse do botão "Enviar"

botao_limpar.bind("<Enter>", ao_passar_mouse)  # Evento ao passar o mouse sobre o botão "Limpar"
botao_limpar.bind("<Leave>", ao_sair_mouse)    # Evento ao sair do mouse do botão "Limpar"

# Iniciando o loop principal
root.mainloop()
