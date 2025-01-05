from rest_framework import serializers
from django.contrib.auth.models import User
from fitFinders.models import FitFinder
from fitMakers.models import FitMaker


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(choices=[('fitFinder', 'Fit Finder'), ('fitMaker', 'Fit Maker')], required=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'user_type']

    def save(self):
        username = self.validated_data['username']    
        email = self.validated_data['email']    
        first_name = self.validated_data['first_name']    
        last_name = self.validated_data['last_name']    
        password = self.validated_data['password']    
        confirm_password = self.validated_data['confirm_password']     
        user_type = self.validated_data['user_type']     

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email already exists"})

        if password != confirm_password:
            raise serializers.ValidationError({'error' : "Password doesn't Matched"})
        
        account = User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password) 
        account.is_active = False

        if user_type == 'fitMaker': 
            account.is_staff = True
        else: 
            account.is_staff = False
            
        account.save()

        if user_type == 'fitMaker':
            FitMaker.objects.create(user = account) 
        else: 
            FitFinder.objects.create(user = account)

        return account

    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)