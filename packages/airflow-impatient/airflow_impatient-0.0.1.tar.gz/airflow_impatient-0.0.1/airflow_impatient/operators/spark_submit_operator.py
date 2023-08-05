# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import os
import signal
from builtins import bytes
from subprocess import Popen, STDOUT, PIPE
from tempfile import gettempdir, NamedTemporaryFile

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.file import TemporaryDirectory
from airflow.utils.operator_helpers import context_to_airflow_vars


class SparkSubmitOperator(BaseOperator):
    """
    This class is derived from the build-in BashOperator,
     and is used to disable some logging for security concern and detect Spark job status.
    """
    template_fields = ('spark_submit_command', 'env')
    template_ext = ('.sh', '.bash',)
    ui_color = '#f0ede4'

    @apply_defaults
    def __init__(self,
                 spark_submit_command,
                 xcom_push=False,
                 env=None,
                 output_encoding='utf-8',
                 *args, **kwargs):

        super(SparkSubmitOperator, self).__init__(*args, **kwargs)
        self.spark_submit_command = spark_submit_command
        self.env = env
        self.xcom_push_flag = xcom_push
        self.output_encoding = output_encoding

    def execute(self, context):
        """
        Execute the the spark-submit bash command in a temporary directory
        which will be cleaned afterwards
        """
        self.log.info('Tmp dir root location: \n %s', gettempdir())

        # Prepare env for child process.
        if self.env is None:
            self.env = os.environ.copy()

        airflow_context_vars = context_to_airflow_vars(context, in_env_var_format=True)
        self.log.info('Exporting the following env vars:\n' +
                      '\n'.join(["{}={}".format(k, v)
                                 for k, v in
                                 airflow_context_vars.items()]))
        self.env.update(airflow_context_vars)

        self.lineage_data = self.spark_submit_command

        with TemporaryDirectory(prefix='airflowtmp') as tmp_dir:
            with NamedTemporaryFile(dir=tmp_dir, prefix=self.task_id) as tmp_file:
                tmp_file.write(bytes(self.spark_submit_command, 'utf_8'))
                tmp_file.flush()
                script_location = os.path.abspath(tmp_file.name)
                self.log.info('Temporary script location: %s', script_location)

                def pre_exec():
                    # Restore default signal disposition and invoke setsid
                    for sig in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                        if hasattr(signal, sig):
                            signal.signal(getattr(signal, sig), signal.SIG_DFL)
                    os.setsid()

                sub_process = Popen(
                    ['bash', tmp_file.name],
                    stdout=PIPE,
                    stderr=STDOUT,
                    cwd=tmp_dir,
                    env=self.env,
                    preexec_fn=pre_exec)

                self.sub_process = sub_process

                self.log.info('Output:')
                line = ''
                job_succeed = True
                for raw_line in iter(sub_process.stdout.readline, b''):
                    line = raw_line.decode(self.output_encoding).rstrip()
                    self.log.info(line)
                    if 'Exit code' in line:
                        exit_code = int(line.split(":")[1].strip())
                        if exit_code != 0:
                            job_succeed = False

                sub_process.wait()

                self.log.info('Command exited with return code %s', sub_process.returncode)

                if sub_process.returncode:
                    raise AirflowException('Bash command failed')

                if not job_succeed:
                    raise AirflowException('Your Spark job failed!')

        if self.xcom_push_flag:
            return line

    def on_kill(self):
        self.log.info('Sending SIGTERM signal to bash process group')
        os.killpg(os.getpgid(self.sub_process.pid), signal.SIGTERM)
