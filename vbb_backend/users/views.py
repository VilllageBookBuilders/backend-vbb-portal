#TODO import and implement Mailchimp API
@api_view(["POST"])
def sign_up_for_newsletters(request):  
    fname = request.data.get("firstName")
    lname = request.data.get("lastName")
    email = request.data.get("email")
    phoneNumber = request.data.get("phoneNumber")
    # countryCode = request.data.get('countryCode'), TODO: when we fix front-end form, we can uncomment this part

    mailchimp = MailchimpMarketing.Client()
    mailchimp_config = os.path.join("api","mailchimp_config.json")
    with open(mailchimp_config) as infile:
        data = json.load(infile)
    mailchimp.set_config(data['keys'])
    list_id = data["listid"]["id"]

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
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))

    #TODO test this functionality more thoroughly
    return Response(
        {"success": "true"}
    )