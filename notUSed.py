# import os
# import glob
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime
# import subprocess
# import sys
# import time
# import pyautogui
# import win32com.client
# import threading
# from PIL import ImageGrab
# import cv2
# import numpy as np
# import json

# def tratar_popup_transferencia_simples():
#     """
#     Função simples para tratar o popup da área de transferência
#     SEM usar thread separada para evitar erros de COM
#     """
#     try:
#         print("Aguardando popup da área de transferência...")
#         time.sleep(2)  # Aguarda o popup aparecer
        
#         # Obtém o tamanho da tela
#         screen_width, screen_height = pyautogui.size()
#         center_x = screen_width // 2
#         center_y = screen_height // 2
        
#         # Clica no centro da tela (onde deve estar o popup)
#         pyautogui.click(center_x, center_y)
#         time.sleep(0.5)
        
#         # Pressiona seta para a direita uma vez (para selecionar "Não")
#         pyautogui.press('right')
#         time.sleep(0.3)
        
#         # Pressiona Enter para confirmar
#         pyautogui.press('enter')
#         time.sleep(0.5)
        
#         print("Popup tratado: clique no centro -> seta direita -> Enter")
        
#     except Exception as e:
#         print(f"Erro ao tratar popup: {e}")

# def abreExcel_copiaDados(file_path):
#     """
#     3. Abra esse arquivo com o Excel;
#     4. Selecione as linhas de 3 a 11 de todas as colunas;
#     5. Copie os dados selecionados (linhas 3 a 11 de todas as colunas);
#     VERSÃO CORRIGIDA - SEM THREAD PARA POPUP
#     """
#     try:
#         # Cria uma instância do Excel através do COM
#         excel_app = win32com.client.Dispatch("Excel.Application")
        
#         # Torna o Excel visível (opcional - pode ser False para execução em background)
#         excel_app.Visible = True
        
#         # Abre o arquivo Excel
#         abreExcel = excel_app.Workbooks.Open(file_path)
        
#         # Seleciona a primeira planilha (seleciona_primeiraAbaPlanilha)
#         seleciona_primeiraPlanilha = abreExcel.ActiveSheet
        
#         # Encontra a última coluna com dados
#         ultimaColuna = seleciona_primeiraPlanilha.UsedRange.Columns.Count
        
#         # Converte o número da coluna para letra (ex: 1 = A, 2 = B, etc.)
#         def column_number_to_letter(n):
#             result = ""
#             while n > 0:
#                 n -= 1
#                 result = chr(n % 26 + ord('A')) + result
#                 n //= 26
#             return result
        
#         ultimaColuna_letter = column_number_to_letter(ultimaColuna)
        
#         # Define o range das linhas 3 a 11 de todas as colunas
#         endereco_linhasExcel = f"A3:{ultimaColuna_letter}11"
        
#         # Seleciona o range especificado
#         endereco_linhasExcel_selecionado = seleciona_primeiraPlanilha.Range(endereco_linhasExcel)
        
#         print(f"Range selecionado: {endereco_linhasExcel}")
        
#         # PRIMEIRO: Limpa a coluna C (remove 'edit') ANTES de copiar
#         print("Limpando dados da coluna C (removendo 'edit')...")
        
#         # Acessa especificamente a coluna C do range (C3:C11)
#         coluna_c_range = seleciona_primeiraPlanilha.Range(f"C3:C11")
        
#         # Percorre cada célula da coluna C e limpa o texto
#         for cell in coluna_c_range:
#             if cell.Value is not None:
#                 valor_original = str(cell.Value)
                
#                 # Remove 'edit' em todas as variações
#                 valor_limpo = valor_original.replace('edit', '').replace('Edit', '').replace('EDIT', '')
#                 valor_limpo = valor_limpo.strip()  # Remove espaços extras
                
#                 # Atualiza a célula se houve mudança
#                 if valor_original != valor_limpo:
#                     cell.Value = valor_limpo
#                     print(f"Célula {cell.Address}: '{valor_original}' -> '{valor_limpo}'")
        
