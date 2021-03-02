from pathlib import Path
import environ

from rest_framework.decorators import api_view
from rest_framework.response import Response

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "vbb_backend"
env = environ.Env()
env.read_env(str(ROOT_DIR / ".env"))

#TODO import and implement Mailchimp API
@api_view(["POST"])
def sign_up_for_newsletter(request):
    # TODO check on desired required fields
    fname = request.data.get("firstName")
    lname = request.data.get("lastName")
    email = request.data.get("email")
    phoneNumber = request.data.get("phoneNumber")
    # countryCode = request.data.get('countryCode'), TODO: when we fix front-end form, we can uncomment this part

    member_info = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
        "FNAME": fname,
        "LNAME": lname,
        "PHONE": phoneNumber,
        # "PHONE": (f'+{countryCode}{phoneNumber}'), TODO: when we fix front-end form, we can uncomment this part
        }
    }

    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": env.str("MAILCHIMP_API_KEY"),
            "server": env.str("MAILCHIMP_SERVER")
        })
        list_id = env.str("MAILCHIMP_LIST_ID")
        response = client.lists.add_list_member(list_id, member_info)
        print(f"Response: {response}")
    except ApiClientError as error:
        print(f"An exception occurred: {error.text}")

    #TODO test this functionality more thoroughly
    return Response(
        {"success": "true"}
    )
    