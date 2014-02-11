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

    @classmethod
    def import_from_txt_data(cls, txtData):
        if not txtData:
            msg = 'Error: txtData can not be empty, expected [address, name]'
            raise ValueError(msg)

        merchant, created = cls.objects.get_or_create(
            name=txtData[1].rstrip(), address=txtData[0]
        )
        return merchant


class Item(BaseModel):
    merchant = models.ForeignKey(Merchant)
    description = models.CharField(u'Description', max_length=100)
    price = models.FloatField(u'Price')

    @classmethod
    def import_from_txt_data(cls, txtData, merchant):
        if not txtData:
            msg = 'Error: txtData can not be empty, expected [description, price]'
            raise ValueError(msg)

        item, created = cls.objects.get_or_create(
            merchant=merchant, description=txtData[0], price=float(txtData[1])
        )
        return item


class Billing(BaseModel):
    def save(self, *args, **kwargs):
        super(Billing, self).save(*args, **kwargs)
        if self.txtBillingFile:
            self.parse_txt_billing_file()

    txtBillingFile = models.FileField(
        upload_to=u'billings', verbose_name=u'Txt Billing File'
    )

    def calculate_gross_revenue(self):
        total = 0.0
        for s in Sale.objects.filter(billing=self):
            total += s.salePrice
        return total
    calculate_gross_revenue.short_description = u'Gross revenue'

    def parse_txt_billing_file(self, verbose=False):
        lineCount = 0

        if self.txtBillingFile.closed:
            self.txtBillingFile.open('r')

        for line in self.txtBillingFile.readlines():
            splitedLine = line.split("\t")

            # Skipping header.
            if not lineCount:
                lineCount +=1
                continue
            try:
                Sale.import_from_txt_data(txtData=splitedLine, billing=self)
            except Exception, e:
                if verbose:
                    print 'Failed to import line:`%s` %s' % (line, e)
                continue
        self.txtBillingFile.close()

class Sale(BaseModel):
    purchaserName = models.CharField(u'Purchaser Name', max_length=100)
    item = models.ForeignKey(Item)
    billing = models.ForeignKey(Billing)
    merchant = models.ForeignKey(Merchant)
    salePrice = models.FloatField(u'Sale Price')
    quantity = models.IntegerField(u'Quantity')

    def get_total_price(self):
        return self.quantity * self.item.price

    @classmethod
    def import_from_txt_data(cls, txtData, billing):
        if not isinstance(billing, Billing):
            raise ValueError('Error: billing is not of type Billing')

        if not billing.txtBillingFile:
            raise ValueError('Error: billing must have an associated file!')

        purchaserName = txtData[0]
        merchant = Merchant.import_from_txt_data(txtData[4:6])
        item = Item.import_from_txt_data(txtData[1:3], merchant=merchant)

        quantity = int(txtData[3])
        salePrice = quantity * item.price

        sale, created = Sale.objects.get_or_create(
            purchaserName=purchaserName, item=item, billing=billing,
            merchant=merchant, salePrice=salePrice, quantity=quantity
        )
