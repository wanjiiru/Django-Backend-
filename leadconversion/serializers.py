from rest_framework import serializers

from .models import Lead, Product,UserRole, Customer


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "location",
            "gender",
            "date_created",
            "created_by",
            "customer"
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            '__all__'
        )


class CustomerSerializer(serializers.ModelSerializer):
    lead=LeadSerializer(many=False,)
    products_of_interest=ProductSerializer(many=True,)

    class Meta:
        model = Customer
        fields = (
            '__all__'
        )

class UserRoleSerializer(serializers.ModelSerializer):
    leads = LeadSerializer(many=True, )
    customers = CustomerSerializer(many=True, )
    # role = serializers.SerializerMethodField('get_alternate_name')

    class Meta:
        model = UserRole
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'leads','customers','role')
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'required': True},
        }

    def get_alternate_name(self,obj):
        return obj.get_role_display()
