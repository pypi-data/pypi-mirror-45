import json

from IPython.display import display, HTML, Javascript,IFrame
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_Go_Js:

    def __init__(self):
        self.frame_id = Misc.random_string_and_numbers(prefix='go_view_')
        self.frame_id = 'go_view_12345'
        self.src      = '/view/html/go-js/incremental-tree.html'
        self.nodes    = []                                          # keep track of nodes added
        pass

    def add_iframe(self):
        iframe_code = "<iframe id='{0}' src='{1}' width='{2}' height='{3}'></iframe>".format(
                        self.frame_id, self.src, "100%",800)
        display(HTML(iframe_code))
        display(Javascript("$('.output_stderr').hide()"))

        #display(IFrame(src=self.src, width=800, height=300,id=self.frame_id, abc="aaaaa" ))

    def invoke_method(self, js_method, params=None):
        data = json.dumps({'method': js_method, 'params': params})

        js_code = "{0}.contentWindow.iframe.contentWindow.postMessage({1}, '*')".format(self.frame_id, data)
        #print(self.frame_id)s
        #print(js_code)
        display(Javascript(js_code))

    def clear(self):
        self.invoke_method('clear_diagram')
        return self

    def add_node(self,key, label=None, color=None):
        if key not in self.nodes:                                   # don't add duplicate nodes
            if label is None: label = key
            if color is None: color = '#E1F5FE'
            node = {'key': key, 'label': label, 'color': color }    #'rootdistance':2}

            self.invoke_method('add_node', node)
            self.nodes.append(key)
        return self

    def add_link(self, from_key,to_key,label=None):
        #jp_go_js.invoke_method('add_link',{'from':'RISK-12','to':'RISK-1' ,'text':'aaaa'})
        self.invoke_method('add_link', {'from': from_key, 'to': to_key, 'text':label})
        #print(json.dumps({'from': from_key, 'to': to_key, 'text':label}))
        return self

    def expand_all  (self): self.invoke_method('expand_all'); return self
    def collapse_all(self): self.invoke_method('collapse_all'); return self

    def expand_node(self,key):
        self.invoke_method('expand_node', key)
        return self

    def zoom_to_fit(self):
        self.invoke_method('zoom_to_fit')

        #jp_go_js.invoke_method('add_node', {'key': 'RISK-1', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-2', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-3', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('expand_node', 'RISK-12')


    ## helper issue methods

    def add_nodes_from_issue(self, issue_key):
        from osbot_jira.api.API_Issues import API_Issues
        issue = API_Issues().issue(issue_key)
        links = issue(issue_key).get('Issue Links')
        #jp_go_js.add_iframe()
        #sleep(1)
        # jp_go_js.clear()
        self.add_node(issue_key).expand_node(issue_key)
        for link_type, values in links.items():
            link_type_key = '{0}_{1}'.format(link_type, issue_key)
            self.add_node(link_type_key, link_type, color='yellow')
            self.add_link(self, link_type_key, None)
            for link_key in values:
                self.add_node(link_key)
                self.add_link(link_type_key, link_key)



                # usefull JS queries

    # myDiagram.model.addNodeData({'key':'RISK-12'})
    # node = myDiagram.findNodeForKey("RISK-12");
    # node.diagram.commandHandler.expandTree(node)
    # node.diagram.commandHandler.collapseTree()