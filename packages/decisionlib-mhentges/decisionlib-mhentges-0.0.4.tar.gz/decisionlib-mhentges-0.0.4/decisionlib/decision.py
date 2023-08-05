import datetime
from enum import Enum
import json
import os
import re

from git import Repo
from typing import Optional, Tuple, List, Any, Callable

import taskcluster

from decisionlib.common import SlugId


class TrustLevel(Enum):
    L1 = 1
    L3 = 3


class Trigger:
    def __init__(self, task_group_id: SlugId, level: TrustLevel, owner: str, source: str):
        self.task_group_id = task_group_id
        self.level = level
        self.owner = owner
        self.source = source

    @staticmethod
    def from_environment():
        """Collects "DECISIONLIB_*" environment variables to create a Trigger

        Assumes that "DECISIONLIB_TASK_GROUP_ID", "DECISIONLIB_TRUST_LEVEL", "DECISIONLIB_OWNER"
        and "DECISIONLIB_SOURCE" are all set as environment variables

        Returns:
            Trigger: details of the cause of this build

        """
        task_group_id = os.environ['DECISIONLIB_TASK_GROUP_ID']
        level = TrustLevel(int(os.environ['DECISIONLIB_TRUST_LEVEL']))
        owner = os.environ['DECISIONLIB_OWNER']
        source = os.environ['DECISIONLIB_SOURCE']
        return Trigger(task_group_id, level, owner, source)


class Checkout:
    def __init__(self, product_id, html_url: str, ref: str, commit: str):
        self.product_id = product_id
        self.html_url = html_url
        self.ref = ref
        self.commit = commit

    @staticmethod
    def from_cwd():
        """Produces checkout information by checking the git repository in the current directory

        Assumes that the "origin" remote is a GitHub HTTPS URL

        Returns:
            Checkout: current source control information

        """
        repo = Repo(os.getcwd())
        remote = repo.remote()
        ref = repo.head.ref

        if not remote.url.startswith('https://github.com'):
            raise RuntimeError('Expected remote to be a GitHub repository (accessed via HTTPs)')

        if remote.url.endswith('.git'):
            html_url = remote.url[:-4]
        elif remote.url.endswith('/'):
            html_url = remote.url[:-1]
        else:
            html_url = remote.url

        product_id = remote.url.split('/')[-1]
        return Checkout(product_id, html_url, str(ref), str(ref.commit))


def write_cot_files(full_task_graph):
    with open('task-graph.json', 'w') as f:
        json.dump(full_task_graph, f)

    # These files are needed to keep chainOfTrust happy. However, they are not needed
    # for many projects at the moment. For more details, see:
    # https://github.com/mozilla-releng/scriptworker/pull/209/files#r184180585
    for file_names in ('actions.json', 'parameters.yml'):
        with open(file_names, 'w') as f:
            json.dump({}, f)


class Scheduler:
    """Assigns IDs to tasks and batch-schedules them"""
    _tasks: List[Tuple[SlugId, 'Task']]

    def __init__(self):
        self._tasks = []

    def append(self, task: 'Task'):
        task_id = taskcluster.slugId().decode('utf-8')
        self._tasks.append((task_id, task))
        return task_id

    def append_all(self, tasks: List['Task']):
        for task in tasks:
            self.append(task)

    def schedule_tasks(
            self,
            queue,
            trigger: Trigger,
            checkout: Checkout,
            write_cot_files=write_cot_files
    ):
        """Schedules all tasks in the order that they were provided to the scheduler

        Args:
            queue: taskcluster queue to append tasks to
            trigger: the details of the action that triggered this build
            checkout: source control information for the current revision
            write_cot_files: method of encoding Chain of Trust files

        Returns:

        """
        full_task_graph = {}

        for task_id, task in self._tasks:
            task = task.render(task_id, trigger, checkout)
            queue.createTask(task_id, task)
            full_task_graph[task_id] = {
                'task': queue.task(task_id)
            }

        write_cot_files(full_task_graph)


class Treeherder:
    def __init__(self, job_kind: str, machine_platform: str, tier: int, symbol: str,
                 group_symbol: str = None):
        self.symbol = symbol
        self.job_kind = job_kind
        self.tier = tier
        self.machine_platform = machine_platform
        self.group_symbol = group_symbol


class Priority(Enum):
    HIGHEST = 'highest'
    VERY_HIGH = 'very-high'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    VERY_LOW = 'very-low'
    LOWEST = 'lowest'
    NORMAL = 'normal'


