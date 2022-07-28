from rest_framework import serializers
from accounts.models import Account_Receivable,School_Bank_payments
from school.models import Students



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields=('id','Surname','firstname')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model =School_Bank_payments
        exclude = ['transaction_date','balance']

class PaymentSucessSerializer(serializers.ModelSerializer):
    class Meta:
        model =School_Bank_payments
        exclude = '__all__'
