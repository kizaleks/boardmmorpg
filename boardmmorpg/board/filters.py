from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter

from .models import Advertisement, Comment

class AdvertisementFilter(FilterSet):
    model = Advertisement

    datetime = DateFilter(
        field_name='dateCreation',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Даты позже'
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'Category', 'dateCreation']

class CommentFilter(FilterSet):
    model = Comment

    commentStatus = CharFilter('commentStatus',
                       label='Статус коментария',
                       lookup_expr='icontains',
                       )

    datetime = DateFilter(
        field_name='dateCreation',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Даты коментариев позже'
    )

    class Meta:
        model = Comment
        fields = ['commentStatus','dateCreation']