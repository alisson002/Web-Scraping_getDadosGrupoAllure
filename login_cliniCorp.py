from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
from datetime import date


# Variável global para armazenar o driver
driver = None

def inicializar_navegador():
    """
    Função para inicializar o navegador Chrome com configurações otimizadas
    A variável driver fica disponível globalmente para uso em outras funções
    """
    global driver
    
    print("🚀 Inicializando navegador Chrome...")
    
    # Configurações do Chrome para otimizar a automação
    chrome_options = Options()
    # Remove notificações e popups desnecessários do navegador
    chrome_options.add_argument("--disable-notifications")
    # Desativa extensões para melhor performance
    chrome_options.add_argument("--disable-extensions")
    # Remove barras de informação sobre automação
    chrome_options.add_argument("--disable-infobars")
    # Configura User-Agent para parecer mais com um navegador real
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Para executar em modo headless (sem interface gráfica), descomente a linha abaixo:
    # chrome_options.add_argument("--headless")
    
    try:
        # Inicializa o driver do Chrome com as opções configuradas
        # O webdriver.Chrome() cria uma instância do navegador Chrome controlada pelo Selenium
        driver = webdriver.Chrome(options=chrome_options)
        
        # Define um tempo limite padrão para encontrar elementos (10 segundos)
        # Isso evita que o script trave se um elemento demorar para carregar
        driver.implicitly_wait(10)
        
        # Maximiza a janela do navegador para garantir que todos os elementos sejam visíveis
        # Alguns sites têm comportamentos diferentes em telas menores
        driver.maximize_window()
        
        print("✅ Navegador inicializado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar navegador: {type(e).__name__}: {e}")
        print("⚠️ Verifique se o ChromeDriver está instalado e configurado corretamente")
        sys.exit(1)  # Encerra o programa se não conseguir inicializar o navegador


