#esse script funciona e possui botao atualizar
import customtkinter as ctk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

# Variável global para armazenar o caminho do arquivo XML selecionado
caminho_arquivo_selecionado = None

# Função para listar as tags e lidar com namespaces
def listar_tags(root):
    tags = set()
    for elem in root.iter():
        tags.add(elem.tag)
    print(f"Tags encontradas no XML: {tags}")
    return tags

def extrair_dados_do_xml(caminho_arquivo):
    def obter_dado(aluno, tag, mensagem_erro):
        elemento = aluno.find(tag, namespaces)
        return elemento.text if elemento is not None else mensagem_erro

    try:
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()

        # Definir o namespace do XML
        namespaces = {'ns': 'http://portal.mec.gov.br/diplomadigital/arquivos-em-xsd'}

        # Listar tags para fins de depuração
        listar_tags(root)

        dados_extraidos = []

        # Buscar a tag Aluno com o namespace
        for aluno in root.findall('.//ns:Aluno', namespaces):
            print(f"Aluno encontrado: {ET.tostring(aluno, encoding='unicode')}")
            dados_extraidos.append({
                "Nome": obter_dado(aluno, 'ns:Nome', 'Nome não encontrado'),
                "Nacionalidade": obter_dado(aluno, 'ns:Nacionalidade', 'Nacionalidade não encontrada'),
                "Naturalidade": obter_dado(aluno, 'ns:Naturalidade/ns:NomeMunicipio', 'Naturalidade não encontrada'),
                "Data de Nascimento": obter_dado(aluno, 'ns:DataNascimento', 'Data de nascimento não encontrada'),
                "Curso": obter_dado(aluno, 'ns:Curso', 'Curso não encontrado')
            })

        if not dados_extraidos:
            raise Exception("Nenhum dado encontrado no arquivo XML.")

        return dados_extraidos

    except ET.ParseError as e:
        raise Exception(f"Erro ao analisar o XML: {e}")
    except FileNotFoundError:
        raise Exception(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
    except Exception as e:
        raise Exception(f"Ocorreu um erro: {e}")

def escolher_arquivo():
    global caminho_arquivo_selecionado
    caminho_arquivo_selecionado = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if caminho_arquivo_selecionado:
        messagebox.showinfo("Arquivo Selecionado", f"Arquivo XML selecionado: {caminho_arquivo_selecionado}")
    else:
        messagebox.showwarning("Nenhum arquivo", "Nenhum arquivo XML foi selecionado.")

# Função para extrair dados do arquivo XML selecionado
def extrair():
    global caminho_arquivo_selecionado
    if caminho_arquivo_selecionado:
        try:
            dados = extrair_dados_do_xml(caminho_arquivo_selecionado)
            dados_formatados = "\n".join([str(dado) for dado in dados])
            messagebox.showinfo("Dados do Aluno", dados_formatados)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Nenhum Arquivo", "Por favor, selecione um arquivo XML primeiro.")

# Interface gráfica
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def abrir_interface_principal():
    root.destroy()

    main_window = ctk.CTk()
    main_window.title("Extrator de Dados XML")
    main_window.geometry("400x300")

    # Botão para selecionar o arquivo XML
    btn_selecionar = ctk.CTkButton(main_window, text="Selecionar Arquivo XML", command=escolher_arquivo)
    btn_selecionar.pack(pady=10)

    # Botão para atualizar (selecionar outro XML)
    btn_atualizar = ctk.CTkButton(main_window, text="Atualizar", command=escolher_arquivo)
    btn_atualizar.pack(pady=10)

    # Botão para extrair os dados do XML
    btn_extrair = ctk.CTkButton(main_window, text="Extrair", command=extrair)
    btn_extrair.pack(pady=10)

    main_window.mainloop()

def login():
    if entry_usuario.get() and entry_senha.get():
        abrir_interface_principal()
    else:
        messagebox.showwarning("Erro", "Por favor, preencha usuário e senha.")

root = ctk.CTk()
root.title("Login")
root.geometry("400x200")

ctk.CTkLabel(root, text="Usuário").pack(pady=5)
entry_usuario = ctk.CTkEntry(root)
entry_usuario.pack(pady=5)

ctk.CTkLabel(root, text="Senha").pack(pady=5)
entry_senha = ctk.CTkEntry(root, show='*')
entry_senha.pack(padx=10, pady=5)

btn_login = ctk.CTkButton(root, text="Login", command=login)
btn_login.pack(padx=10, pady=10)

root.mainloop()

