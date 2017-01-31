from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from sys import getsizeof


class ReportPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('REPORTE SENSAIT - HEADER.', styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - (h - 10))

        # Footer
        footer = Paragraph('REPORTE SENSAIT - FOOTER   ', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    def print_users(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=50,
                                leftMargin=50,
                                topMargin=60,
                                bottomMargin=50,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = User.objects.all()
        elements.append(Paragraph('My User Names', styles['Heading1']))
        for i, user in enumerate(users):
            elements.append(Paragraph('user id: %d' % user.id, styles['Normal']))

        # for data in report_instance.sensor_data():
            # elements.append(Paragraph('Fecha : %s, Valor: %s' % (datetime.fromtimestamp(data.epoch).strftime('%d/%m/%Y %H:%M:%S'), data.data), styles['Normal']))

        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        # pdf = buffer.getvalue()
        # buffer.close()
        # return pdf

    def print_sensor_data(self, report_instance):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=50,
                                leftMargin=50,
                                topMargin=60,
                                bottomMargin=50,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Titulo de la seccion
        elements.append(Paragraph('Reporte get Tipo de re' + str(report_instance.tipo_reporte), styles['Heading1']))

        elements.append(Paragraph('El siguiente reporte abarca el periodo de tiempo de: ' + datetime.fromtimestamp(report_instance.fecha_inicial).strftime('%d/%m/%Y %H:%M:%S') + " al " + datetime.fromtimestamp(report_instance.fecha_final).strftime('%d/%m/%Y %H:%M:%S'), styles['Heading2']))

        elements.append(Paragraph('La informacion que se despliega a continuacion son propiedad de la empresa que contrata el servicio de SENSAIT.', styles['Normal']))

        elements.append(Paragraph('Transmisor' + report_instance.sensor.arduino.name, styles['Normal']))

        elements.append(Paragraph('Projecto' + report_instance.sensor.arduino.project.name, styles['Normal']))

        elements.append(Paragraph('Valor Minimo' + str(report_instance.sensor.min_value), styles['Normal']))

        elements.append(Paragraph('Valor Maximo' + str(report_instance.sensor.max_value), styles['Normal']))

        elements.append(Paragraph('Descripcion' + report_instance.sensor.description, styles['Normal']))

        elements.append(Paragraph('Equipo' + report_instance.sensor.equipment.equipment_name, styles['Normal']))

        elements.append(Paragraph('Encargado' + report_instance.sensor.arduino.project.nombre_encargado, styles['Normal']))

        min_value = report_instance.sensor.min_value
        max_value = report_instance.sensor.max_value
        totalAlertas = 0
        promedioRegistros = 0.0
        totalRegistros = 0

        for num, data in enumerate(report_instance.sensor_data(), start=0):
            totalRegistros = num
            promedioRegistros += float(data.data)
            if float(data.data) > float(max_value) or float(min_value) > float(data.data):
                totalAlertas += 1

        elements.append(Paragraph('Promedio' + str(promedioRegistros / totalRegistros), styles['Normal']))
        elements.append(Paragraph('Total Registros' + str(totalRegistros), styles['Normal']))
        elements.append(Paragraph('Total Alertas' + str(totalAlertas), styles['Normal']))



        # Tabla de ejemplo
        main_table = []
        dataTable_L = []
        dataTable_R = []
        table_data = []

        # Creamos la MAIN tabla para poner todos los registros.

        # Cargaremos los titulos de la tabla
        table_data.append(("Fecha y Hora", "Valor Registrado", "Estatus"))
        sensorStatus = "Correcto"
        for num, data in enumerate(report_instance.sensor_data(), start=0):
            if float(data.data) > float(max_value) or float(min_value) > float(data.data):
                sensorStatus = "Alerta"
            else:
                sensorStatus = "Correcto"
            if num % 2 == 0:
                dataTable_L.append((datetime.fromtimestamp(data.epoch).strftime('%d/%m/%Y %H:%M:%S'), data.data, sensorStatus))
            else:
                dataTable_R.append((datetime.fromtimestamp(data.epoch).strftime('%d/%m/%Y %H:%M:%S'), data.data, sensorStatus))

        if len(dataTable_L) > len(dataTable_R):
            total = len(dataTable_L) - len(dataTable_R)
            print total
            for data in range(0, total):
                dataTable_R.append(("", "", ""))

        if len(dataTable_R) > len(dataTable_L):
            total = len(dataTable_R) - len(dataTable_L)
            for data in range(0, total):
                dataTable_L.append(("", "", ""))

        table_L = Table(dataTable_L, colWidths=[(doc.width) / 3.0] * 3)
        table_L.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        table_R = Table(dataTable_R, colWidths=[(doc.width) / 3.0] * 3)
        table_R.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        dataTable_Main = [[table_L, table_R]]
        table_Main = Table(dataTable_Main, colWidths=[doc.width])
        table_Main.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.red), ('BOX', (0, 0), (-1, -1), 0.25, colors.red)]))

        elements.append(table_L)
        elements.append(table_R)

        # Se agrega el llamado del header y footer
        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)


# Clase para agregar los numeros de las paginas.
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 5 * mm + (0.2 * inch),
                             "Pagina %d de %d" % (self._pageNumber, page_count))
