from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user_email, user_name):
    subject = "¡Gracias por registrarte!"
    message = f"""
    Hola {user_name},

    ¡Gracias por unirte a nuestra plataforma! Estamos emocionados de tenerte aquí.

    Explora nuestras ofertas, productos y mucho más. Si tienes alguna pregunta, no dudes en contactarnos.

    Atentamente,
    El equipo de Tu Ecommerce.
    """
    from_email = settings.EMAIL_HOST_USER  # Usa el correo configurado en settings.py
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)


