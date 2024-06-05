import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime, timedelta
from request_manager import RequestManager
from logger import logger


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Reprocessamento de Notas")

        # Labels e campos de entrada
        tk.Label(root, text="Owner ID:").grid(row=0, column=0, padx=10, pady=10)
        self.owner_id_entry = tk.Entry(root)
        self.owner_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Data Inicial (AAAA-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        self.start_date_entry = tk.Entry(root)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Data Final (AAAA-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        self.end_date_entry = tk.Entry(root)
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botões
        tk.Button(root, text="Enviar por Período", command=self.enviar_por_periodo).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Enviar por ID", command=self.enviar_por_id).grid(row=4, column=0, columnspan=2, pady=10)

        # Área de logs
        self.log_text = ScrolledText(root, width=50, height=20)
        self.log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.log_text.config(state=tk.DISABLED)

    def log_message(self, message: str) -> None:
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
        logger.info(message)

    def enviar_por_periodo(self):
        owner_id = self.owner_id_entry.get()
        start_date_input = self.start_date_entry.get()
        end_date_input = self.end_date_entry.get()

        if not owner_id:
            messagebox.showerror("Erro", "Owner ID não pode estar vazio.")
            return

        try:
            start_date = datetime.strptime(start_date_input + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(end_date_input + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Erro de Formato", "Por favor, insira as datas no formato correto (AAAA-MM-DD).")
            return

        excel_file_path = f"Reprocessamento_{start_date_input}_a_{end_date_input}.xlsx"
        request_manager = RequestManager(owner_id, excel_file_path)

        current_start = start_date
        while current_start < end_date:
            current_end = min(current_start + timedelta(hours=1), end_date)
            request_manager.processar_intervalo(current_start, current_end)
            current_start = current_end + timedelta(seconds=1)
            self.log_message(f"Processado período de {current_start} a {current_end}")

        messagebox.showinfo("Concluído", "Processamento por período concluído com sucesso!")

    def enviar_por_id(self):
        owner_id = self.owner_id_entry.get()
        if not owner_id:
            messagebox.showerror("Erro", "Owner ID não pode estar vazio.")
            return

        id_file_path = filedialog.askopenfilename(title="Selecione o arquivo de IDs", filetypes=[("Text Files", "*.txt")])
        if not id_file_path:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
            return

        excel_file_path = f"Reprocessamento_por_ID_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        request_manager = RequestManager(owner_id, excel_file_path)
        request_manager.processar_por_id(id_file_path)
        messagebox.showinfo("Concluído", "Processamento por ID concluído com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()