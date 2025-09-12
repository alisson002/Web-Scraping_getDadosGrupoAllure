import os
import glob
import gspread
from google.oauth2.service_account import Credentials
import time
import pyautogui
import win32com.client
import threading
import json
import win32gui
import win32con
import re

def setup_google_credentials(credentials_file_path):
    """
    Configura as credenciais para acessar Google Sheets - VERSÃO CORRIGIDA
    """
    try:
        # Define os escopos corretos para Google Sheets API
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Carrega as credenciais do arquivo JSON
        credentials = Credentials.from_service_account_file(
            credentials_file_path, 
            scopes=scopes
        )
        
        # Autoriza o cliente gspread
        client = gspread.authorize(credentials)
        
        print("Credenciais do Google configuradas com sucesso")
        return client
        
    except FileNotFoundError:
        print(f"Arquivo de credenciais não encontrado: {credentials_file_path}")
        raise
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo de credenciais JSON. Verifique se o arquivo está correto.")
        raise
    except Exception as e:
        print(f"Erro ao configurar credenciais do Google: {e}")
        raise

def encontra_arquivoReport_maisRecente():
    """
    1. Acesse a pasta de downloads do meu computador;
    2. Procure o arquivo mais recente que contenha "Report" no nome e seja do tipo .xlsx;
    """
    # Obtém o caminho da pasta Downloads do usuário atual
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Cria o padrão de busca para arquivos que contenham "Report" e sejam .xlsx
    padrao_busca = os.path.join(downloads_path, '*Report*.xlsx')
    
    # Encontra todos os arquivos que correspondem ao padrão
    arquivos_correspondentes = glob.glob(padrao_busca)
    
    print("🔍 Procurando o arquivo 'Report.xlsx' mais recente...")
    # Verifica se encontrou algum arquivo
    if not arquivos_correspondentes:
        raise FileNotFoundError("❌ Nenhum arquivo com 'Report' no nome e extensão .xlsx foi encontrado na pasta Downloads")
    
    # Encontra o arquivo mais recente baseado na data de modificação
    arquivo_maisRecente = max(arquivos_correspondentes, key=os.path.getmtime)
    
    print(f"✅ Arquivo mais recente encontrado: {arquivo_maisRecente}")
    return arquivo_maisRecente

