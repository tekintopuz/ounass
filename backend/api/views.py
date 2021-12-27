import os
import pprint

import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.utils import timezone
from django.views import View
from dotenv import load_dotenv
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from requests.structures import CaseInsensitiveDict
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from api.models import MyCampaign, MyAdset, MyAdCreative, MyAdImage
from api.serializers import MyCampaignSerializer, MyAdsetSerializer, MyAdCreativeSerializer

from ounass.settings import MEDIA_ROOT
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview

load_dotenv()
EMAIL_HOST = os.getenv("EMAIL_HOST")

access_token = os.getenv("ACCESS_TOKEN")
app_secret = os.getenv("APP_SECRET")
app_id = os.getenv("APP_ID")
ad_account_id = os.getenv("AD_ACCOUNT_ID")
FacebookAdsApi.init(access_token=access_token)

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer {}".format(access_token)


class CampaignView(View):
    def get(self, request):
        fields = ['id', 'name', 'objective']
        params = {
            'effective_status': ['ACTIVE', 'PAUSED'],
        }
        campaigns = AdAccount(ad_account_id).get_campaigns(fields=fields, params=params)
        pprint.pprint(campaigns)
        context = {'campaigns': campaigns}

        template = loader.get_template('campaigns.html')
        return HttpResponse(template.render(context, request))


class AddsetView(View):
    def get(self, request):
        fields = ['id', 'name', 'campaign_id', 'lifetime_budget', 'daily_budget', 'start_time', 'end_time',
                  'targeting', 'bid_amount', 'status', 'optimization_goal']
        params = {

        }
        addsets = AdAccount(ad_account_id).get_ad_sets(fields=fields, params=params)
        context = {'adsets': addsets}

        template = loader.get_template('adsets.html')
        return HttpResponse(template.render(context, request))


class AdPreviewView(View):
    def get(self, request):
        fields = [
        ]
        params = {
            'ad_format': 'DESKTOP_FEED_STANDARD',
        }
        previews = []
        for ad_creative in MyAdCreative.objects.all():
            try:
                my_preview = AdCreative(ad_creative.id).get_previews(fields=fields, params=params)
                pprint.pp(my_preview)
                previews.append((ad_creative.id, my_preview[0]["body"]))
            except Exception as e:
                print(str(e))
                pass

        print(previews)
        context = {'previews': previews}

        template = loader.get_template('adpreviews.html')
        return HttpResponse(template.render(context, request))


