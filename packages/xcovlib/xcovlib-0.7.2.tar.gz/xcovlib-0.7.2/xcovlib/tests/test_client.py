from unittest import TestCase

import responses

from ..client import Client


class TestClient(TestCase):

    @responses.activate
    def test_booking_quote(self):
        self.client = Client(host='127.0.0.1:8001', key='XCOVAPIKEY',
                             secret='testsecret', partner='XCOV', prefix='')

        quote_package_response = {
            'id': 'XX-INS',
            'quotes': {'0': {'id': '123'}},
        }
        responses.add(responses.POST, 'https://127.0.0.1:8001/partners/XCOV/quotes/', status=201,
                      json=quote_package_response)
        responses.add(responses.GET, 'https://127.0.0.1:8001/partners/XCOV/bookings/XX-INS/', status=200,
                      json=quote_package_response)
        responses.add(responses.POST, 'https://127.0.0.1:8001/partners/XCOV/bookings/XX-INS/', status=200,
                      json=quote_package_response)
        data = [{
            'policy_type': 'parcel_insurance',
            'policy_type_version': 1,
            'policy_start_date': '2018-12-12T13:00:00Z',
            'from_country': 'AU',
            'from_zipcode': '2000',
            'to_country': 'US',
            'ship_cost': 251,
            'to_zipcode': '10002',
            'cover_amount': 1000,
            'from_company_name': 'company name',
            'ship_date': '2018-11-02T13:00:00Z',
            'parcel_products': [{
                'sku': '20001',
                'value': 1000,
            }]
        }]

        quote = self.client.create_quote(
            partner_id='XCOV', currency='AUD', customer_country='AU', destination_country='US',
            request=data
        )

        # save quotes
        self.assertIsNotNone(quote.id)
        package_id = quote.id
        quote_id = quote.quotes['0']['id']

        # create a new booking
        booking_data = {
            'quotes': [{
                'id': quote_id,
                'insured': [{
                    'first_name': '{{firstname_i}}',
                    'last_name': '{{firstname_i}}',
                    'email': 'test@email.com',
                    'age': 22,
                }]
            }],
            'policyholder': {
                'first_name': '{{firstname}}',
                'last_name': '{{firstname}}',
                'email': 'test@email.com',
                'age': 22,
                'country': 'AU',
            }
        }
        booking = self.client.create_booking(
            partner_id='XCOV', quote_package_id=package_id, **booking_data
        )
        self.assertIsNotNone(booking.id)

        new_booking = self.client.get_booking(partner_id='XCOV', quote_package_id=package_id)
        self.assertIsNotNone(new_booking.id)
