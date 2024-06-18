import paramiko
import pandas as pd
import openpyxl
import socket
import datetime

def check_ip_connectivity(ip_address, port=22, timeout=3):
    """
    Verifica se o IP está ativo e respondendo na porta especificada.

    Args:
        ip_address (str): O endereço IP a ser verificado.
        port (int, optional): A porta a ser verificada. Defaults to 22 (SSH).
        timeout (int, optional): O tempo limite em segundos. Defaults to 3.

    Returns:
        bool: True se o IP está ativo e respondendo, False caso contrário.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip_address, port))
            return True
    except socket.timeout:
        return False
    except Exception as e:
        print(f"Erro ao verificar conectividade com {ip_address}: {e}")
        return False

def connect_to_server(ip_address, username, password):
    """
    Establishes an SSH connection to the specified server.

    Args:
        ip_address (str): The IP address of the server.
        username (str): The username to use for authentication.
        password (str): The password to use for authentication.

    Returns:
        paramiko.SSHClient: The SSH client object if successful, or None if connection fails.

    Raises:
        paramiko.AuthenticationException: If authentication fails.
    """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip_address, username=username, password=password, timeout=10)
        print(f"Successfully connected to server {ip_address}")
        return ssh
    except paramiko.AuthenticationException:
        print(f"Failed to connect to server {ip_address}: Invalid credentials")
        with open("erro_conexao.log", "a", encoding="utf-8") as f:  # Codificação UTF-8
            f.write(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Erro de conexão com o servidor: {ip_address} - Credenciais inválidas\n")
        return None
    except TimeoutError as e:
        print(f"Tempo limite excedido ao conectar ao servidor {ip_address}: {e}")
        with open("erro_conexao.log", "a", encoding="utf-8") as f:  # Codificação UTF-8
            f.write(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Tempo limite excedido ao conectar ao servidor: {ip_address}\n")
        return None

def configure_log_retention(ssh, day_old=180):
    """
    Configures log retention on the connected server.

    Args:
        ssh (paramiko.SSHClient): The SSH client object connected to the server.
        day_old (int, optional): The number of days to retain logs. Defaults to 180.

    Returns:
        None
    """

    # Modify logrotate.conf file
    stdin, stdout, stderr = ssh.exec_command(f"sudo sed -i 's/366/{day_old}/' /etc/logrotate.conf")
    if stderr.read().decode('utf-8').strip():
        print(f"Error modifying logrotate.conf on server {ssh.get_transport().getpeername()[0]}: {stderr.read().decode('utf-8')}")
        return

    # Set DAYOLD variable
    ssh.exec_command(f"echo DAYOLD={day_old} >> /etc/profile")

    # Clean up old log files
    ssh.exec_command(f"/usr/bin/find /var/log/ -type f -mtime +{day_old} | xargs /bin/rm -v")
    print(f"Log cleanup completed on server {ssh.get_transport().getpeername()[0]}")

if __name__ == "__main__":
    # Read server information from Excel spreadsheet
    try:
        data = pd.read_excel('servers.xlsx')
    except FileNotFoundError:
        print("Error: Excel file 'servers.xlsx' not found.")
        exit(1)
    ip_addresses = data['IP Address'].tolist()
    usernames = data['Username'].tolist()
    passwords = data['Password'].tolist()

    # Connect to each server and configure log retention
    for ip_address, username, password in zip(ip_addresses, usernames, passwords):
        if check_ip_connectivity(ip_address):
            ssh = connect_to_server(ip_address, username, password)
            if ssh:
                configure_log_retention(ssh)
                ssh.close()
        else:
            print(f"Servidor {ip_address} não está respondendo. Pulando...")
            with open("erro_conexao.log", "a", encoding="utf-8") as f:  # Codificação UTF-8
                f.write(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Servidor {ip_address} não está respondendo ou está desligado.\n")

    # Display success message when the list is complete
    print("\nLog retention configuration completed for all servers in 'servers.xlsx'.")