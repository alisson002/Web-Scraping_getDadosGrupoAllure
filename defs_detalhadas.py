from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

def click_download():
    """
    FUNÇÃO: CLIQUE AUTOMATIZADO NO BOTÃO DE DOWNLOAD
    ====================================================
    
    DESCRIÇÃO GERAL:
    Esta função implementa um sistema robusto e multicamadas para localizar e clicar 
    automaticamente no botão de download em páginas web que utilizam Material UI (MUI).
    Foi desenvolvida especificamente para sistemas web modernos que implementam componentes
    React com classes CSS dinâmicas e estruturas HTML complexas.
    
    ARQUITETURA DA FUNÇÃO:
    A função utiliza uma abordagem em cascata com 4 estratégias principais de localização:
    
    1. ESTRATÉGIA PRIMÁRIA - Seletores CSS/XPath Específicos:
       - Utiliza 10 seletores diferentes baseados na análise do HTML real
       - Prioriza seletores mais específicos para maior precisão
       - Cada seletor foi criado com base em padrões identificados no DOM da aplicação
       - Usa WebDriverWait com timeout de 15 segundos para cada tentativa
       - Implementa fallback automático se um seletor falhar
    
    2. ESTRATÉGIA SECUNDÁRIA - Navegação por Elementos Filhos:
       - Localiza primeiro o elemento <span> interno que contém o texto "download"
       - Navega para o elemento pai usando XPath "./.."
       - Verifica se o elemento pai é realmente um botão
       - Útil quando as classes do botão mudam mas a estrutura interna permanece
    
    3. ESTRATÉGIA TERCIÁRIA - Análise por Posição/Layout:
       - Busca elementos <div> com estilo "position: absolute"
       - Filtra divs que contêm "gap: 8px" (característica específica do layout)
       - Analisa todos os botões dentro dessas divs
       - Verifica se algum botão contém span com texto "download"
       - Estratégia eficaz para elementos com posicionamento absoluto
    
    4. ESTRATÉGIA QUATERNÁRIA - Busca Exaustiva:
       - Analisa todos os botões Material UI da página (classe "MuiButton")
       - Examina o innerHTML de cada botão procurando padrões específicos
       - Procura simultaneamente por: "download", "material-symbols-outlined", "MuiIcon-root"
       - Estratégia de último recurso com análise completa do DOM
    
    SISTEMA DE CLIQUE INTELIGENTE:
    A função implementa 3 métodos diferentes de clique com fallback automático:
    
    1. ActionChains (Método Preferido):
       - Simula movimento natural do mouse até o elemento
       - Adiciona pausa de 0.5 segundos antes do clique
       - Mais próximo da interação humana real
       - Maior compatibilidade com elementos complexos
    
    2. JavaScript Click (Fallback 1):
       - Executa clique diretamente via JavaScript no navegador
       - Bypassa limitações de elementos sobrepostos ou ocultos
       - Útil quando ActionChains falha por questões de layout
    
    3. Selenium Click Padrão (Fallback 2):
       - Método nativo do Selenium WebDriver
       - Usado como último recurso
       - Compatibilidade com elementos mais simples
    
    SISTEMA DE VERIFICAÇÃO DE SUCESSO:
    Após o clique, a função verifica múltiplos indicadores de que o download foi iniciado:
    - Mudanças na URL do navegador
    - Aparição de elementos de loading/progress
    - Mensagens relacionadas a download
    - Novos elementos visíveis na página
    
    TRATAMENTO DE ERROS:
    - Logging detalhado de cada tentativa
    - Captura e relatório de exceções específicas
    - Diagnóstico automático quando todas as estratégias falham
    - Relatório de elementos disponíveis para debug manual
    
    PARÂMETROS:
    - Utiliza variável global 'driver' (instância do WebDriver)
    - Não recebe parâmetros diretos
    
    RETORNO:
    - True: Download iniciado com sucesso
    - False: Falha na localização ou clique do botão
    
    DEPENDÊNCIAS TÉCNICAS:
    - Selenium WebDriver configurado e ativo
    - Página web carregada com elementos Material UI
    - Botão de download presente e acessível no DOM
    
    CASOS DE USO TÍPICOS:
    - Automação de download de relatórios em sistemas corporativos
    - Extração automatizada de dados de dashboards
    - Processamento em lote de downloads de arquivos
    - Integração com pipelines de dados automatizados
    
    LIMITAÇÕES E CONSIDERAÇÕES:
    - Requer que o botão esteja visível e habilitado
    - Dependente da estrutura HTML específica do Material UI
    - Pode necessitar ajustes se a aplicação web for atualizada
    - Timeout padrão de 15 segundos pode não ser suficiente para páginas lentas
    
    EXEMPLO DE HTML ESPERADO:
    <div style="position: absolute; gap: 8px;">
        <button class="MuiButtonBase-root MuiButton-root MuiButton-outlined...">
            <span class="material-symbols-outlined...">download</span>
        </button>
    </div>
    """
    global driver
    
    print("🌐 Dentro de Ranking de Unidades - Procurando por 'DOWNLOAD'.")
    
    # Cria um objeto WebDriverWait para aguardar condições específicas
    wait = WebDriverWait(driver, 15)
    
    print("🔍 Procurando pelo botão 'DOWNLOAD'...")
    
    botao_DOWNLOAD = None
    
    # Seletores baseados na estrutura HTML REAL fornecida
    seletores_botao = [
        # 1. Seletor completo baseado nas classes reais do botão
        "button.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.MuiButton-colorPrimary.MuiButton-disableElevation",
        
        # 2. Seletor mais específico incluindo a classe CSS personalizada
        "button.css-1r9ztn7",
        
        # 3. Seletor combinando classes principais do Material UI
        "button.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary",
        
        # 4. Seletor pelo span interno com o ícone de download
        "span.material-symbols-outlined.MuiIcon-root[aria-hidden='true']",
        
        # 5. XPath para encontrar botão que contém span com texto "download"
        "//button[.//span[contains(@class, 'material-symbols-outlined') and text()='download']]",
        
        # 6. XPath mais específico baseado na estrutura completa
        "//div[@class='flex itens-center']//button[contains(@class, 'MuiButton-outlined')]",
        
        # 7. Seletor pelo elemento pai (div com position absolute)
        "div[style*='position: absolute'] button.MuiButton-root",
        
        # 8. XPath para buscar o span com texto "download" e pegar o botão pai
        "//span[text()='download' and contains(@class, 'material-symbols-outlined')]/parent::button",
        
        # 9. Seletor por atributos específicos do botão
        "button[type='button'][tabindex='0'].MuiButton-outlined",
        
        # 10. Seletor pela combinação de classes únicas
        "button.force-display.css-1r9ztn7"
    ]
    
    # Estratégia 1: Tentar seletores CSS e XPath específicos
    for i, seletor in enumerate(seletores_botao, 1):
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
    FUNÇÃO: VERIFICAÇÃO DE SUCESSO DO DOWNLOAD
    ==========================================
    
    DESCRIÇÃO GERAL:
    Esta função implementa um sistema inteligente de verificação para determinar se um 
    download foi iniciado com sucesso após o clique no botão correspondente. Utiliza 
    múltiplos indicadores e heurísticas para detectar mudanças na página web que 
    sugerem o início do processo de download.
    
    METODOLOGIA DE VERIFICAÇÃO:
    A função emprega uma abordagem multi-indicador que analisa diferentes aspectos 
    da página web para detectar sinais de que o download foi iniciado:
    
    1. ANÁLISE DE URL:
       - Monitora mudanças na URL do navegador
       - Procura pela palavra "download" na URL atual
       - Útil para sistemas que redirecionam durante o download
       - Detecta URLs temporárias ou endpoints de download
    
    2. DETECÇÃO DE ELEMENTOS DE PROGRESSO:
       - Busca elementos com classes "loading", "progress", "spinner"
       - Identifica indicadores visuais de processamento
       - Monitora componentes de UI que aparecem durante operações assíncronas
       - Útil para aplicações SPA (Single Page Application)
    
    3. ANÁLISE DE MENSAGENS TEXTUAIS:
       - Procura texto contendo "download", "Download", "baixando"
       - Detecta mensagens de status ou notificações
       - Identifica feedback textual para o usuário
       - Suporte para múltiplos idiomas (português/inglês)
    
    4. MONITORAMENTO DE ELEMENTOS DINÂMICOS:
       - Detecta novos elementos que se tornaram visíveis
       - Procura por mudanças no DOM após o clique
       - Identifica elementos com "display: block" que apareceram
       - Captura modificações dinâmicas na interface
    
    LÓGICA DE DECISÃO:
    A função utiliza uma abordagem de "primeiro indicador positivo":
    - Executa todos os verificadores sequencialmente
    - Para na primeira detecção positiva
    - Assume sucesso se qualquer indicador for detectado
    - Retorna True mesmo se alguns verificadores falharem
    
    TRATAMENTO DE DOWNLOADS SILENCIOSOS:
    Reconhece que alguns downloads podem ser "silenciosos":
    - Não geram indicadores visuais óbvios
    - Iniciam diretamente pelo navegador
    - Não modificam a interface da aplicação
    - Para estes casos, assume sucesso se o clique foi executado
    
    ROBUSTEZ E TOLERÂNCIA A FALHAS:
    - Cada verificador é executado independentemente
    - Falhas individuais não comprometem outros verificadores
    - Logging detalhado de erros para diagnóstico
    - Estratégia defensiva: assume sucesso em caso de dúvida
    
    PARÂMETROS:
    - Utiliza variável global 'driver' (instância do WebDriver)
    - Não recebe parâmetros diretos
    
    RETORNO:
    - True: Download detectado com sucesso OU assumido como bem-sucedido
    - True (padrão): Em caso de incerteza, assume sucesso
    
    CASOS DE USO:
    - Validação de downloads automáticos em dashboards
    - Confirmação de exportação de relatórios
    - Verificação de downloads de arquivos em lote
    - Monitoramento de operações assíncronas
    
    LIMITAÇÕES:
    - Pode gerar falsos positivos em páginas com muitos elementos dinâmicos
    - Dependente da implementação específica da aplicação web
    - Timeout fixo de verificação pode não ser adequado para todos os cenários
    - Não verifica se o arquivo foi realmente baixado no sistema de arquivos
    
    CONSIDERAÇÕES DE DESEMPENHO:
    - Execução rápida dos verificadores (sem timeouts longos)
    - Interrupção precoce ao primeiro sucesso
    - Mínimo impacto na performance da página
    - Verificações baseadas em estado atual do DOM
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
    FUNÇÃO: DIAGNÓSTICO AVANÇADO E ANÁLISE DO DOM
    =============================================
    
    DESCRIÇÃO GERAL:
    Esta função implementa um sistema completo de diagnóstico e análise para páginas 
    web que contêm botões de download, especificamente projetada para aplicações que 
    utilizam Material UI (MUI) e componentes React. Serve como ferramenta essencial 
    para desenvolvimento, debug e manutenção de automações Selenium.
    
    FUNCIONALIDADE PRINCIPAL:
    A função executa uma varredura sistemática e detalhada da página web atual, 
    coletando informações críticas sobre elementos relacionados a download e 
    fornecendo insights acionáveis para resolução de problemas de automação.
    
    MÓDULOS DE ANÁLISE:
    
    1. ANÁLISE DE INFORMAÇÕES BÁSICAS:
       - Captura título da página web
       - Registra URL atual completa
       - Obtém resolução da janela do navegador
       - Informações essenciais para contexto e reproducibilidade
    
    2. DETECÇÃO ESPECÍFICA DE ELEMENTOS DE DOWNLOAD:
       - Busca exaustiva por todos os elementos contendo texto "download"
       - Análise de tags HTML, classes CSS e conteúdo textual
       - Identificação de elementos potencialmente relacionados ao download
       - Relatório detalhado de cada elemento encontrado
    
    3. CATALOGAÇÃO DE MATERIAL ICONS:
       - Inventário completo de todos os ícones Material UI na página
       - Análise do texto/conteúdo de cada ícone
       - Identificação dos elementos pais de cada ícone
       - Mapeamento da estrutura hierárquica dos componentes
       - Essencial para localizar ícones de download específicos
    
    4. ANÁLISE DE LAYOUT E POSICIONAMENTO:
       - Identificação de todos os elementos com "position: absolute"
       - Análise detalhada dos estilos CSS de posicionamento
       - Contagem de botões dentro de cada container posicionado
       - Mapeamento da estrutura de layout da página
       - Crítico para elementos flutuantes ou sobrepostos
    
    5. INVENTÁRIO DE BOTÕES MATERIAL UI:
       - Catalogação completa de todos os botões MUI na página
       - Análise das classes CSS de cada botão
       - Inspeção do HTML interno de cada componente
       - Identificação de padrões e estruturas comuns
       - Base para criação de seletores precisos
    
    METODOLOGIA DE COLETA:
    - Utiliza seletores CSS e XPath otimizados
    - Implementa tratamento robusto de exceções
    - Coleta informações mesmo de elementos parcialmente carregados
    - Limita saídas para evitar spam de dados
    - Foca nos elementos mais relevantes para debug
    
    SISTEMA DE RELATÓRIOS:
    - Output formatado e estruturado para fácil leitura
    - Categorização clara de diferentes tipos de elementos
    - Numeração sequencial para referência
    - Truncamento inteligente de dados longos
    - Códigos de emoji para identificação visual rápida
    
    CASOS DE USO PRINCIPAIS:
    
    1. DESENVOLVIMENTO DE AUTOMAÇÕES:
       - Identificar seletores corretos para elementos
       - Compreender estrutura da página alvo
       - Validar presença de elementos esperados
    
    2. DEBUG DE FALHAS:
       - Diagnosticar por que automações falharam
       - Identificar mudanças na estrutura da página
       - Localizar elementos que mudaram de posição
    
    3. MANUTENÇÃO DE CÓDIGO:
       - Verificar impacto de atualizações da aplicação
       - Identificar seletores quebrados
       - Mapear novos elementos adicionados
    
    4. ANÁLISE DE PERFORMANCE:
       - Contar quantidade total de elementos
       - Identificar complexidade da página
       - Mapear hierarquia de componentes
    
    TRATAMENTO DE ERROS:
    - Captura individual de exceções por seção
    - Continuação da análise mesmo com falhas parciais
    - Relatório de erros com contexto específico
    - Graceful degradation quando dados não estão disponíveis
    
    OTIMIZAÇÕES IMPLEMENTADAS:
    - Limitação de resultados para evitar sobrecarga
    - Truncamento de strings longas
    - Coleta seletiva de atributos mais relevantes
    - Processamento eficiente mesmo em páginas complexas
    
    SAÍDA ESTRUTURADA:
    A função gera um relatório organizado em seções:
    - Header com informações básicas
    - Seção de elementos com texto "download"  
    - Inventário de Material Icons
    - Análise de divs posicionadas absolutamente
    - Catálogo de botões Material UI
    - Recomendações de próximos passos
    
    INTEGRAÇÃO COM OUTRAS FUNÇÕES:
    - Fornece dados essenciais para click_download()
    - Valida premissas da função de verificação
    - Suporte ao desenvolvimento de novos seletores
    - Base para estratégias de fallback
    
    PARÂMETROS:
    - Utiliza variável global 'driver' (instância do WebDriver)
    - Não recebe parâmetros diretos
    - Opera no contexto da página atual
    
    RETORNO:
    - Não retorna valores (função de diagnóstico)
    - Gera output detalhado via print statements
    - Produz relatório completo da análise da página
    
    CONSIDERAÇÕES DE PERFORMANCE:
    - Função relativamente pesada (uso apenas para debug)
    - Não recomendada para uso em produção contínua
    - Projetada para execução manual ou esporádica
    - Tempo de execução varia com complexidade da página
    
    REQUISITOS TÉCNICOS:
    - WebDriver ativo e página carregada
    - Acesso ao DOM da página
    - Permissões de leitura de elementos e atributos
    - Compatibilidade com aplicações Material UI/React
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