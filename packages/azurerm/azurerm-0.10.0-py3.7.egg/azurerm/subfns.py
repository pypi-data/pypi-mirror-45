'''subnfs - place to store azurerm functions related to subscriptions'''
import io
import json
import os

from .restfns import do_get
from .settings import BASE_API, get_rm_endpoint


def get_subscription_from_cli(name=None):
    '''Get the default, or named, subscription id from CLI's local cache.

    Args:
        name (str): Optional subscription name. If this is set, the subscription id of the named
           subscription is returned from the CLI cache if present. If not set, the subscription id
           of the default subscription is returned.

    Returns:
        Azure subscription ID string.

    Requirements:
        User has run 'az login' once, or is in Azure Cloud Shell.
    '''
    home = os.path.expanduser('~')
    azure_profile_path = home + os.sep + '.azure' + os.sep + 'azureProfile.json'
    if os.path.isfile(azure_profile_path) is False:
        print('Error from get_subscription_from_cli(): Cannot find ' +
              azure_profile_path)
        return None
    with io.open(azure_profile_path, 'r', encoding='utf-8-sig') as azure_profile_fd:
        azure_profile = json.load(azure_profile_fd)
    for subscription_info in azure_profile['subscriptions']:
        if (name is None and subscription_info['isDefault'] is True) or \
                                            subscription_info['name'] == name:
            return subscription_info['id']
    return None


def list_locations(access_token, subscription_id):
    '''List available locations for a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response. JSON list of locations.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/locations?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def list_subscriptions(access_token):
    '''List the available Azure subscriptions for this user account or service principle.

    Args:
        access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON list of subscriptions.
    '''
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/',
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def list_tenants(access_token):
    '''List tenants accessible by this user.

    Args:
          access_token (str): A valid Azure authentication token.

    Returns:
        HTTP response. JSON list of tenant IDs.
    '''  
    endpoint = ''.join([get_rm_endpoint(),
                        '/tenants/',
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)