from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse

class ContactUsView(APIView):
    @extend_schema(
        summary="Enviar mensaje de contacto",
        description="Permite a los usuarios enviar un mensaje a través del formulario de contacto.",
        request={
            "application/json": {
                "example": {
                    "full_name": "John Doe",
                    "email": "johndoe@example.com",
                    "subject": "Consulta sobre productos",
                    "message": "Hola, me gustaría saber más sobre sus productos."
                }
            }
        },
        responses={
            200: JsonResponse({"message": "Correo enviado exitosamente."}),
            400: JsonResponse({"error": "Todos los campos son obligatorios."}),
            500: JsonResponse({"error": "Se produjo un error inesperado."}),
        },
    )
    def post(self, request):
        """
        API para enviar un mensaje de contacto.
        """
        data = request.data
        full_name = data.get("full_name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        if not all([full_name, email, subject, message]):
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        email_subject = f"Mensaje de Contacto: {subject}"
        email_message = f"""
        Nombre completo: {full_name}
        Correo electrónico: {email}

        Mensaje:
        {message}
        """

        send_mail(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ["rauledmore98@outlook.com"],
            fail_silently=False,
        )

        return Response({"message": "Correo enviado exitosamente."}, status=status.HTTP_200_OK)