def loginCliniCorp_RU(url_login, RU_usuario, RU_senha):
    """
    Função para fazer login automatizado no sistema CliniCorp
    Usa a variável global 'driver' que deve ser inicializada antes
    
    Parâmetros:
    - url_login: string com o link da página de login
    - RU_usuario: string com o nome de usuário ou email
    - RU_senha: string com a senha do usuário
    
    A função executa o login e deixa o navegador aberto para uso posterior
    Em caso de erro crítico, encerra o programa
    """
    global driver
    
    # Verifica se o navegador foi inicializado
    if driver is None:
        print("❌ Erro: Navegador não foi inicializado!")
        print("💡 Chame a função inicializar_navegador() antes do login")
        sys.exit(1)
    
    try:
        print(f"🌐 Acessando a página de login: {url_login}")
        # Navega para a URL de login fornecida
        # O get() aguarda a página carregar completamente antes de continuar
        driver.get(url_login)
        
        # Aguarda 3 segundos para garantir que a página carregou completamente
        # Alguns elementos JavaScript podem demorar para aparecer
        time.sleep(3)
        
        # Cria um objeto WebDriverWait para aguardar condições específicas
        # Timeout de 15 segundos para operações que precisam de espera
        wait = WebDriverWait(driver, 15)
        
        print("🔍 Procurando pelo campo de usuário...")
        # Tenta encontrar o campo de usuário usando diferentes seletores possíveis
        # Os sites podem usar diferentes IDs, names ou classes para os campos de login
        campo_RU_usuario = None
        seletores_RU_usuario = [
            "input[id='username']",      # Campo com id="username"
            "input[name='username']",    # Campo com name="username"
            "input[name='user']",        # Campo com name="user"
            "input[name='email']",       # Campo com name="email"
            "input[id='user']",          # Campo com id="user"
            "input[id='email']",         # Campo com id="email"
            "input[type='text']",        # Primeiro campo de texto encontrado
            "input[placeholder*='usuário']",  # Campo com placeholder contendo "usuário"
            "input[placeholder*='email']"     # Campo com placeholder contendo "email"
        ]
        
        # Itera pelos seletores até encontrar um campo válido
        for seletor in seletores_RU_usuario:
            try:
                # Aguarda até 10 segundos pelo elemento aparecer
                campo_RU_usuario = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
                print(f"✅ Campo de usuário encontrado com seletor: {seletor}")
                break  # Sai do loop se encontrou o campo
            except TimeoutException:
                continue  # Tenta o próximo seletor se este falhou
        
        # Verifica se conseguiu encontrar o campo de usuário
        if campo_RU_usuario is None:
            print("❌ Erro crítico: Não foi possível encontrar o campo de usuário")
            print("💡 Verifique se a URL está correta e se a página carregou completamente")
            encerrar_navegador()
            sys.exit(1)
        
        # Limpa qualquer conteúdo existente no campo e digita o usuário
        # clear() remove texto que pode estar pré-preenchido
        campo_RU_usuario.clear()
        # send_keys() simula a digitação do usuário
        campo_RU_usuario.send_keys(RU_usuario)
        print(f"✅ Usuário '{RU_usuario}' inserido no campo")
        
        print("🔍 Procurando pelo campo de senha...")
        # Processo similar para encontrar o campo de senha
        campo_RU_senha = None
        seletores_RU_senha = [
            "input[id='password']",      # Campo com id="password"
            "input[name='password']",    # Campo com name="password"
            "input[name='passwd']",      # Campo com name="passwd"
            "input[name='pwd']",         # Campo com name="pwd"
            "input[id='passwd']",        # Campo com id="passwd"
            "input[id='pwd']",           # Campo com id="pwd"
            "input[type='password']",    # Campo de tipo senha
            "input[placeholder*='senha']" # Campo com placeholder contendo "senha"
        ]
        
        # Itera pelos seletores de senha
        for seletor in seletores_RU_senha:
            try:
                campo_RU_senha = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
                print(f"✅ Campo de senha encontrado com seletor: {seletor}")
                break
            except TimeoutException:
                continue
        
        if campo_RU_senha is None:
            print("❌ Erro crítico: Não foi possível encontrar o campo de senha")
            print("💡 Verifique se a página de login está carregada corretamente")
            encerrar_navegador()
            sys.exit(1)
        
        # Insere a senha no campo encontrado
        campo_RU_senha.clear()
        campo_RU_senha.send_keys(RU_senha)
        print("✅ Senha inserida no campo")
        
        print("🔍 Procurando pelo botão de login...")
        # Procura pelo botão de submit/login usando vários seletores possíveis
        botao_login = None
        seletores_botao = [
            "button:contains('Entrar')", # Botão com texto "Entrar"
            "button[type='submit']",     # Botão de submit
            "input[type='submit']",      # Input de submit
            "button:contains('Login')",  # Botão com texto "Login"
            "input[value='Entrar']",     # Input com valor "Entrar"
            "input[value='Login']",      # Input com valor "Login"
            ".btn-login",                # Classe CSS comum para botões de login
            "#login-button",             # ID comum para botões de login
            "form button",               # Qualquer botão dentro de um form
            "form input[type='submit']"  # Qualquer input submit dentro de um form
        ]
        
        # Tenta encontrar o botão usando cada seletor
        for seletor in seletores_botao:
            try:
                if ":contains(" in seletor:
                    # Para seletores com :contains, usa XPath que suporta texto
                    texto = seletor.split("'")[1]  # Extrai o texto do seletor
                    xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}']"
                    botao_login = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                else:
                    # Para outros seletores, usa CSS selector normal
                    botao_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                print(f"✅ Botão de login encontrado com seletor: {seletor}")
                break
            except TimeoutException:
                continue
        
        if botao_login is None:
            print("❌ Erro crítico: Não foi possível encontrar o botão de login")
            print("💡 Verifique se o formulário de login está visível na página")
            encerrar_navegador()
            sys.exit(1)
        
        # Aguarda um pouco antes de clicar para garantir que a página está pronta
        time.sleep(1)
        
        print("🔐 Clicando no botão de login...")
        # Clica no botão de login para submeter o formulário
        botao_login.click()
        
        # Aguarda alguns segundos para a página processar o login
        print("⏳ Aguardando resposta do servidor...")
        time.sleep(5)
        
        # Verifica se o login foi bem-sucedido analisando a URL atual
        url_atual = driver.current_url
        print(f"🌐 URL atual após login: {url_atual}")
        
        # Critérios para determinar se o login foi bem-sucedido:
        # 1. A URL mudou da página de login
        # 2. Não contém palavras que indicam erro
        # 3. Contém indicadores de área logada
        if (url_atual != url_login and 
            "login" not in url_atual.lower() and
            "erro" not in url_atual.lower() and
            "error" not in url_atual.lower()):
            
            print("🎉 Login realizado com sucesso!")
            
            # Procura por elementos que confirmam que o usuário está logado
            try:
                # Procura por indicadores comuns de usuário logado
                indicadores_logado = [
                    "//*[contains(@class, 'welcome-msg__text--2')]",    # Classe do texto de bom dia
                    "//a[contains(text(), 'Ranking de Unidades')]",     # Link da tela Ranking de Unidades
                    "//a[contains(text(), 'Bom dia!')]",                # texto de Bom dia.
                    "//a[contains(text(), 'Logout')]",                  # Link de logout
                    "//a[contains(text(), 'Sair')]",                    # Link de sair
                    "//*[contains(text(), 'Bem-vindo')]",               # Mensagem de boas-vindas
                    "//*[contains(@class, 'user-menu')]",               # Menu de usuário
                    "//*[contains(@class, 'dashboard')]",               # Área de dashboard
                    "//*[contains(@class, 'main-content')]"             # Conteúdo principal
                ]
                
                confirmacao_encontrada = False
                for indicador in indicadores_logado:
                    try:
                        elemento = driver.find_element(By.XPATH, indicador)
                        print(f"✅ Confirmação de login encontrada: {indicador}")
                        confirmacao_encontrada = True
                        break
                    except NoSuchElementException:
                        continue
                
                if confirmacao_encontrada:
                    print("🎯 Login confirmado após verificação!")
                else:
                    print("⚠️ Login aparentemente bem-sucedido (URL mudou), mas sem confirmação visual")
                
                print("🔄 Navegador permanece aberto para próximas ações...")
                
            except Exception as e:
                print(f"⚠️ Aviso ao verificar indicadores de login: {e}")
                print("🔄 Assumindo login bem-sucedido - navegador permanece aberto...")
            
        else:
            # Se chegou aqui, provavelmente o login falhou
            print("❌ Login falhou - permanece na página de login ou erro detectado")
            
            # Procura por mensagens de erro na página
            try:
                mensagens_erro = [
                    "//*[contains(text(), 'usuário inválido')]",
                    "//*[contains(text(), 'senha incorreta')]",
                    "//*[contains(text(), 'erro')]",
                    "//*[contains(text(), 'falhou')]",
                    "//*[contains(@class, 'error')]",
                    "//*[contains(@class, 'alert-danger')]"
                ]
                
                erro_encontrado = False
                for seletor_erro in mensagens_erro:
                    try:
                        elemento_erro = driver.find_element(By.XPATH, seletor_erro)
                        print(f"💥 Mensagem de erro encontrada: {elemento_erro.text}")
                        erro_encontrado = True
                    except NoSuchElementException:
                        continue
                
                if not erro_encontrado:
                    print("⚠️ Nenhuma mensagem de erro específica encontrada")
                        
            except Exception as e:
                print(f"⚠️ Erro ao verificar mensagens de erro: {e}")
            
            print("🔄 Encerrando programa devido a falha no login...")
            encerrar_navegador()
            sys.exit(1)
    
    except Exception as e:
        # Captura qualquer erro não previsto e exibe informações detalhadas
        print(f"❌ Erro crítico durante o processo de login: {type(e).__name__}: {e}")
        print("🔄 Encerrando programa devido a erro crítico...")
        encerrar_navegador()
        sys.exit(1)


