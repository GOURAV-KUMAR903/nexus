from models.product_model import Product
from helpers.save_image import save_img
from helpers.view_template import render_view
from fastapi import UploadFile
from helpers.super_helper import SuperHelper
from fastapi import Request
from fastapi.encoders import jsonable_encoder
import random
import json
from fastapi import FastAPI
import os
import secrets  # <-- add this at the top
from constants import CURRENCY, BASE_URL  # import constants
from datetime import datetime, timedelta

def Autodelete_Cron(request: Request):
    today = datetime.now().date()

    cron = SuperHelper.get_single_record(
        "tbl_cron",
        {"date": today, "cron_name": "Autodelete_Cron"}
    )

    if not cron:
        SuperHelper.add("tbl_cron", {
            "cron_name": "Autodelete_Cron",
            "date": today
        })
        records = SuperHelper.get_records("tbl_addresses")
        for rec in records:
            date1 = datetime.now()
            date2 = rec["created_at"] + timedelta(hours=1)

            diff = (date1 - date2).total_seconds()

            print(f"{diff} / {rec['id']}")

            if diff >= 0:
                check = SuperHelper.get_single_record(
                    "tbl_orders",
                    {"secret_key": rec['secret_key']}
                )

                if not check:
                    SuperHelper.delete_record(
                        "tbl_addresses",
                        {"id": rec['id']}
                    )

        return {"message": "Cron executed successfully"}  # ✅

    else:
        return {"message": "Today cron already run!"}
         