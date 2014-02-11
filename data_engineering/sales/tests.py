from os import path
from django.test import TestCase
from django.conf import settings
from django.core.files import File
from sales.models import (Merchant, Item, Billing, Sale)


class MerchantModelTest(TestCase):
    def test_import_merchant_from_txt_data(self):
        txtData = ['Merchant Address', 'Merchant Name']
        Merchant.import_from_txt_data(txtData)

        # Retrieve it from database.
        merchant = Merchant.objects.all()[0]

        # Check its attributes.
        self.assertEquals(merchant.name, txtData[1])
        self.assertEquals(merchant.address, txtData[0])


class ItemModelTest(TestCase):
    def setUp(self):
        self.merchanTxtData = ['Merchant Name', 'Merchant Address']
        self.merchant = Merchant.import_from_txt_data(self.merchanTxtData)

    def test_import_item_from_txt_data(self):
        txtData = ['R$20 Sneakers for R$5', '5.0']
        Item.import_from_txt_data(txtData, merchant=self.merchant)

        # Retrieve it from database.
        item = Item.objects.all()[0]

        # Check its attributes.
        self.assertEquals(item.merchant, self.merchant)
        self.assertEquals(item.description, txtData[0])
        self.assertEquals(item.price, float(txtData[1]))


class BillingModelTest(TestCase):
    def setUp(self):
        self.billing = BillingModelTest.create_billing()

    def tearDown(self):
        self.billing.txtBillingFile.close()

    @classmethod
    def create_billing(cls):
        billingFileSample = path.join(
            settings.BASE_DIR, 'sales', 'example_input.tab'
        )

        billing = Billing()
        billing.txtBillingFile.save(
            'test_billing.txt', File(open(billingFileSample, 'r'))
        )

        billing.save()
        return billing

    def test_calculate_gross_revenue(self):
        self.billing.parse_txt_billing_file(verbose=True)

        self.assertEquals(self.billing.calculate_gross_revenue(), 95.0)

    def test_parse_txt_billing_file(self):
        self.billing.parse_txt_billing_file(verbose=True)
        lineCount = 0
        totalPrice = 0

        if self.billing.txtBillingFile.closed:
            self.billing.txtBillingFile.open('r')

        for line in self.billing.txtBillingFile.readlines():
            # Skipping header.
            if not lineCount:
                lineCount +=1
                continue

            splitedLine = line.split("\t")
            # Parsing Attributes.
            purchaserName = splitedLine[0]
            itemDescription = splitedLine[1]
            itemPrice = float(splitedLine[2])
            quantity = int(splitedLine[3])
            merchantAddress = splitedLine[4]
            merchantName = splitedLine[5].rstrip()
            salePrice = itemPrice * quantity
            totalPrice += salePrice

            # Trying to find imported data on database.
            merchant = Merchant.objects.get(
                name=merchantName, address=merchantAddress
            )

            item = Item.objects.get(
                merchant=merchant, description=itemDescription,
                price=itemPrice
            )

            Sale.objects.get(
                purchaserName=purchaserName, item=item, billing=self.billing,
                merchant=merchant, salePrice=salePrice, quantity=quantity
            )
        self.assertEquals(self.billing.calculate_gross_revenue(), totalPrice)

class SaleModelTest(TestCase):
    def setUp(self):
        self.billing = BillingModelTest.create_billing()
        self.txtData = [
            'Snake Plissken', 'R$20 Sneakers for R$5', '5.0', '4',
             '123 Fake St', 'Sneaker Store Emporium\n'
        ]

        self.merchant = Merchant.import_from_txt_data(self.txtData[4:6])
        self.item = Item.import_from_txt_data(self.txtData[1:3], self.merchant)

    def test_import_sale_from_txt_data(self):
        Sale.import_from_txt_data(txtData=self.txtData, billing=self.billing)

        # Retrieve it from database.
        sale = Sale.objects.all()[0]

        # Check its attributes.
        self.assertEquals(sale.purchaserName, self.txtData[0])
        self.assertEquals(sale.item, self.item)
        self.assertEquals(sale.billing, self.billing)
        self.assertEquals(sale.merchant, self.merchant)
        self.assertEquals(sale.quantity, int(self.txtData[3]))
        self.assertEquals(
            sale.salePrice, float(self.txtData[2]) * int(self.txtData[3])
        )
