from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer
from robots.models import RobotInfo


@receiver(post_save, sender=RobotInfo)
def send_email_to_customers(sender, instance, created, **kwargs):
    if created:
        serial = instance.serial
        customers = Customer.objects.filter(order__robot_serial=serial)
        for customer in customers:
            if not RobotInfo.objects.filter(serial=serial).exclude(pk=instance.pk).exists():
                subject = 'Робот доступен'
                message = (f'Добрый день!\n\nНедавно вы интересовались нашим роботом серийным номером {serial}'
                           f'.\n\nЭтот робот теперь в наличии. Если вам подходит этот вариант'
                           f' - пожалуйста, свяжитесь с нами.')
                from_email = 'noreply@example.com'
                to_email = [customer.email]
                send_mail(subject, message, from_email, to_email)
