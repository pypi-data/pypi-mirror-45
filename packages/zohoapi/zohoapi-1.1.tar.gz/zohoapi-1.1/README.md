# README #

This is a simple wrapper for Zoho CRM's API

Example Usage:
    
    >>> from zohoapi.api import ZohoConnection
    >>> zc = ZohoConnection()
    >>> first_two_hundred_contacts = zc.Contacts.get_records()
    >>> zc.Accounts.insert_record({'First Name': 'Richard',
    ...                            'Last Name': 'Johnson'})
