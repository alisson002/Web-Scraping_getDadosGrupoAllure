import login_vg as lvg # dados de login
import login_cliniCorp as lcc # função de login
import outrasDefs as defs
import addDados_EXtoGS as exgs
from datetime import date

exgs.copiandoDados_excelToGs(lvg.gs_link,lvg.caminho_credenciais)
