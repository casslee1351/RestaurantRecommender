from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine
from restaurants.models import Restaurant


class Command(BaseCommand):
    # add help =

    def handle(self, *args, **options):

        excel_file = "restaurants.xlsx"
        df = pd.read_excel(excel_file)
        engine = create_engine("sqlite:///db.sqlite3")

        df.to_sql(Restaurant._meta.db_table, con=engine,
                  if_exists='append', index=False)
