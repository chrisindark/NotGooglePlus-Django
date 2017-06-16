

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework.exceptions import ValidationError
from django.conf import settings
from api.utility import webutil, ewoauthorization, appConstants
from api.utility.awsutility import AwsUtility
from api.models.all import Employee, Tenant, TenantContact, Vendor, VendorContact
# from uuid import uuid4
# import boto3

# class EmployeePhotoUploadSignature(APIView):
#     """
#     Provided the S3 file Upload URL and AWS verification data
#     """
#     def get(self, request):
#         """
#         Verification with AWS S3 file storage
#         """
#         file_name = request.query_params.get('name')
#         file_type = request.query_params.get('type')
#         company_id = request.query_params.get('company')

#         awsutility = AwsUtility(aws_path=appConstants.S3_EMPLOYEE_PHOTO)

#         employee = webutil.get_company_employee(request=None)
#         if request.user.is_superuser:
#             pass
#         elif employee is None or employee.company.id != company_id:
#             raise ValidationError('You are not a valid user to access this resource.')

#         presigned_data = awsutility.getpresigneddata(company_id, request, file_name, file_type)
#         return Response(presigned_data)


class S3FileSignature(APIView):
    """
    Provides the S3 file Upload URL and AWS verification data
    """
    def get(self, request):
        """
        Verification with AWS S3 file storage
        """
        file_name = request.query_params.get('name')
        file_type = request.query_params.get('type')
        related_id = request.query_params.get('rid')
        entity_type = request.query_params.get('etype')
        is_doc = True if request.query_params.get('isdoc') is not None else False
        awsutility = None
        if not self._isvalidrequest(request):
            raise ValidationError('Not a valide request.')
        if entity_type == 'tc':
            if is_doc:
                awsutility = AwsUtility(aws_path=appConstants.S3_TENANT_DOCUMENT)
            else:
                awsutility = AwsUtility(aws_path=appConstants.S3_TENANT_CONTACT_PHOTO)
        elif entity_type == 'vc':
            if is_doc:
                awsutility = AwsUtility(aws_path=appConstants.S3_VENDOR_DOCUMENT)
            else:
                awsutility = AwsUtility(aws_path=appConstants.S3_VENDOR_CONTACT_PHOTO)
        elif entity_type == 'emp':
            awsutility = AwsUtility(aws_path=appConstants.S3_EMPLOYEE_PHOTO)

        presigned_data = awsutility.getpresigneddata(related_id, request, file_name, file_type)
        return Response(presigned_data)


    def _isvalidrequest(self, request):
        entity_type = request.query_params.get('etype')
        related_id = request.query_params.get('rid')
        if entity_type == 'tc':
            pass
        elif entity_type == 'vc':
            pass
        elif entity_type == 'emp':
            employee = webutil.get_company_employee(request=None)
            if request.user.is_superuser:
                pass
            elif employee is None or employee.company.id != related_id:
                raise ValidationError('You are not a valid user to access this resource.')
        else:
            raise ValidationError('Invalide request option, etype is not defined.')

        return True
