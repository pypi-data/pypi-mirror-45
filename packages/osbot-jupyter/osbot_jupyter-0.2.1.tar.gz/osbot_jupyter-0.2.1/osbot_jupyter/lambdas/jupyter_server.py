def run(event, context):
    url       = event.get('url')
    token     = event.get('token')
    notebook = event.get('notebook')

    from osbot_jupyter.api.Jupyter import Jupyter
    jp = Jupyter().set_url(url).set_token(token)
    jp.login()
    jp.open_notebook(notebook)
    #return jp.browser().sync__url()
    return jp.screenshot_base64()
