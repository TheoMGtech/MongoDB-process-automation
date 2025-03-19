import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import time

def open_mongo():
    # Fecha a janela popup
    janela.destroy()

    # Abre o mongod.exe em uma nova janela do cmd
    subprocess.Popen(
        ["start", "", "C:\\Program Files\\MongoDB\\Server\\8.0\\bin\\mongod.exe"],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    # Aguarda 3 segundos
    time.sleep(3)

    # Abre o mongosh.exe em uma nova janela do cmd
    subprocess.Popen(
        ["start", "", "C:\\Users\\theomartins-ieg\\OneDrive - Instituto Germinare\\MongoShell_Arquivos\\bin\\mongosh.exe"],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def import_file():
    def select_file():
        # Abre a janela de seleção de arquivo de forma modal
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo",
            filetypes=[("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("TSV Files", "*.tsv")],
            parent=janela_importar  # Define a janela de importação como pai
        )
        if arquivo:
            file_path.set(arquivo)
        validate_values()  # Verifica os campos após selecionar o arquivo

    def execute_importation(db, collection, type, file):
        # Definindo o caminho onde o command deve ser executado
        execution_path = r"C:\Users\theomartins-ieg\OneDrive - Instituto Germinare\MongoShell_Arquivos\bin"

        if type == "CSV":
            command = rf'.\mongoimport.exe --db={db} --collection={collection} --type=csv --headerline --file="{file}"'
        elif type == "JSON":
            command = rf'.\mongoimport.exe --db={db} --collection={collection} --file="{file}" --jsonArray'
        elif type == "TSV":
            command = rf'.\mongoimport.exe --db={db} --collection={collection} --type=tsv --headerline --file="{file}"'

        # Inicializa o processo usando Popen
        process = subprocess.Popen(
            command,
            cwd=execution_path,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,  # Captura a saída padrão
            stderr=subprocess.PIPE   # Captura erros
        )
        
        # Lê e imprime a saída em tempo real no console
        stdout, stderr = "", ""
        for line in iter(process.stdout.readline, ""):
            print(line, end="")  # Mostra a saída no console
            stdout += line       # Armazena a saída na variável
        
        # Aguarda o término do processo
        process.stdout.close()
        process.wait()

        # Verifica se houve erro (returncode != 0)
        if process.returncode != 0:
            stderr = process.stderr.read()
            process.stderr.close()
            return stderr  # Retorna apenas o stderr em caso de erro
        else:
            return stdout  # Retorna stdout se não houver erro

    def validate_values():
        db = data_base.get()
        coll = collection.get()
        type = file_type.get()
        path = file_path.get()

        # Validação dos campos
        if not db or not coll or not type or not path:
            confirm_button.config(state="disabled")  # Desabilita o botão se algum campo estiver vazio
            return False

        # Validação do tipo de arquivo
        extensao_arquivo = os.path.splitext(path)[1].lower()
        if extensao_arquivo != f".{type.lower()}":
            confirm_button.config(state="disabled")  # Desabilita o botão se o tipo de arquivo não corresponder
            return False 

        confirm_button.config(state="normal")  # Habilita o botão se tudo estiver correto
        return True 

    def confirm_import():
        if not validate_values():
            return  # Interrompe a função se a validação falhar

        db = data_base.get()
        coll = collection.get()
        type = file_type.get()
        path = file_path.get()

        # Executa a importação
        answer = execute_importation(db, coll, type, path)
        if answer:
            if "error" in answer.lower():  # Verifica se há uma mensagem de erro na saída
                messagebox.showerror("Erro na Importação", answer)
            else:
                messagebox.showinfo("Sucesso", f"Arquivo importado com sucesso!\n\n{answer}")
                option = messagebox.askyesno("Abrir MongoDB", "Deseja abrir o MongoDB?")
                if option:
                    open_mongo()
                else:
                    janela_importar.destroy()  # Fecha a janela de importação
                    janela.destroy()  # Fecha a janela principal
        else:
            messagebox.showinfo("Sucesso", "Arquivo importado com sucesso!")
            option = messagebox.askyesno("Abrir MongoDB", "Deseja abrir o MongoDB?")
            if option:
                open_mongo()
            else:
                janela_importar.destroy()  # Fecha a janela de importação
                janela.destroy()  # Fecha a janela principal

    janela_importar = tk.Toplevel()
    janela_importar.title("Importar Arquivo")
    centralizar_janela(janela_importar, 400, 300)  # Define o tamanho e centraliza a janela

    tk.Label(janela_importar, text="Data base:").grid(row=0, column=0, padx=10, pady=10)
    data_base = tk.Entry(janela_importar)
    data_base.grid(row=0, column=1, padx=10, pady=10)
    data_base.bind("<KeyRelease>", lambda event: validate_values())  # Valida os campos ao digitar

    tk.Label(janela_importar, text="Collection:").grid(row=1, column=0, padx=10, pady=10)
    collection = tk.Entry(janela_importar)
    collection.grid(row=1, column=1, padx=10, pady=10)
    collection.bind("<KeyRelease>", lambda event: validate_values())  # Valida os campos ao digitar

    tk.Label(janela_importar, text="File type:").grid(row=2, column=0, padx=10, pady=10)
    file_type = ttk.Combobox(janela_importar, values=["CSV", "JSON", "TSV"])
    file_type.grid(row=2, column=1, padx=10, pady=10)
    file_type.current(0)  # Define o valor padrão como "CSV"
    file_type.bind("<<ComboboxSelected>>", lambda event: validate_values())  # Valida os campos ao selecionar

    tk.Label(janela_importar, text="File:").grid(row=3, column=0, padx=10, pady=10)
    file_path = tk.StringVar()
    tk.Entry(janela_importar, textvariable=file_path, state="readonly", width=30).grid(row=3, column=1, padx=10, pady=10)
    tk.Button(janela_importar, text="Selecionar Arquivo", command=select_file).grid(row=3, column=2, padx=10, pady=10)

    # Botão Confirmar (inicialmente desabilitado)
    confirm_button = tk.Button(janela_importar, text="Confirmar", command=confirm_import, state="disabled")
    confirm_button.grid(row=4, column=1, pady=20)

def centralizar_janela(janela, largura, altura):
    # Obtém as dimensões da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcula a posição x e y para centralizar a janela
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)

    # Define a geometria da janela
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def main():
    global janela  # Torna a janela principal global para ser acessível em outras funções
    janela = tk.Tk()
    janela.title("Automatização MongoDB")
    centralizar_janela(janela, 400, 200)  # Define o tamanho e centraliza a janela principal

    tk.Label(janela, text="O que você deseja fazer?", font=("Arial", 12)).pack(pady=20)

    # Botões para abrir o MongoDB ou importar arquivo
    tk.Button(janela, text="Abrir Mongo", command=open_mongo, width=20).pack(pady=10)
    tk.Button(janela, text="Importar Arquivo", command=import_file, width=20).pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()