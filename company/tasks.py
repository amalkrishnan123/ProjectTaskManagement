from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_employee_credentials(email, password):
    
    try:
        subject = 'Your Login Credentials'
        message = f"""
        Dear User,

        Your account has been created successfully.

        Username: {email}
        Password: {password}

        Please log in and change your password after first login.

        Regards,
        Admin Team
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,   # Admin email
            [email],                    # Employee email
            fail_silently=False,
        )

    except Exception as e:
        return f"error:{str(e)}"