class CampaignViewSet(GenericViewSet,  # generic view functionality
                      CreateModelMixin,  # handles POSTs
                      RetrieveModelMixin,  # handles GETs for 1 Campaign
                      UpdateModelMixin,  # handles PUTs and PATCHes
                      DestroyModelMixin,  # handles DELETE
                      ListModelMixin):  # handles GETs for many Campaign

    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = MyCampaignSerializer

    def get_queryset(self):
        fields = ['id', 'name', 'objective']
        params = {
            'effective_status': ['ACTIVE', 'PAUSED'],
        }
        if 'pk' in self.kwargs:
            params = {
                'pk': self.kwargs['pk'],
                'effective_status': ['ACTIVE', 'PAUSED']
            }
            campaign = AdAccount(ad_account_id).get_campaigns(fields=fields, params=params)
            serialized_campaigns = MyCampaignSerializer(campaign)
        else:
            campaigns = AdAccount(ad_account_id).get_campaigns(fields=fields, params=params)
            serialized_campaigns = MyCampaignSerializer(campaigns, many=True)
        return serialized_campaigns.data

    def list(self, request, *args, **kwargs):
        fields = ['id', 'name', 'objective']
        params = {
            'effective_status': ['ACTIVE', 'PAUSED'],
        }

        campaigns = AdAccount(ad_account_id).get_campaigns(fields=fields, params=params)
        serialized_campaigns = MyCampaignSerializer(campaigns, many=True)
        return Response(serialized_campaigns.data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            fields = ['name', 'objective', 'status']
            params = {
                'name': 'Conversions Campaign [Tekin TOPUZ]' if "name" not in request.data else request.data["name"],
                'objective': 'REACH',
                'status': 'PAUSED',
                'special_ad_categories': [],
            }
            created_campaign = AdAccount(ad_account_id).create_campaign(
                fields=fields,
                params=params,
            )

            if not MyCampaign.objects.filter(id=created_campaign["id"]).exists():
                my_campaign = MyCampaign()
                my_campaign.id = created_campaign["id"]
                my_campaign.name = created_campaign["name"]
                my_campaign.objective = created_campaign["objective"]
                my_campaign.save()

                serializer = self.serializer_class(my_campaign)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                my_campaign = MyCampaign.objects.get(id=created_campaign["id"])
                serializer = self.serializer_class(my_campaign)
                return Response({"campaign": serializer.data,
                                 "status": "Warning",
                                 "message": "Campaign with this id already exists."
                                 }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "ERROR", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddsetViewSet(GenericViewSet,  # generic view functionality
                    CreateModelMixin,  # handles POSTs
                    RetrieveModelMixin,  # handles GETs for 1 Message
                    UpdateModelMixin,  # handles PUTs and PATCHes
                    DestroyModelMixin,  # handles DELETE
                    ListModelMixin):  # handles GETs for many Messages

    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = MyAdsetSerializer
    queryset = MyCampaign.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        fields = ['id', 'name', 'campaign_id', 'lifetime_budget', 'daily_budget', 'start_time', 'end_time',
                  'targeting', 'bid_amount', 'status', 'optimization_goal']
        start_time = timezone.now()
        pprint.pprint(request.data)
        params = {
            'name': 'My First AdSet [Tekin TOPUZ]' if "name" not in request.data else request.data["name"],
            'daily_budget': 2000,
            'start_time': start_time,
            'end_time': start_time + timezone.timedelta(days=10),
            'campaign_id': '120330000091598609' if 'campaign_id' not in request.data else request.data["campaign_id"],
            'bid_amount': 5,
            'billing_event': 'IMPRESSIONS',
            'optimization_goal': 'REACH',
            'targeting': {'age_min': 20 if "age_min" not in request.data else request.data["age_min"],
                          'age_max': 35 if "age_max" not in request.data else request.data["age_max"],
                          'geo_locations': {
                              'countries': ['AE', 'SA', 'KW'] if "countries" not in request.data else request.data[
                                  "countries"],
                              "location_types": [
                                  "home"
                              ]
                              },
                          'facebook_positions': ['story']},
            'status': 'ACTIVE',
        }

        crated_addset = AdAccount(ad_account_id).create_ad_set(fields=fields, params=params)

        pprint.pprint(crated_addset)

        if not MyAdset.objects.filter(id=crated_addset["id"]).exists():
            my_adset = MyAdset()
            my_adset.id = crated_addset["id"]
            my_adset.name = crated_addset["name"]
            my_adset.campaign_id = crated_addset["campaign_id"]
            my_adset.lifetime_budget = crated_addset["lifetime_budget"]
            my_adset.daily_budget = crated_addset["daily_budget"]
            my_adset.start_time = crated_addset["start_time"]
            my_adset.end_time = crated_addset["end_time"]
            my_adset.targeting = params["targeting"]
            my_adset.bid_amount = crated_addset["bid_amount"]
            my_adset.status = crated_addset["status"]
            my_adset.optimization_goal = crated_addset["optimization_goal"]
            my_adset.save()
            serializer = self.serializer_class(my_adset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            my_adset = MyAdset.objects.get(id=crated_addset["id"])
            serializer = self.serializer_class(my_adset)
            return Response({"adset": serializer.data,
                             "status": "Warning",
                             "message": "MyAdset with this id already exists."
                             }, status=status.HTTP_200_OK)


class AdCreativeViewSet(GenericViewSet,  # generic view functionality
                        CreateModelMixin,  # handles POSTs
                        RetrieveModelMixin,  # handles GETs for 1 Message
                        UpdateModelMixin,  # handles PUTs and PATCHes
                        DestroyModelMixin,  # handles DELETE
                        ListModelMixin):  # handles GETs for many Messages

    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = MyAdCreativeSerializer
    queryset = MyAdCreative.objects.all()

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        3. Create an ad via API.
            - The creative link message will be “try it out”
            - The creative link will be “https://www.ounass.ae/designers/gucci”
            - The page id will be “104413048775500”
            - The creative name will be “Gucci AdCreative for Link Ad.”
            - The creative image will be https://ibb.co/pP9hNwV
        """
        try:
            files = {'upload_file': open(os.path.join(MEDIA_ROOT, "gucci-bag.jpg"), 'rb')}
            url = 'https://graph.facebook.com/v12.0/act_3061829570753376/adimages'
            response = requests.post(url=url, files=files, headers=headers)

            json_data = response.json()
            new_adimage = MyAdImage()
            for k, v in json_data['images'].items():
                new_adimage.name = k
                new_adimage.hash = v["hash"]
                new_adimage.url = v["url"]
                new_adimage.save()
                break

            """
            create an ad, with return image hash and given parameters
            """
            fields = ["id", "name", "object_story_spec"]

            params = {
                'name': 'Gucci AdCreative for Link Ad.',
                'object_story_spec': {'page_id': os.getenv("PAGE_ID"),
                                      'link_data': {'image_hash': new_adimage.hash,
                                                    'link': 'https://www.ounass.ae/women/designers/gucci',
                                                    'message': 'try it out'}},
            }

            ad_creative = AdAccount(ad_account_id).create_ad_creative(fields=fields, params=params)

            new_adcreative = MyAdCreative()
            new_adcreative.id = ad_creative["id"]
            new_adcreative.name = ad_creative["name"]
            new_adcreative.object_story_spec = {"link_data": {
                "image_hash": ad_creative["object_story_spec"]["link_data"]["image_hash"],
                "link": ad_creative["object_story_spec"]["link_data"]["link"],
                "message": ad_creative["object_story_spec"]["link_data"]["message"]
            },
                "page_id": ad_creative["object_story_spec"]["page_id"]
            }

            new_adcreative.save()
            return Response(self.serializer_class(new_adcreative).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AdSetInsightAPi(APIView):
    """
       4. Use Adset insight API to display the click and impressions results.
        * You may get empty result. Mock the api response from Facebook documentation
    """

    def get(self, request, ad_set_id, format=None):
        try:
            url = 'https://graph.facebook.com/v12.0/{}/insights?fields=ad_impression_actions, clicks'.format(ad_set_id)
            json_data = requests.get(url, headers=headers).json()
            data = json_data["data"]
            if len(data) == 0:
                return Response({"body": None}, status=status.HTTP_200_OK)
            else:
                return Response({"body": data[0]["body"]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreativePreviewApi(APIView):
    """
        5. Use Preview API to display the ad that you created via API
    """

    def get(self, request, creative_id, format=None):
        try:
            url = 'https://graph.facebook.com/v12.0/{}/previews?ad_format=DESKTOP_FEED_STANDARD'.format(creative_id)
            json_data = requests.get(url, headers=headers).json()
            data = json_data["data"]
            if len(data) == 0:
                return Response({"body": None}, status=status.HTTP_200_OK)
            else:
                return Response({"body": data[0]["body"]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
