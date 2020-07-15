from flask import *
import autodynatrace
import oneagent
import json
import mistune
import html

from os import listdir
from os.path import isfile, join
from xml.sax import saxutils as su

from oneagent.common import DYNATRACE_HTTP_HEADER_NAME
app = Flask("Dynatrace Support Lab Landing Page")

init_result = oneagent.initialize()
print('OneAgent SDK initialization result' + repr(init_result))
if init_result:
    print('SDK should work (but agent might be inactive).')
else:
    print('SDK will definitely not work (i.e. functions will be no-ops):', init_result)

sdk = oneagent.get_sdk()

def getMenuConfig():
    ''' getMenuConfig: a function that handles getting the configuration for the menu '''

    mypath = './sourceFiles'
    returnObject = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    with open('./configFiles/linkInfo.json', 'w') as fp:
        json.dump(returnObject, fp)

    dict_menuData = dict()

    try:
        with open('./configFiles/linkInfo.json') as json_configMenu:
            list_menuData = json.load(json_configMenu)
        for x in list_menuData:
            dict_menuData[x[0:-3]] = str("./" + x[0:-3])
    except Exception as error:
        dict_menuData = None

        print(error)
    return dict_menuData



@autodynatrace.trace

@app.route("/debug", methods=['GET'])
def debug():

    mypath = './sourceFiles'
    returnObject = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    with open('./configFiles/linkInfo.json', 'w') as fp:
        json.dump(returnObject, fp)
    return str(returnObject)

@app.route("/<url_pass>", methods=['GET'])
def non_index(url_pass):
    ''' standards: a function that handles the request for the standards page'''
    try:
        with open('./sourceFiles/' + url_pass + '.md') as string_markDown:
            string_markDownText = Markup(html.unescape(mistune.markdown(string_markDown.read())))
            print(url_pass)
    except Exception as error:
        string_markDownText = None
        print(error)
    return render_template("layout.html", string_markDownText=string_markDownText, dict_menuData=getMenuConfig())

@app.route("/", methods=['GET'])
def index():
    ''' standards: a function that handles the request for the standards page'''
    try:
        with open('./sourceFiles/markdown_index.md') as string_markDown:
            string_markDownText = Markup(html.unescape(mistune.markdown(string_markDown.read())))
            print(url_pass)
    except Exception as error:
        string_markDownText = None
        print(error)
    return render_template("layout.html", string_markDownText=string_markDownText, dict_menuData=getMenuConfig())



if __name__ == "__main__":
    app.run('0.0.0.0')