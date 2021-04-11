import random
import string

from django.utils import timezone
from social_core.exceptions import AuthForbidden

from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
from urllib.request import urlretrieve

import requests

from authapp.models import UserProfile
from geekshop.settings import MEDIA_ROOT


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == "vk-oauth2":
        api_url = urlunparse(("https", "api.vk.com", "/method/users.get", None,
                              urlencode(OrderedDict(fields=",".join(("bdate", "sex", "about", "photo_max")),
                                                    access_token=response["access_token"], v="5.92")), None
                              ))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()["response"][0]
        if data["sex"]:
            user.userprofile.gender = UserProfile.MALE if data["sex"] == 2 else UserProfile.FEMALE

        if data["about"]:
            user.userprofile.about_me = data["about"]

        if data["bdate"]:
            bday = datetime.strptime(data["bdate"], "%d.%m.%Y").date()
            user.userprofile.birthday = bday
            age = timezone.now().date().year - bday.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if data["photo_max"]:
            path_to_avatar = f"{MEDIA_ROOT}/users_avatars/" \
                             f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}.jpg"
            urlretrieve(data["photo_max"], path_to_avatar)
            user.avatar = path_to_avatar
    elif backend.name == "google-oauth2":
        if response["picture"]:
            path_to_avatar = f"{MEDIA_ROOT}/users_avatars/" \
                             f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}.jpg"
            urlretrieve(response["picture"], path_to_avatar)
            user.avatar = path_to_avatar
    return
