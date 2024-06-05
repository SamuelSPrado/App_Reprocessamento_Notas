import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
from request_manager import RequestManager
import time
import random

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Reprocessamento de Notas")

        # Labels e campos de entrada
        tk.Label(root, text="Owner ID:").grid(row=0, column=0, padx=10, pady=10)
        self.owner_id_entry = tk.Entry(root)
        self.owner_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Botões
        tk.Button(root, text="Enviar por Período", command=self.abrir_janela_periodo).grid(row=1, column=0,
                                                                                           columnspan=2, pady=10)
        tk.Button(root, text="Enviar por ID", command=self.enviar_por_id).grid(row=2, column=0, columnspan=2, pady=10)

    def log_message(self, message):
        print(message)

    def abrir_janela_periodo(self):
        self.period_window = tk.Toplevel(self.root)
        self.period_window.title("Enviar por Período")

        # Adicionar o nome do local no topo
        local_name = self.get_owner_name(self.owner_id_entry.get())
        tk.Label(self.period_window, text=f"{local_name}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.period_window, text="Owner ID:").grid(row=1, column=0, padx=10, pady=10)
        owner_id_label = tk.Label(self.period_window, text=self.owner_id_entry.get())
        owner_id_label.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.period_window, text="Data Inicial:").grid(row=2, column=0, padx=10, pady=10)
        self.start_date_entry = tk.Entry(self.period_window)
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.period_window, text="Data Final:").grid(row=3, column=0, padx=10, pady=10)
        self.end_date_entry = tk.Entry(self.period_window)
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.period_window, text="Reprocessar Notas", command=self.enviar_por_periodo).grid(row=4, column=0,
                                                                                           columnspan=2, pady=10)
        tk.Button(self.period_window, text="Voltar", command=self.voltar).grid(row=5, column=0, columnspan=2, pady=10)

    def enviar_por_periodo(self):
        owner_id = self.owner_id_entry.get()
        start_date_input = self.start_date_entry.get()
        end_date_input = self.end_date_entry.get()

        try:
            start_date = datetime.strptime(start_date_input + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(end_date_input + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Erro de Formato", "Por favor, insira as datas no formato correto (AAAA-MM-DD).")
            return

        excel_file_path = f"Reprocessamento {start_date_input} a {end_date_input}.xlsx"
        request_manager = RequestManager(owner_id, self.log_message, excel_file_path)

        # Dividir o período em intervalos de 1 hora
        interval = timedelta(hours=1)
        current_start = start_date

        while current_start < end_date:
            current_end = min(current_start + interval, end_date)
            print(f"Processando de {current_start} até {current_end}")
            request_manager.processar_intervalo(current_start, current_end)
            current_start = current_end
            time.sleep(1)  # Esperar 1 segundo entre as requisições

        messagebox.showinfo("Concluído", "Processamento por período concluído com sucesso!")
        self.period_window.destroy()

    def enviar_por_id(self):
        owner_id = self.owner_id_entry.get()
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
            return

        request_manager = RequestManager(owner_id, self.log_message)
        request_manager.processar_por_id(file_path)
        messagebox.showinfo("Concluído", "Processamento por ID concluído com sucesso!")

    def voltar(self):
        self.period_window.destroy()

    def get_owner_name(self, owner_id):
        # Dicionário de exemplos de Owner IDs e nomes correspondentes
        owners = [
            {"id": "FE77413A-30A5-785F-2406-D285CD393D24", "name": "MTC - Unidade I"},
            {"id": "1A2B3C4D-5E6F-7G8H-9I0J-KLMNOPQRSTU", "name": "Local ABC"},
            {"id": "9Z8Y7X6W-5V4U-3T2S-1RQ0P-ONMLKJIHGFED", "name": "Loja XYZ"},
            # Adicione mais Owner IDs e nomes correspondentes conforme necessário
        ]

        # Procura o nome correspondente ao Owner ID fornecido
        for owner in owners:
            if owner["id"] == owner_id:
                return owner["name"]
        return "N/A"


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()