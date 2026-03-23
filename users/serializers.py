from rest_framework import serializers
from users.models import User, UserProfile
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(source='profile.profile_image', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone', 'profile_image', 'bio']
        read_only_fields = ['email']
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        profile, created = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        instance.refresh_from_db()
        return instance
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only = True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone', 'profile', 'is_staff']
class UserCreateSerializers(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'address', 'phone', 'password')