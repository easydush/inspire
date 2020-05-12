from rest_framework import serializers

from main.models import Company


class CompanySerializer(serializers.ModelSerializer):

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.save()
    #     return instance
    #
    # def create(self, validated_data):
    #     return Company.objects.create(**validated_data)

    class Meta:
        model = Company
        fields = '__all__'
