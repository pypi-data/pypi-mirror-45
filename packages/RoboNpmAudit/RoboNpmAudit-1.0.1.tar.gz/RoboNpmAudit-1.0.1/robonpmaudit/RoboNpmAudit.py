import docker
from robot.api import logger
from docker.types import Mount
import requests

class RoboNpmAudit(object):

    def __init__(self):
        self.client = docker.from_env()
        self.npm_audit_docker = "abhaybhargav/npmaudit"

    def run_npmaudit_against_source(self, code_path, results_path):
        self.source_path = code_path
        self.results_path = results_path
        source_mount = Mount("/src", self.source_path, type = "bind")
        results_mount = Mount("/results", self.results_path, type = "bind")
        self.client.containers.run(self.npm_audit_docker, mounts = [source_mount, results_mount])
        logger.info("Successfully ran NPM Audit against the src. Please find the *.json files in the results directory")

    def npmaudit_write_to_orchy(self, report_file, secret, access, hook_uri):
        """
                Generates an XML Report and writes said report to orchestron over a webhook.

                Mandatory Fields:
                - Report_file: Absolute Path of Report File - JSON or XML
                - Token: Webhook Token
                - hook_uri: the unique URI to post the XML Report to

                Examples:

                | zap write to orchy  | report_file_path | token | hook_uri

        """
        # xml_report = self.zap.core.xmlreport()
        # with open('zap_scan.xml','w') as zaprep:
        #     zaprep.write(xml_report)
        try:
            files = {'file': open(report_file, 'rb')}
            auth = {'Secret-Key': secret, 'Access-Key': access}
            r = requests.post(hook_uri, headers=auth, files=files)
            if r.status_code == 200:
                return "Successfully posted to Orchestron"
            else:
                raise Exception("Unable to post successfully")
        except Exception as e:
            print(e)
