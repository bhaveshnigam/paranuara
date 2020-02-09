from rest_framework import generics
from rest_framework.response import Response

from civilisation.models import Citizen
from civilisation.serializers import CitizenSerializer, CitizenCrucialInformationSerializer, CitizenMinimalSerializer, \
    CitizenFavouriteFoodOverviewSerializer


class CompanyEmployees(generics.ListAPIView):
    """View to get all the employees of a company."""
    serializer_class = CitizenSerializer
    company_id = None
    lookup_url_kwarg = 'company_id'

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(self.lookup_url_kwarg):
            self.company_id = self.kwargs.get(self.lookup_url_kwarg)
        return super(CompanyEmployees, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Citizen.objects.filter(
            company__company_index=self.company_id
        )


class CitizenMutualFriends(generics.RetrieveAPIView):
    """Given two individuals provide essential information and their mutual friends"""
    serializer_class = CitizenCrucialInformationSerializer
    friends_serializer_class = CitizenMinimalSerializer
    model = Citizen

    def get_mutual_friends(self, person_1, person_2):
        """Get mutual friends common between person 1 and person 2, who are alive and have brown eyes"""
        mutual_friend_ids = set(person_1.friends_csv.split(',')).intersection(set(person_2.friends_csv.split(',')))
        citizen_queryset = Citizen.objects.filter(
            index__in=mutual_friend_ids,
            has_died=False,
            eye_color='brown'
        )
        return CitizenMinimalSerializer(citizen_queryset, many=True).data

    def retrieve(self, request, *args, **kwargs):
        person_1 = self.model.objects.filter(
            _id=self.kwargs.get('person_1_id')
        ).first()
        person_2 = self.model.objects.filter(
            _id=self.kwargs['person_2_id']
        ).first()
        person_1_serialized_data = self.get_serializer(person_1).data if person_1 else {}
        person_2_serialized_data = self.get_serializer(person_2).data if person_2 else {}

        if person_1 and person_2:
            mutual_friends_data = self.get_mutual_friends(person_1, person_2)
        else:
            mutual_friends_data = []

        return Response({
            'person_1': person_1_serialized_data,
            'person_2': person_2_serialized_data,
            'mutual_friends': mutual_friends_data
        })


class CitizenFavouriteFoodOverview(generics.RetrieveAPIView):
    """View to get details about the citizen"""
    queryset = Citizen.objects.all()
    serializer_class = CitizenFavouriteFoodOverviewSerializer
    lookup_url_kwarg = 'person_1_id'
    lookup_field = '_id'
