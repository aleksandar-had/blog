import json
import requests
import uuid
from flask_babel import _
from app import app


def translate(text, source_language, dest_language):
    if (
        "MS_TRANSLATOR_KEY" not in app.config
        or not app.config["MS_TRANSLATOR_KEY"]
    ):
        return _("Error: the translation service is not configured.")

    path = "/translate?api-version=3.0"
    params = f"&from={source_language}&to={dest_language}"
    constructed_url = (
        "https://api.cognitive.microsofttranslator.com" + path + params
    )

    body = [{"text": text}]
    headers = {
        "Ocp-Apim-Subscription-Key": app.config["MS_TRANSLATOR_KEY"],
        "Ocp-Apim-Subscription-Region": "westeurope",
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    r = requests.post(constructed_url, headers=headers, json=body)
    if r.status_code != 200:
        return _("Error: the translation service failed.")
    return (
        json.loads(r.content.decode("utf-8-sig"))[0]
        .get("translations")[0]
        .get("text")
    )
