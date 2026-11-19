import json
import os
import tempfile
from datetime import date
from time import sleep

import pandas as pd
from ossapi import Ossapi, serialize_model
from ossapi.models import UserStatistics
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm


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


@sleep_and_retry
@limits(calls=1, period=1)
def callapi(user_id):
    user = api.user(int(user_id))
    stats = user.statistics
    userstats = to_dict(stats)
    userstats["user_id"] = int(user_id)
    data.append(userstats)


for user_id in tqdm(users["user_id"], desc="Snapshot"):
    callapi(user_id)
json.dump(
    data, open(f"./data/snapshots/{date.today().isoformat()}.json", "w"), indent=2
)
