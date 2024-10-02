import customtkinter as ctk
from tkinter import messagebox, Canvas, Scrollbar, Frame
from datetime import datetime, timedelta
import json
import os

# Caminho do arquivo JSON para armazenar os clientes
ARQUIVO_CLIENTES = "clientes.json"

# Função para carregar clientes do arquivo JSON
def carregar_clientes():
    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, "r") as arquivo:
            return json.load(arquivo)
    return []

# Função para salvar clientes no arquivo JSON
def salvar_clientes():
    with open(ARQUIVO_CLIENTES, "w") as arquivo:
        json.dump(clientes, arquivo)

# Lista de clientes
clientes = carregar_clientes()

# Função para calcular o vencimento
def calcular_vencimento(data_entrada):
    entrada_date = datetime.strptime(data_entrada, "%Y-%m-%d")
    vencimento_date = entrada_date + timedelta(days=30)
    return vencimento_date.strftime("%Y-%m-%d")

# Função para adicionar cliente
def adicionar_cliente():
    nome = entry_nome.get()
    barco = entry_barco.get()
    data_entrada = entry_data.get()
    mensalidade = entry_mensalidade.get()
    contato = entry_contato.get()

    if nome and barco and data_entrada and mensalidade and contato:
        try:
            vencimento = calcular_vencimento(data_entrada)
            cliente = {
                "nome": nome,
                "barco": barco,
                "data_entrada": data_entrada,
                "mensalidade": float(mensalidade),
                "vencimento": vencimento,
                "status_pago": False,
                "contato": contato
            }
            clientes.append(cliente)
            salvar_clientes()
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            limpar_campos()
        except ValueError:
            messagebox.showerror("Erro", "Data de entrada inválida. Use o formato YYYY-MM-DD.")
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

# Função para limpar os campos
def limpar_campos():
    entry_nome.delete(0, ctk.END)
    entry_barco.delete(0, ctk.END)
    entry_data.delete(0, ctk.END)
    entry_mensalidade.delete(0, ctk.END)
    entry_contato.delete(0, ctk.END)

# Função para exibir a lista de clientes
def exibir_clientes():
    for widget in frame_clientes.winfo_children():
        widget.destroy()

    if not clientes:
        mensagem = ctk.CTkLabel(frame_clientes, text="Nenhum cliente encontrado.")
        mensagem.pack(pady=5)
        return
    
    for index, cliente in enumerate(clientes):
        status = "Pago" if cliente.get('status_pago') else "Não Pago"
        item_text = (f"{cliente.get('nome')} - {cliente.get('barco')} - "
                     f"{cliente.get('data_entrada')} - R${cliente.get('mensalidade')} - "
                     f"Vencimento: {cliente.get('vencimento')} - {status} - "
                     f"Contato: {cliente.get('contato')}")
        
        cliente_label = ctk.CTkLabel(frame_clientes, text=item_text)
        cliente_label.pack(anchor='w', padx=10, pady=5)

        botao_pagamento = ctk.CTkButton(frame_clientes, text="Marcar Pagamento", command=lambda idx=index: marcar_pagamento(idx))
        botao_pagamento.pack(anchor='e', padx=10, pady=5)

        botao_excluir = ctk.CTkButton(frame_clientes, text="Excluir Cliente", command=lambda idx=index: excluir_cliente(idx))
        botao_excluir.pack(anchor='e', padx=10, pady=5)

# Função para marcar pagamento
def marcar_pagamento(index):
    if index >= 0 and index < len(clientes):
        clientes[index]['status_pago'] = True
        clientes[index]['vencimento'] = calcular_vencimento(clientes[index]['vencimento'])
        salvar_clientes()
        messagebox.showinfo("Sucesso", "Pagamento confirmado e data de vencimento atualizada!")
        exibir_clientes()

# Função para excluir cliente
def excluir_cliente(index):
    if index >= 0 and index < len(clientes):
        clientes.pop(index)
        salvar_clientes()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        exibir_clientes()

# Interface gráfica
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

root = ctk.CTk()  # Mudando para CTk
root.title("Registro de Clientes")

# Campos de entrada
ctk.CTkLabel(root, text="Nome do Cliente:").pack(pady=5)
entry_nome = ctk.CTkEntry(root)
entry_nome.pack(pady=5)

ctk.CTkLabel(root, text="Nome do Barco:").pack(pady=5)
entry_barco = ctk.CTkEntry(root)
entry_barco.pack(pady=5)

ctk.CTkLabel(root, text="Data de Entrada (YYYY-MM-DD):").pack(pady=5)
entry_data = ctk.CTkEntry(root)
entry_data.pack(pady=5)

ctk.CTkLabel(root, text="Valor da Mensalidade:").pack(pady=5)
entry_mensalidade = ctk.CTkEntry(root)
entry_mensalidade.pack(pady=5)

ctk.CTkLabel(root, text="Número de Contato:").pack(pady=5)
entry_contato = ctk.CTkEntry(root)
entry_contato.pack(pady=5)

# Botão para adicionar cliente
botao_adicionar = ctk.CTkButton(root, text="Adicionar Cliente", command=adicionar_cliente)
botao_adicionar.pack(pady=10)

# Frame para exibir a lista de clientes com rolagem
frame_lista = ctk.CTkFrame(root)
frame_lista.pack(pady=10)

canvas = Canvas(frame_lista)
scrollbar_vertical = Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
scrollbar_horizontal = Scrollbar(frame_lista, orient="horizontal", command=canvas.xview)
frame_clientes = Frame(canvas)

# Configurando a rolagem
canvas.create_window((0, 0), window=frame_clientes, anchor='nw')

def atualizar_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_clientes.bind("<Configure>", atualizar_scrollregion)

canvas.configure(yscrollcommand=scrollbar_vertical.set)
canvas.configure(xscrollcommand=scrollbar_horizontal.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar_vertical.pack(side="right", fill="y")
scrollbar_horizontal.pack(side="bottom", fill="x")

# Botão para exibir a lista de clientes
botao_exibir = ctk.CTkButton(root, text="Exibir Lista de Clientes", command=exibir_clientes)
botao_exibir.pack(pady=10)

# Executar a interface
root.mainloop()
