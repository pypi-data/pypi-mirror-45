from osbot_aws.apis.Lambda import Lambda


class GSBot_Execution:

    def __init__(self):
        self._lambda = Lambda('osbot.lambdas.osbot')

    def invoke(self,command):
        payload = {'event': {'type': 'message',
                             'text': command,
                             'user': 'jovyan'}}

        result = self._lambda.invoke(payload)
        text = result.get('text')
        attachments = result.get('attachments')
        return text,attachments