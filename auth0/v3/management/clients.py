from .rest import RestClient


class Clients(object):

    """Auth0 applications endpoints

    Args:
        domain (str): Your Auth0 domain, e.g: 'username.auth0.com'

        token (str): Management API v2 Token

        telemetry (bool, optional): Enable or disable Telemetry
            (defaults to True)
    """

    def __init__(self, domain, token, telemetry=True):
        self.domain = domain
        self.client = RestClient(jwt=token, telemetry=telemetry)

    def _url(self, id=None):
        url = 'https://%s/api/v2/clients' % self.domain
        if id is not None:
            return url + '/' + id
        return url

    def all(self, fields=None, include_fields=True, page=None, per_page=None, extra_params=None):
        """Retrieves a list of all the applications.

        Important: The client_secret and encryption_key attributes can only be
        retrieved with the read:client_keys scope.

        Args:
           fields (list of str, optional): A list of fields to include or
              exclude from the result (depending on include_fields). Empty to
              retrieve all fields.

           include_fields (bool, optional): True if the fields specified are
              to be included in the result, False otherwise.

           page (int): The result's page number (zero based).

           per_page (int, optional): The amount of entries per page.

           extra_params (dictionary, optional): The extra parameters to add to
             the request. The fields, include_fields, page and per_page values
             specified as parameters take precedence over the ones defined here.
        """
        params = extra_params or {}
        params['fields'] = fields and ','.join(fields) or None
        params['include_fields'] = str(include_fields).lower()
        params['page'] = page
        params['per_page'] = per_page
        
        return self.client.get(self._url(), params=params)

    def create(self, body):
        """Create a new application.

        Args:
           body (dict): Attributes for the new application.
              See: https://auth0.com/docs/api/v2#!/Clients/post_clients
        """

        return self.client.post(self._url(), data=body)

    def get(self, id, fields=None, include_fields=True):
        """Retrieves an application by its id.

        Important: The client_secret, encryption_key and signing_keys
        attributes can only be retrieved with the read:client_keys scope.

        Args:
           id (str): Id of the application to get.

           fields (list of str, optional): A list of fields to include or
              exclude from the result (depending on include_fields). Empty to
              retrieve all fields.

           include_fields (bool, optional): True if the fields specified are
              to be included in the result, False otherwise.
        """

        params = {'fields': fields and ','.join(fields) or None,
                  'include_fields': str(include_fields).lower()}

        return self.client.get(self._url(id), params=params)

    def delete(self, id):
        """Deletes an application and all its related assets.

        Args:
           id (str): Id of application to delete.
        """

        return self.client.delete(self._url(id))

    def update(self, id, body):
        """Modifies an application.

        Important: The client_secret, encryption_key and signing_keys
        attributes can only be updated with the update:client_keys scope.

        Args:
           id (str): Client id of the application.

           body (dict): Attributes to modify.
        """

        return self.client.patch(self._url(id), data=body)
