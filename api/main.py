from fastapi import FastAPI
from neomodel import config, db
import graphene

from starlette.graphql import GraphQLApp

from schema import schema

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
config.DATABASE_URL = f'bolt://{USERNAME}:{PASSWORD}@localhost:7687'

app.add_route("/graphql/", GraphQLApp(schema=schema))


