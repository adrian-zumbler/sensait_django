from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
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
        header = Paragraph(' ', styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - (h - 10))

        # Footer
        footer = Paragraph('REPORTE SENSAIT ', styles['Normal'])
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
                                topMargin=20,
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

        # Tabla con reporte de incidencias y LOGOS.
        titulo_data = []
        titulo_table = []
        logo_cliente = Paragraph('' + report_instance.sensor.arduino.project.enterprise.name, style_Normal)
        titulo_ciente = Paragraph('Reporte de incidencias<br/>Sensor ' + report_instance.sensor.description, style_Title_Center)

        img_sensait = Image("arduino/static/sensait/logos/Sensait_logo.png")
        img_sensait.drawHeight = 8 * mm
        img_sensait.drawWidth = 20 * mm

        titulo_data.append((logo_cliente, titulo_ciente, img_sensait))

        titulo_table = Table(titulo_data, colWidths=(50 * mm, 100 * mm, 50 * mm))
        titulo_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white), ('BOX', (0, 0), (-1, -1), 0.25, colors.white)]))
        elements.append(titulo_table)

        elements.append(saltosDeLineax2)

        resumen_data = []
        resumen_table = []

        resumen_laboratorio = Paragraph('<b>Laboratorio:</b><br/>' + report_instance.sensor.arduino.project.name, style_Normal)
        resumen_equipo = Paragraph('<b>Equipo:</b><br/>' + report_instance.sensor.arduino.name, style_Normal)
        resumen_serie = Paragraph('<b>Modelo:</b><br/>' + report_instance.sensor.arduino.modelo_transmisor, style_Normal)

        resumen_data.append((resumen_laboratorio, resumen_equipo, resumen_serie))

        resumen_periodo = Paragraph('<b>Periodo:</b><br/>' + datetime.fromtimestamp(report_instance.fecha_inicial).strftime('%d/%m/%Y %H:%M:%S') + " al <br/>" + datetime.fromtimestamp(report_instance.fecha_final).strftime('%d/%m/%Y %H:%M:%S'), style_Normal)

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
            periodoReporte = str(difEpochDias) + " dias"
        else:
            periodoReporte = str(difEpochDias) + " Dia"

        resumen_rangodias = Paragraph('<b>Periodo Generado:</b><br/>' + str(periodoReporte), style_Normal)
        resumen_void = Paragraph(" ", style_Normal)

        resumen_data.append((resumen_periodo, resumen_rangodias, resumen_void))

        # resumen_proyecto = Paragraph('<b>Proyecto:</b><br/>' + report_instance.sensor.arduino.project.name, style_Normal)
        # resumen_transmisor = Paragraph('<b>Transmisor:</b><br/>' + report_instance.sensor.arduino.name, style_Normal)
        # resumen_void = Paragraph(" ", style_Normal)

        # resumen_data.append((resumen_proyecto, resumen_transmisor, resumen_void))

        resumen_sensor = Paragraph('<b>Sensor:</b><br/>' + report_instance.sensor.description, style_Normal)
        resumen_valmin = Paragraph('<b>Valor Minimo:</b><br/>' + "%.2f" % report_instance.sensor.min_value, style_Normal)
        resumen_valmax = Paragraph('<b>Valor Maximo:</b><br/>' + "%.2f" % report_instance.sensor.max_value, style_Normal)

        resumen_data.append((resumen_sensor, resumen_valmin, resumen_valmax))

        # VALORES MINIMOS Y MAXIMOS CALCULO.
        min_value = report_instance.sensor.min_value
        max_value = report_instance.sensor.max_value

        totalAlertas = 0
        promedioRegistros = 0.0
        totalRegistros = 0

        valmax = 0
        valmin = 0

        # Tabla de ejemplo
        main_table = []
        dataTable_L = []
        dataTable_R = []
        table_data = []

        all_alerts = []
        alert_list = []

        dataTable_L.append(("Fecha y Hora", "Lectura", "Estado", "Numero incidencia"))
        sensorStatus = "Correcto"


        for num, data in enumerate(report_instance.sensor_data(), start=0):
            if str(data.data) != str("-127.00"):
                totalRegistros = num
                promedioRegistros += float(data.data)
                if num == 0:
                    valmin = float(data.data)
                if float(data.data) > float(max_value) or float(min_value) > float(data.data):
                    sensorStatus = "Fuera de Rango"
                    alert_list.append(data)
                    totalAlertas += 1
                else:
                    sensorStatus = "Correcto"
                    if len(alert_list) > 0:
                        # print "New List " + str(len(all_alerts))
                        all_alerts.append(list(alert_list))
                        alert_list = []

                if float(data.data) > float(valmax):
                    valmax = float(data.data)
                if float(valmin) > float(data.data):
                    valmin = float(data.data)

                if len(alert_list) > 0:
                    alerta_code = "Alerta # " + str(len(all_alerts))
                else:
                    alerta_code = " "

                dataTable_L.append((datetime.fromtimestamp(data.epoch).strftime('%d/%m/%Y %H:%M:%S'), data.data, sensorStatus, alerta_code))

        table_L = Table(dataTable_L, colWidths=[(doc.width) / 4.0] * 4)
        table_L.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        val_promedio = float(promedioRegistros) / float(totalRegistros)

        resumen_promedio = Paragraph('<b>Temperatura Promedio:</b><br/>' + "%.2f" % val_promedio, style_Normal)
        resumen_minima = Paragraph('<b>Temperatura Minimo Registrada:</b><br/>' + "%.2f" % valmin, style_Normal)
        resumen_maxima = Paragraph('<b>Temperatura Maxima Registrada:</b><br/>' + "%.2f" % valmax, style_Normal)

        resumen_data.append((resumen_promedio, resumen_minima, resumen_maxima))

        resumen_totalregistros = Paragraph('<b>Total de Registros:</b><br/>' + "%.2f" % totalRegistros, style_Normal)
        resumen_totalfuera = Paragraph('<b>Resumen Registros:</b><br/>' + "X %.2f" % totalAlertas + "<br/> + %.2f" % (totalRegistros - totalAlertas), style_Normal)
        resumen_alertasregistradas = Paragraph('<b>Total alertas registradas:</b><br/>' + str(len(all_alerts)), style_Normal)
        resumen_void = Paragraph(" ", style_Normal)

        resumen_data.append((resumen_totalregistros, resumen_totalfuera, resumen_alertasregistradas))

        resumen_table = Table(resumen_data, colWidths=[(doc.width) / 3.0] * 3, rowHeights=(16 * mm))
        resumen_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white), ('BOX', (0, 0), (-1, -1), 0.25, colors.white), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        elements.append(resumen_table)

        # Informacion del reporte digamos LEGAL.
        # elements.append(Paragraph('La informacion que se despliega a continuacion son propiedad de la empresa que contrata el servicio de SENSAIT. La informacion que se despliega a continuacion son propiedad de la empresa que contrata el servicio de SENSAIT. ', styles['Normal']))

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

        elements.append(Paragraph('Responsable ' + report_instance.sensor.arduino.project.nombre_encargado, style_Title))

        elements.append(PageBreak())

        # table_R = Table(dataTable_R, colWidths=[(doc.width) / 3.0] * 3)
        # table_R.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        # dataTable_Main = [table_L]  table_R
        # table_Main = Table(table_L, colWidths=[doc.width])
        # table_Main.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.red), ('BOX', (0, 0), (-1, -1), 0.25, colors.red)]))

        # Tabla con todos los registros...
        elements.append(Paragraph(str(len(all_alerts)) + ' ALERTAS REGISTRADAS', style_Title_Center))

        # Tablas POR ALERTA...
        alert_data_tables = []
        alerts_tables = []
        alert_content = []

        alerts_onedata_data = []
        alerts_onedata_table = []
        # print "all_alerts.len()"
        # print len(all_alerts)

        alerts_onedata_data.append(("Fecha Alerta", "# Registros en alerta ", "Valor"))
        alert_max_value = float(report_instance.sensor.max_value)
        alert_min_value = float(report_instance.sensor.min_value)

        for num, alertlist in enumerate(all_alerts, start=0):
            print str(len(alertlist))
            # Esto genera la tabla para un rango de registros NO LO QUITARE jeje
            if len(alertlist) > 200:
                one_fecha = str(datetime.fromtimestamp(alertlist[len(alertlist) - 1].epoch).strftime('%d/%m/%Y %H:%M:%S'))
                one_registros = len(alertlist)
                one_value = str(alertlist[len(alertlist) - 1].data)
                alerts_onedata_data.append((one_fecha, one_registros, one_value))
                # alerts_onedata_data.append( alertlist[num] , drawing))
            else:
                titulo = Paragraph('<b>Alerta # ' + str(num) + ' </b>', style_Normal)

                alert_data_tables = []
                alert_content = []
                alert_graph = []
                alert_limit = []
                alert_graph_dates = []

                alerta_primer_registro = Paragraph('<b>Fecha inicio alerta:</b><br/>' + str(datetime.fromtimestamp(alertlist[0].epoch).strftime('%d/%m/%Y %H:%M:%S') + "<br/><br/>"), style_Normal)
                alerta_ultima_registro = Paragraph('<b>Fecha final alerta:</b><br/>' + str(datetime.fromtimestamp(alertlist[len(alertlist) - 1].epoch).strftime('%d/%m/%Y %H:%M:%S') + "<br/><br/>"), style_Normal)
                tiempoAlerta = alertlist[len(alertlist) - 1].epoch - alertlist[0].epoch

                alerta_duracion = Paragraph('<b>Duracion alerta:</b><br/>' + str(datetime.fromtimestamp(tiempoAlerta).strftime('%M:%S') + "<br/><br/>"), style_Normal)
                alerta_total_registros = Paragraph('<b>Registros fuera de rango:</b><br/>' + str(len(alertlist)) + "<br/><br/>", style_Normal)
                rango_maximo = Paragraph('<b>Valor Maximo:</b><br/>' + "%.2f" % report_instance.sensor.max_value + "<br/><br/>", style_Normal)
                rango_minimo = Paragraph('<b>Valor Maximo:</b><br/>' + "%.2f" % report_instance.sensor.min_value + "<br/><br/>", style_Normal)
                alerta_comentarios = Paragraph("<b>Comentarios:</b><br/>__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br/>", style_Normal)
                alerta_accioncorrectiva = Paragraph("<b>Accion correctiva:</b><br/>__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br/>", style_Normal)

                alerta_data = []
                alerta_table = []

                alerta_data.append((titulo, " "))
                alerta_data.append((alerta_primer_registro, alerta_ultima_registro))
                alerta_data.append((alerta_duracion, alerta_total_registros))
                alerta_data.append((rango_maximo, rango_minimo))
                alerta_data.append((" ", saltosDeLineax2))
                # alerta_data.append((alerta_comentarios))

                alerta_table = Table(alerta_data, colWidths=(50 * mm, 50 * mm))
                alerta_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white), ('BOX', (0, 0), (-1, -1), 0.25, colors.white)]))

                # alert_content.append(alerta_primer_registro)
                # alert_content.append(alerta_ultima_registro)
                # alert_content.append(alerta_duracion)
                # alert_content.append(alerta_total_registros)
                # alert_content.append(rango_maximo)
                # alert_content.append(rango_minimo)
                # alert_content.append(alerta_comentarios)
                # alert_content.append(saltosDeLineax2)
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
                    alert_limit.append(alert_max_value)
                    alert_graph_dates.append(str(datetime.fromtimestamp(alert.epoch).strftime('%H:%M:%S')))
                # END FOR
                drawing = Drawing(200, 220)
                data = [alert_graph, alert_limit]
                lc = HorizontalLineChart()
                lc.x = 10
                lc.y = 30
                lc.height = 150
                lc.width = 220
                lc.data = data
                # lc.strokeColor = colors.black
                catNames = alert_graph_dates
                lc.categoryAxis.categoryNames = catNames
                lc.categoryAxis.labels.dx = 0
                lc.categoryAxis.labels.dy = -15
                lc.categoryAxis.labels.angle = 75
                lc.categoryAxis.labels.boxAnchor = 'n'
                lc.joinedLines = 1
                lc.lines[0].symbol = makeMarker('FilledCircle')
                # lc.lineLabelFormat = '%2.0f'
                # lc.strokeColor = colors.black
                lc.valueAxis.valueMin = alert_max_value - 1
                lc.valueAxis.valueMax = valMax + 2
                lc.valueAxis.valueStep = 1
                lc.lines[0].strokeWidth = 2
                # lc.lines[1].strokeWidth = 1.5
                drawing.add(lc)

                # print "endFor"

                alert_data_tables.append((drawing, alerta_table))
                alert_data_tables.append((alerta_comentarios, alerta_accioncorrectiva))

                alerts_tables = Table(alert_data_tables, colWidths=[(doc.width) / 2.0] * 2)
                alerts_tables.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white), ('BOX', (0, 0), (-1, -1), 0.25, colors.white)]))
                elements.append(alerts_tables)

                # elements.append(PageBreak())

        if len(alerts_onedata_data) > 1:

            elements.append(Paragraph('ALERTAS CON 5 REGISTROS O MENOS', style_Title_Center))
            elements.append(saltosDeLineax1)
            alerts_onedata_table = Table(alerts_onedata_data, colWidths=[(doc.width) / 3.0] * 3)
            alerts_onedata_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
            elements.append(alerts_onedata_table)
            # elements.append(PageBreak())

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
