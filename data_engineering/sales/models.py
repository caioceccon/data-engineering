from django.db import models

class BaseModel(models.Model):
    """
    BaseModel is an abstract class with basic fields used for time, date,
    creatiton and modification control, that all the system entities
    should have.
    """

    creationDate = models.DateTimeField(
        u"Criation Date", auto_now_add=True, editable=False
    )

    modificationDate = models.DateTimeField(
        u"Update Date", auto_now=True, auto_now_add=True,
        editable=False
    )

    class Meta:
        abstract = True


class Merchant(BaseModel):
    name = models.CharField(u'Name', max_length=100)
    address = models.CharField(u'Address', max_length=100)


class Item(BaseModel):
    merchant = models.ForeignKey(Merchant)
    description = models.CharField(u'Description', max_length=100)
    price = models.FloatField(u'Price')
