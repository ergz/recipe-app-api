"""Serialiazers to Users API View"""


from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User object"""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update and return user"""

        # grab password from data and remove it from data
        password = validated_data.pop("password", None)

        # call super() so that we can use the update method of the superset class
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the User auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input-type": "password"}, 
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validate and authenticate the user"""

        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user 
        return attrs

