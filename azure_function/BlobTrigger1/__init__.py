import azure.functions as func
import numpy as np
from PIL import Image
from io import BytesIO
import json
import base64
import os
import pyodbc


def main(myblob: func.InputStream):
    if myblob.name[-5:] == ".json":
        file_json = json.loads(myblob.read())
        file_name = file_json["path"].split("/")[-1]

        img = np.array(Image.open(
            BytesIO(base64.b64decode(file_json["content"]))))
        px_count = int(np.sum(img))

        db_connection_str = os.environ["db_connection_str"]
        with pyodbc.connect(db_connection_str) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO processed_data(filename, pixel_count)
                    VALUES ('{file_name}', '{px_count}')
                    """)
                cursor.commit()   
