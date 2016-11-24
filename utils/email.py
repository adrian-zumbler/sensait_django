from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from arduino.models import SensorData

s_data = SensorData.objects.get(id=18112)


plaintext = get_template('utils/email/alerta_rango.txt')
htmly = get_template('utils/email/alerta_rango.html')

d = Context({ 'username': 'my user' })

subject, from_email, to = 'hello', 'alertas@esensait.com', 'olimpuz@gmail.com'
text_content = plaintext.render(d)
html_content = htmly.render(d)
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")


def send_message(msg):
    msg.send()
