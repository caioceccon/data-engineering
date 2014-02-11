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
