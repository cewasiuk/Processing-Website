from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import ProcessingRequest


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessingRequest
        fields = ['company_name', 'sales_PIC', 'engineer_PIC', 'track_num_in', 'track_num_out', 'process_date', 'quantity', 'material_1', 'grind_request', 'dicing_request']