#         print("Limpeza da coluna C concluída.")
        
#         # SEGUNDO: Agora copia os dados já limpos
#         endereco_linhasExcel_selecionado.Copy()
#         print(f"Dados copiados do range: {endereco_linhasExcel}")
        
#         # TERCEIRO: Trata o popup da área de transferência (SEM THREAD)
#         tratar_popup_transferencia_simples()
        
#         # QUARTO: Extrai os dados para retornar (já limpos)
#         data = []
#         for row in endereco_linhasExcel_selecionado.Rows:
#             row_data = []
#             for cell in row.Cells:
#                 row_data.append(cell.Value)
#             data.append(row_data)
        
#         # Garante que o Excel permaneça em primeiro plano
#         try:
#             excel_app.WindowState = -4137  # xlMaximized
#             excel_app.Activate()
#         except:
#             pass  # Ignora erro se não conseguir ativar
        
#         # Fecha o arquivo Excel mas mantém o Excel aberto para manter os dados na área de transferência
#         abreExcel.Close(SaveChanges=False)
        
#         return data, excel_app
        
#     except Exception as e:
#         print(f"Erro ao processar o arquivo Excel: {str(e)}")
#         raise

# def abreExcel_copiaDados_sem_popup(file_path):
#     """
#     VERSÃO ALTERNATIVA - Ignora completamente o popup
#     Use esta versão se o popup não estiver atrapalhando o funcionamento
#     """
#     try:
#         # Cria uma instância do Excel através do COM
#         excel_app = win32com.client.Dispatch("Excel.Application")
        
#         # Torna o Excel visível
#         excel_app.Visible = True
        
#         # Desabilita alertas para evitar popups
#         excel_app.DisplayAlerts = False
        
#         # Abre o arquivo Excel
#         abreExcel = excel_app.Workbooks.Open(file_path)
        
#         # Seleciona a primeira planilha
#         seleciona_primeiraPlanilha = abreExcel.ActiveSheet
        
#         # Encontra a última coluna com dados
#         ultimaColuna = seleciona_primeiraPlanilha.UsedRange.Columns.Count
        
#         # Converte o número da coluna para letra
#         def column_number_to_letter(n):
#             result = ""
#             while n > 0:
#                 n -= 1
#                 result = chr(n % 26 + ord('A')) + result
#                 n //= 26
#             return result
        
#         ultimaColuna_letter = column_number_to_letter(ultimaColuna)
        
#         # Define o range das linhas 3 a 11 de todas as colunas
#         endereco_linhasExcel = f"A3:{ultimaColuna_letter}11"
#         endereco_linhasExcel_selecionado = seleciona_primeiraPlanilha.Range(endereco_linhasExcel)
        
#         print(f"Range selecionado: {endereco_linhasExcel}")
        
#         # Limpa a coluna C (remove 'edit') ANTES de copiar
#         print("Limpando dados da coluna C (removendo 'edit')...")
#         coluna_c_range = seleciona_primeiraPlanilha.Range(f"C3:C11")
        
#         for cell in coluna_c_range:
#             if cell.Value is not None:
#                 valor_original = str(cell.Value)
#                 valor_limpo = valor_original.replace('edit', '').replace('Edit', '').replace('EDIT', '')
#                 valor_limpo = valor_limpo.strip()
                
#                 if valor_original != valor_limpo:
#                     cell.Value = valor_limpo
#                     print(f"Célula {cell.Address}: '{valor_original}' -> '{valor_limpo}'")
        
#         print("Limpeza da coluna C concluída.")
        
#         # Copia os dados já limpos
#         endereco_linhasExcel_selecionado.Copy()
#         print(f"Dados copiados do range: {endereco_linhasExcel}")
        
#         # Extrai os dados para retornar
#         data = []
#         for row in endereco_linhasExcel_selecionado.Rows:
#             row_data = []
#             for cell in row.Cells:
#                 row_data.append(cell.Value)
#             data.append(row_data)
        