class ConfigurationContext:
    product_id: str
    checkout: Checkout
    trigger: Trigger

    def __init__(
            self,
            product_id: str,
            checkout: Checkout,
            trigger: Trigger,
    ):
        self.product_id = product_id
        self.checkout = checkout
        self.trigger = trigger


class Task:
    _name: str
    _provisioner_id: str
    _payload: Any
    _decide_worker_type: Callable[[TrustLevel], str]
    _description: str
    _priority: Optional[Priority]
    _treeherder: Optional[Treeherder]
    _routes: List[str]
    _dependencies: List[SlugId]
    _scopes: List[str]
    _map_functions: List[Callable[['Task', ConfigurationContext], None]]

    def __init__(
            self,
            name: str,
            provisioner_id: str,
            decide_worker_type: Callable[[TrustLevel], str],
            payload: Any = None,
    ):
        self._name = name
        self._provisioner_id = provisioner_id
        self._payload = payload
        self._decide_worker_type = decide_worker_type
        self._description = ''
        self._routes = []
        self._dependencies = []
        self._scopes = []
        self._map_functions = []
        self._priority = None
        self._treeherder = None

    def with_description(self, description: str):
        self._description = description
        return self

    def with_priority(self, priority: Priority):
        self._priority = priority
        return self

    def with_payload(self, payload: Any):
        self._payload = payload
        return self

    def append_route(self, route: str):
        self._routes.append(route)
        return self

    def append_routes(self, routes: List[str]):
        self._routes.extend(routes)
        return self

    def append_scope(self, scope: str):
        self._scopes.append(scope)
        return self

    def append_scopes(self, scopes: List[str]):
        self._scopes.extend(scopes)
        return self

    def append_dependency(self, dependency: SlugId):
        self._dependencies.append(dependency)
        return self

    def append_dependencies(self, dependencies: List[SlugId]):
        self._dependencies.extend(dependencies)
        return self

    def with_notify_owner(self):
        return self.map(lambda task, context: task.append_route(
            'notify.email.{}.on-failed'.format(context.trigger.owner)))

    def with_treeherder(self, job_kind: str, machine_platform: str, tier: int, symbol: str,
                        group_symbol: str = None):
        self._treeherder = Treeherder(job_kind, machine_platform, tier, symbol, group_symbol)
        return self.map(lambda task, context: task.append_route(
            'tc-treeherder.v2.{}.{}'.format(context.product_id, context.checkout.commit)))

    def map(self, configuration: Callable[['Task', ConfigurationContext], None]):
        self._map_functions.append(configuration)
        return self

    def schedule(self, scheduler: Scheduler):
        return scheduler.append(self)

    def render(
            self,
            task_id: SlugId,
            trigger: Trigger,
            checkout: Checkout,
    ):
        """Produces raw Taskcluster task definition

        Should only be called by Scheduler

        Args:
            task_id: id of task
            trigger: details around the cause of this build
            checkout: source control information

        Returns:
            dict: raw taskcluster task definition

        """
        context = ConfigurationContext(checkout.product_id, checkout, trigger)
        worker_type = self._decide_worker_type(trigger.level)
        for map_function in self._map_functions:
            map_function(self, context)

        return {
            'scheduler_id': '{}-level-{}'.format(checkout.product_id, trigger.level.value),
            'taskGroupId': trigger.task_group_id,
            'provisionerId': self._provisioner_id,
            'workerType': worker_type,
            'metadata': {
                'name': self._name,
                'description': self._description,
                'owner': trigger.owner,
                'source': trigger.source,
            },
            'routes': self._routes,
            'dependencies': [task_id] + self._dependencies,
            'scopes': self._scopes,
            'payload': self._payload or {},
            'priority': self._priority.value if self._priority else None,
            'extra': {
                'treeherder': {
                    'symbol': self._treeherder.symbol,
                    'groupSymbol': self._treeherder.group_symbol,
                    'jobKind': self._treeherder.job_kind,
                    'tier': self._treeherder.tier,
                    'machine': {
                        'platform': self._treeherder.machine_platform
                    },
                } if self._treeherder else {}
            },
            'created': taskcluster.stringDate(datetime.datetime.now()),
            'deadline': taskcluster.fromNow('1 day'),
        }


class ArtifactType(Enum):
    FILE = 'file'
    DIRECTORY = 'directory'


class AndroidArtifact:
    taskcluster_path: str
    outputs_apk_path: str
    type: ArtifactType

    def __init__(self, public_path: str, outputs_apk_path: str):
        """

        Args:
            public_path: path of artifact on Taskcluster
            outputs_apk_path: path to apk within gradle's "outputs/apks/
        """
        self.taskcluster_path = public_path
        self.outputs_apk_path = outputs_apk_path
        self.type = ArtifactType.FILE

    def fs_path(self, product_id: str):
        return '/build/{}/app/build/outputs/apk/{}'.format(product_id, self.outputs_apk_path)


