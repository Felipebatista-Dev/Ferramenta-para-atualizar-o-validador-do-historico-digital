#não esta funcionado!!!
import customtkinter as ctk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

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
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if caminho_arquivo:
        try:
            dados = extrair_dados_do_xml(caminho_arquivo)
            dados_formatados = "\n".join([str(dado) for dado in dados])
            messagebox.showinfo("Dados do Aluno", dados_formatados)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# Interface gráfica
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def abrir_interface_principal():
    root.destroy()

    main_window = ctk.CTk()
    main_window.title("Extrator de Dados XML")
    main_window.geometry("400x300")

    btn_selecionar = ctk.CTkButton(main_window, text="Selecionar Arquivo XML", command=escolher_arquivo)
    btn_selecionar.pack(pady=10)

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