def indice_para_coluna_letra_old(indice):
    """Converte índice para letra da coluna (0=A, 1=B, 2=C, etc.)"""
    if indice < 26:
        return chr(ord('A') + indice)
    else:
        return chr(ord('A') + (indice // 26) - 1) + chr(ord('A') + (indice % 26))

def limpar_dados_completo_brasileiro_old(data):
    """
    Função melhorada que limpa dados mantendo formato brasileiro:
    - Remove 'edit' de todas as colunas
    - Remove "'R$" das colunas de moeda (C, D, G, L, M, P, S, V, Y, AQ, AT)
    - MANTÉM formato brasileiro (vírgula como separador decimal)
    - Prepara dados para formatação de moeda no Google Sheets
    """
    try:
        # Define as colunas que contêm valores monetários (convertendo letras para índices)
        def coluna_letra_para_indice(letra):
            """Converte letra da coluna para índice (A=0, B=1, C=2, etc.)"""
            if len(letra) == 1:
                return ord(letra.upper()) - ord('A')
            elif len(letra) == 2:
                return (ord(letra[0].upper()) - ord('A') + 1) * 26 + (ord(letra[1].upper()) - ord('A'))
            else:  # Para colunas como AAA, etc.
                result = 0
                for i, char in enumerate(reversed(letra.upper())):
                    result += (ord(char) - ord('A') + 1) * (26 ** i)
                return result - 1
        
        # Colunas de moeda: C, D, G, L, M, P, S, V, Y, AQ, AT
        colunas_moeda = ['C', 'D', 'G', 'L', 'M', 'P', 'S', 'V', 'Y', 'AQ', 'AT']
        indices_moeda = [coluna_letra_para_indice(col) for col in colunas_moeda]
        
        print(f"🔍 Colunas de moeda identificadas: {colunas_moeda}")
        print(f"📊 Índices correspondentes: {indices_moeda}")
        
        linhas_alteradas = 0
        
        for i, row in enumerate(data):
            linha_alterada = False
            
            # Percorre todas as colunas da linha
            for j, cell_value in enumerate(row):
                if cell_value is not None:
                    valor_original = str(cell_value)
                    valor_processado = valor_original
                    
                    # ETAPA 1: Remove 'edit' de qualquer coluna
                    if 'edit' in valor_processado.lower():
                        valor_processado = valor_processado.replace('edit', '').replace('Edit', '').replace('EDIT', '')
                        linha_alterada = True
                    
                    # ETAPA 2: Tratamento especial para colunas de moeda
                    if j in indices_moeda:
                        # Remove "'R$" do início (os 3 primeiros caracteres)
                        if valor_processado.startswith("'R$"):
                            valor_processado = valor_processado[3:]  # Remove os 3 primeiros caracteres
                            linha_alterada = True
                        
                        # Também remove apenas "'" do início, caso apareça sozinho
                        elif valor_processado.startswith("'"):
                            valor_processado = valor_processado[1:]
                            linha_alterada = True
                        
                        # Remove "R$" que possa ter sobrado
                        if valor_processado.startswith("R$"):
                            valor_processado = valor_processado[2:]
                            linha_alterada = True
                        
                        # IMPORTANTE: MANTÉM formato brasileiro (vírgula decimal)
                        # Só limpa espaços, não altera separadores decimais
                        valor_processado = valor_processado.strip()
                        
                        # Converte para número mantendo formato brasileiro para Google Sheets
                        if valor_processado and not valor_processado.isalpha():
                            try:
                                # Remove separadores de milhares (pontos) mas MANTÉM vírgula decimal
                                # Exemplo: "480.040,00" -> "480040,00"
                                partes = valor_processado.split(',')
                                if len(partes) == 2:
                                    parte_inteira = partes[0].replace('.', '')  # Remove pontos dos milhares
                                    parte_decimal = partes[1]
                                    valor_processado = f"{parte_inteira},{parte_decimal}"
                                else:
                                    # Se não tem vírgula, só remove os pontos dos milhares
                                    valor_processado = valor_processado.replace('.', '')
                                
                                # Converte para float para Google Sheets (mas usando vírgula)
                                valor_para_sheets = valor_processado.replace(',', '.')
                                float(valor_para_sheets)  # Testa se é válido
                                
                                # Retorna valor numérico (float) para Google Sheets aplicar formatação correta
                                valor_processado = float(valor_para_sheets)
                                
                            except ValueError:
                                # Se não conseguir converter, mantém como string limpa
                                valor_processado = valor_processado.strip()
                    
                    else:
                        # Para colunas não-monetárias, só remove espaços
                        valor_processado = valor_processado.strip()
                    
                    # Atualiza o valor se houve mudança
                    if str(valor_original) != str(valor_processado):
                        data[i][j] = valor_processado
                        linha_alterada = True
                        
                        # Log detalhado das mudanças
                        coluna_letra = indice_para_coluna_letra(j)
                        print(f"Linha {i+3}, Coluna {coluna_letra}: '{valor_original}' -> '{valor_processado}'")
            
            if linha_alterada:
                linhas_alteradas += 1
        
        print(f"✅ Limpeza concluída. {linhas_alteradas} linhas foram alteradas.")
        
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")
    
    return data

def encontrar_popup_transferencia1():
    """
    Encontra especificamente a janela do popup da área de transferência
    """
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            
            # Procura por janelas que podem ser o popup do Excel
            # O popup geralmente tem título relacionado ao Excel ou área de transferência
            if any(keyword in window_text.lower() for keyword in ['excel', 'microsoft', 'transferência', 'clipboard']):
                if any(keyword in class_name.lower() for keyword in ['dialog', 'popup', '#32770']):
                    windows.append((hwnd, window_text, class_name))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def tratar_popup_transferencia2():
    """
    Versão melhorada que procura especificamente pelo popup
    """
    try:
        print("🫸 Aguardando popup da área de transferência...")
        time.sleep(3)
        
        # Procura pelo popup específico
        popup_windows = encontrar_popup_transferencia1()
        
        if popup_windows:
            for hwnd, title, class_name in popup_windows:
                print(f"Popup encontrado: {title} ({class_name})")
                
                # Traz a janela para frente e foca nela
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.5)
                
                # Pressiona Tab para navegar até "Não" e Enter para confirmar
                pyautogui.press('tab')
                time.sleep(0.3)
                pyautogui.press('enter')
                time.sleep(0.5)
                
                print("Popup tratado via detecção de janela específica")
                return True
        
        # Se não encontrou popup específico, usa método alternativo
        print("Popup não encontrado, usando método alternativo...")
        return False
        
    except Exception as e:
        print(f"Erro ao detectar popup específico: {e}")
        return False

def tratar_popup_transferencia3():
    """
    Método alternativo usando apenas teclado
    Mais seguro que clicar no centro da tela
    """
    try:
        print("🫸 Tratando popup via teclado...")
        time.sleep(2)
        
        # Método 1: Alt+Tab para garantir que estamos na janela correta
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        
        # Método 2: Pressiona Escape para tentar fechar
        pyautogui.press('escape')
        time.sleep(0.3)
        
        # Método 3: Se ainda há popup, navega com Tab e confirma com Enter
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.press('tab')  # Pode precisar de mais tabs
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("Popup tratado via navegação por teclado")
        
    except Exception as e:
        print(f"Erro no tratamento via teclado: {e}")

def tratar_popup_transferencia4():
    """
    Método mais seguro que não clica em lugar nenhum
    """
    try:
        print("🫸 Aguardando popup da área de transferência...")
        time.sleep(3)
        
        # Primeira tentativa: detecção específica de janela
        if tratar_popup_transferencia2():
            return
        
        # Segunda tentativa: método de teclado
        print("Tentando método de teclado...")
        tratar_popup_transferencia3()
        
        # Terceira tentativa: método mais direto
        print("Método final: pressiona teclas específicas...")
        time.sleep(1)
        
        # Sequência específica para o popup do Excel
        pyautogui.press('n')  # Tecla 'N' para "Não"
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("Popup tratado com método seguro")
        
    except Exception as e:
        print(f"Erro no tratamento seguro do popup: {e}")

def tratar_popup_transferencia_seguro():
    """
    Método mais seguro que não clica em lugar nenhum
    """
    try:
        print("🫸 Aguardando popup da área de transferência...")
        time.sleep(3)
        
        # Primeira tentativa: detecção específica de janela
        if tratar_popup_transferencia2():
            return
        
        # Segunda tentativa: método de teclado
        print("Tentando método de teclado...")
        tratar_popup_transferencia3()
        
        # Terceira tentativa: método mais direto
        print("Método final: pressiona teclas específicas...")
        time.sleep(1)
        
        # Sequência específica para o popup do Excel
        pyautogui.press('n')  # Tecla 'N' para "Não"
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("Popup tratado com método seguro")
        
    except Exception as e:
        print(f"Erro no tratamento seguro do popup: {e}")

def abreExcel_copiaDados_formato_brasileiro_old(file_path):
    """
    Função integrada que mantém formato brasileiro e prepara para Google Sheets
    """
    try:
        import win32com.client
        
        excel_app = win32com.client.Dispatch("Excel.Application")
        excel_app.Visible = True
        excel_app.DisplayAlerts = False
        
        abreExcel = excel_app.Workbooks.Open(file_path)
        seleciona_primeiraPlanilha = abreExcel.ActiveSheet
        
        ultimaColuna = seleciona_primeiraPlanilha.UsedRange.Columns.Count
        ultimaLinha = seleciona_primeiraPlanilha.UsedRange.Rows.Count
        
        def column_number_to_letter(n):
            result = ""
            while n > 0:
                n -= 1
                result = chr(n % 26 + ord('A')) + result
                n //= 26
            return result
        
        ultimaColuna_letter = column_number_to_letter(ultimaColuna)
        endereco_linhasExcel = f"A3:{ultimaColuna_letter}{ultimaLinha}"
        
        print(f"Range selecionado: {endereco_linhasExcel}")
        
        # Extrai os dados primeiro
        endereco_linhasExcel_selecionado = seleciona_primeiraPlanilha.Range(endereco_linhasExcel)
        
        data = []
        for row in endereco_linhasExcel_selecionado.Rows:
            row_data = []
            for cell in row.Cells:
                row_data.append(cell.Value)
            data.append(row_data)
        
        # Aplicação da limpeza mantendo formato brasileiro
        print("🧹 Iniciando limpeza dos dados...")
        data = limpar_dados_completo_brasileiro_expandido(data)
        
        # Copia os dados (opcional, já que vamos usar os dados extraídos)
        endereco_linhasExcel_selecionado.Copy()
        print(f"📋 Processo de extração concluído: {endereco_linhasExcel}")
        
        excel_app.DisplayAlerts = True
        abreExcel.Close(SaveChanges=False)
        
        return data, excel_app
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        try:
            excel_app.DisplayAlerts = True
        except:
            pass
        raise

def aplicar_formatacao_moeda_google_sheets_old(worksheet, data, linha_inicio=1):
    """
    Aplica formatação de moeda brasileira às colunas específicas no Google Sheets
    """
    try:
        print("💰 Aplicando formatação de moeda no Google Sheets...")
        
        # Colunas de moeda: C, D, G, L, M, P, S, V, Y, AQ, AT
        colunas_moeda = ['C', 'D', 'G', 'L', 'M', 'P', 'S', 'V', 'Y', 'AQ', 'AT']
        
        num_linhas = len(data)
        linha_fim = linha_inicio + num_linhas - 1
        
        # Formato de moeda brasileira
        formato_moeda_br = {
            "numberFormat": {
                "type": "CURRENCY",
                "pattern": "\"R$\"#,##0.00"
            }
        }
        
        # Aplica formatação para cada coluna de moeda
        for coluna in colunas_moeda:
            try:
                range_formatacao = f"{coluna}{linha_inicio}:{coluna}{linha_fim}"
                
                # Aplica formatação usando a API do Google Sheets
                worksheet.format(range_formatacao, formato_moeda_br)
                print(f"💱 Formatação aplicada na coluna {coluna} (range: {range_formatacao})")
                
            except Exception as e:
                print(f"⚠️ Erro ao formatar coluna {coluna}: {e}")
        
        print("✅ Formatação de moeda concluída.")
        
    except Exception as e:
        print(f"❌ Erro na formatação de moeda: {e}")

def aplicar_formatacao_completa_google_sheets(worksheet, data, linha_inicio=1):
    """
    Aplica formatação completa (moeda, porcentagem, número) às colunas específicas no Google Sheets
    """
    try:
        print("🎨 Aplicando formatação completa no Google Sheets...")
        
        # Definir todas as colunas por tipo
        colunas_moeda = ['C', 'D', 'F', 'G', 'L', 'M', 'O', 'P', 'R', 'S', 'U', 'V', 'X', 'Y', 'AP', 'AQ', 'AS', 'AT']
        colunas_porcentagem = ['E', 'H', 'I', 'J', 'K', 'N', 'Q', 'T', 'W', 'Z', 'AC', 'AF', 'AI', 'AL', 'AO', 'AR', 'AU']
        colunas_numero = ['AA', 'AB', 'AD', 'AE', 'AG', 'AH', 'AJ', 'AK', 'AM', 'AN']
        
        num_linhas = len(data)
        linha_fim = linha_inicio + num_linhas - 1
        
        # Formatos
        formato_moeda_br = {
            "numberFormat": {
                "type": "CURRENCY",
                "pattern": "\"R$\"#,##0.00"
            }
        }
        
        formato_porcentagem = {
            "numberFormat": {
                "type": "PERCENT",
                "pattern": "0.00%"
            }
        }
        
        formato_numero = {
            "numberFormat": {
                "type": "NUMBER",
                "pattern": "#,##0.00"
            }
        }
        
        # Aplica formatação de moeda
        print("💰 Aplicando formatação de moeda...")
        for coluna in colunas_moeda:
            try:
                range_formatacao = f"{coluna}{linha_inicio}:{coluna}{linha_fim}"
                worksheet.format(range_formatacao, formato_moeda_br)
                print(f"💱 Formatação de moeda aplicada na coluna {coluna}")
            except Exception as e:
                print(f"⚠️ Erro ao formatar moeda na coluna {coluna}: {e}")
        
        # Aplica formatação de porcentagem
        print("📊 Aplicando formatação de porcentagem...")
        for coluna in colunas_porcentagem:
            try:
                range_formatacao = f"{coluna}{linha_inicio}:{coluna}{linha_fim}"
                worksheet.format(range_formatacao, formato_porcentagem)
                print(f"📈 Formatação de porcentagem aplicada na coluna {coluna}")
            except Exception as e:
                print(f"⚠️ Erro ao formatar porcentagem na coluna {coluna}: {e}")
        
        # Aplica formatação de número
        print("🔢 Aplicando formatação de número...")
        for coluna in colunas_numero:
            try:
                range_formatacao = f"{coluna}{linha_inicio}:{coluna}{linha_fim}"
                worksheet.format(range_formatacao, formato_numero)
                print(f"🔢 Formatação de número aplicada na coluna {coluna}")
            except Exception as e:
                print(f"⚠️ Erro ao formatar número na coluna {coluna}: {e}")
        
        print("✅ Formatação completa concluída.")
        
    except Exception as e:
        print(f"❌ Erro na formatação: {e}")

def verificar_configuracao_google(credentials_file, google_sheets_url):
    """
    Função para verificar se a configuração do Google Sheets está correta
    """
    print("=== VERIFICAÇÃO DA CONFIGURAÇÃO DO GOOGLE SHEETS ===")
    
    try:
        # Verifica se o arquivo de credenciais existe
        if not os.path.exists(credentials_file):
            print(f"❌ Arquivo de credenciais não encontrado: {credentials_file}")
            return False
        else:
            print(f"✅ Arquivo de credenciais encontrado: {credentials_file}")
        
        # Verifica se o arquivo é um JSON válido
        with open(credentials_file, 'r') as f:
            creds_data = json.load(f)
            
        # Verifica campos obrigatórios
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        for field in required_fields:
            if field not in creds_data:
                print(f"❌ Campo obrigatório ausente no JSON: {field}")
                return False
        
        print("✅ Arquivo de credenciais JSON válido")
        print(f"📧 Email da conta de serviço: {creds_data.get('client_email')}")
        
        # Verifica URL
        if '/d/' not in google_sheets_url:
            print("❌ URL do Google Sheets inválida")
            return False
        else:
            spreadsheet_id = google_sheets_url.split('/d/')[1].split('/')[0]
            print(f"✅ URL válida - ID da planilha: {spreadsheet_id}")
        
        # Testa conexão
        print("🔄 Testando conexão com Google Sheets...")
        client = setup_google_credentials(credentials_file)
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet(0)
        
        print(f"✅ Conexão bem-sucedida!")
        print(f"📊 Planilha: {spreadsheet.title}")
        print(f"📄 Aba: {worksheet.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação: {str(e)}")
        return False




def indice_para_coluna_letra(indice):
    """Converte índice para letra da coluna (0=A, 1=B, 2=C, etc.)"""
    result = ""
    while indice >= 0:
        result = chr(indice % 26 + ord('A')) + result
        indice = indice // 26 - 1
    return result

def limpar_dados_completo_brasileiro_expandido(data):
    """
    Função expandida que limpa dados mantendo formato brasileiro:
    - Remove 'edit' e 'add' de todas as colunas
    - Remove "'R$" das colunas de moeda
    - MANTÉM formato brasileiro (vírgula como separador decimal)
    - Substitui códigos de unidades por nomes das cidades na coluna A
    - Prepara dados para formatação no Google Sheets
    """
    try:
        # Define as colunas que contêm valores monetários
        def coluna_letra_para_indice(letra):
            """Converte letra da coluna para índice (A=0, B=1, C=2, etc.)"""
            if len(letra) == 1:
                return ord(letra.upper()) - ord('A')
            elif len(letra) == 2:
                return (ord(letra[0].upper()) - ord('A') + 1) * 26 + (ord(letra[1].upper()) - ord('A'))
            else:  # Para colunas como AAA, etc.
                result = 0
                for i, char in enumerate(reversed(letra.upper())):
                    result += (ord(char) - ord('A') + 1) * (26 ** i)
                return result - 1
        
        # Mapeamento de códigos para cidades
        mapeamento_unidades = {
            '1odontologiasa': 'Santo Antônio',
            '2odontologiana': 'Natal (odonto)',
            '3odontologiasjm': 'São José do Mipibu',
            '4odontologiacg': 'Canguaretama',
            '5odontologiagoi': 'Goianinha',
            '6mbestetica': 'Natal (MBEstética)',
            '7odontoma': 'Monte Alegre',
            '8odontologiabj': 'Brejinho',
            '9odontorecife': 'Recife'
        }
        
        # Mapeamento de cidades para CEPs
        mapeamento_ceps = {
            'Santo Antônio': '59255-000',
            'Natal (odonto)': '59010-000',
            'São José do Mipibu': '59162-000',
            'Canguaretama': '59190-000',
            'Goianinha': '59173-000',
            'Natal (MBEstética)': '59010-000',
            'Monte Alegre': '59182-000',
            'Brejinho': '59219-000',
            'Recife': '50010-000'
        }
        
        # Colunas de moeda: C, D, F, G, L, M, O, P, R, S, U, V, X, Y, AP, AQ, AS, AT
        colunas_moeda = ['C', 'D', 'F', 'G', 'L', 'M', 'O', 'P', 'R', 'S', 'U', 'V', 'X', 'Y', 'AP', 'AQ', 'AS', 'AT']
        indices_moeda = [coluna_letra_para_indice(col) for col in colunas_moeda]
        
        # Colunas de porcentagem: E, H, I, J, K, N, Q, T, W, Z, AC, AF, AI, AL, AO, AR, AU
        colunas_porcentagem = ['E', 'H', 'I', 'J', 'K', 'N', 'Q', 'T', 'W', 'Z', 'AC', 'AF', 'AI', 'AL', 'AO', 'AR', 'AU']
        indices_porcentagem = [coluna_letra_para_indice(col) for col in colunas_porcentagem]
        
        # Colunas de número: AA, AB, AD, AE, AG, AH, AJ, AK, AM, AN
        colunas_numero = ['AA', 'AB', 'AD', 'AE', 'AG', 'AH', 'AJ', 'AK', 'AM', 'AN']
        indices_numero = [coluna_letra_para_indice(col) for col in colunas_numero]
        
        # Coluna AV (índice para CEP)
        indice_av = coluna_letra_para_indice('AV')
        
        print(f"🔍 Colunas de moeda identificadas: {colunas_moeda}")
        print(f"📊 Colunas de porcentagem identificadas: {colunas_porcentagem}")
        print(f"🔢 Colunas de número identificadas: {colunas_numero}")
        
        linhas_alteradas = 0
        
        for i, row in enumerate(data):
            linha_alterada = False
            cidade_linha = None  # Para armazenar a cidade da linha atual
            
            # Primeiro, verifica se há substituição de unidade na coluna A
            if len(row) > 0 and row[0] is not None:
                valor_coluna_a = str(row[0]).strip()
                if valor_coluna_a in mapeamento_unidades:
                    cidade_linha = mapeamento_unidades[valor_coluna_a]
                    row[0] = cidade_linha
                    linha_alterada = True
                    print(f"Linha {i+3}, Coluna A: '{valor_coluna_a}' -> '{cidade_linha}'")
            
            # Percorre todas as colunas da linha
            for j, cell_value in enumerate(row):
                if cell_value is not None:
                    valor_original = str(cell_value)
                    valor_processado = valor_original
                    
                    # ETAPA 1: Remove 'edit' e 'add' de qualquer coluna
                    if 'edit' in valor_processado.lower():
                        valor_processado = valor_processado.replace('edit', '').replace('Edit', '').replace('EDIT', '')
                        linha_alterada = True
                    
                    if 'add' in valor_processado.lower():
                        valor_processado = valor_processado.replace('add', '').replace('Add', '').replace('ADD', '')
                        linha_alterada = True
                    
                    # ETAPA 2: Tratamento específico por tipo de coluna
                    if j in indices_moeda:
                        # Tratamento para colunas de moeda
                        if valor_processado.startswith("'R$"):
                            valor_processado = valor_processado[3:]
                            linha_alterada = True
                        elif valor_processado.startswith("'"):
                            valor_processado = valor_processado[1:]
                            linha_alterada = True
                        elif valor_processado.startswith("R$"):
                            valor_processado = valor_processado[2:]
                            linha_alterada = True
                        
                        valor_processado = valor_processado.strip()
                        
                        if valor_processado and not valor_processado.isalpha():
                            try:
                                partes = valor_processado.split(',')
                                if len(partes) == 2:
                                    parte_inteira = partes[0].replace('.', '')
                                    parte_decimal = partes[1]
                                    valor_processado = f"{parte_inteira},{parte_decimal}"
                                else:
                                    valor_processado = valor_processado.replace('.', '')
                                
                                valor_para_sheets = valor_processado.replace(',', '.')
                                float(valor_para_sheets)
                                valor_processado = float(valor_para_sheets)
                                
                            except ValueError:
                                valor_processado = valor_processado.strip()
                    
                    elif j in indices_porcentagem:
                        # Tratamento para colunas de porcentagem
                        valor_processado = valor_processado.strip()
                        
                        # Remove % se estiver presente
                        if valor_processado.endswith('%'):
                            valor_processado = valor_processado[:-1].strip()
                            linha_alterada = True
                        
                        if valor_processado and not valor_processado.isalpha():
                            try:
                                # Converte vírgula para ponto para processamento
                                valor_para_sheets = valor_processado.replace(',', '.')
                                valor_numerico = float(valor_para_sheets)
                                
                                # Se o valor é maior que 1, assume que já está em formato percentual (ex: 15 = 15%)
                                # Se o valor é menor que 1, assume que está em decimal (ex: 0.15 = 15%)
                                if valor_numerico > 1:
                                    valor_processado = valor_numerico / 100  # Converte para decimal para Google Sheets
                                else:
                                    valor_processado = valor_numerico
                                
                            except ValueError:
                                valor_processado = valor_processado.strip()
                    
                    elif j in indices_numero:
                        # Tratamento para colunas de número
                        valor_processado = valor_processado.strip()
                        
                        if valor_processado and not valor_processado.isalpha():
                            try:
                                # Remove separadores de milhares e converte vírgula decimal
                                partes = valor_processado.split(',')
                                if len(partes) == 2:
                                    parte_inteira = partes[0].replace('.', '')
                                    parte_decimal = partes[1]
                                    valor_processado = f"{parte_inteira}.{parte_decimal}"
                                else:
                                    valor_processado = valor_processado.replace('.', '')
                                
                                valor_processado = float(valor_processado)
                                
                            except ValueError:
                                valor_processado = valor_processado.strip()
                    
                    else:
                        # Para outras colunas, só remove espaços
                        valor_processado = valor_processado.strip()
                    
                    # Atualiza o valor se houve mudança
                    if str(valor_original) != str(valor_processado):
                        data[i][j] = valor_processado
                        linha_alterada = True
                        
                        coluna_letra = indice_para_coluna_letra(j)
                        print(f"Linha {i+3}, Coluna {coluna_letra}: '{valor_original}' -> '{valor_processado}'")
            
            # Preenche CEP na coluna AV se temos uma cidade identificada
            if cidade_linha and len(row) > indice_av:
                cep = mapeamento_ceps.get(cidade_linha, '')
                if cep:
                    data[i][indice_av] = cep
                    linha_alterada = True
                    print(f"Linha {i+3}, Coluna AV: CEP '{cep}' adicionado para '{cidade_linha}'")
            
            if linha_alterada:
                linhas_alteradas += 1
        
        print(f"✅ Limpeza concluída. {linhas_alteradas} linhas foram alteradas.")
        
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")
    
    return data

def paste_to_google_sheets_com_formatacao_completa(google_sheets_url, data, credentials_file):
    """
    Versão completa que cola dados E aplica todas as formatações
    """
    try:
        from google.oauth2.service_account import Credentials
        
        print("🔧 Configurando acesso ao Google Sheets...")
        
        # Configura as credenciais
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(credentials)
        
        # Extrai o ID da planilha
        if '/d/' in google_sheets_url:
            spreadsheet_id = google_sheets_url.split('/d/')[1].split('/')[0]
            print(f"📋 ID da planilha extraído: {spreadsheet_id}")
        else:
            raise ValueError("URL do Google Sheets inválida")
        
        # Abre a planilha
        print("📂 Abrindo planilha do Google Sheets...")
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet(0)
        
        print(f"📊 Planilha acessada: {spreadsheet.title}")
        print(f"📄 Aba selecionada: {worksheet.title}")
        
        # Encontra a primeira linha vazia
        print("🔍 Procurando primeira linha vazia...")
        all_values = worksheet.get_all_values()
        
        next_row = 1
        if all_values:
            for i, row in enumerate(all_values):
                if not any(cell.strip() for cell in row if cell):
                    next_row = i + 1
                    break
            else:
                next_row = len(all_values) + 1
        
        print(f"📍 Inserindo dados a partir da linha {next_row}")
        
        # Prepara os dados
        if not data or not data[0]:
            raise ValueError("Nenhum dado para inserir")
            
        num_rows = len(data)
        num_cols = len(data[0])
        
        def num_to_col_letters(num):
            letters = ''
            while num:
                mod = (num - 1) % 26
                letters = chr(mod + 65) + letters
                num = (num - 1) // 26
            return letters
        
        start_col = 'A'
        end_col = num_to_col_letters(num_cols)
        end_row = next_row + num_rows - 1
        
        range_name = f'{start_col}{next_row}:{end_col}{end_row}'
        print(f"📐 Range de inserção: {range_name}")
        
        # Limpa dados None
        cleaned_data = []
        for row in data:
            cleaned_row = []
            for cell in row:
                if cell is None:
                    cleaned_row.append('')
                else:
                    cleaned_row.append(cell)
            cleaned_data.append(cleaned_row)
        
        # Insere os dados na planilha
        print("💾 Inserindo dados na planilha...")
        worksheet.update(range_name, cleaned_data, value_input_option='USER_ENTERED')
        
        print("🎨 Aplicando formatações completas...")
        # Aplica todas as formatações após inserir os dados
        aplicar_formatacao_completa_google_sheets(worksheet, cleaned_data, next_row)
        
        print(f"✅ Dados inseridos e formatados com sucesso!")
        print(f"📊 Range utilizado: {range_name}")
        print(f"📝 Número de linhas inseridas: {num_rows}")
        print(f"📋 Número de colunas: {num_cols}")
        print(f"🔗 Planilha acessível em: {google_sheets_url}")
        
    except Exception as e:
        print(f"❌ Erro ao acessar ou modificar a planilha: {str(e)}")
        raise

def paste_to_google_sheets_com_formatacao_old(google_sheets_url, data, credentials_file):
    """
    Versão melhorada que cola dados E aplica formatação de moeda
    """
    try:
        from google.oauth2.service_account import Credentials
        
        print("Configurando acesso ao Google Sheets...")
        
        # Configura as credenciais
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(credentials)
        
        # Extrai o ID da planilha
        if '/d/' in google_sheets_url:
            spreadsheet_id = google_sheets_url.split('/d/')[1].split('/')[0]
            print(f"ID da planilha extraído: {spreadsheet_id}")
        else:
            raise ValueError("URL do Google Sheets inválida")
        
        # Abre a planilha
        print("Abrindo planilha do Google Sheets...")
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet(0)
        
        print(f"Planilha acessada: {spreadsheet.title}")
        print(f"Aba selecionada: {worksheet.title}")
        
        # Encontra a primeira linha vazia
        print("Procurando primeira linha vazia...")
        all_values = worksheet.get_all_values()
        
        next_row = 1
        if all_values:
            for i, row in enumerate(all_values):
                if not any(cell.strip() for cell in row if cell):
                    next_row = i + 1
                    break
            else:
                next_row = len(all_values) + 1
        
        print(f"Inserindo dados a partir da linha {next_row}")
        
        # Prepara os dados
        if not data or not data[0]:
            raise ValueError("Nenhum dado para inserir")
            
        num_rows = len(data)
        num_cols = len(data[0])
        
        def num_to_col_letters(num):
            letters = ''
            while num:
                mod = (num - 1) % 26
                letters = chr(mod + 65) + letters
                num = (num - 1) // 26
            return letters
        
        start_col = 'A'
        end_col = num_to_col_letters(num_cols)
        end_row = next_row + num_rows - 1
        
        range_name = f'{start_col}{next_row}:{end_col}{end_row}'
        print(f"Range de inserção: {range_name}")
        
        # Limpa dados None
        cleaned_data = []
        for row in data:
            cleaned_row = []
            for cell in row:
                if cell is None:
                    cleaned_row.append('')
                else:
                    cleaned_row.append(cell)  # Mantém o tipo original (float para moeda)
            cleaned_data.append(cleaned_row)
        
        # Insere os dados na planilha
        print("Inserindo dados na planilha...")
        worksheet.update(range_name, cleaned_data, value_input_option='USER_ENTERED')
        
        print("💰 Aplicando formatação de moeda...")
        # Aplica formatação de moeda após inserir os dados
        aplicar_formatacao_completa_google_sheets(worksheet, cleaned_data, next_row)
        
        print(f"✅ Dados inseridos e formatados com sucesso!")
        print(f"📊 Range utilizado: {range_name}")
        print(f"📝 Número de linhas inseridas: {num_rows}")
        print(f"📋 Número de colunas: {num_cols}")
        print(f"🔗 Planilha acessível em: {google_sheets_url}")
        
    except Exception as e:
        print(f"❌ Erro ao acessar ou modificar a planilha: {str(e)}")
        raise

def abreExcel_copiaDados_formato_completo(file_path):
    """
    Função integrada que aplica limpeza completa e prepara para Google Sheets
    """
    try:
        import win32com.client
        
        excel_app = win32com.client.Dispatch("Excel.Application")
        excel_app.Visible = True
        excel_app.DisplayAlerts = False
        
        abreExcel = excel_app.Workbooks.Open(file_path)
        seleciona_primeiraPlanilha = abreExcel.ActiveSheet
        
        ultimaColuna = seleciona_primeiraPlanilha.UsedRange.Columns.Count
        ultimaLinha = seleciona_primeiraPlanilha.UsedRange.Rows.Count
        
        def column_number_to_letter(n):
            result = ""
            while n > 0:
                n -= 1
                result = chr(n % 26 + ord('A')) + result
                n //= 26
            return result
        
        ultimaColuna_letter = column_number_to_letter(ultimaColuna)
        endereco_linhasExcel = f"A3:{ultimaColuna_letter}{ultimaLinha}"
        
        print(f"📐 Range selecionado: {endereco_linhasExcel}")
        
        # Extrai os dados primeiro
        endereco_linhasExcel_selecionado = seleciona_primeiraPlanilha.Range(endereco_linhasExcel)
        
        data = []
        for row in endereco_linhasExcel_selecionado.Rows:
            row_data = []
            for cell in row.Cells:
                row_data.append(cell.Value)
            data.append(row_data)
        
        # Aplicação da limpeza completa
        print("🧹 Iniciando limpeza completa dos dados...")
        data = limpar_dados_completo_brasileiro_expandido(data)
        
        # Copia os dados
        endereco_linhasExcel_selecionado.Copy()
        print(f"📋 Processo de extração concluído: {endereco_linhasExcel}")
        
        excel_app.DisplayAlerts = True
        abreExcel.Close(SaveChanges=False)
        
        return data, excel_app
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        try:
            excel_app.DisplayAlerts = True
        except:
            pass
        raise

def copiandoDados_excelToGs(link_gs, path_cred):
    """
    Função principal que executa todo o processo
    """
    # CONFIGURAÇÕES - MODIFIQUE ESTAS VARIÁVEIS CONFORME NECESSÁRIO
    GOOGLE_SHEETS_URL = link_gs
    CREDENTIALS_FILE = path_cred
    
    try:
        print("🚀 Iniciando o processo de transferência de dados...")
        
        # 1 e 2: Encontra o arquivo mais recente com "Report" na pasta Downloads
        latest_file = encontra_arquivoReport_maisRecente()
        
        # 3, 4 e 5: Abre o Excel, seleciona e copia os dados
        copied_data, excel_app = abreExcel_copiaDados_formato_completo(latest_file)
        
        # 6 e 7: Acessa o Google Sheets e cola os dados
        paste_to_google_sheets_com_formatacao_completa(GOOGLE_SHEETS_URL, copied_data, CREDENTIALS_FILE)
        
        # Fecha o Excel após a operação
        excel_app.Quit()
        
        print("Processo concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
        
        # Tenta fechar o Excel em caso de erro
        try:
            excel_app.Quit()
        except:
            pass
