"""Populate the database with fixture data

"""

import json
from importlib import import_module

from todo_api.constants import FIXTURES
from todo_api.db import db


def load_fixtures():
    with open(FIXTURES) as fixture_file:
        fixtures_data = json.load(fixture_file)

    for fixture in fixtures_data:
        data = fixture["data"]
        module_path = fixture["module"]
        model_name = fixture["model"]

        model = getattr(import_module(module_path), model_name)

        if model.query.count():
            continue

        for item in data:
            obj = model(**item)
            db.session.add(obj)

        db.session.commit()
