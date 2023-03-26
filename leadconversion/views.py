import datetime

from django.contrib.auth.forms import SetPasswordForm
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
# from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken

from .models import Product, Customer, Lead, UserRole
from .serializers import LeadSerializer, CustomerSerializer, ProductSerializer, UserRoleSerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.get_all()
    serializer_class = LeadSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        if request.user.userrole.role != 'lead-creator':
            return Response({'message': 'This role is not authorized to create leads,', 'status': 403},
                            status=status.HTTP_403_FORBIDDEN)
        if "id" in request.data:
            if request.data["id"] not in [0, "0"]:
                lead = Lead.get_id(request.data["id"])
            else:
                lead = Lead()
        else:
            lead = Lead()
        lead.created_by = request.user.userrole
        lead.first_name = request.data['first_name']
        lead.middle_name = request.data['middle_name']
        lead.last_name = request.data['last_name']
        lead.phone_number = request.data['phone_number']
        lead.location = request.data['location']
        lead.gender = request.data['gender']
        lead.save()
        leads = LeadSerializer(Lead.get_all(), many=True)
        return Response({'message': 'Lead created successfully!', "leads_data":leads.data}, status=status.HTTP_200_OK)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.get_all()
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if request.user.userrole.role != 'customer-creator':
            return Response({'message': 'This role is not authorized to create customers,', 'status': 403},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            print(request.data)
            if "id" in request.data:
                if request.data["id"] not in [0, "0"]:
                    customer = Customer.get_id(request.data["id"])
                else:
                    customer = Customer()
            else:
                customer = Customer()
            customer.lead = Lead.get_id(request.data['lead_id'])
            customer.created_by = request.user.userrole
            customer.annual_earning = request.data['annual_earning']
            # customer.photo = request.data['photo']
            customer.save()
            customer.products_of_interest.set([])
            for product in request.data['products_of_interest']:
                customer.products_of_interest.add(Product.get_id(product))
            customers = CustomerSerializer(Customer.get_all(), many=True)
            leads = LeadSerializer(Lead.get_all(), many=True)
            return Response({'message': 'Customer created successfully', "customers_data":customers.data, "leads_data":leads.data}, status=status.HTTP_200_OK)
        except Exception as err:
            message = err.args[0]
            if err.args[0] == 'UNIQUE constraint failed: leadconversion_customer.lead_id':
                message = "A lead with this lead_id already exists, try another lead"
            return Response({"message": message, "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.get_all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

class UserRoleAuth(viewsets.ModelViewSet):
    queryset = UserRole.get_all()
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        print(request.user)

        user_data = UserRoleSerializer(request.user.userrole)
        leads_data=LeadSerializer(Lead.get_all(),many=True)
        product_data = ProductSerializer(Product.get_all(), many=True)

        return Response(
            {
                "message":"User Retrieved successfuly",
                "user_data":user_data.data,
                "leads_data":leads_data.data,
                "product_data":product_data.data,
                "status": 200
            }, status=status.HTTP_200_OK
        )

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.get_all()
    serializer_class = UserRoleSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            user = UserRole.objects.create(
                username=request.data['username'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email=request.data['email'],
                role=request.data["userrole"]
            )
            set_password = SetPasswordForm(user)
            set_password.cleaned_data = {"new_password1": request.data["password"],
                                         "new_password2": request.data["password"]}
            set_password.save()
            return Response({"message": "User created successfully", "status": 200}, status=status.HTTP_200_OK)
        except Exception as err:
            message = err.args[0]
            if err.args[0] == 'UNIQUE constraint failed: auth_user.username':
                message = "Username is taken. Please select another username"
            return Response({"message": message, "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        return Response({'message':"You're not authorized to perform this task","status":403}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        return Response({'message':"You're not authorized to perform this task","status":403}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        return Response({'message':"You're not authorized to perform this task","status":403}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response({'message':"You're not authorized to perform this task","status":403}, status=status.HTTP_403_FORBIDDEN)

# class CustomObtainAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         re
#         # return Response({'token': token.key, 'spswkid':encrypt_token(UserRoleSerializer(user).data)})
