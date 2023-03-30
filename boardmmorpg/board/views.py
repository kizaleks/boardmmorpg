from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.views.generic.edit import FormMixin
from .models import Advertisement, Comment
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from .filters import AdvertisementFilter, CommentFilter
from .forms import CommentForm

class AdvertisementList(ListView):
    '''Список объявлений'''

    model = Advertisement
    template_name = 'advertisement.html'
    context_object_name = 'Advertisement'
    queryset = Advertisement.objects.order_by('-dateCreation')
    paginate_by = 10
    success_url = '/board'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class CustomSuccessMessageMixin:
    pass


class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    '''Отображение объявления с коментариями'''
    model = Advertisement
    template_name = 'advertisementdetail.html'
    context_object_name = 'advertisementdetail'
    form_class = CommentForm
    # success_msg = 'Комментарий успешно создан, ожидайте модерации'
    success_url ='/board'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.commentAdvertisement = self.get_object()
        self.object.commentUser = self.request.user
        success_url = ''

        self.object.save()
        return super().form_valid(form)


class AdvertisementSearch(ListView):
    '''Список объявлений пользователя с коментариями'''
    model = Advertisement
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Advertisement.objects.order_by('-dateCreation')
    paginate_by = 10
    success_url = '/board'

    def get_queryset(self):
        queryset =Advertisement.objects.filter(author=self.request.user.id)
        self.filterset = AdvertisementFilter(self.request.GET, queryset)

        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdvertisementFilter(self.request.GET, queryset=self.get_queryset())
        return context

class CommentList(ListView):
    '''Список коментариев'''
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'
    queryset = Comment.objects.order_by('-dateCreation')
    paginate_by = 10
    success_url = '/board'
    def get_queryset(self, queryset=None):
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        return context

class AdvertisementForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'size': 200}))
    class Meta:
        model = Advertisement
        fields = ['title','image','text', 'Category']


class AdvertisementCreate(PermissionRequiredMixin, CreateView):
    '''Добавление  объявления'''
    permission_required = ('board.add_advertisement',)
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'add.html'
    success_url = '/board'

    #
    def form_valid(self, form):
        Advertisement = form.save(commit=False)
        Advertisement.author=self.request.user
        Advertisement.save()
        return super().form_valid(form)

class AdvertisementUpdateView(PermissionRequiredMixin, UpdateView):
    '''Редактирование объявления'''
    permission_required = ('board.change_advertisement',)
    template_name = 'add.html'
    form_class = AdvertisementForm
    success_url = '/board'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisement.objects.get(pk=id)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','commentStatus']

class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    '''Модерация коментария'''
    permission_required = ('board.change_comment',)
    template_name = 'editcomment.html'
    form_class = CommentForm
    success_url = '/board'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Comment.objects.get(pk=id)


class AdvertisementDeleteView(DeleteView):
    '''Удаление объявлений'''
    permission_required = ('board.delete_advertisement',)
    model = Advertisement
    template_name = 'delete.html'
    queryset = Advertisement.objects.all
    context_object_name = 'Advertisement'
    success_url = '/board'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisement.objects.get(pk=id)