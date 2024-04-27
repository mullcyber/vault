"""Download content from the es index to the csv files"""
import csv
from typing import Any

import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-eh", help="IP ElasticSearch")
parser.add_argument(
    "-ak",
    default=None,
    required=False,
    help="ApiKey ElasticSearch",
)
parser.add_argument(
    "-i",
    help=("The list of indicies in one string; Indices separate by ','."
          "Example: indexA,indexB,IndexC"),
)


class CSVWriter:
    def __init__(self, host: str, indicies: list[str], api_key: str = None) -> None:
        self.auth_header = {"Authorization": f"ApiKey {api_key}"}
        ssl = "https://" if api_key else "http://"
        self.url = f"{ssl}{host}:9200"
        self.indicies = indicies

    def __prepare_data(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"_id": document["_id"]} | document["_source"]
            for document in data.get("hits").get("hits")
        ]

    def write(self) -> None:
        for index in self.indicies:
            self._load_and_write_index(index)

    def _load_and_write_index(self, index_name: str) -> None:
        index_data = self._load_index_data(index_name)
        self._write_to_csv(index_name, index_data)

    def _load_index_data(self, index_name: str) -> list[dict[str, Any]]:
        url = (
            f"{self.url}/{index_name}/_search?size=10000"
            "&filter_path=hits.hits._source,hits.hits._id"
        )
        response = requests.post(url, headers=self.auth_header)
        if response.status_code != 200:
            raise AttributeError(f"Load index {index_name} failed: {response.text}")
        return self.__prepare_data(response.json())

    def _write_to_csv(self, index_name: str, documents: list[dict[str, Any]]) -> None:
        """Write index data to a CSV file."""
        fieldnames = documents[0].keys()
        try:
            with open(
                f"{index_name}.csv", mode="w", newline="", encoding="utf-8"
            ) as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(fieldnames)
                writer.writerows(map(dict.values, documents))
        except Exception as e:
            error = e
            msg = f"❗{e.__class__.__name__}:" f"\n\tcode = None\n\tdetail = {error}"
            raise AttributeError(msg)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.eh is None or args.i is None:
        raise AttributeError()
    indicies = args.i.strip().replace(" ", "").split(",")
    CSVWriter(host=args.eh, indicies=indicies, api_key=args.ak).write()
