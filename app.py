from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from datetime import datetime
from execucao_ano import df_html
import os

def send_mail(assunto, titulo, tabela):
    msg = MIMEMultipart('related')
    msg['From'] = os.getenv('REMETENTE')
    msg['To'] = os.getenv('DESTINATARIOS')
    msg['Subject'] = assunto
    
    estilo = '''
    <style>
        table {
            margin: 0 auto;
            border-collapse: collapse;
            width: 90%;
            font-family: Arial, sans-serif;
            border: 1px solid #dddddd;
        }
        th {
            border: 1px solid #dddddd;
            padding: 8px;
            background-color: #1e43a2;
            text-align: center;
            color: white;
        }
        td {
            border: 1px solid #dddddd;
            padding: 8px;
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
    '''

    html_parte = MIMEText(
       f'<html><head>{estilo}</head>' 
        + '<body style="border-radius: 15px; width: 50vw; min-width: 330px; padding: 20px; border: solid #C8C8C8 1px; text-align: center;">' 
        + '<div style="border-radius: 10px; width: 250px; font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande", "Lucida Sans Unicode", Geneva, Verdana, sans-serif; margin: 0 auto;" >' 
        + f'<img src="cid:header_image" style="border-radius: 10px; width: 100%; height: 100%;" alt="Header_png"> {titulo}{tabela}</div>' 
        + f'<img src="cid:footer_image" style="border-radius: 10px; width: 100%; height: 100%; margin-top: 25px;" alt="Footer_png"></body></html>',
        'html',
    )
    msg.attach(html_parte)

    # Imagem do cabeçalho
    image_path = './header.png'
    with open(image_path, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name='header.png')
        image.add_header('Content-ID', '<header_image>')
        msg.attach(image)

    # Imagem do rodapé
    image_footer = './footer.png'
    with open(image_footer, 'rb') as image_file_footer:
        imageFooter = MIMEImage(image_file_footer.read(), name='footer.png')
        imageFooter.add_header('Content-ID', '<footer_image>')
        msg.attach(imageFooter)

    # Envio de e-mail
    with smtplib.SMTP(os.getenv('SERVER'), os.getenv('PORTA')) as server:
        server.starttls()
        server.login(os.getenv('REMETENTE'), os.getenv('PASSWORD'))
        server.sendmail(os.getenv('REMETENTE'), os.getenv('DESTINATARIOS'), msg.as_string())

if __name__ == '__main__':
    today_date = datetime.now().strftime('%Y-%m-%d')

    tabela = df_html

    send_mail(
        f'Posição da execução orçamentária por UO 2024: {today_date}',
        f'<h1 style=" border-bottom: 1px solid #C8C8C8; font-size: 25px; text-align: center; color: #1e43a2; font-weight: bold;">Posição da execução orçamentária por UO 2024<br>{today_date}</h1>',
        tabela
    )
