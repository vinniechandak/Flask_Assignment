from flask import Flask, request, send_file
import json
import csv
from datetime import datetime
from collections import OrderedDict
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

app = Flask(__name__)


@app.route("/get_csv")
def get_csv():
    return send_file('presidents.csv', mimetype='text/csv', attachment_filename='presidents.csv', as_attachment=True)


@app.route("/response", methods=['GET', 'POST'])
def response():
    json_content = request.json
    if json_content is not None:
        print(json_content)
    else:
        return "Invalid JSON Error!"

    president_infos = json.loads(json_content, object_hook=lambda d: Namespace(**d))
    print(president_infos)

    # Get All Presidents which are not from Federalist Party
    presidents_without_federalist_party = get_all_presidents_without_federalist_party(president_infos)
    # Make the first name of all presidents into reverse order
    presidents_with_reverse_first_name = get_reverse_first_name_president_info(presidents_without_federalist_party)
    # Create acronym for the party
    presidents_with_party_acronyms = get_acronym_for_party_info(presidents_with_reverse_first_name)
    # Get only start term information for all the presidents
    presidents_with_only_start_term = get_president_start_term_info(presidents_with_party_acronyms)
    # Group all the presidents by century in which they were in power
    presidents_grouped_by_centuries = get_century_wise_presidents(presidents_with_only_start_term)

    presidents_data = []
    for key, value in presidents_grouped_by_centuries:
        presidents_sorted_data = get_sorted_president_info(value)
        for president_info in presidents_sorted_data:
            presidents_data.append(president_info)

    # Generate CSV File for download
    generate_csv(presidents_data)
    return "Request processed!"


def get_all_presidents_without_federalist_party(president_infos):
    for president_info in president_infos:
        if "Federalist" not in president_info.pp:
            yield president_info


def get_reverse_first_name_president_info(president_infos):
    for president_info in president_infos:
        president_info.nm = president_info.nm.split()[0][::-1]
        yield president_info


def get_acronym_for_party_info(president_infos):
    for president_info in president_infos:
        if "-" in president_info.pp:
            president_info.pp = president_info.pp.split("-")[0][0] + president_info.pp.split("-")[1][0]
        else:
            president_info.pp = president_info.pp[0]
        yield president_info


def get_president_start_term_info(president_infos):
    presidents = []
    for president_info in president_infos:
        if "-" in president_info.tm:
            president_info.tm = president_info.tm.split("-")[0]
        presidents.append(president_info)
    return presidents


def __get_century_for_year(year):
    if year % 100 == 0:
        return int(year/100)
    else:
        return int(year/100 + 1)


def get_century_wise_presidents(president_infos):
    output = {}
    for president_info in president_infos:
        president_info.century = __get_century_for_year(int(president_info.tm))
        if president_info.century in output:
            output[president_info.century].append(president_info)
        else:
            output[president_info.century] = [president_info]
    output = OrderedDict(sorted(output.items()))
    return output.items()


def get_sorted_president_info(president_infos):
    return sorted(list(president_infos), key=lambda a: a.nm)


def generate_csv(president_infos):
    with open("presidents.csv", mode="w", newline="") as writer:
        writer = csv.writer(writer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Name", "Party", "Presidential term", "President Number", "Ingestion Time"])
        for president_info in list(president_infos):
            writer.writerow([president_info.nm, president_info.pp, president_info.tm,
                             president_info.president, datetime.now().strftime('%Y/%m/%d %H:%M:%S')])


if __name__ == '__main__':
    app.run(port=4050)
