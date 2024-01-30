import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.config import settings


smtp_server = settings.SMTP_SERVER
smtp_port = settings.SMTP_PORT
smtp_use_ssl = True

from_address = settings.EMAIL_ADDRESS
password = settings.PASSWORD_EMAIL

SECRET_KEY = settings.SECRET_KEY_EMAIL
ALGORITHM = settings.ALGORITHM_EMAIL


def send_confirmation_email(email: str, confirmation_token: str):
    to_address = email
    subject = "Confirma tu cuenta"

    link = settings.USERS_LOCALHOST + "api/confirm/?token=" + confirmation_token
    html_content = (f"Click <a href={link}>here</a> to "
                    f"confirm your registration.")
    html_message = MIMEText(html_content, "html")

    msg = MIMEMultipart()
    msg.attach(html_message)

    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject

    try:
        if smtp_use_ssl:
            smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            smtp = smtplib.SMTP(smtp_server, smtp_port)

        smtp.login(from_address, password)

        smtp.sendmail(from_address, to_address, msg.as_string())

    except Exception as e:
        print("Hubo un error al enviar el correo:", str(e))

    finally:
        smtp.quit()


def create_confirmation_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
