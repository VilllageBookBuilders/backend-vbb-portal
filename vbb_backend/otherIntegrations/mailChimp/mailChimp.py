import mailchimp_marketing as MailchimpMarketing
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError


def subscribe_newsletter(data):
    try:
        client = MailchimpMarketing.Client()
        client.set_config(
            {"api_key": settings.MAILCHIMP_API_KEY, "server": settings.MAILCHIMP_SERVER}
        )
        list_id = settings.MAILCHIMP_LIST_ID
        # Unused as yet, response info here: https://mailchimp.com/developer/marketing/api/list-members/add-member-to-list/
        client.lists.add_list_member(list_id, data)
        return True
    except ApiClientError as error:
        raise Exception from error