#         # Reabilita alertas
#         excel_app.DisplayAlerts = True
        
#         # Fecha o arquivo Excel
#         abreExcel.Close(SaveChanges=False)
        
#         print("Processo Excel concluído sem tratar popup (DisplayAlerts desabilitado)")
        
#         return data, excel_app
        
#     except Exception as e:
#         print(f"Erro ao processar o arquivo Excel: {str(e)}")
#         try:
#             excel_app.DisplayAlerts = True
#         except:
#             pass
#         raise

# # Função para usar no código principal
# def processar_arquivo_excel(file_path, tratar_popup=True):
#     """
#     Função wrapper que escolhe a versão adequada
#     """
#     if tratar_popup:
#         return abreExcel_copiaDados(file_path)
#     else:
#         return abreExcel_copiaDados_sem_popup(file_path)

# # Primeira versão da função de setup. Acabou dando problema dps de usar algumas vezes.
# def setup_google_credentials(credentials_file_path):
#     """
#     Configura as credenciais para acessar Google Sheets
#     """
#     # Define os escopos necessários para Google Sheets
#     escopos = ['https://abre_planilhaExcels.google.com/feeds',
#             'https://www.googleapis.com/auth/drive']
    
#     # Carrega as credenciais do arquivo JSON
#     creds = Credentials.from_service_account_file(credentials_file_path, scopes=escopos)
    
#     # Autoriza o cliente gspread
#     client = gspread.authorize(creds)
    
#     return client

# def detectar_e_fechar_popup():
#     """
#     Função que detecta e fecha o popup da área de transferência do Excel
#     Desenvolvida após alguns teste e ser atestado que sempre iria aparecer um popup devido ao volume de dados sendo copiados
#     """
#     try:
#         # Aguarda um momento para o popup aparecer
#         time.sleep(1)
        
#         # Procura pela janela do popup usando pyautogui
#         # Tenta encontrar o botão "Não" na tela
#         try:
#             # Método 1: Procurar pelo texto "Não" na tela
#             nao_button = pyautogui.locateOnScreen('nao_button.png', confidence=0.8)
#             if nao_button:
#                 pyautogui.click(nao_button)
#                 print("Popup detectado e botão 'Não' clicado com sucesso")
#                 return True
#         except:
#             pass
        
#         # Método 2: Usar coordenadas aproximadas (pode precisar ajustar)
#         # Captura screenshot e procura por padrões do popup
#         screenshot = ImageGrab.grab()
#         screenshot_np = np.array(screenshot)
        
#         # Converte para escala de cinza
#         gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        
#         # Procura por botões típicos do Windows (método alternativo)
#         # Se encontrar área suspeita de popup, pressiona Tab + Enter para "Não"
#         try:
#             # Pressiona Alt+Tab para garantir que o popup esteja em foco
#             pyautogui.keyDown('alt')
#             pyautogui.press('tab')
#             pyautogui.keyUp('alt')
#             time.sleep(0.2)
            
#             # Pressiona Tab para navegar até "Não" e Enter para confirmar
#             pyautogui.press('tab')
#             time.sleep(0.1)
#             pyautogui.press('enter')
            
#             print("Tentativa de fechamento do popup via teclado executada")
#             return True
            
#         except Exception as e:
#             print(f"Erro ao tentar fechar popup via teclado: {e}")
            
#     except Exception as e:
#         print(f"Erro na detecção do popup: {e}")
    
#     return False

# # Primeira versão da função de abrir o excel e copiar os dados
# def abreExcel_copiaDados(file_path):
#     """
#     3. Abra esse arquivo com o Excel;
#     4. Selecione as linhas de 3 a 11 de todas as colunas;
#     5. Copie os dados selecionados (linhas 3 a 11 de todas as colunas);
#     """
#     try:
#         # Cria uma instância do Excel através do COM
#         excel_app = win32com.client.Dispatch("Excel.Application")
        
