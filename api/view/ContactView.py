from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json

def contact_us(request):
    if request.method == "POST":
        try:
            # Decodificar el cuerpo de la solicitud JSON
            data = json.loads(request.body)
            full_name = data.get("full_name")  # Nombre completo del usuario
            email = data.get("email")  # Correo electrónico del usuario
            subject = data.get("subject")  # Asunto del mensaje
            message = data.get("message")  # Contenido del mensaje

            # Validación de campos obligatorios
            if not all([full_name, email, subject, message]):
                return JsonResponse({"error": "Todos los campos son obligatorios."}, status=400)

            # Formatear el contenido del correo
            email_subject = f"Mensaje de Contacto: {subject}"
            email_message = f"""
            Nombre completo: {full_name}
            Correo electrónico: {email}

            Mensaje:
            {message}
            """

            # Enviar el correo
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,  # Remitente (de settings.py)
                ["rauledmore98@outlook.com"],  # Destinatario
                fail_silently=False,
            )

            # Respuesta de éxito
            return JsonResponse({"message": "Correo enviado exitosamente."})
        except Exception as e:
            # Manejo de errores
            return JsonResponse({"error": f"Se produjo un error: {str(e)}"}, status=500)
    else:
        # Respuesta para métodos que no sean POST
        return JsonResponse({"error": "Método no permitido."}, status=405)