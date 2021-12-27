from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import MyCampaign, MyAdset, MyAdCreative


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MyCampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyCampaign
        fields = ['id', 'name', 'objective']


class MyAdsetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyAdset
        fields = ['id', 'name', 'campaign_id', 'lifetime_budget', 'daily_budget', 'start_time', 'end_time',
                  'targeting', 'bid_amount', 'status', 'optimization_goal']


class MyAdCreativeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyAdCreative
        fields = ['id', 'name', 'object_story_spec']
