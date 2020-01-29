import re
from robobrowser import RoboBrowser
import config

MOBILE_USER_AGENT = r"Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://m.facebook.com/v5.0/dialog/oauth?auth_type=rerequest&client_id=287435711376482&default_audience=friends&display=touch&e2e=%7B%22init%22%3A211560.20663954099%7D&fbapp_pres=0&local_client_id=hinge&redirect_uri=fb287435711376482hinge%3A%2F%2Fauthorize%2F&response_type=token_or_nonce%2Csigned_request&return_scopes=true&scope=user_photos%2Cuser_birthday%2Cuser_hometown%2Cpublic_profile%2Cemail%2Cuser_friends%2Cuser_likes&sdk=ios&sdk_version=5.11.0&state=%7B%22challenge%22%3A%22Ks5gntbMoB8IFaEzFfZA%253DbLQxaQ%253D%22%2C%220_auth_logger_id%22%3A%2232C01630-411B-480E-AB3E-B2A16B507787%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D"


def get_access_token():
    s = RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    f = s.get_form()
    f["pass"] = config.FB_PASS
    f["email"] = config.FB_EMAIL
    s.submit_form(f)
    f = s.get_form()
    if f.submit_fields.get('__CONFIRM__'):
        try:
            s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
        except Exception as e:
            exc_str = str(e)
            access_token = re.search(
                r"access_token=([\w\d]+)", exc_str).groups()[0]
            return access_token

    else:
        raise Exception(
            "Couldn't find the continue button. Maybe you supplied the wrong login credentials? Or maybe Facebook is asking a security question?")

    return access_token
