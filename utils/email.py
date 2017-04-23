from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from arduino.models import SensorData, ArduinoAlert

from django.views.generic import DetailView

# s_data = SensorData.objects.get(id=18112)

plaintext = get_template('utils/email/alerta_rango.txt')
htmly = get_template('utils/email/alerta_rango.html')

d = Context({'username': 'my user'})
# d = Context({'site_url': self.request.get_host()})


subject, from_email, to = 'Alerta Sensait - Su equipo (NombreDelRefrigerado) salio del rango de terperatura de operacion.', 'alertas@sensait.com', 'olimpuz@gmail.com,direccion@corporativobit.com'

text_content = plaintext.render({'username': 'my user'})
html_content = htmly.render({'username': 'my user'})
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")


def send_message(msg):
    msg.send()


class EmailView(DetailView):
    template_name = 'utils/email/alerta_rango.html'
    model = ArduinoAlert
