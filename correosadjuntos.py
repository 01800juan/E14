import smtplib, os, getpass, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64

sender_email = input("remitente:")
password = getpass.getpass()
receiver_email = input ("destinatario:")
asunto = input("asunto:")
mensaje = input("mensaje: ")
archivo = input("Archivo: ")

message = MIMEMultipart("alternative")
message["Subject"] = asunto
message["From"] = sender_email
message["To"] = receiver_email



# Turn these into plain/html MIMEText objects
part1 = MIMEText(mensaje, "plain")


# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)


if (os.path.isfile(archivo)):
    adjunto = MIMEBase("application", "octet-stream")
    adjunto.set_payload(open(archivo, "rb").read())
    encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(archivo))
    message.attach(adjunto)



# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP("outlook.office365.com", 587) as server:
    server.ehlo()
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )