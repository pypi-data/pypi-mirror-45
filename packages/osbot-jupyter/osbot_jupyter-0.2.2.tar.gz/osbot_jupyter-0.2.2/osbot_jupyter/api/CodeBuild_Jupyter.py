from time import sleep

from osbot_aws.apis.CodeBuild import CodeBuild
from osbot_aws.apis.IAM import IAM
from osbot_aws.apis.Logs import Logs
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Local_Cache import use_local_cache_if_available
from pbx_gs_python_utils.utils.Misc import Misc


class CodeBuild_Jupyter_Helper:
    def __init__(self):
        self.project_name = 'OSBot-Jupyter'
        self.code_build   = CodeBuild(project_name=self.project_name,role_name=None)
        self.max_builds   = 10

    def get_active_build_id(self):
        builds = self.get_active_builds(stop_when_match=True)
        return Misc.array_pop(list(set(builds)))

    def get_active_builds(self, stop_when_match=False):
        build_ids   = list(self.code_build.project_builds_ids(self.project_name))[0:self.max_builds]
        build_infos = self.code_build.codebuild.batch_get_builds(ids=build_ids).get('builds')
        builds = {}
        for build_info in build_infos:
            build_id = build_info.get('id')
            if build_info.get('currentPhase') != 'COMPLETED':
                builds[build_id] = CodeBuild_Jupyter(build_id=build_id, build_info=build_info)
                if stop_when_match:
                    return builds
        return builds

    def start_build(self):
        build_arn =self.code_build.build_start()
        build_id = build_arn.split('build/').pop()
        return CodeBuild_Jupyter(build_id=build_id)

    def start_build_and_wait_for_jupyter_load(self, max_seconds=60):
        seconds_sleep = 5
        build = self.start_build()
        for i in range(0,max_seconds,seconds_sleep):
            sleep(seconds_sleep)
            #print("after #{0}".format(i))
            (url,_) = build.get_server_details_from_logs()
            if url is not None:
                return build


    def stop_all_active(self):
        available_builds = CodeBuild_Jupyter_Helper().get_active_builds()
        stopped = []
        for build_id in available_builds.keys():
            self.code_build.codebuild.stop_build(id=build_id).get('build')
            stopped.append(build_id)
        return stopped

    def save_active_server_details(self, file):
        build_id     = self.get_active_build_id()
        server,token = CodeBuild_Jupyter(build_id).get_server_details_from_logs()
        config = { 'build_id': build_id,
                   'server'  : server  ,
                   'token'   : token   }
        Json.save_json(file, config)
        return config



class CodeBuild_Jupyter:
    def __init__(self, build_id, build_info=None):
        self.project_name = 'OSBot-Jupyter'
        self.code_build   = CodeBuild(project_name=self.project_name,role_name=None)
        self.build_id     = build_id
        self._build_info  = build_info

    def build_info(self, reload_data=False):
        if reload_data or self._build_info is None:
            self._build_info = self.code_build.build_info(self.build_id)
        return self._build_info

    def build_status(self):
        return self.build_info(reload_data=True).get('buildStatus')

    def build_phase(self):
        return self.build_info(reload_data=True).get('currentPhase')

    def build_log_messages(self):
        build_info = self.build_info()
        group_name = build_info.get('logs').get('groupName')
        stream_name = build_info.get('logs').get('streamName')
        logs = Logs(group_name=group_name, stream_name=stream_name)
        return logs.messages()

    def build_stop(self):
        self.code_build.codebuild.stop_build(id=self.build_id).get('build')
        return self.build_status()

    def get_server_details_from_logs(self):
        def find_in(array, text):
            return [item for item in array if text in item]

        try:
            messages = self.build_log_messages()
            ngrok_url      = find_in(messages, 'name=command_line addr')[0].split('url=')[1].strip()
            jupyter_token  = find_in(messages, 'token=')[0].split('token=')[1].strip()
            return ngrok_url,jupyter_token
        except:
            return None,None

    def url(self):
        ngrok_url, jupyter_token = self.get_server_details_from_logs()
        if ngrok_url:
            return "{0}?token={1}".format(ngrok_url,jupyter_token)