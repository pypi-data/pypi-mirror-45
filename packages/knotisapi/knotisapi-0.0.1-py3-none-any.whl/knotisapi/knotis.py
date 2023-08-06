from librestapi import (
    Client,
    Resource
)


class Location(object):
    def __init__(
        self,
        latitude,
        longitude
    ):
        self.latitude = latitude
        self.longitude = longitude


class Knotis(Client):
    def __init__(
        self,
        *args,
        **kwargs
    ):
        super(Knotis, self).__init__(*args, **kwargs)

        self._location = None

        self.User = Resource(
            self,
            path='auth/user',
            name='user'
        )

        self.Image = Resource(
            self,
            path='media/image',
            name='image'
        )

        self.OneTimeUseToken = Resource(
            self,
            path='auth/onetimeusetoken',
            name='onetimeusetoken',
            auth_required=False
        )

        self.NewUser = Resource(
            self,
            path='auth/new',
            name='new_user',
            auth_required=False
        )

        self.ResetPassword = Resource(
            self,
            path='auth/resetpassword',
            name='reset_password',
            auth_required=False
        )

        self.IdentitySwitcher = Resource(
            self,
            path='identity/switcher',
            name='identity_switcher'
        )

        self.Identity = Resource(
            self,
            path='identity',
            name='identity'
        )

        self.Offers = Resource(
            self,
            path='offers',
            name='offers'
        )

        self.Offer = Resource(
            self,
            path='offer',
            name='offer'
        )

        self.Individual = Resource(
            self,
            path='identity/individual',
            name='individual'
        )

        self.Establishment = Resource(
            self,
            path='identity/establishment',
            name='establishment'
        )

        self.Business = Resource(
            self,
            path='identity/business',
            name='business'
        )

        self.PlaidItem = Resource(
            self,
            path='plaid/item',
            name='plaid_item'
        )

        self.PlaidTransaction = Resource(
            self,
            path='plaid/transaction',
            name='plaid_transaction'
        )

        self.Purchase = Resource(
            self,
            path='transaction/purchase',
            name='purchase',
            api_version='v2'
        )

        self.Redemption = Resource(
            self,
            path='transaction/redemption',
            name='redemption',
            api_version='v2'
        )

        self.ImageUpload = Resource(
            self,
            path='media/imageinstance',
            name='image_upload'
        )

        self.Search = Resource(
            self,
            path='search',
            name='search'
        )

        self.SearchSuggest = Resource(
            self,
            path='search/suggest',
            name='search_suggest'
        )

    def authenticate(
        self,
        **credentials
    ):
        method = 'post'
        uri = self.auth_uri
        '''
            Force application/x-www-form-urlencoded because
            our OAUTH2 endpoint doens't support JSON.
        '''
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = self.request(
            method,
            uri,
            credentials,
            headers
        )

        self.set_credentials(**response.data)

        user_response = self.User.retrieve()
        self.set_credentials(**{
            'current_identity': user_response.data.get('default_identity'),
            'current_identity_type': user_response.data.get('default_identity_type')
        })

        return user_response

    def refresh_token(
        self,
        refresh_token
    ):
        credentials = {
            'grant_type': 'refresh_token',
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'refresh_token': refresh_token
        }

        return self.authenticate(**credentials)

    def password_grant(
        self,
        username,
        password
    ):
        credentials = {
            'grant_type': 'password',
            'client_id': self.api_key,
            'username': username,
            'password': password
        }

        return self.authenticate(**credentials)

    def get_location(self):
        return self._location

    def set_location(
        self,
        latitude,
        longitude
    ):
        self._location = Location(
            latitude,
            longitude
        )

        return self._location
