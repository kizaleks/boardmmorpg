from django.db import models
from django.contrib.auth.models import User

class Advertisement(models.Model):
    '''Класс объявление'''
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    image=models.ImageField(upload_to='media/',blank=True)
    text = models.CharField(max_length=1024)
    dateCreation = models.DateTimeField(auto_now_add=True)
    Tanks = 'Tanks'
    Hily = 'Hily'
    DD = 'DD'
    traders = 'traders'
    GuildMasters = 'Guild Masters'
    QuestGivers = 'Quest Givers'
    Blacksmiths = 'Blacksmiths'
    Tanners = 'Tanners'
    PotionMakers = 'Potion Makers'
    SpellMasters = 'Spell Masters'

    CATEGORY_CHOICES = (
        (Tanks, 'Танки'),
        (Hily, 'Хилы'),
        (DD, 'ДД'),
        (traders, 'Торговцы'),
        (GuildMasters, 'Гилдмастеры'),
        (QuestGivers, 'Квестгиверы'),
        (Blacksmiths, 'Кузнецы'),
        (Tanners, 'Кожевники'),
        (PotionMakers, 'Зельевары'),
        (SpellMasters, 'Мастера заклинаний'),
    )
    Category = models.CharField(max_length=13, choices=CATEGORY_CHOICES, default=Tanks)

class Comment(models.Model):
    '''Класс коментарий'''
    commentAdvertisement=models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments')
    commentUser=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    New='New'
    Accept='Accept'
    Reject='Reject'
    STATUS = (
        (New, 'Новая'),
        (Accept, 'Принята'),
        (Reject, 'Отклонена'),
    )
    commentStatus = models.CharField(max_length=6, choices=STATUS, default=New)
    dateCreation=models.DateTimeField(auto_now_add=True)
