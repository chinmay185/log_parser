from logfmt import parse
from io import StringIO
import pandas as pd
import re
import os
import sys
import json


class Log:
    def __init__(self, time, model, sdk_version, transaction_id, ip, latency, path, status_code):
        self.time = time
        self.model = model
        self.transaction_id = transaction_id
        self.ip = ip
        self.latency = latency
        self.path = path
        self.status_code = status_code
        self.sdk_version = sdk_version

    def get_attributes(self):
        return [self.time, self.model, self.sdk_version, self.transaction_id, self.ip, self.latency, self.path, self.status_code]


class Parser:
    def __init__(self):
        pass

    def get_logs(self, jsonfile):
        df = pd.read_json(jsonfile)
        return df

    def parse_logs(self, df):
        for ind in df.index:
            logline = Log(0, 0, 0, "NULL", 0, 0, 0, 0)
            message = StringIO(df["events"][ind]["message"])
            for values in parse(message):
                for key, value in values.items():
                    if key == "path":
                        logline.path = value

                    elif key == "status":
                        logline.status_code = value

                    elif key == "time":
                        # convert it to IST
                        logline.time = value

                    elif key == "ip":
                        logline.ip = value

                    elif key == "latency":
                        logline.latency = value

                    elif key == "headers":
                        for ele in value[4:-1:].split("] "):
                            if "X-Tv-Sdk-Version" in ele:
                                logline.sdk_version = ele.replace(":[", "").replace(
                                    "]", "").replace("X-Tv-Sdk-Version", "")

                            elif "X-Tv-Device-Model" in ele:
                                logline.model = ele.replace(" ", "_").replace(
                                    ":[", " ").replace("X-Tv-Device-Model", "")

                            elif "X-Tv-Transaction" in ele:
                                logline.transaction_id = ele.replace(":[", " ").replace(
                                    "]", "").replace("X-Tv-Transaction", "")
                    else:
                        continue
            print(' '.join(logline.get_attributes()))


if __name__ == "__main__":
    # cmd = 'papertrail --min-time "yesterday at 1pm" --max-time "yesterday at 2pm" -j "vil-prod-api android AND (path=/v1/compare_faces_sync OR path=/v1/verify_face_liveness_sync OR path=/v1/verify_portrait_sanity OR path=/v1/verify_id_card_sanity_sync OR path=/v1/read_id_card_info_sync OR path=/v1/images OR path=/v1/client_settings)" > dummy.json'
    # cmd = 'papertrail -j "vil-prod-api android AND (path=/v1/compare_faces_sync OR path=/v1/verify_face_liveness_sync OR path=/v1/verify_portrait_sanity OR path=/v1/verify_id_card_sanity_sync OR path=/v1/read_id_card_info_sync OR path=/v1/images OR path=/v1/client_settings)" > dummy.json'
    # os.system(cmd)

    # Taking input from terminal
    # x = sys.stdin.readlines()
    # x = json.dumps(x)
    # df = p.get_logs(x)

    p = Parser()
    df = p.get_logs("dummy.json")
    p.parse_logs(df)
