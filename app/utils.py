from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from Queue import Queue, Empty
import sys
import os
import logging

logger = logging.getLogger(__name__)

jjb = '/usr/local/bin/jenkins-jobs'
templates_dir = '/opt/jenkins-job-builder/templates'
projects_dir = '/opt/jenkins-job-builder/projects'
lock_file = '/opt/jenkins-job-builder/logs/update_all_jobs.lock'
projects = {
    'docker': ['lint', 'build', 'test', 'publish', 'deploy'],
    'ansible': ['lint']
}


def create_project_yaml(project, project_type):
    try:
        f = open('%s/%s.yaml' % (projects_dir, project), 'w')
        f.write('- project:\n')
        f.write('    name: %s\n' % project)
        f.write('    jobs:\n')
        f.write('      - %s\n' % project_type)
        f.close()
        logger.info('created project yaml file')
        return True
    except Exception, err:
        logger.exception('unable to handle the file')


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
        logger.info(line.strip())
    out.close()


def run_command_async(cmd):
    cmd = 'touch %s && %s && rm -f %s' % (lock_file, cmd, lock_file)
    logger.info('running command:\n%s' % cmd)
    try:
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1, shell=True)
        q = Queue()
        t = Thread(target=enqueue_output, args=(p.stdout, q))
        t.daemon = True
        t.start()
    except Exception, err:
        logger.exception('unable to execute the command in async')
        if os.path.isfile(lock_file):
            logger.exception('removed a lock file %s' % lock_file)
            os.remove(lock_file)


def run_command(cmd):
    logger.info('running command:\n%s' % cmd)
    try:
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        while p.poll() is None:
            logger.info(p.stdout.read().strip())
    except Exception, err:
        logger.exception('unable to execute the command')
