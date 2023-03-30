import json


class Property():

    def __init__(self, address, price, property_type, property_details, address_href):
        self.address = address
        self.price = price
        self.property_type = property_type
        self.property_details = property_details
        self.address_href = address_href

    def get_address(self):
        return self.address

    def get_price(self):
        return self.price

    def get_property_type(self):
        return self.property_type

    def get_property_details(self):
        return self.property_details

    def get_address_href(self):
        return self.address_href

    def get_property(self):
        return {
            'address': self.address,
            'price': self.price,
            'property_type': self.property_type,
            'property_details': self.property_details,
            'address_href': self.address_href
        }

    def print_property(self):
        print(f'Address: {self.address}')
        print(f'Price: {self.price}')
        print(f'Type: {self.property_type}')
        print('Property_Details:')
        for x in self.property_details:
            print(f'\t{x}')
        print(f'URL: https://www.realestate.com.au{self.address_href}')

    def serialize(self):
        return json.dumps(self.get_property())
