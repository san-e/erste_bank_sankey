import matplotlib.pyplot as plt
from sankeyflow import Sankey
import json
from collections import defaultdict
import re
import os
from datetime import datetime


def generate_and_save(data):
    eingänge = defaultdict(list)
    ausgänge = defaultdict(list)

    groups = {
        re.compile(r".*(REWE).*", flags=re.IGNORECASE): "Lebensmittel",
        re.compile(r".*(LIDL).*", flags=re.IGNORECASE): "Lebensmittel",
        re.compile(r".*(BILLA).*", flags=re.IGNORECASE): "Lebensmittel",
        re.compile(r".*(HOFER).*", flags=re.IGNORECASE): "Lebensmittel",
        re.compile(r".*(PENNY).*", flags=re.IGNORECASE): "Lebensmittel",
        re.compile(r".*(SPAR).*", flags=re.IGNORECASE): "Lebensmittel",
        re.compile(r".*(MCDONALDS).*", flags=re.IGNORECASE): "Gastronomie",
        re.compile(r".*(MENSA).*", flags=re.IGNORECASE): "Gastronomie",
        re.compile(r".*(DM\-FIL).*", flags=re.IGNORECASE): "Drogerie",
        re.compile(r".*(Apotheke).*", flags=re.IGNORECASE): "Drogerie",
        re.compile(r".*(WIEN Energie).*", flags=re.IGNORECASE): "Wohnen",
        re.compile(r".*(Oberlojer).*", flags=re.IGNORECASE): "Wohnen",
        re.compile(r".*(GREEN & CLEAN).*", flags=re.IGNORECASE): "Wohnen",
        re.compile(r".*(DB).*"): "Mobilität",
        re.compile(r".*(WIENER L).*", flags=re.IGNORECASE): "Mobilität",
        re.compile(r".*", flags=re.IGNORECASE): "Sonstiges",
    }

    einkommen = 0
    ausgaben = 0

    for l in data:
        if l["partnerName"] == None:
            continue

        if l["amount"]["value"] >= 0:
            wert = l["amount"]["value"] / 100
            einkommen += wert
            eingänge[l["partnerName"]].append(wert)
        else:
            wert = l["amount"]["value"] / 100 * -1
            ausgaben += wert
            ausgänge[l["partnerName"]].append(wert)

    flows = list()

    for name, amount in eingänge.items():
        flag = False
        if name in ausgänge.keys():
            to_remove = []
            for wert in ausgänge[name]:
                if wert in amount:
                    to_remove.append(wert)
                    flag = True
            for wert in to_remove:
                ausgänge[name].pop(ausgänge[name].index(wert))

        if flag:
            continue

        flow = (name, "Einkommen", sum(amount))
        flows.append(flow)

    a = list()

    for name, amount in ausgänge.items():
        for regex, group in groups.items():
            if regex.findall(name):
                name = group
                break
        flow = ("Einkommen", name, sum(amount))
        a.append(flow)
    a.sort(key=lambda x: x[1])

    for entry in a:
        flows.append(entry)

    flows.append(("Einkommen", "Ersparnis", einkommen - ausgaben))

    nodes = Sankey.infer_nodes(flows=flows)
    for a in nodes[2]:
        a.append({"label_pos": "right"})

    s = Sankey(
        flows=flows, nodes=nodes, node_opts=dict(label_format="{label} €{value:.2f}")
    )
    plt.figure(figsize=(13, 7), dpi=100)
    plt.subplots_adjust(left=0.3, right=0.8)
    s.draw()

    filename = datetime.strptime(
        data[0]["valuation"], "%Y-%m-%dT%H:%M:%S.%f%z"
    ).strftime("%Y.%m")
    plt.savefig(f"./sankeys/{filename}.svg", format="svg")


def main():
    auszuege = os.listdir("./kontoauszüge")

    for auszug in auszuege:
        if not auszug.endswith(".json"):
            continue
        print(auszug)

        with open(f"./kontoauszüge/{auszug}", "r") as f:
            generate_and_save(json.load(f))


if __name__ == "__main__":
    main()