#         # Torna o Excel visível (opcional - pode ser False para execução em background)
#         excel_app.Visible = True
        
#         # Desabilita alertas para evitar popups
#         excel_app.DisplayAlerts = False
        
#         # Abre o arquivo Excel
#         abreExcel = excel_app.Workbooks.Open(file_path)
        
#         # Seleciona a primeira planilha (seleciona_primeiraAbaPlanilha)
#         seleciona_primeiraPlanilha = abreExcel.ActiveSheet
        
#         # Encontra a última coluna com dados
#         ultimaColuna = seleciona_primeiraPlanilha.UsedRange.Columns.Count
        
#         # Converte o número da coluna para letra (ex: 1 = A, 2 = B, etc.)
#         def column_number_to_letter(n):
#             result = ""
#             while n > 0:
#                 n -= 1
#                 result = chr(n % 26 + ord('A')) + result
#                 n //= 26
#             return result
        
#         ultimaColuna_letter = column_number_to_letter(ultimaColuna)
        
#         # Define o range das linhas 3 a 11 de todas as colunas
#         endereco_linhasExcel = f"A3:{ultimaColuna_letter}11"
        
#         # Seleciona o range especificado
#         endereco_linhasExcel_selecionado = seleciona_primeiraPlanilha.Range(endereco_linhasExcel)
        
#         # Copia os dados selecionados
#         endereco_linhasExcel_selecionado.Copy()
        
#         print(f"Dados copiados do range: {endereco_linhasExcel}")
        
#         # Extrai os dados para retornar (para uso posterior)
#         data = []
#         for row in endereco_linhasExcel_selecionado.Rows:
#             row_data = []
#             for cell in row.Cells:
#                 row_data.append(cell.Value)
#             data.append(row_data)
        
#         limpar_dados_coluna_c(data)
#         # tratar_popup_transferencia()
        
#         # Fecha o arquivo Excel mas mantém o Excel aberto para manter os dados na área de transferência
#         abreExcel.Close(SaveChanges=False)
        
#         return data, excel_app
        
#     except Exception as e:
#         print(f"Erro ao processar o arquivo Excel: {str(e)}")
#         raise

# # Versão alternativa mais simples usando apenas automação de teclado
# def abreExcel_copiaDados_simples(file_path):
#     """
#     Versão alternativa mais simples que usa apenas automação de teclado
#     """
#     try:
#         # Cria uma instância do Excel através do COM
#         excel_app = win32com.client.Dispatch("Excel.Application")
        
#         # Torna o Excel visível
#         excel_app.Visible = True
        
#         # Desabilita alertas temporariamente
#         excel_app.DisplayAlerts = False
#         excel_app.ScreenUpdating = False
        
#         # Abre o arquivo Excel
#         abreExcel = excel_app.Workbooks.Open(file_path)
        
#         # Seleciona a primeira planilha
#         seleciona_primeiraPlanilha = abreExcel.ActiveSheet
        
#         # Encontra a última coluna com dados
#         ultimaColuna = seleciona_primeiraPlanilha.UsedRange.Columns.Count
        
#         # Converte o número da coluna para letra
#         def column_number_to_letter(n):
#             result = ""
#             while n > 0:
#                 n -= 1
#                 result = chr(n % 26 + ord('A')) + result
#                 n //= 26
#             return result
        
#         ultimaColuna_letter = column_number_to_letter(ultimaColuna)
        
#         # Define o range das linhas 3 a 11 de todas as colunas
#         endereco_linhasExcel = f"A3:{ultimaColuna_letter}11"
        
#         # Seleciona o range especificado
#         endereco_linhasExcel_selecionado = seleciona_primeiraPlanilha.Range(endereco_linhasExcel)
#         endereco_linhasExcel_selecionado.Select()
        
#         # Reabilita atualizações da tela temporariamente para a cópia
#         excel_app.ScreenUpdating = True
        
