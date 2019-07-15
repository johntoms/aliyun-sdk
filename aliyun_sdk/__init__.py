# BuildIn Packages
import json

# Part3 Packages
import xmltodict
import requests
from retry import retry

retry_for_requests = retry((requests.ConnectionError, requests.Timeout), tries=3, delay=1, backoff=2, jitter=(1, 2))


def parse_response(response):
    resp_content_type = response.headers.get('content-type') or ''
    resp_content_type = resp_content_type.lower().split(';')[0].strip()

    if resp_content_type == 'application/json':
        return json.loads(response.text)

    elif resp_content_type == 'text/xml':
        return xmltodict.parse(response.text)

    else:
        try:
            return json.loads(response.text)

        except ValueError:
            try:
                return xmltodict.parse(response.text)

            except xmltodict.expat.ExpatError:
                return response.content

            except:
                raise

        except:
            raise