class ShellTask(Task):
    _image: str
    _script: str
    _artifacts: List[AndroidArtifact]
    _file_secrets: List[Tuple[str, str, str]]

    def __init__(
            self,
            name: str,
            provisioner_id: str,
            decide_worker_type: Callable[[TrustLevel], str],
            image: str,
            script: str,
    ):
        super().__init__(name, provisioner_id, decide_worker_type)
        self._image = image
        self._script = script
        self._artifacts = []
        self._file_secrets = []

    def append_artifact(self, artifact: AndroidArtifact):
        self._artifacts.append(artifact)
        return self

    def append_artifacts(self, artifacts: List[AndroidArtifact]):
        self._artifacts.extend(artifacts)
        return self

    def append_secret(self, secret: str):
        self.append_scope('secrets:get:{}'.format(secret))
        return self

    def append_file_secret(self, secret, key, target_file):
        self._file_secrets.append((secret, key, target_file))
        return self.append_secret(secret)

    def render(
            self,
            task_id: SlugId,
            trigger: Trigger,
            checkout: Checkout,
    ):
        if self._file_secrets:
            fetch_file_secrets_commands = ['pip install decisionlib-mhentges'] + [
                'decisionlib get-secret {} {} > {}'.format(secret, key, target_file)
                for secret, key, target_file in self._file_secrets
            ]
        else:
            fetch_file_secrets_commands = []

        def configuration(task: Task, context: ConfigurationContext):
            script = '\n'.join([
                """
                export TERM=dumb
                git fetch {url} {ref}
                git config advice.detachedHead false
                git checkout FETCH_HEAD
                """.format(url=context.checkout.html_url, ref=context.checkout.ref),
                *fetch_file_secrets_commands,
                self._script
            ])
            script = re.sub('\n +', '\n', script)  # de-indent

            task.with_payload({
                'features': {
                    'chainOfTrust': True if self._artifacts else False,
                    'taskclusterProxy': True if self._file_secrets else False,
                },
                'image': self._image,
                'command': ['/bin/bash', '--login', '-cxe', script],
                'artifacts': {
                    artifact.taskcluster_path: {
                        'type': artifact.type.value,
                        'path': artifact.fs_path(context.product_id),
                    }
                    for artifact in self._artifacts
                }
            })

        self.map(configuration)
        return super().render(task_id, trigger, checkout)


def shell_task(
        name: str,
        image: str,
        script: str,
):
    """Builds task that runs as shell commands in a docker container

    Args:
        name: name of task
        image: docker image
        script: commands to run within the container

    Returns:
        ShellTask: shell task builder
    """
    def decide_worker_type(level: TrustLevel):
        return 'mobile-{}-b-ref-browser'.format(level.value)

    return ShellTask(
        name,
        'aws-provisioner-v1',
        decide_worker_type,
        image,
        script,
    )


class SigningType(Enum):
    DEP = 'dep'
    RELEASE = 'release'


def sign_task(
        name: str,
        signing_format: str,
        signing_type: SigningType,
        artifacts: List[Tuple[SlugId, List[str]]],
):
    """Builds task that runs within "mobile-signing-(dep-)v1" workers

    Args:
        name: name of task
        signing_format: signing format, such as "autograph_apk"
        signing_type: what type of signing key should be used
        artifacts: task id and path to apks that this task will sign

    Returns:
        Task: task builder
    """
    payload = {
        'upstreamArtifacts': [{
            'paths': apk_paths,
            'formats': [signing_format],
            'taskId': assemble_task_id,
            'taskType': 'build'
        } for assemble_task_id, apk_paths in artifacts]
    }

    def decide_worker_type(level: TrustLevel):
        if level == TrustLevel.L1 and signing_type == SigningType.RELEASE:
            raise RuntimeError('Cannot use RELEASE signing type with a trust level of 1')

        return 'mobile-signing-dep-v1' if signing_type == SigningType.DEP else 'mobile-signing-v1'

    return Task(name, 'scriptworker-prov-v1', decide_worker_type, payload) \
        .append_dependencies([assemble_task_id for assemble_task_id, _ in artifacts]) \
        .map(
        lambda task, context: task.with_scopes([
            'project:mobile:{}:releng:signing:format:{}'.format(
                context.product_id, signing_format),
            'project:mobile:{}:releng:signing:cert:{}'.format(
                context.product_id, signing_type.value),
        ]))


