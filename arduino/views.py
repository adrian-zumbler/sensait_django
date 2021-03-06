# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime

from django.http import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from django.db.models.query import QuerySet
from arduino.serializers import (ArduinoSerializer, SensorTypeSerializer,
                                 ArduinoSensorSerializer, SensorDataSerializer)
from arduino.permissions import isArduinoPermission
from arduino.models import Arduino, SensorType, SensorEquipment, AlertObservation
from .forms import SensorTypeForm, SensorEquipmentForm, AlertObservationForm
from .exceptions import StandardAPIException

from urlparse import parse_qsl

from channels import Channel


def parse_qs(qs, keep_blank_values=0, strict_parsing=0):
    dict = {}
    for name, value in parse_qsl(qs, keep_blank_values, strict_parsing):
        dict[name] = value
    return dict


class ArduinoViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ArduinoSerializer
    permission_classes = (IsAuthenticated, )
    queryset = serializer_class.Meta.model.objects.all()

    def get_queryset(self, arduino_pk=None):
        queryset = self.queryset
        # if isinstance(queryset, QuerySet):
        #     # Ensure queryset is re-evaluated on each request.
        #     queryset = queryset.filter(arduino__pk=arduino_pk)
        # TODO: Filter arduino per user
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class SensorViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = SensorTypeSerializer
    permission_classes = (IsAuthenticated, )
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, request, *args, **kwargs):
        return super(SensorViewSet, self).list(request, *args, **kwargs)


class ArduinoSensorViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = ArduinoSensorSerializer
    permission_classes = (IsAuthenticated, )
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, request, arduino_pk, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(arduino_pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, arduino_pk=None):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(arduino__pk=arduino_pk)
        return queryset


class ArduinoDataViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = SensorDataSerializer
    permission_classes = (IsAuthenticated, )
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, request, arduino_pk, *args, **kwargs):
        arduino = Arduino.objects.get(pk=arduino_pk)
        sensors = arduino.arduino_sensors.all()
        ret = []
        for sensor in sensors:
            queryset = self.filter_queryset(self.get_queryset(sensor.pk))

            serializer = self.get_serializer(queryset, many=True)
            ret.append({'sensor': sensor.id, 'data': serializer.data})
        return Response(ret)

    def get_queryset(self, sensor_pk=None):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(arduino_sensor__pk=sensor_pk)
        min_time = self.request.query_params.get('min_time', None)
        if min_time is not None:
            queryset = queryset.filter(created_at__gt=min_time)
        return queryset


class SensorDataViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = SensorDataSerializer
    permission_classes = (IsAuthenticated, )
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, request, arduino_pk, sensor_pk, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(sensor_pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, sensor_pk=None):
        queryset = self.queryset

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(
                arduino_sensor__pk=sensor_pk
            ).order_by('epoch')
        if not queryset:
            return queryset

        # TODO: Add exceptions for integer types
        min_time = self.request.query_params.get('min_time', None)

        max_time = self.request.query_params.get('max_time', None)

        last = self.request.query_params.get('last', None)

        first = self.request.query_params.get('first', None)

        if min_time is not None:
            # min_time = datetime.strptime(min_time, '%Y-%m-%d %H:%M:%S')
            queryset = queryset.filter(epoch__gte=int(min_time))
        if max_time is not None:
            # max_time = datetime.strptime(max_time, '%Y-%m-%d %H:%M:%S')
            queryset = queryset.filter(epoch__lte=int(max_time))
        if last is not None:
            length = len(queryset)
            cutoff = length - int(last)
            if cutoff > 0:
                queryset = queryset[cutoff:]
        if first is not None:
            queryset = queryset[:int(first)]
        return queryset

    def paginate_queryset(self, queryset):
        return super(SensorDataViewSet, self).paginate_queryset(queryset)


class DataViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = SensorDataSerializer
    permission_classes = (isArduinoPermission, )
    queryset = serializer_class.Meta.model.objects.all()

    def initialize_request(self, request, *args, **kwargs):
        request = super(DataViewSet, self).initialize_request(request, *args, **kwargs)
        try:
            request.arduino = Arduino.objects.get(arduino_token=request.META['HTTP_X_ARDUINOTOKEN'])
        except Exception:
            pass
        return request

    def create(self, request, *args, **kwargs):

        sensors = request.arduino.arduino_sensors.all()
        ret = []

        try:
            request_data = request.data.copy()
            epoch = int(request_data.pop('field1')[0])
        except Exception as exc:
            print(exc)
            request_data = parse_qs(request.body)
            epoch = request_data.pop('field1')

        if epoch < int(time.time()) - 200:
            epoch += 18000

        for k in request_data:
            a_sensor = sensors.filter(data_key=k)
            if not a_sensor:
                detail = 'No se tiene registrado el sensor %s en el administrador' % k
                raise StandardAPIException(detail=detail)
            data = {
                'arduino_sensor': a_sensor,
                'data': request_data[k],
                'epoch': epoch
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            ret.append(serializer.data)
        self.publish_data(request, ret)
        return Response({'message': 'data created'}, status=status.HTTP_201_CREATED)

    @staticmethod
    def publish_data(request, ret):
        Channel('arduino-alert').send({
            'data_list': json.dumps(ret)
        })
        Channel("arduino-state").send({
            "arduino_token": request.arduino.arduino_token,
            "state": json.dumps(ret),
        })


class BulkDataViewSet(DataViewSet):
    @staticmethod
    def publish_data(request, ret):
        pass


class AdminSensorTypeListView(LoginRequiredMixin, ListView):
    template_name = 'admin/admin_sensorType_list.html'
    queryset = SensorType.objects.all()


class AdminSensorTypeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/admin_sensorType_edit.html'
    form_class = SensorTypeForm
    success_url = reverse_lazy('sensorTypeList')


class AdminSensorTypeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_sensorType_detail.html'
    queryset = SensorType.objects.all()


class AdminSensorTypeEditView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/admin_sensorType_edit.html'
    form_class = SensorTypeForm
    queryset = SensorType.objects.all()
    success_url = reverse_lazy('sensorTypeList')


class AdminSensorTypeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_sensorType_delete.html'
    success_url = reverse_lazy('sensorTypeList')
    queryset = SensorType.objects.all()


# ALERTA Observacion
class AdminAlertObservationListView(LoginRequiredMixin, ListView):
    template_name = 'admin/admin_alertObservation_list.html'
    queryset = AlertObservation.objects.all()


class AdminAlertObservationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/admin_alertObservation_edit.html'
    form_class = AlertObservationForm
    success_url = reverse_lazy('alertObservationList')


class AdminAlertObservationDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_alertObservation_detail.html'
    queryset = AlertObservation.objects.all()


class AdminAlertObservationEditView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/admin_alertObservation_edit.html'
    form_class = AlertObservationForm
    queryset = AlertObservation.objects.all()
    success_url = reverse_lazy('alertObservationList')


class AdminAlertObservationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_alertObservation_delete.html'
    success_url = reverse_lazy('alertObservationList')
    queryset = AlertObservation.objects.all()


# SENSOR EQUIPMENT


class AdminSensorEquipmentListView(LoginRequiredMixin, ListView):
    template_name = 'admin/admin_sensorEquipment_list.html'
    queryset = SensorEquipment.objects.all()


class AdminSensorEquipmentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/admin_sensorEquipment_edit.html'
    form_class = SensorEquipmentForm
    success_url = reverse_lazy('sensorEquipmentList')


class AdminSensorEquipmentDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_sensorEquipment_detail.html'
    queryset = SensorEquipment.objects.all()


class AdminSensorEquipmentEditView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/admin_sensorEquipment_edit.html'
    form_class = SensorEquipmentForm
    queryset = SensorEquipment.objects.all()
    success_url = reverse_lazy('sensorEquipmentList')


class AdminSensorEquipmentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_sensorEquipment_delete.html'
    success_url = reverse_lazy('sensorEquipmentList')
    queryset = SensorEquipment.objects.all()


class AdminArduinoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_arduino_detail.html'
    queryset = Arduino.objects.all()


class AdminArduinoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_arduino_delete.html'
    success_url = reverse_lazy('projectsDetail')
    queryset = Arduino.objects.all()
