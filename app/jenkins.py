import os
import json
import requests
from flask.ext.restful import Resource, reqparse
import logging
from utils import *

logger = logging.getLogger(__name__)


def create_job(project, project_type):
    try:
        logger.info('execute jenkins-jobs to create %s project' % project)
        if not create_project_yaml(project, project_type):
            return False
        cmd = 'PYTHONUNBUFFERED=1 %s --ignore-cache update %s:%s/%s.yaml ' % (jjb, templates_dir, projects_dir, project)
        for job in projects[project_type]:
            cmd += '%s.%s ' % (project, job)
        run_command(cmd)
        return True
    except Exception, err:
        logger.exception('cannot create jenkins jobs')


def delete_job(project, project_type):
    try:
        logger.info('execute jenkins-jobs to delete %s project' % project)
        cmd = 'PYTHONUNBUFFERED=1 %s delete ' % jjb
        for job in projects[project_type]:
            cmd += '%s.%s ' % (project, job)
        run_command(cmd)
        os.remove('%s/%s.yaml' % (projects_dir, project))
        logger.info('deleted project yaml file')
        return True
    except Exception, err:
        logger.exception('cannot delete jenkins jobs')


def update_job(project, project_type):
    try:
        logger.info('execute jenkins-jobs to update %s project' % project)
        cmd = 'PYTHONUNBUFFERED=1 %s --ignore-cache update %s:%s/%s.yaml ' % (jjb, templates_dir, projects_dir, project)
        for job in projects[project_type]:
            cmd += '%s.%s ' % (project, job)
        run_command(cmd)
        return True
    except Exception, err:
        logger.exception('cannot update jenkins jobs')


def update_all_jobs():
    try:
        logger.info('execute jenkins-jobs to update all projects')
        cmd = 'PYTHONUNBUFFERED=1 %s --flush-cache update --delete-old %s:%s' % (jjb, templates_dir, projects_dir)
        run_command_async(cmd)
        return True
    except Exception, err:
        logger.exception('unable to update all projects')


class JenkinsJobBuilderVersionAPI(Resource):
    def get(self):
        return {'message': 'Jenkins Job Builder API version is 1.0'}

class JenkinsJobBuilderJobAPI(Resource):
    def __init__(self):
        logger.info('process input JSON parameters for /v1/job')
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type=str, required=True, help='Jenkins Project is missing', location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        super(JenkinsJobBuilderJobAPI, self).__init__()

    def post(self):
        logger.info('handle POST request for /v1/job')
        args = self.reqparse.parse_args()
        project = args.project
        project_type = args.type
        if project_type is None:
            return {'message': 'Jenkins Project Type is missing'}, 400
        if not project_type in projects:
            return {'message': 'Jenkins Project Type is invalid'}, 400
        if os.path.isfile('%s/%s.yaml' % (projects_dir, project)):
            return {'message': 'Jenkins Project exists already'}, 400
        if create_job(project, project_type):
            url = 'http://localhost:8080/search/?q=%s' % project
            return {'message': 'Created ' + project + ' Jenkins jobs', 'url': url}, 201
        else:
            return {'message': 'Failed to create ' + project + ' Jenkins jobs'}

    def put(self):
        logger.info('handle PUT request for /v1/job')
        args = self.reqparse.parse_args()
        project = args.project.lower()
        project_type = args.type
        if project != 'all' and project_type is None:
            return {'message': 'Jenkins Project Type is missing'}, 400
        if project != 'all' and not project_type in projects:
            return {'message': 'Jenkins Project Type is invalid'}, 400
        if project == 'all' and project_type is not None:
            return {'message': 'Jenkins Project is invalid'}, 400
        if project == 'all':
            if os.path.isfile(lock_file):
                return {'message': 'Request has been ignored. Jenkins jobs are being updated by different request'}
            if update_all_jobs():
                return {'message': 'Request has been accepted to update all Jenkins jobs'}, 202
            else:
                return {'message': 'Failed to update all Jenkins jobs'}
        if not os.path.isfile('%s/%s.yaml' % (projects_dir, project)):
            return {'message': 'Jenkins Project does not exist'}, 400
        if update_job(project, project_type):
            url = 'http://localhost:8080/search/?q=%s' % project
            return {'message': 'Updated ' + project + ' Jenkins jobs', 'url': url}
        else:
            return {'message': 'Failed to update ' + project + ' Jenkins jobs'}

    def delete(self):
        logger.info('handle DELETE request for /v1/job')
        args = self.reqparse.parse_args()
        project = args.project
        project_type = args.type
        if project_type is None:
            return {'message': 'Jenkins Project Type is missing'}, 400
        if not project_type in projects:
            return {'message': 'Jenkins Project Type is invalid'}, 400
        if not os.path.isfile('%s/%s.yaml' % (projects_dir, project)):
            return {'message': 'Jenkins Project does not exist'}, 400
        if delete_job(project, project_type):
            return {'message': 'Deleted ' + project + ' Jenkins jobs'}
        else:
            return {'message': 'Failed to delete ' + project + ' Jenkins jobs'}