def google_play_task(
        name: str,
        track: str,
        artifacts: List[Tuple[SlugId, List[str]]],
):
    """Builds task that runs within "mobile-pushapk-(dep-)v1" workers

    Args:
        name: name of task
        track: Google Play track
        artifacts: task id and path to apks that this task will push to Google Play

    Returns:
        Task: task builder
    """
    payload = {
        'commit': True,
        'google_play_track': track,
        'upstreamArtifacts': [{
            'paths': apk_paths,
            'taskId': signing_task_id,
            'taskType': 'signing'
        } for signing_task_id, apk_paths in artifacts]
    }

    def decide_worker_type(level: TrustLevel):
        return 'mobile-pushapk-dep-v1' if level == TrustLevel.L1 else 'mobile-pushapk-v1'

    return Task(name, 'scriptworker-prov-v1', decide_worker_type, payload) \
        .append_dependencies([signing_task_id for signing_task_id, _ in artifacts]) \
        .map(
        lambda task, context: task.with_scopes([
            'project:mobile:{name}:releng:googleplay:product:{name}{type}'.format(
                name=name,
                type=':dep' if context.trigger.level == TrustLevel.L1 else ''
            )
        ]))


class RemoteArtifact:
    """Represents direct URL to artifact on Taskcluster"""
    def __init__(self, task_id: str, path: str):
        self.task_id = task_id
        self.path = path

    def url(self):
        return 'https://queue.taskcluster.net/v1/task/{}/artifacts/{}'.format(self.task_id,
                                                                              self.path)


def raptor_task(
        name: str,
        signed_apk: Tuple[SlugId, str],
        mozharness_task_id: str,
        is_arm: bool,
        raptor_app_id: str,
        package_name: str,
        activity_class_name: str,
        gecko_revision: str,
):
    """Builds raptor performance-testing task

    Args:
        name: name of task
        signed_apk: id of signing task and path to apk
        mozharness_task_id: id of mozharness task
        is_arm: true if signed apk uses the ARM abi
        raptor_app_id: raptor-specific app identifier
        package_name: package name
        activity_class_name: activity to test
        gecko_revision: gecko revision

    Returns:
        Task: task builder
    """
    signed_apk = RemoteArtifact(signed_apk[0], signed_apk[1])
    worker_type = 'gecko-t-ap-perf-g5' if is_arm else 'gecko-t-ap-perf-p2'
    artifacts = [{
        'path': '/builds/worker/{}'.format(worker_path),
        'type': 'directory',
        'name': 'public/{}/'.format(public_folder),
    } for worker_path, public_folder in (
        ('artifacts', 'test'),
        ('workspace/build/logs', 'logs'),
        ('workspace/build/blobber_upload_dir', 'test_info')
    )]

    payload = {
        'artifacts': artifacts,
        'command': [
            './test-linux.sh',
            '--installer-url={}'.format(signed_apk.url()),
            '--test-packages-url={}'.format(RemoteArtifact(
                mozharness_task_id, 'public/build/target.test_packages.json').url()),
            '--test=raptor-speedometer',
            '--app={}'.format(raptor_app_id),
            '--binary={}'.format(package_name),
            '--activity={}'.format(activity_class_name),
            '--download-symbols=ondemand',
        ],
        'env': {
            'XPCOM_DEBUG_BREAK': 'warn',
            'MOZ_NO_REMOTE': '1',
            'MOZ_HIDE_RESULTS_TABLE': '1',
            'TAKSLUCSTER_WORKER_TYPE': 'proj-autophone/{}'.format(worker_type),
            'MOZHARNESS_URL': RemoteArtifact(
                mozharness_task_id, 'public/build/mozharness.zip').url(),
            'MOZHARNESS_SCRIPT': 'raptor_script.py',
            'NEED_XVFB': 'false',
            'WORKING_DIR': '/builds/worker',
            'WORKSPACE': '/builds/worker/workspace',
            'MOZ_NODE_PATH': '/usr/local/bin/node',
            'NO_FAIL_ON_TEST_ERRORS': '1',
            'MOZHARNESS_CONFIG': 'raptor/android_hw_config.py',
            'MOZ_AUTOMATION': '1',
            'MOZILLA_BUILD_URL': signed_apk.url()
        },
        'context': 'https://hg.mozilla.org/mozilla-central/raw-file/{}/'
                   'taskcluster/scripts/tester/test-linux.sh'.format(gecko_revision),
    }

    return Task(name, 'proj-autophone', lambda _: worker_type) \
        .append_dependency(signed_apk.task_id) \
        .with_payload(payload)
