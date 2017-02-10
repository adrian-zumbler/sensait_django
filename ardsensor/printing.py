from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.widgets.markers import makeMarker
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from sys import getsizeof
from decimal import Decimal


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

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        style_Normal = styles["Normal"]
        style_Normal.textColor = colors.black

        style_Alerta = styles["Normal"]
        style_Alerta.textColor = colors.black

        style_Title = styles["Heading1"]
        style_Title.alignment = TA_LEFT

        style_Title_Center = styles["Heading1"]
        style_Title_Center.alignment = TA_CENTER

        # Our container for 'Flowable' objects
        elements = []

        # Saltos de linea
        saltosDeLineax1 = Paragraph("<br/>", style_Title)
        saltosDeLineax2 = Paragraph("<br/><br/>", style_Title)
        saltosDeLineax3 = Paragraph("<br/><br/><br/>", style_Title)

        # ps = ParagraphStyle('title', fontSize=20, leading=24)
        #  p1 = "here is some paragraph to see in large font"
        # Paragraph(p1, ps),

        # Primer texto SENSAIT
        elements.append(Paragraph('SENSAIT', style_Title_Center))

        elements.append(saltosDeLineax1)
        # Tipo de Reporte a mostrar...
        elements.append(Paragraph(str(report_instance.get_tipo_reporte_display()) + " del Sensor " + report_instance.sensor.description, style_Title))
        elements.append(saltosDeLineax1)

        # Calculos necesarios para el template
        # Cantidad de Dias del reporte seleccionado.
        difEpochDias = (report_instance.fecha_final - report_instance.fecha_inicial) / 86400
        periodoReporte = "Dia"

        if difEpochDias == 30:
            periodoReporte = "Mensual"
        elif difEpochDias == 15 or difEpochDias == 14:
            periodoReporte = "Quincenal"
        elif difEpochDias == 7 or difEpochDias == 6:
            periodoReporte = "Semanal"
        elif difEpochDias != 1:
            periodoReporte = "Diario"
        else:
            periodoReporte = str(difEpochDias) + " Dia"

        elements.append(Paragraph('Periodo Seleccionado ' + str(periodoReporte), style_Title))
        elements.append(saltosDeLineax1)

        elements.append(Paragraph('Responsable ' + report_instance.sensor.arduino.project.nombre_encargado, style_Title))

        elements.append(saltosDeLineax1)

        elements.append(Paragraph('Este reporte abarca del ' + datetime.fromtimestamp(report_instance.fecha_inicial).strftime('%d/%m/%Y %H:%M:%S') + " al " + datetime.fromtimestamp(report_instance.fecha_final).strftime('%d/%m/%Y %H:%M:%S') + " Siendo creado el " + str(report_instance.created_at), styles['Heading2']))

        elements.append(saltosDeLineax1)

        # Informacion del reporte digamos LEGAL.
        elements.append(Paragraph('La informacion que se despliega a continuacion son propiedad de la empresa que contrata el servicio de SENSAIT. La informacion que se despliega a continuacion son propiedad de la empresa que contrata el servicio de SENSAIT. ', styles['Normal']))

        elements.append(saltosDeLineax2)
        # Informacion del SENSOR DEL REPORTE.
        transmisor_data = []
        data_transmisor = Paragraph('<b>Transmisor:</b><br/>' + report_instance.sensor.arduino.name, style_Normal)
        data_proyecto = Paragraph('<b>Proyecto:</b><br/>' + report_instance.sensor.arduino.project.name, style_Normal)
        data_equipo = Paragraph('<b>Equipo:</b><br/>' + report_instance.sensor.equipment.equipment_name, style_Normal)

        transmisor_data.append((data_transmisor, data_proyecto, data_equipo))

        data_sensor = Paragraph('<b>Sensor:</b><br/>' + report_instance.sensor.description, style_Normal)
        data_sensor_max = Paragraph('<b>Val. Maximo:</b><br/>' + str(report_instance.sensor.max_value), style_Normal)
        data_sensor_min = Paragraph('<b>Val. Minimo:</b><br/>' + str(report_instance.sensor.min_value), style_Normal)

        transmisor_data.append((data_sensor, data_sensor_max, data_sensor_min))

        min_value = report_instance.sensor.min_value
        max_value = report_instance.sensor.max_value

        totalAlertas = 0
        promedioRegistros = 0.0
        totalRegistros = 0

        for num, data in enumerate(report_instance.sensor_data(), start=0):
            if str(data.data) != str("-127.00"):
                totalRegistros = num
                promedioRegistros += float(data.data)
                if float(data.data) > float(max_value) or float(min_value) > float(data.data):
                    totalAlertas += 1

        data_total_registros = Paragraph('<b>Total Registros:</b><br/>' + str(totalRegistros), style_Normal)
        data_registros_alerta = Paragraph('<b>Total Registros fuera de rango:</b><br/>' + str(totalAlertas), style_Normal)
        data_promedio = Paragraph('<b>Temperatura Promedio:</b><br/>' + str(float(promedioRegistros) / float(totalRegistros)), style_Normal)

        transmisor_data.append((data_total_registros, data_registros_alerta, data_promedio))
        transmisor_table = Table(transmisor_data, colWidths=[(doc.width) / 3.0] * 3)
        transmisor_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(transmisor_table)

        elements.append(saltosDeLineax3)
        valores_Correctos = int(totalRegistros - totalAlertas)
        drawing = Drawing(400, 200)
        data = [
            (valores_Correctos, int(totalAlertas))
        ]
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 200
        bc.width = 400
        bc.data = data
        bc.barSpacing = 2.5
        bc.barWidth = 5
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = int(totalRegistros)
        bc.valueAxis.valueStep = 50
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        # bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = ['Correctos = ' + str(valores_Correctos), 'Fuera de Rango = ' + str(totalAlertas)]
        bc.bars[(0, 0)].fillColor = colors.green
        bc.bars[(0, 1)].fillColor = colors.red
        drawing.add(bc)
        elements.append(drawing)

        elements.append(PageBreak())

        # Tabla de ejemplo
        main_table = []
        dataTable_L = []
        dataTable_R = []
        table_data = []

        all_alerts = []
        alert_list = []

        # Cargaremos los titulos de la tabla
        dataTable_L.append(("Fecha y Hora", "Valor Registrado", "Estatus"))
        sensorStatus = "Correcto"
        for num, data in enumerate(report_instance.sensor_data(), start=0):
            if str(data.data) != str("-127.00"):
                if float(data.data) > float(max_value) or float(min_value) > float(data.data):
                    sensorStatus = "Alerta"
                    alert_list.append(data)
                    # print str(len(alert_list)) + " -- " + data.data + " " + str(datetime.fromtimestamp(data.epoch).strftime('%d/%m/%Y %H:%M:%S')) + " " + str(num)

                else:
                    sensorStatus = "Correcto"
                    if len(alert_list) > 0:
                        # print "New List " + str(len(all_alerts))
                        all_alerts.append(list(alert_list))
                        alert_list = []

                dataTable_L.append((datetime.fromtimestamp(data.epoch).strftime('%d/%m/%Y %H:%M:%S'), data.data, sensorStatus))

        table_L = Table(dataTable_L, colWidths=[(doc.width) / 3.0] * 3)
        table_L.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        # table_R = Table(dataTable_R, colWidths=[(doc.width) / 3.0] * 3)
        # table_R.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        # dataTable_Main = [table_L]  table_R
        # table_Main = Table(table_L, colWidths=[doc.width])
        # table_Main.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.red), ('BOX', (0, 0), (-1, -1), 0.25, colors.red)]))

        # Tabla con todos los registros...
        elements.append(Paragraph('ALERTAS REGISTRADAS', style_Title_Center))

        # Tablas POR ALERTA...
        alert_data_tables = []
        alerts_tables = []
        alert_content = []

        # print "all_alerts.len()"
        # print len(all_alerts)

        for num, alertlist in enumerate(all_alerts, start=0):
            # print str(len(alertlist))
            titulo = Paragraph('<b>Alerta # ' + str(num) + ' </b>', style_Normal)
            elements.append(titulo)

            alert_data_tables = []
            alert_content = []
            alert_graph = []
            alert_graph_dates = []

            alerta_primer_registro = Paragraph('<b>Fecha inicio alerta:</b><br/>' + str(datetime.fromtimestamp(alertlist[0].epoch).strftime('%d/%m/%Y %H:%M:%S') + "<br/><br/>"), style_Normal)
            alerta_ultima_registro = Paragraph('<b>Fecha final alerta:</b><br/>' + str(datetime.fromtimestamp(alertlist[len(alertlist) - 1].epoch).strftime('%d/%m/%Y %H:%M:%S') + "<br/><br/>"), style_Normal)
            alerta_total_registros = Paragraph('<b>Registros fuera de rango:</b><br/>' + str(len(alertlist)) + "<br/><br/>", style_Normal)
            rango_maximo = Paragraph('<b>Valor Maximo:</b><br/>' + str(report_instance.sensor.max_value) + "<br/><br/>", style_Normal)
            rango_minimo = Paragraph('<b>Valor Maximo:</b><br/>' + str(report_instance.sensor.min_value) + "<br/><br/>", style_Normal)
            alerta_comentarios = Paragraph("<b>Comentarios:</b><br/>__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br/>", style_Normal)
            alert_content.append(alerta_primer_registro)
            alert_content.append(alerta_ultima_registro)
            alert_content.append(alerta_total_registros)
            alert_content.append(rango_maximo)
            alert_content.append(rango_minimo)
            alert_content.append(alerta_comentarios)
            alert_content.append(saltosDeLineax2)
            valMax = 0
            valMin = 0
            valTmp = 0
            for ids, alert in enumerate(alertlist, start=0):
                # print alert.data
                # datos = Paragraph(str(alert.data), style_Normal)
                valTmp = float(alert.data)
                # print "tmp: " + str(valTmp)
                # print "max: " + str(valMax)
                # print "min: " + str(valMin)
                if float(valTmp) > float(valMax):
                    valMax = valTmp
                    if valMin == 0:
                        valMin = float(valTmp)
                if float(valMin) > float(alert.data):
                    valMin = float(alert.data)
                if float(valMin) > float(valTmp):
                    valMin = float(valTmp)

                valueData = float(alert.data)

                alert_graph.append(valueData)
                alert_graph_dates.append(str(datetime.fromtimestamp(alert.epoch).strftime('%H:%M:%S')))
            # END FOR
            drawing = Drawing(300, 400)
            data = [alert_graph]
            lc = HorizontalLineChart()
            lc.x = 10
            lc.y = 30
            lc.height = 250
            lc.width = 230
            lc.data = data
            lc.joinedLines = 1
            catNames = alert_graph_dates
            lc.categoryAxis.categoryNames = catNames
            lc.categoryAxis.labels.dx = 0
            lc.categoryAxis.labels.dy = -22
            lc.categoryAxis.labels.angle = 60
            lc.categoryAxis.labels.boxAnchor = 'n'
            lc.valueAxis.valueMin = valMin - 2
            lc.valueAxis.valueMax = valMax + 2
            lc.valueAxis.valueStep = 1
            lc.lines[0].strokeWidth = 2
            # lc.lines[1].strokeWidth = 1.5
            drawing.add(lc)

            # print "endFor"

            alert_data_tables.append((alert_content, drawing))
            alerts_tables = Table(alert_data_tables, colWidths=[(doc.width) / 2.0] * 3)
            alerts_tables.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.white)]))
            elements.append(alerts_tables)
            elements.append(PageBreak())

        elements.append(Paragraph('DETALLE DE REGISTROS', style_Title_Center))
        elements.append(table_L)
        # elements.append(table_R)

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
