import csv
import cx_Oracle
import paramiko
import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def check_internet():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def check_database():
    try:
        con = cx_Oracle.connect('xxxxxxxxxxxxxxx')
        con.close()
        return True
    except cx_Oracle.DatabaseError:
        return False

def monta_csv(query, file_name):
    con = cx_Oracle.connect('xxxxxxxxxxxxxxx')
    headerList = ['nome', 'email', 'telefone', 'telefone_residencial' , 'codigo_ext', 'cpf', 'idade', 'data atendimento','data do disparo',
                  'segmentação', 'convenio', 'especialidade', 'medicos', 'setores', 'tipo']
    cursor = con.cursor()
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            dw = csv.DictWriter(csv_file, delimiter=',', fieldnames=headerList)
            dw.writeheader()
            writer = csv.writer(csv_file, delimiter=',')
            cursor.execute(query)
            for row in cursor:
                writer.writerow(row)
    finally:
        cursor.close()
        con.close()

def enviar_via_sftp(file_name):
    sftp_host = 'xxxxxxxxxxxxxxx'
    sftp_port = 22
    sftp_username = 'xxxxxxxxxxxxxxx'
    sftp_key_path = "xxxxxxxxxxxxxxx"
    sftp_remote_path = '/'

    transport = paramiko.Transport((sftp_host, sftp_port))
    transport.connect(username=sftp_username, pkey=paramiko.RSAKey.from_private_key_file(sftp_key_path))
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.put(file_name, sftp_remote_path + file_name.split('\\')[-1])
    finally:
        sftp.close()
        transport.close()

def sem_internet():
    con = cx_Oracle.connect('xxxxxxxxxxxxxxx')
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO shac_valida_envio_email_NPS VALUES ('NPS NAO ENVIADO. Sem Internet', sysdate)")
        con.commit()
    finally:
        cursor.close()
        con.close()

def sem_BD():
    host = "smtp.gmail.com"
    port = 587
    login = "xxxxxxxxxxxxxxx"
    senha = "xxxxxxxxxxxxxxx"

    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(login, senha)

    corpo = '<b>NPS Track Nao enviado.</b> <b>Ao tentar enviar o arquivo .CSV, via SFTP, nao obteve acesso ao Banco de dados. </b>'

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = 'xxxxxxxxxxxxxxx'
    email_msg['Subject'] = 'Atenção NPS Track não enviado'
    email_msg.attach(MIMEText(corpo, 'html'))
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

def process_files():
    queries = {
        "C:\\Hospital\\Padrao\\O2JC_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'INTERNACAO' AND CONVENIO = 'SUS'",
        "C:\\Hospital\\Padrao\\dSLz_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'AMBULATORIO'",
        "C:\\Hospital\\Padrao\\naAs_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'HOSPITAL_DIA'",
        "C:\\Hospital\\Padrao\\RJCx_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'INTERNACAO' AND CONVENIO <> 'SUS'",
        "C:\\Hospital\\Padrao\\yJ5R_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'EXAMES'",
        "C:\\Hospital\\Padrao\\zxeW_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'PRONTO_ATENDIMENTO'",
        "C:\\Hospital\\Padrao\\4pC6_WHATSAPP_WIHASHpThme5_TWNAMEangelinacaron_TWLANGpt-BR_TWVARcustomer.name.csv": "SELECT * FROM SHAC_ATEND_NPS_SFTP_V WHERE SEGMENTACAO = 'HOSPITAL_DIA' AND IDADE >= 50"
    }

    for file_name, query in queries.items():
        monta_csv(query, file_name)
        ##enviar_via_sftp(file_name) test

while True:
    internet_available = check_internet()
    database_available = check_database()

    if internet_available and database_available:
        process_files()
        break
    else:
        if not internet_available:
            sem_internet()
        if not database_available:
            sem_BD()
        time.sleep(2 * 60 * 60)

with open('programa_log.txt', 'a') as log_file:
    log_file.write(f'Programa executado com sucesso em: {datetime.datetime.now()}\n')
