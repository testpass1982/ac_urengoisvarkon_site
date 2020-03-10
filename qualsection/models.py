from django.db import models
from django.utils import timezone


# Create your models here.
class CokPlaceInfo(models.Model):
    org_name = models.CharField(u'Полное наименование', max_length=500)
    org_addr = models.CharField(u'Место нахождения ЦОК', max_length=500)
    cok_code = models.CharField(u'Шифр ЦОК', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Место нахождения ЦОК'
        verbose_name_plural = 'Места нахождения ЦОК'

    def __str__(self):
        return self.org_name


class CokContact(models.Model):
    post_addr = models.CharField(u'Адрес для почтовых отправлений', max_length=500)
    email = models.EmailField(u'Адрес электронной почты ЦОК')
    site_url = models.URLField(u'Адрес официального сайта ЦОК')
    spks_site_url = models.URLField(u'Адрес официального сайта СПКС')
    cok_phones = models.CharField(u'Контактный(е) телефон(ы) ЦОК', max_length=200)

    class Meta:
        verbose_name = 'Набор контактов ЦОК'
        verbose_name_plural = 'Наборы контактов ЦОК'

    def __str__(self):
        return self.post_addr



class CokProfstandard(models.Model):
    title = models.CharField(u'Название профстандарта', max_length=300)
    number = models.SmallIntegerField(u'Порядок вывода', default=500)

    class Meta:
        verbose_name = 'Профстандарт'
        verbose_name_plural = 'Профстандарты'

    def __str__(self):
        return self.title

class CokDocument(models.Model):
    title = models.CharField(u'Наименование документа', max_length=300)
    # qualification = models.ForeignKey(CokQualification, null=True, on_delete=models.SET_NULL)
    example = models.FileField(u'Образец документа', upload_to='cok-documents/', null=True, blank=True)
    task_example = models.NullBooleanField(u'Является примером задания')
    pseudo = models.CharField(u'Псевдоним', default='', max_length=20, blank=True)
    number = models.SmallIntegerField(u'Порядок вывода', default=500)
    published_date = models.DateField(u'Дата публикации', null=True, blank=True, default=timezone.now)

    class Meta:
        verbose_name = 'Документ ЦОК'
        verbose_name_plural = 'Документы ЦОК'

    def __str__(self):
        return self.title


class CokQualification(models.Model):
    profstandard = models.ForeignKey(CokProfstandard, null=True, on_delete=models.SET_NULL)
    qual_code = models.CharField(u'Номер в реестре', max_length=20)
    title = models.CharField(u'Наименование квалификации', max_length=200)
    period = models.SmallIntegerField(u'Срок действия св-ва(лет)')
    professions = models.TextField(u'Наименования профессий с разрядами ЕТКС')
    documents = models.ManyToManyField(CokDocument, blank=True)
    pseudo = models.CharField(u'Псевдоним', max_length=20, null=True, blank=True)
    number = models.SmallIntegerField(u'Порядок вывода', default=500)
    active = models.BooleanField(u'Активность', default=False)

    class Meta:
        verbose_name = 'Квалификация'
        verbose_name_plural = 'Квалификации'

    def __str__(self):
        return '{} - {}'.format(self.qual_code, self.title)



class CokQualExamPlace(models.Model):
    title = models.CharField(u'Наименование', max_length=300)
    address = models.CharField(u'Адрес', max_length=500)
    number = models.SmallIntegerField(u'Порядок вывода', default=500)

    class Meta:
        verbose_name = 'Адрес места проведения ПЭ'
        verbose_name_plural = 'Адреса мест проведения ПЭ'

    def __str__(self):
        return self.title





