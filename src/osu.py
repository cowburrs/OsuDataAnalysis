import json
import os
import tempfile
from datetime import date
from time import sleep

import pandas as pd
from ossapi import Ossapi, serialize_model
from ossapi.models import UserStatistics


def to_dict(obj):
    return {
        k: v
        for k in dir(obj)
        if not k.startswith("_")
        and isinstance(v := getattr(obj, k), (int, float, str, bool, type(None)))
    }


api = Ossapi(
    int(os.environ["OSU_CLIENT_ID"]),
    os.environ["OSU_CLIENT_SECRET"],
    token_directory=tempfile.gettempdir(),
)

users = pd.read_csv("./data/input/random_users.csv")
data = []
for user_id in users["user_id"][:5]:

    user = api.user(user_id)
    stats = user.statistics
    if stats is not None:
        userstats = to_dict(user.statistics)
        userstats["user_id"] = user_id
        data.append(userstats)
    else:
        print("Error for some reason")
    print(f"did {user.username}")
    sleep(1)
json.dump(
    data, open(f"./data/snapshots/{date.today().isoformat()}.json", "w"), indent=2
)
