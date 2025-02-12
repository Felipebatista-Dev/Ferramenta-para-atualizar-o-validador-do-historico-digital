import customtkinter as ctk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from datetime import datetime

# Função para buscar e retornar o dado de um elemento XML
def obter_dado(elemento, tag, valor_default):
    # Tenta buscar o valor da tag dentro do elemento
    found_element = elemento.find(tag, namespaces)
    
    if found_element is not None and found_element.text:
        valor = found_element.text.strip()
        try:
            # Tenta o formato de data YYYY-MM-DD
            data_formatada = datetime.strptime(valor, '%Y-%m-%d').strftime('%d/%m/%Y')
            return data_formatada
        except ValueError:
            # Se não for uma data, retorna o valor original
            return valor  
    else:
        return valor_default  # Se não encontrado, retorna o valor padrão

# Função para concatenar duas tags de dados
def obter_dado_concatenado(elemento, tag1, tag2, valor_default):
    elemento1 = elemento.find(tag1, namespaces)
    elemento2 = elemento.find(tag2, namespaces)
    
    if elemento1 is not None and elemento2 is not None:
        return f"{elemento1.text.strip()}/{elemento2.text.strip()}"
    else:
        return valor_default

def extrair_dados_do_xml(caminho_arquivo):
    try:
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()

        # Definindo namespaces utilizados no XML
        global namespaces
        namespaces = {'ns': 'http://portal.mec.gov.br/diplomadigital/arquivos-em-xsd'}

        dados_extraidos = []

        # Buscando as tags principais e extraindo os dados
        aluno = root.find(".//ns:Aluno", namespaces)
        curso = root.find(".//ns:DadosCurso", namespaces)
        historico = root.find(".//ns:HistoricoEscolar", namespaces)
        seguranca = root.find(".//ns:SegurancaHistorico", namespaces)
        situacao_atual = root.find(".//ns:SituacaoAtualDiscente", namespaces)

        # Pegando a carga horária integralizada
        carga_horaria_integralizada = historico.find(".//ns:CargaHorariaCursoIntegralizada/ns:HoraRelogio", namespaces)

        # Situação do histórico como "Válida" ou "Inválida"
        situacao_do_historico = obter_dado(situacao_atual, 'ns:Formado/ns:DataConclusaoCurso', 'Inválida')
        if situacao_do_historico != 'Inválida':
            situacao_do_historico = "Válida"

        if aluno and curso and historico and seguranca and situacao_atual:
            numero_identidade = obter_dado(aluno, 'ns:RG/ns:Numero', 'Identidade não encontrada')
            orgao_emissor = obter_dado(aluno, 'ns:RG/ns:OrgaoExpedidor', 'Órgão expedidor não encontrado')
            uf_identidade = obter_dado(aluno, 'ns:RG/ns:UF', 'UF não encontrada')

            # Remover a UF do começo do número de identidade (ex: "MG17504984" -> "17504984")
            numero_identidade = numero_identidade[2:]  # Remover os 2 primeiros caracteres que são a UF

            dados_extraidos.append({
                "Nome do Aluno": obter_dado(aluno, 'ns:Nome', 'Nome do aluno não encontrado'),
                "Nome do Curso": obter_dado(curso, 'ns:NomeCurso', 'Curso não encontrado'),
                "Carga Horária Integralizada": carga_horaria_integralizada.text if carga_horaria_integralizada is not None else "Carga horária não encontrada",
                "Documento de Identidade": f"{numero_identidade} - {orgao_emissor}/{uf_identidade}",
                "Nacionalidade": obter_dado(aluno, 'ns:Nacionalidade', 'Nacionalidade não encontrada'),
                "Naturalidade": obter_dado_concatenado(aluno, 'ns:Naturalidade/ns:NomeMunicipio', 'ns:Naturalidade/ns:UF', 'Naturalidade não encontrada'),
                "Data de Nascimento": obter_dado(aluno, 'ns:DataNascimento', 'Data de nascimento não encontrada'),
                "Data de Colação de Grau": obter_dado(situacao_atual, 'ns:Formado/ns:DataColacaoGrau', 'Data de colação não encontrada'),
                "Data Expedição do Diploma": obter_dado(situacao_atual, 'ns:Formado/ns:DataExpedicaoDiploma', 'Data de expedição do diploma não encontrada'),
                "Data da Emissão do Histórico": obter_dado(historico, 'ns:DataEmissaoHistorico', 'Data da emissão não encontrada'),
                "Hora da Emissão do Histórico": obter_dado(historico, 'ns:HoraEmissaoHistorico', 'Hora da emissão não encontrada'),
                "Situação do Histórico": situacao_do_historico,
                "Código de Validação": obter_dado(seguranca, 'ns:CodigoValidacao', 'Código de validação não encontrado')
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
        global arquivo_selecionado
        arquivo_selecionado = caminho_arquivo
        btn_extrair.configure(state=ctk.NORMAL)  # Habilita o botão de extração
        messagebox.showinfo("Arquivo Selecionado", f"Arquivo selecionado: {arquivo_selecionado}")

def extrair_dados():
    try:
        dados = extrair_dados_do_xml(arquivo_selecionado)
        mostrar_dados(dados)
        messagebox.showinfo("Sucesso", "Dados extraídos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def mostrar_dados(dados):
    dados_formatados = "\n\n".join(
        ["\n".join([f"{key}: {value}" for key, value in item.items()]) for item in dados]
    )
    messagebox.showinfo("Dados do Aluno", dados_formatados)

# Criar a interface gráfica
ctk.set_appearance_mode("dark")  # Configurando o modo para "dark"
ctk.set_default_color_theme("blue")  # Ou qualquer tema que preferir

# Janela de Login
def abrir_interface_principal():
    root.destroy()  # Fecha a janela de login

    main_window = ctk.CTk()
    main_window.title("Extrator de Dados XML")
    main_window.geometry("400x300")  # Definindo as proporções conforme o primeiro código

    btn_selecionar = ctk.CTkButton(main_window, text="Selecionar Arquivo XML", command=escolher_arquivo, fg_color="white")
    btn_selecionar.pack(pady=10)

    # Botão de Atualizar
    btn_atualizar = ctk.CTkButton(main_window, text="Atualizar", command=lambda: messagebox.showinfo("Atualizar", "Atualizado!"))
    btn_atualizar.pack(pady=10)

    # Botão de Extrair Dados
    global btn_extrair
    btn_extrair = ctk.CTkButton(main_window, text="Extrair Dados", command=extrair_dados, state=ctk.DISABLED)
    btn_extrair.pack(pady=10)

    # Variável global para armazenar o caminho do arquivo selecionado
    global arquivo_selecionado
    arquivo_selecionado = ""

    main_window.mainloop()

# Função de login
def login():
    if entry_usuario.get() and entry_senha.get():
        abrir_interface_principal()
    else:
        messagebox.showwarning("Erro", "Por favor, preencha usuário e senha.")

# Criar a janela de login
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