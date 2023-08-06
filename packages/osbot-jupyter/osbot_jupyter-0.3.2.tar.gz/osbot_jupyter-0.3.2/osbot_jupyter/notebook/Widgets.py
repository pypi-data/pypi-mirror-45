from __future__ import print_function
from ipywidgets import interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display


class Widgets:

    # @staticmethod
    # def f(x):
    #     return x * 3

    def ping_1(self):
        def f(aa_aa,b,c):
            display(aa_aa + b)
            return aa_aa * 2

        w = interactive(f, aa_aa=10,b=20,c=30)
        display(w)
        #f(40,2)
        #return w.children
        #return interact(self.f, x=10);
        #return 'pong'

    def ping_2(self):
        # a = widgets.IntSlider()
        # b = widgets.IntSlider()
        # c = widgets.IntSlider()
        # ui = widgets.HBox([a, b, c])
        #
        # def f(a, b, c):
        #     print((a, b, c))
        #
        # out = widgets.interactive_output(f, {'a': a, 'b': b, 'c': c})
        #
        # display(ui, out)

        #a = widgets.Text('this is a value')
        #b = widgets.FloatSlider()

        a = widgets.Textarea(value='Hello World',
                             placeholder='Type something',
                             description='String:',
                             disabled=False)
        b = widgets.Textarea(value='',
                             placeholder='Type something',
                             description='String:',
                             disabled=False)
        c = widgets.ToggleButtons(
            options=['Slow ', 'Regular', 'Fast '],
            description='Speed:',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
            icons=['check','','check']
        )
        display(a,b,c)
        return a.value

        #mylink = widgets.jslink((a, 'value'), (b, 'value'))

    def ping(self):
        from IPython.display import display
        button = widgets.Button(description="Click Me!")
        display(button)

        def on_button_clicked(b):
            print("Button clicked.... in another cell ")

        button.on_click(on_button_clicked)