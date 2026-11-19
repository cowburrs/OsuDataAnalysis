import json
import os
import tempfile
from datetime import date
from time import sleep

import pandas as pd
from ossapi import Ossapi, serialize_model
from ossapi.models import UserStatistics
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
for user_id in tqdm(users["user_id"], desc="Snapshot"):
    user = api.user(int(user_id))
    stats = user.statistics
    if stats is None:
        tqdm.write(f"no statistics for {user_id}")
        continue
    userstats = to_dict(stats)
    userstats["user_id"] = int(user_id)
    data.append(userstats)
    sleep(1)
json.dump(
    data, open(f"./data/snapshots/{date.today().isoformat()}.json", "w"), indent=2
)
