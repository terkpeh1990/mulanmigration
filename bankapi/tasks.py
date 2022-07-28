from celery.utils.log import get_task_logger
from celery import shared_task
from django.conf import settings
from school_management_system.celery import app
from school_management_system.settings import mulan_sender_id,endPoint,apiKey
import requests
from school.models import Students
import sys


logger = get_task_logger(__name__)

@shared_task(name="send_notification_alert")
def send_notification_alert(amount,student,balance):
    logger.info("Creating the task..")
    student = Students.objects.get(id=student)

    father_no = student.parent_id.father_phone


    mother_no = student.parent_id.mother_phone
    try:
        message = "Dear Parent" +",\n\nPayment Notification Details:"+ "\n\nAmount Paid : "+ "GHC" +" " + str(amount) + "\nStudent Name : "+student.Surname + " "+ student.firstname+"\nOutsanding Fees : "+ str(balance)+"\n\nThank you for choosing Mulan Smart Educational Center"
        sender_id= mulan_sender_id
        url = endPoint + '?key=' + apiKey
        response = requests.post(url+'&to='+father_no +'&msg='+message+'&sender_id='+sender_id)

        data = response.json()

        print(data)
    except:
        print(sys.exc_info()[0])
        return False
    try:
        message = "Dear Parent" + ",\n\nPayment Notification Details:"+ "\n\nAmount Paid : "+ "GHC" +" " + str(amount) + "\nStudent Name : "+student.Surname + " "+ student.firstname+"\nOutsanding Fees : "+ str(balance)+"\n\nThank you for choosing Mulan Smart Educational Center"
        sender_id= mulan_sender_id
        url = endPoint + '?key=' + apiKey
        response = requests.post(url+'&to='+mother_no +'&msg='+message+'&sender_id='+sender_id)

        data = response.json()



        print(data)
    except IOError:
        print(sys.exc_info()[0])
        return False

    logger.info("Finishing task..")