#         # Copia os dados selecionados
#         endereco_linhasExcel_selecionado.Copy()
        
#         print(f"Dados copiados do range: {endereco_linhasExcel}")
        
#         # Aguarda 1 segundo e pressiona Escape para fechar qualquer popup
#         time.sleep(1)
#         pyautogui.press('escape')
#         time.sleep(0.5)
        
#         # Se ainda houver popup, pressiona Tab e Enter (para "Não")
#         pyautogui.press('tab')
#         time.sleep(0.2)
#         pyautogui.press('enter')
        
#         # Extrai os dados para processamento
#         data = []
#         for row in endereco_linhasExcel_selecionado.Rows:
#             row_data = []
#             for cell in row.Cells:
#                 row_data.append(cell.Value)
#             data.append(row_data)
        
#         # Limpa os dados da coluna C
#         data = limpar_dados_coluna_c(data)
        
#         # Reativa configurações do Excel
#         excel_app.DisplayAlerts = True
#         excel_app.ScreenUpdating = True
        
#         # Fecha o arquivo Excel
#         abreExcel.Close(SaveChanges=False)
        
#         return data, excel_app
        
#     except Exception as e:
#         print(f"Erro ao processar o arquivo Excel: {str(e)}")
#         try:
#             excel_app.DisplayAlerts = True
#             excel_app.ScreenUpdating = True
#         except:
#             pass
#         raise


# def colaDados_googleSheets(google_sheets_url, data, credentials_file):
#     """
#     6. Acesse uma planilha do Google Sheets de acordo com o link fornecido;
#     7. Cole esses dados na planilha do Google Sheets a partir da primeira linha vazia disponível;
#     """
#     try:
#         # Configura as credenciais do Google Sheets
#         client = setup_google_credentials(credentials_file)
        
#         # Extrai o ID da planilha a partir da URL
#         if '/d/' in google_sheets_url:
#             abre_planilhaExcel_id = google_sheets_url.split('/d/')[1].split('/')[0]
#         else:
#             raise ValueError("URL do Google Sheets inválida")
        
#         # Abre a planilha pelo ID
#         abre_planilhaExcel = client.open_by_key(abre_planilhaExcel_id)
        
#         # Seleciona a primeira aba da planilha
#         seleciona_primeiraAbaPlanilha = abre_planilhaExcel.get_seleciona_primeiraAbaPlanilha(0)
        
#         # Encontra a primeira linha vazia
#         all_values = seleciona_primeiraAbaPlanilha.get_all_values()
#         next_row = len(all_values) + 1
        
#         # Se a planilha estiver completamente vazia, inicia na linha 1
#         if not any(any(row) for row in all_values):
#             next_row = 1
#         else:
#             # Encontra a primeira linha completamente vazia
#             for i, row in enumerate(all_values):
#                 if not any(cell.strip() for cell in row):
#                     next_row = i + 1
#                     break
        
#         print(f"Inserindo dados a partir da linha {next_row}")
        
#         # Determina o range onde os dados serão colados
#         num_rows = len(data)
#         num_cols = len(data[0]) if data else 0
        
#         # Converte números das colunas em letras para o range
#         def num_to_col_letters(num):
#             letters = ''
#             while num:
#                 mod = (num - 1) % 26
#                 letters = chr(mod + 65) + letters
#                 num = (num - 1) // 26
#             return letters
        
#         start_col = 'A'
#         end_col = num_to_col_letters(num_cols)
#         end_row = next_row + num_rows - 1
        
#         range_name = f'{start_col}{next_row}:{end_col}{end_row}'
        
#         # Insere os dados na planilha
#         seleciona_primeiraAbaPlanilha.update(range_name, data)
        
#         print(f"Dados inseridos com sucesso no range {range_name}")
#         print(f"Planilha acessível em: {google_sheets_url}")
        
#     except Exception as e:
#         print(f"Erro ao acessar ou modificar a planilha do Google Sheets: {str(e)}")
#         raise