import login_vg as lvg # dados de login
import login_cliniCorp as lcc # função de login
import outrasDefs as defs
import addDados_EXtoGS as exgs

# Chamada de função para efetuar o login automático no sistema clinicorp
# RU = Ranking de Unidades
# lcc.loginCliniCorp_RU(login_page, lvg.RU_user, lvg.RU_pass)

RU_usuario = lvg.RU_user
RU_senha = lvg.RU_pass
numeroDivisores = 100

# Inicializa o navegador
lcc.inicializar_navegador()

print("✅ Chrome inicializado.")

defs.divisor(numeroDivisores)

# Dados para login
url_login = 'https://sistema.clinicorp.com/login/' # Link da página de login da CliniCorp
RU_usuario = lvg.RU_user
RU_senha = lvg.RU_pass

# Faz o login (função não retorna valores)
lcc.loginCliniCorp_RU(url_login, RU_usuario, RU_senha)

defs.divisor(numeroDivisores)

# Aqui você pode fazer outras ações após o login
print("🚀 Pronto para executar outras ações...")

defs.divisor(numeroDivisores)

# Procura o botão "Ranking de Unidades" e clica nele
lcc.click_RankinUnidades()

defs.divisor(numeroDivisores)

# Essa função só deve ser chamada após lcc.click_RankinUnidades() pois é para uma tabela dentro da página de rankings
lcc.click_RU_listarRanking()

defs.divisor(numeroDivisores)

rankList = ['Vendas', 'Orçamentos', 'Conversão', 'Orçamentos Aprovados', 'Ticket Médio', 'Orçamentos em Aberto', 'Orçamentos em Follow Up', 'Orçamentos Reprovados', 'Atendimentos', 'Faltas', 'Agendamentos Novos Pacientes', 'Agendamento Pacientes Antigos', 'Entradas', 'Saídas']
periodo = ['Mês atual', 'Semana atual', 'Mês anterior', 'Data']

lcc.procura_periodo(periodo[3])
lcc.clica_dataFim()
lcc.clica_ano(2024)

# lcc.debug_pagina_download()
# lcc.click_download()

# Exemplo de como usar o driver para outras ações:
# driver_atual = obter_driver()
# if driver_atual:
#     driver_atual.get("https://outra-pagina.com")

'''copiandoDados_excelToGs(gs_link,caminho_credenciais)
Função que acumula todo o processo abaixo:

1. Acessa a pasta de downloads do meu computador;
2. Procura o arquivo mais recente que contenha "Report" no nome e seja do tipo .xlsx;
3. Abre esse arquivo com o Excel;
4. Seleciona as linhas de 3 a 11 de todas as colunas;
5. Copia os dados selecionados (linhas 3 a 11 de todas as colunas);
6. Acessa uma planilha do Google Sheets de acordo com o link fornecido;
7. Cola esses dados na planilha do Google Sheets a partir da primeira linha vazia disponível;

# Configura as credenciais para acessar Google Sheets
def setup_google_credentials(credentials_file_path)

# Executa os passos 1 e 2
def encontra_arquivoReport_maisRecente()

# Executa os passos 3, 4, e 5
def abreExcel_copiaDados(file_path)

# Executa os passos 6 e 7
def colaDados_googleSheets(google_sheets_url, data, credentials_file)

# Coloca todo o processo dentro de um try-except para informar de a operação foi um sucesso ou se ocorreu algum erro, com o arquivo sendo fechado caso ocorra ou ao final da execução.

# Existem alguns outros processos no meio, como: emoção do 'edit' de dados numéricos da coluna C e fechar um popup do excel que alerta sobre a área de transferencia.

'''
# exgs.copiandoDados_excelToGs(lvg.gs_link,lvg.caminho_credenciais)

# No final do programa, sempre encerre o navegador
input("Pressione Enter para encerrar o programa...")
lcc.encerrar_navegador()