import json

from IPython.display import display, HTML, Javascript
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_Vis_Js:
    def __init__(self):
        self.require_js = {"paths": {"vis": "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min" }}
        #self.test = 42

    #def invoke(js_code):

    def js_invoke(self,div_id, code):
        js_code = "requirejs.config({0});\n".format(json.dumps(self.require_js)) + \
                  "require(['vis'], function(vis) {\n\n" +  code + "\n\n})";

        display(HTML("<div id='{0}'></div>".format(div_id)))
        display(Javascript(js_code))

        return


    def test_vis(self):
        nodes = [{"id": 1, "label": '1st label'},
                 {"id": 2, "label": '2nd label'}]
        edges = [{"from": 1, "to": 2, "arrows": 'to'}]
        options = {"height": "200px", "nodes": {"shape": "box", "color": "lightgreen"}}
        self.show_vis(nodes, edges,options)

    def show_vis(self,nodes, edges, options):
        div_id = Misc.random_string_and_numbers(prefix='network_')
        print(div_id)


        js_code = """            
                        var container = document.getElementById('{0}');
                        var data= {{
                            nodes: {1},
                            edges: {2}
                        }};
                        var options = {3}         
                        window['_{0}'] = new vis.Network(container, data, options);    
                  """.format(div_id, json.dumps(nodes), json.dumps(edges),options)
        self.js_invoke(div_id,js_code)


    # display(Javascript(data=js_code,lib=['https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js']))
    # #text = Misc.random_string_and_numbers()
    #     html =  """ <h2 id='aaa'> this is html: {0}</h2> ...
    #                 <script>
    #                     $('h2#aaa').text(window.text)
    #                 </script>
    #             """

    # IPython.notebook.kernel.execute("a=42")