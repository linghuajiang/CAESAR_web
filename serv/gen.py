"Generate json file"
import ast
import json
from pprint import pprint
import jinja2
import os

def gen_json(chr, p11, p12, p21, p22, pid, ):
    context = {
        "chr_1" : "chr7",
        "start_1": 100431452,
        "end_1": 100449162,
        "chr_2": "chr7",
        "start_2": 100482500,
        "end_2": 100490325,
        "idn": 0,
        "label":"MAIN",
        "port": 3000
    }
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'templates'
    )
    print(jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)).get_template("template.json").render(context))

gen_json()
