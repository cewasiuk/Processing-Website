from django.db import models


class Customer(models.Model):
    company = models.CharField('Company Name', max_length=100)
    # TODO: Split the address into street, city, state, zip, and country
    address = models.CharField('Shipping Address', max_length=300)
    
    '''# TODO: Find out why this method doesn't work
    def get_company(self):
        return "\n".join([c.company_name for c in self.company_name])
    '''
    customers = models.Manager()
    # TODO: Add more fields if necessary

    def __str__(self):
        return self.company
    
