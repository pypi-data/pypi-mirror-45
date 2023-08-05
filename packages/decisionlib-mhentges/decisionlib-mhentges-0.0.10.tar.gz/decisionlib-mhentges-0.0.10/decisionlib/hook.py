import datetime
import os
import subprocess

import git
import jsone
import slugid
import taskcluster
import yaml

from decisionlib.common import SlugId


def clone(html_url, branch):
    subprocess.check_call(
        'git clone {} --single-branch {} --depth 1'.format(html_url, branch),
        shell=True
    )


def checkout_revision(revision):
    subprocess.check_call('git checkout {}'.format(revision), shell=True)


def fetch_revision():
    return subprocess.check_output('git rev-parse --verify HEAD', encoding='utf-8', shell=True)


def schedule_hook(task_id: SlugId, html_url: str, branch: str, revision: str = None):
    if not html_url.startswith('https://github.com/'):
        raise ValueError('expected repository to be a GitHub repository (accessed via HTTPs)')

    html_url = html_url[:-4] if html_url.endswith('.git') else html_url
    html_url = html_url[:-1] if html_url.endswith('/') else html_url

    repository_full_name = html_url[len('https://github.com/'):]
    clone(html_url, branch)
    if revision:
        checkout_revision(revision)
    else:
        revision = fetch_revision()

    with open(os.path.join('repository', '.taskcluster.yml'), 'rb') as f:
        taskcluster_yml = yaml.safe_load(f)

    # provide a similar JSON-e context to what taskcluster-github provides
    slugids = {}

    def as_slugid(name):
        if name not in slugids:
            slugids[name] = slugid.nice()
        return slugids[name]

    context = {
        'tasks_for': 'cron',
        'cron': {
            'task_id': task_id,
        },
        'now': datetime.datetime.utcnow().isoformat()[:23] + 'Z',
        'as_slugid': as_slugid,
        'event': {
            'repository': {
                'html_url': html_url,
                'full_name': repository_full_name,
            },
            'release': {
                'tag_name': revision,
                'target_commitish': 'refs/heads/{}'.format(branch),
            },
            'sender': {
                'login': 'TaskclusterHook',
            },
        },
    }

    rendered = jsone.render(taskcluster_yml, context)
    if len(rendered['tasks']) != 1:
        raise RuntimeError('Expected .taskcluster.yml in {} to only produce one cron task'
                           .format(html_url))

    task = rendered['tasks'][0]
    queue = taskcluster.Queue({'baseUrl': 'http://taskcluster/queue/v1'})
    queue.createTask(task['taskId'], task)




