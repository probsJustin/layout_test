from flask import *
import autodynatrace
import oneagent
import json
import mistune
import html
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
    ''' getMenuConfig: a function that handles getting the configuration for the menu'''
    try:
        with open('./sourceFiles/json_config_menu.json') as json_configMenu:
            dict_menuData = json.load(json_configMenu)
    except Exception as error:
        dict_menuData = None
        print(error)
    return dict_menuData



@autodynatrace.trace
@app.route("/<url_pass>", methods=['GET'])
def standards(url_pass):
    ''' standards: a function that handles the request for the standards page'''
    try:
        with open('./sourceFiles/markdown_' + url_pass + '.md') as string_markDown:
            string_markDownText = Markup(html.unescape(mistune.markdown(string_markDown.read())))
            print(url_pass)
    except Exception as error:
        string_markDownText = None
        print(error)
    return render_template("layout.html", string_markDownText=string_markDownText, dict_menuData=getMenuConfig())

if __name__ == "__main__":
    app.run('0.0.0.0')