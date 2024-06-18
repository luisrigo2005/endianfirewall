# endianfirewall
README.md
ESCOPO = 
    1 - Endian Firewall utiliza 366 dias para retenção dos logs;
    2 - Isso gera demanda para executar uma limpeza nos logs do servidor, 
        afeta o registro de novos logs que não são gravados;
    3 - Gera demanda de chamado para liberar espaço no servidor.

SOLUÇÃO = 
    1 - Diminuir o tempo de retenção dos logs para 180 dias;
    2 - Executar uma limpeza no servidor para eliminar logs mais antigos;
    3 - Automatizar esta tarefa para diminuir o tempo da execução da atividade;
    
ATIVIDADES = 
    1 - Alterar o número de dias de retenção dos logs no arquivo /etc/logrotate.conf
        na linha rotate trocar de 366 para 180;
    2 - Setar a variavél DAYOLD para 180 utilizando o comando:
        DAYOLD=+180
    3 - Executar a limpeza dos arquivos de log mantendo os ultimos 180 dias
         /usr/bin/find /var/log/ -type f -mtime $DAYOLD | xargs /bin/rm -v
 
PROBLEMAS ENCONTRADOS = 
    1 - Instalar as bibliotecas necessárias, não passam pelo firewall com o comando pip install
        Para corrigir este problema utilizar:
        pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org paramiko pandas openpyxl sockets datetime

Este repositório contém um script Python para automatizar a configuração de retenção de logs em servidores remotos via SSH.

Pré-requisitos
Python 3.x instalado
Bibliotecas Python: paramiko, pandas, openpyxl, socket
Arquivo Excel servers.xlsx com as seguintes colunas:
IP Address: O endereço IP do servidor.
Username: O nome de usuário para autenticação SSH.
Password: A senha para autenticação SSH.

Instalação
Clone este repositório.
Instale as bibliotecas Python necessárias:
pip install paramiko pandas openpyxl
Crie um arquivo Excel chamado servers.xlsx com a informação dos servidores que você deseja configurar.
Execução
Execute o script Python:
python automate.py

Funcionamento
O script lê as informações do servidor a partir do arquivo servers.xlsx.
Verifica a conectividade com cada servidor via IP e porta SSH (22 por padrão).
Se o servidor estiver respondendo, tenta conectar via SSH usando as credenciais do arquivo Excel.
Se a conexão for bem-sucedida, configura a retenção de logs no servidor, definindo o número de dias de logs a serem mantidos (por padrão 180 dias).
Limpa arquivos de logs antigos.
Registra erros de conexão em um arquivo erro_conexao.log com a data e hora.
Configurações
O número de dias de retenção de logs pode ser ajustado na função configure_log_retention (parâmetro day_old).
A porta SSH também pode ser modificada na função check_ip_connectivity (parâmetro port).
Notas
As credenciais SSH estão armazenadas em um arquivo Excel. É recomendado que este arquivo seja mantido em um local seguro e acessível apenas aos usuários autorizados.
O script assume que o usuário tem privilégios de administrador nos servidores remotos para executar comandos sudo.
É importante ter em mente as políticas de segurança de seus servidores e garantir que o script esteja em conformidade com as mesmas.