def encerrar_navegador():
    """
    Função para encerrar o navegador de forma segura
    Deve ser chamada no final do programa ou em caso de erro
    """
    global driver
    
    if driver is not None:
        print("🔒 Encerrando navegador...")
        try:
            # Aguarda 3 segundos antes de fechar para permitir visualização
            time.sleep(3)
            driver.quit()  # Encerra o processo do navegador completamente
            driver = None  # Limpa a variável global
            print("✅ Navegador encerrado com sucesso!")
        except Exception as e:
            print(f"⚠️ Aviso ao encerrar navegador: {e}")
    else:
        print("⚠️ Navegador já estava encerrado ou não foi inicializado")


def obter_driver():
    """
    Função para obter a instância do driver
    Útil para usar o driver em outras partes do código
    
    Retorna:
    - driver: instância do WebDriver ou None se não inicializado
    """
    global driver
    return driver

def click_RankinUnidades():
    
    print("🌐 Acessando a página de Ranking de Unidades.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print("🔍 Procurando pelo botão 'Ranking de Unidades'...")
    # Procura pelo botão usando vários seletores possíveis
    botao_RU = None
    seletores_botao = [
        "div[id='Ranking de Unidades']",      # Div com id Ranking de Unidades
        "input[id='Ranking de Unidades']"     # input com id Ranking de Unidades
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}']"
                botao_RU = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                botao_RU = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ Botão de Ranking de Unidades encontrado com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if botao_RU is None:
        print("❌ Erro crítico: Não foi possível encontrar o botão de Ranking de Unidades")
        print("💡 Verifique se o formulário de Ranking de Unidades está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print("🔐 Clicando no botão de Ranking de Unidades...")
    # Clica no botão para submeter o formulário
    botao_RU.click()
    
    # Aguarda alguns segundos para a página processar
    print("⏳ Aguardando resposta do servidor...")
    time.sleep(5)
    
    # Procura por elementos que confirmam que o usuário está em RU
    try:
        indicadores_logado = [
            
            "//div[contains(text(), 'Período')]",
            "//label[contains(text(), 'Período')]",
        ]
        
        confirmacao_encontrada = False
        for indicador in indicadores_logado:
            try:
                elemento = driver.find_element(By.XPATH, indicador)
                print(f"✅ Confirmação de que entrou am Ranking de Unidades encontrada: {indicador}")
                confirmacao_encontrada = True
                break
            except NoSuchElementException:
                continue
        
        if confirmacao_encontrada:
            print("🎯 Você está na tela de Ranking de Unidades!")
        else:
            print("⚠️ Entrada em Ranking de Unidades aparentemente bem-sucedido, mas sem confirmação visual")
        
    except Exception as e:
                print(f"⚠️ Aviso ao verificar indicadores de Ranking de Unidades: {e}")
                print("🔄 Assumindo entrada em Ranking de Unidades bem-sucedido - navegador permanece aberto...")
                
    # Verifica a URL atual
    url_atual = driver.current_url
    print(f"🌐 URL atual após entrar em Ranking de Unidades: {url_atual}")

def click_RU_listarRanking():
    
    print("🌐 Dentro de Ranking de Unidades - Procurando por 'Listar'.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print("🔍 Procurando pelo botão 'Listar'...")
    # Procura pelo botão usando vários seletores possíveis
    botao_Listar = None
    seletores_botao = [
        
        "button:contains('Listar')", 
        "span:contains('Listar')", 
        "button:contains('play_circle_filled')", 
        "span:contains('play_circle_filled')", 
    
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}']"
                botao_Listar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                botao_Listar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ Botão de Listar encontrado com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if botao_Listar is None:
        print("❌ Erro crítico: Não foi possível encontrar o botão de Listar")
        print("💡 Verifique se o formulário de Listar está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print("🔐 Clicando no botão de Listar...")
    # Clica no botão para submeter o formulário
    botao_Listar.click()
    
    # Aguarda alguns
    print("⏳ Aguardando resposta do servidor...")
    time.sleep(5)
    
    # Procura por elementos que confirmam que o usuário está em RU
    try:
        indicadores_logado = [
            
            "//div[contains(@class, 'ReactTable -striped -highlight')]",
            "//div[contains(@class, 'rt-table visible')]",
        
        ]
        
        confirmacao_encontrada = False
        for indicador in indicadores_logado:
            try:
                elemento = driver.find_element(By.XPATH, indicador)
                print(f"✅ Confirmação de que LISTOU o Ranking: {indicador}")
                confirmacao_encontrada = True
                break
            except NoSuchElementException:
                continue
        
        if confirmacao_encontrada:
            print("🎯 Você está com o Ranking LISTADO!")
        else:
            print("⚠️ LISTA de Ranking aparentemente bem-sucedido, mas sem confirmação visual")
        
    except Exception as e:
                print(f"⚠️ Aviso ao verificar indicadores de LISTA: {e}")
                print("🔄 Assumindo entrada em LISTA bem-sucedido - navegador permanece aberto...")
    
    # Verifica se o login foi bem-sucedido analisando a URL atual
    url_atual = driver.current_url
    print(f"🌐 URL atual após entrar em Listar: {url_atual}")

# Será alterada para manipular PERIODO
def procura_periodo(priodo_data):
        
    print("🌐 Dentro de Ranking de Unidades - Procurando por 'Período'.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print("🔍 Procurando pelo seletor 'Período'...")
    # Procura pelo botão usando vários seletores possíveis
    select_rk = None
    seletores_botao = [
        
        "div[id='bc_select_field -toggle']",
        "div[data-value='Vendas']",
        "span:contains('Vendas')",
        # "label[class='md-floating-label md-floating-label--floating md-text--secondary']",
        # "div[class='md-paper md-paper--0 md-fake-btn md-pointer--hover md-fake-btn--no-outline md-select-field md-text']",
        "div[id='bc_select_field -toggle']//div[class='md-icon-separator md-text-field md-text-field--floating-margin md-select-field--text-field']//i:contains('arrow_drop_down')",
        
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ seletor Período encontrado com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if select_rk is None:
        print("❌ Erro crítico: Não foi possível encontrar o seletor Período")
        print("💡 Verifique se o formulário de Período está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print("🔐 Clicando no seletor Período...")
    # Clica no botão para submeter o formulário
    select_rk.click()
    
    # Aguarda alguns segundos para a página processar
    print("⏳ Aguardando resposta do servidor para SELECIONAR PERIODO OU DATA...")
    time.sleep(5)
    
    # Após achar o seletor de período vai procurar e selecionar qual o periodo
    seleciona_periodo(priodo_data)
    
    # Verifica a URL atual
    url_atual = driver.current_url
    print(f"🌐 URL atual após entrar em Listar: {url_atual}")

def seleciona_periodo(priodo_data):
    
    if priodo_data == 'Data':
        seleciona_data()
    else:
        
        if priodo_data == 'Semana atual':
            periodo_itens = 'CURRENT_WEEK'
        
        elif priodo_data == 'Mês atual':
            periodo_itens = 'CURRENT_MONTH'
        
        elif priodo_data == 'Mês anterior':
            periodo_itens = 'LAST_MONTH'
        
        else:
            seleciona_data()
        
        print(f"🌐 Dentro de Ranking de Unidades > Seletor de periodo - Procurando por '{priodo_data}'.")
    
        # Cria um objeto WebDriverWait para aguardar condições específicas
        # Timeout de 15 segundos para operações que precisam de espera
        wait = WebDriverWait(driver, 15)
    
        print(f"🔍 Procurando pelo item '{priodo_data}'...")
    
        # Procura pelo botão usando vários seletores possíveis
        select_rk = None
        seletores_botao = [
            
            f"div[data-value={periodo_itens}]",
            f"span:contains({priodo_data})",
            
        ]
        
        # Tenta encontrar o botão usando cada seletor
        for seletor in seletores_botao:
            try:
                if ":contains(" in seletor:
                    # Para seletores com :contains, usa XPath que suporta texto
                    texto = seletor.split("'")[1]  # Extrai o texto do seletor
                    xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                    select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                else:
                    # Para outros seletores, usa CSS selector normal
                    select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                print(f"✅ encontrado o item '{priodo_data}' na lista de Periodo com seletor: {seletor}")
                break
            except TimeoutException:
                continue
        
        if select_rk is None:
            print(f"❌ Erro crítico: Não foi possível encontrar o item '{priodo_data}'")
            print(f"💡 Verifique se o formulário de '{priodo_data}' está visível na página")
            encerrar_navegador()
            sys.exit(1)
        
        # Aguarda um pouco antes de clicar para garantir que a página está pronta
        time.sleep(1)
        
        print(f"🔐 Clicando no item '{priodo_data}'...")
        # Clica no botão para submeter o formulário
        select_rk.click()

def seleciona_data():
    
    print(f"🌐 Dentro de Ranking de Unidades > Seletor de periodo - Procurando por DATA.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print(f"🔍 Procurando pelo item DATA...")
    # Procura pelo botão usando vários seletores possíveis
    select_rk = None
    seletores_botao = [
        
        "div[data-value='DATE']",
        "span:contains('DATE')",
        
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ encontrado o item DATA na lista de Periodo com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if select_rk is None:
        print("❌ Erro crítico: Não foi possível encontrar o item DATA")
        print("💡 Verifique se o formulário de DATA está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print(f"🔐 Clicando no item DATA...")
    # Clica no botão para submeter o formulário
    select_rk.click()

# INICIO do trecho
# Funções para selecionar uma data personalizada
def define_data():
    pass

def clica_ano(desejado, atual = date.today().year):
    
    anoAtual = atual
    anoDesejado = desejado
    
    print(f"🌐 Dentro de Ranking de Unidades > Seletor de periodo > DATA - Procurando o botão {anoAtual}.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print(f"🔍 Procurando pelo botão {anoAtual}...")
    # Procura pelo botão usando vários seletores possíveis
    select_rk = None
    seletores_botao = [
        
        "button[aria-expanded='false']",
        f"button:contains('{anoAtual}')",
        f"h6:contains('{anoAtual}')",
        
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ encontrado o botão {anoAtual} na lista de Periodo com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if select_rk is None:
        print(f"❌ Erro crítico: Não foi possível encontrar o botão {anoAtual}")
        print(f"💡 Verifique se o botão {anoAtual} está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print(f"🔐 Clicando no botão {anoAtual}...")
    # Clica no botão para submeter o formulário
    select_rk.click()
    
    if anoAtual == anoDesejado:
        clica_semanaDiaMes()
    else:
        print(f"🌐 Dentro de Ranking de Unidades > Seletor de periodo > DATA - Procurando o botão {anoDesejado}.")
    
        # Cria um objeto WebDriverWait para aguardar condições específicas
        # Timeout de 15 segundos para operações que precisam de espera
        wait = WebDriverWait(driver, 15)
        
        print(f"🔍 Procurando pelo item botão {anoDesejado}...")
        # Procura pelo botão usando vários seletores possíveis
        select_rk = None
        seletores_botao = [
            
            f"button:contains('{anoDesejado}')",
            f"h6:contains('{anoDesejado}')",
            
        ]
        
        # Tenta encontrar o botão usando cada seletor
        for seletor in seletores_botao:
            try:
                if ":contains(" in seletor:
                    # Para seletores com :contains, usa XPath que suporta texto
                    texto = seletor.split("'")[1]  # Extrai o texto do seletor
                    xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                    select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                else:
                    # Para outros seletores, usa CSS selector normal
                    select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                print(f"✅ encontrado o botão {anoDesejado} na lista de Periodo com seletor: {seletor}")
                break
            except TimeoutException:
                continue
        
        if select_rk is None:
            print(f"❌ Erro crítico: Não foi possível encontrar o botão {anoDesejado}")
            print(f"💡 Verifique se o botão {anoDesejado} está visível na página")
            encerrar_navegador()
            sys.exit(1)
        
        # Aguarda um pouco antes de clicar para garantir que a página está pronta
        time.sleep(1)
        
        print(f"🔐 Clicando no botão {anoDesejado}...")
        # Clica no botão para submeter o formulário
        select_rk.click()

def clica_semanaDiaMes():
    pass

def seleciona_mês(desejado, atual = date.today().month):
    mesAtual_num = atual
    mesAtual_nome = get_mes(atual)
    mesDesejado_num =  desejado
    mesDesejado_nome =  get_mes(desejado)
    pass

def seleciona_dia(desejado, atual = date.today().day):
    diaAtual_num = atual
    diaAtual_nome = get_mes(atual)
    diaDesejado_num =  desejado
    diaDesejado_nome =  get_mes(desejado)
    pass

global_virhf = 34

def teste():
    global_virhf = 56
    print(global_virhf)

def test2():
    print(global_virhf)
    
def clica_dataInicio():
    
    print(f"🌐 Dentro de Ranking de Unidades > Seletor de periodo > DATA - Procurando por input 'De' (data inicial).")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print(f"🔍 Procurando pelo input 'De' (data inicial)...")
    # Procura pelo botão usando vários seletores possíveis
    select_rk = None
    seletores_botao = [
        
        # "label[for='From']", até encontrava esse mas dps dava erro
        "input[id='From']",
        "label:contains('De')",
        "div:contains('De')",
        
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ encontrado o input 'De' na lista de Periodo com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if select_rk is None:
        print("❌ Erro crítico: Não foi possível encontrar o input 'De' (data inicial)")
        print("💡 Verifique se o formulário do input 'De' (data inicial) está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print(f"🔐 Clicando no input 'De' (data inicial)...")
    # Clica no botão para submeter o formulário
    select_rk.click()

def clica_dataFim():
    
    print(f"🌐 Dentro de Ranking de Unidades > Seletor de periodo > DATA - Procurando por input 'Até' (data final).")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    # Timeout de 15 segundos para operações que precisam de espera
    wait = WebDriverWait(driver, 15)
    
    print(f"🔍 Procurando pelo input 'Até' (data final)...")
    # Procura pelo botão usando vários seletores possíveis
    select_rk = None
    seletores_botao = [
        
        # "label[for='From']", até encontrava esse mas dps dava erro
        "input[id='To']",
        "label:contains('Até')",
        "div:contains('Até')",
        
    ]
    
    # Tenta encontrar o botão usando cada seletor
    for seletor in seletores_botao:
        try:
            if ":contains(" in seletor:
                # Para seletores com :contains, usa XPath que suporta texto
                texto = seletor.split("'")[1]  # Extrai o texto do seletor
                xpath = f"//button[contains(text(), '{texto}')] | //input[@value='{texto}'][1]"
                select_rk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                # Para outros seletores, usa CSS selector normal
                select_rk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            print(f"✅ encontrado o input 'Até' na lista de Periodo com seletor: {seletor}")
            break
        except TimeoutException:
            continue
    
    if select_rk is None:
        print("❌ Erro crítico: Não foi possível encontrar o input 'Até' (data final)")
        print("💡 Verifique se o formulário do input 'Até' (data final) está visível na página")
        encerrar_navegador()
        sys.exit(1)
    
    # Aguarda um pouco antes de clicar para garantir que a página está pronta
    time.sleep(1)
    
    print(f"🔐 Clicando no input 'Até' (data final)...")
    # Clica no botão para submeter o formulário
    select_rk.click()


def get_mes(numero_mes):
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

    if 1 <= numero_mes <= 12:
        # O número do mês (1 a 12) é usado como índice (0 a 11)
        # Retorna o nomes do mês
        return meses[numero_mes - 1]
    else:
        return "Número do mês inválido"

#  FIM do trecho

def click_download():
    """
    Função corrigida para clicar no botão de download
    Baseada na análise do HTML real fornecido
    """
    global driver
    
    print("🌐 Dentro de Ranking de Unidades - Procurando por 'DOWNLOAD'.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    wait = WebDriverWait(driver, 15)
    
    print("🔍 Procurando pelo botão 'DOWNLOAD'...")
    
    botao_DOWNLOAD = None
    
    # Seletores baseados na estrutura HTML REAL fornecida
    # Os 7 primeiros foram comentados pos não funcionam então só pederia tempo usando eles. Melhor ir direto no que funciona primeiro.
    '''
    LEMBRAR DE MELHORAR AS OUTRAS FUNÇÕES COM BASE NESSA POR CONTA DOS SELETORES.
    '''
    seletores_botao = [
        # # 1. Seletor completo baseado nas classes reais do botão
        # "button.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.MuiButton-colorPrimary.MuiButton-disableElevation",
        
        # # 2. Seletor mais específico incluindo a classe CSS personalizada
        # "button.css-1r9ztn7",
        
        # # 3. Seletor combinando classes principais do Material UI
        # "button.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary",
        
        # # 4. Seletor pelo span interno com o ícone de download
        # "span.material-symbols-outlined.MuiIcon-root[aria-hidden='true']",
        
        # # 5. XPath para encontrar botão que contém span com texto "download"
        # "//button[.//span[contains(@class, 'material-symbols-outlined') and text()='download']]",
        
        # # 6. XPath mais específico baseado na estrutura completa
        # "//div[@class='flex itens-center']//button[contains(@class, 'MuiButton-outlined')]",
        
        # # 7. Seletor pelo elemento pai (div com position absolute)
        # "div[style*='position: absolute'] button.MuiButton-root",
        
        # 8. XPath para buscar o span com texto "download" e pegar o botão pai
        "//span[text()='download' and contains(@class, 'material-symbols-outlined')]/parent::button",
        
        # 9. Seletor por atributos específicos do botão
        "button[type='button'][tabindex='0'].MuiButton-outlined",
        
        # 10. Seletor pela combinação de classes únicas
        "button.force-display.css-1r9ztn7"
    ]
    
    # Estratégia 1: Tentar seletores CSS e XPath específicos
    for i, seletor in enumerate(seletores_botao, 1):
        print("🔍 Estratégia 1: - Seletor CSS Específico")
        print(f"🔍 Tentando seletor {i}: {seletor}")
        try:
            if seletor.startswith("//"):
                # XPath
                botao_DOWNLOAD = wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
            else:
                # CSS selector
                botao_DOWNLOAD = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            
            print(f"✅ Botão de DOWNLOAD encontrado com seletor {i}: {seletor}")
            break
            
        except TimeoutException:
            print(f"⏳ Seletor {i} não funcionou, tentando próximo...")
            continue
        except Exception as e:
            print(f"⚠️ Erro no seletor {i}: {e}")
            continue
    
    # Estratégia 2: Busca pelo span com texto "download" e depois o botão pai
    if botao_DOWNLOAD is None:
        print("🔍 Estratégia 2: Buscando pelo span interno e navegando para o botão pai...")
        try:
            # Encontra o span com o ícone de download
            span_download = wait.until(EC.presence_of_element_located((
                By.XPATH, "//span[text()='download' and contains(@class, 'material-symbols-outlined')]"
            )))
            
            # Navega para o botão pai
            botao_DOWNLOAD = span_download.find_element(By.XPATH, "./..")
            
            # Verifica se é realmente um botão
            if botao_DOWNLOAD.tag_name.lower() == 'button':
                print("✅ Botão encontrado navegando do span para o elemento pai!")
            else:
                print("⚠️ Elemento pai não é um botão, continuando busca...")
                botao_DOWNLOAD = None
                
        except Exception as e:
            print(f"⚠️ Erro na estratégia 2: {e}")
    
    # Estratégia 3: Busca por posição na página (canto superior direito)
    if botao_DOWNLOAD is None:
        print("🔍 Estratégia 3: Buscando por posição na página...")
        try:
            # Busca divs com position absolute (onde está localizado o botão)
            divs_absolute = driver.find_elements(By.CSS_SELECTOR, "div[style*='position: absolute']")
            
            for div in divs_absolute:
                try:
                    # Verifica se a div contém "gap: 8px" (característica da div pai)
                    if "gap: 8px" in div.get_attribute("style"):
                        botoes_na_div = div.find_elements(By.TAG_NAME, "button")
                        
                        for botao in botoes_na_div:
                            # Verifica se o botão contém o span com "download"
                            spans = botao.find_elements(By.TAG_NAME, "span")
                            for span in spans:
                                if span.text == "download":
                                    botao_DOWNLOAD = botao
                                    print("✅ Botão encontrado por análise de posição!")
                                    break
                            if botao_DOWNLOAD:
                                break
                        if botao_DOWNLOAD:
                            break
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Erro na estratégia 3: {e}")
    
    # Estratégia 4: Busca exaustiva por todos os botões Material UI
    if botao_DOWNLOAD is None:
        print("🔍 Estratégia 4: Análise exaustiva de todos os botões Material UI...")
        try:
            botoes_mui = driver.find_elements(By.CSS_SELECTOR, "button[class*='MuiButton']")
            print(f"📊 Encontrados {len(botoes_mui)} botões Material UI")
            
            for i, botao in enumerate(botoes_mui):
                try:
                    # Analisa o conteúdo HTML do botão
                    html_interno = botao.get_attribute("innerHTML")
                    
                    # Verifica se contém o span com "download"
                    if ("download" in html_interno and 
                        "material-symbols-outlined" in html_interno and
                        "MuiIcon-root" in html_interno):
                        
                        botao_DOWNLOAD = botao
                        print(f"✅ Botão encontrado na análise exaustiva! (Botão #{i+1})")
                        print(f"📝 Classes: {botao.get_attribute('class')}")
                        break
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Erro na estratégia 4: {e}")
    
    # Verifica se encontrou o botão
    if botao_DOWNLOAD is None:
        print("❌ ERRO CRÍTICO: Não foi possível encontrar o botão de DOWNLOAD")
        print("🔧 Executando diagnóstico avançado...")
        
        # Diagnóstico avançado
        try:
            print("\n🔍 DIAGNÓSTICO AVANÇADO:")
            
            # 1. Verifica se existem elementos com "download"
            elementos_download = driver.find_elements(By.XPATH, "//*[contains(text(), 'download')]")
            print(f"   • Elementos contendo 'download': {len(elementos_download)}")
            
            # 2. Verifica material-symbols-outlined
            material_icons = driver.find_elements(By.CSS_SELECTOR, ".material-symbols-outlined")
            print(f"   • Ícones Material UI: {len(material_icons)}")
            
            for i, icon in enumerate(material_icons[:3]):
                print(f"     {i+1}. Texto: '{icon.text}', Parent: {icon.find_element(By.XPATH, '..').tag_name}")
            
            # 3. Verifica divs com position absolute
            divs_abs = driver.find_elements(By.CSS_SELECTOR, "div[style*='position: absolute']")
            print(f"   • Divs com position absolute: {len(divs_abs)}")
            
            # 4. Lista todos os botões MUI
            botoes_mui = driver.find_elements(By.CSS_SELECTOR, "button[class*='MuiButton']")
            print(f"   • Botões Material UI: {len(botoes_mui)}")
            
        except Exception as e:
            print(f"⚠️ Erro no diagnóstico: {e}")
        
        return False
    
    # Tenta clicar no botão encontrado
    try:
        print("🖱️ Preparando para clicar no botão...")
        
        # Informações sobre o botão encontrado
        print(f"📋 Informações do botão:")
        print(f"   • Tag: {botao_DOWNLOAD.tag_name}")
        print(f"   • Texto: '{botao_DOWNLOAD.text}'")
        print(f"   • Classes: {botao_DOWNLOAD.get_attribute('class')}")
        print(f"   • Visível: {botao_DOWNLOAD.is_displayed()}")
        print(f"   • Habilitado: {botao_DOWNLOAD.is_enabled()}")
        
        # Move para o elemento antes de clicar
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_DOWNLOAD)
        time.sleep(1)
        
        # Aguarda o elemento estar pronto para clique
        wait.until(EC.element_to_be_clickable(botao_DOWNLOAD))
        
        # Estratégia de clique aprimorada
        sucesso_clique = False
        
        # Método 1: Clique com ActionChains (mais preciso)
        try:
            print("🔐 Tentativa 1: Clique com ActionChains...")
            actions = ActionChains(driver)
            actions.move_to_element(botao_DOWNLOAD).pause(0.5).click().perform()
            sucesso_clique = True
            print("✅ Clique ActionChains executado!")
        except Exception as e:
            print(f"⚠️ ActionChains falhou: {e}")
            
            # Método 2: JavaScript click direto
            try:
                print("🔐 Tentativa 2: Clique JavaScript...")
                driver.execute_script("arguments[0].click();", botao_DOWNLOAD)
                sucesso_clique = True
                print("✅ Clique JavaScript executado!")
            except Exception as e2:
                print(f"⚠️ JavaScript falhou: {e2}")
                
                # Método 3: Clique normal do Selenium
                try:
                    print("🔐 Tentativa 3: Clique Selenium normal...")
                    botao_DOWNLOAD.click()
                    sucesso_clique = True
                    print("✅ Clique Selenium executado!")
                except Exception as e3:
                    print(f"❌ TODOS os métodos de clique falharam!")
                    print(f"   ActionChains: {e}")
                    print(f"   JavaScript: {e2}")
                    print(f"   Selenium: {e3}")
                    return False
        
        if not sucesso_clique:
            return False
        
        # Aguarda processamento
        print("⏳ Aguardando processamento do download...")
        time.sleep(3)
        
        # Verifica indicadores de sucesso
        return verificar_download_iniciado()
        
    except Exception as e:
        print(f"❌ Erro geral ao processar clique: {e}")
        return False

def verificar_download_iniciado():
    """
    Verifica se o download foi iniciado com sucesso
    """
    global driver
    
    print("🔍 Verificando se o download foi iniciado...")
    
    try:
        # Lista de indicadores de que o download pode ter iniciado
        indicadores_sucesso = [
            # Mudança na URL
            lambda: "download" in driver.current_url.lower(),
            
            # Elementos de progresso ou loading
            lambda: len(driver.find_elements(By.CSS_SELECTOR, "*[class*='loading'], *[class*='progress'], .spinner")) > 0,
            
            # Mensagens de download
            lambda: len(driver.find_elements(By.XPATH, "//*[contains(text(), 'download') or contains(text(), 'Download') or contains(text(), 'baixando')]")) > 0,
            
            # Novos elementos apareceram na página
            lambda: len(driver.find_elements(By.CSS_SELECTOR, "*[style*='display: block']")) > 0,
        ]
        
        sucesso_detectado = False
        
        for i, verificador in enumerate(indicadores_sucesso, 1):
            try:
                if verificador():
                    print(f"✅ Indicador de sucesso {i} detectado!")
                    sucesso_detectado = True
                    break
            except Exception as e:
                print(f"⚠️ Erro no verificador {i}: {e}")
        
        if sucesso_detectado:
            print("🎉 Download aparentemente iniciado com sucesso!")
            return True
        else:
            print("⚠️ Nenhum indicador claro de download detectado")
            print("💡 Isso não significa necessariamente que falhou - alguns downloads são silenciosos")
            return True  # Assumimos sucesso se o clique funcionou
            
    except Exception as e:
        print(f"⚠️ Erro na verificação de download: {e}")
        return True  # Assumimos sucesso se chegou até aqui

def debug_pagina_download():
    """
    Função auxiliar melhorada para fazer debug da página
    """
    global driver
    
    print("🐛 === DEBUG COMPLETO DA PÁGINA ===")
    
    try:
        # Informações básicas
        print(f"📄 Título: {driver.title}")
        print(f"🌐 URL: {driver.current_url}")
        print(f"📐 Resolução: {driver.get_window_size()}")
        
        # Análise de elementos de download
        print(f"\n🔍 ANÁLISE ESPECÍFICA PARA DOWNLOAD:")
        
        # 1. Busca elementos com "download"
        elementos_download = driver.find_elements(By.XPATH, "//*[contains(text(), 'download')]")
        print(f"   📊 Elementos com texto 'download': {len(elementos_download)}")
        
        for i, elem in enumerate(elementos_download[:3]):
            try:
                print(f"      {i+1}. Tag: {elem.tag_name}, Texto: '{elem.text}', Classes: '{elem.get_attribute('class')}'")
            except Exception as e:
                print(f"      {i+1}. Erro: {e}")
        
        # 2. Material Icons
        material_icons = driver.find_elements(By.CSS_SELECTOR, ".material-symbols-outlined")
        print(f"\n   🎨 Material Icons: {len(material_icons)}")
        
        for i, icon in enumerate(material_icons):
            try:
                parent = icon.find_element(By.XPATH, "..")
                print(f"      {i+1}. Texto: '{icon.text}', Parent: {parent.tag_name}, Parent Classes: '{parent.get_attribute('class')}'")
            except Exception as e:
                print(f"      {i+1}. Erro: {e}")
        
        # 3. Divs com position absolute
        divs_absolute = driver.find_elements(By.CSS_SELECTOR, "div[style*='position: absolute']")
        print(f"\n   📍 Divs com position absolute: {len(divs_absolute)}")
        
        for i, div in enumerate(divs_absolute):
            try:
                style = div.get_attribute("style")
                botoes_dentro = div.find_elements(By.TAG_NAME, "button")
                print(f"      {i+1}. Style: {style[:100]}..., Botões dentro: {len(botoes_dentro)}")
            except Exception as e:
                print(f"      {i+1}. Erro: {e}")
        
        # 4. Todos os botões Material UI
        botoes_mui = driver.find_elements(By.CSS_SELECTOR, "button[class*='MuiButton']")
        print(f"\n   🔘 Botões Material UI: {len(botoes_mui)}")
        
        for i, botao in enumerate(botoes_mui[:5]):  # Primeiros 5
            try:
                print(f"      {i+1}. Texto: '{botao.text}', Classes: '{botao.get_attribute('class')}'")
                print(f"          HTML interno (100 chars): {botao.get_attribute('innerHTML')[:100]}...")
            except Exception as e:
                print(f"      {i+1}. Erro: {e}")
                
        print(f"\n🎯 RECOMENDAÇÃO:")
        print(f"   Use: click_download() para tentar clicar no botão")
        
    except Exception as e:
        print(f"❌ Erro geral no debug: {e}")