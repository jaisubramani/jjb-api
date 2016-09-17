FROM python:2

RUN apt-get update -y
RUN apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
RUN pip install jenkins-job-builder

RUN mkdir -p /etc/gunicorn
COPY app/*.conf /etc/gunicorn/

RUN mkdir -p /opt/jenkins-job-builder/app
COPY app/*.py /opt/jenkins-job-builder/app/
COPY app/requirements.txt /opt/jenkins-job-builder/app

RUN pip install --no-cache-dir -r /opt/jenkins-job-builder/app/requirements.txt

RUN mkdir -p /etc/jenkins_jobs/
COPY jenkins_jobs.ini /etc/jenkins_jobs

RUN mkdir -p /opt/jenkins-job-builder/templates
COPY jobs.yaml /opt/jenkins-job-builder/templates
COPY default-projects.yaml /opt/jenkins-job-builder/templates

RUN mkdir -p /opt/jenkins-job-builder/logs
RUN mkdir -p /opt/jenkins-job-builder/projects

EXPOSE 8000

WORKDIR /opt/jenkins-job-builder/app

ENTRYPOINT ["/usr/local/bin/gunicorn", "--log-config", "/etc/gunicorn/logging.conf", "--config", "/etc/gunicorn/gunicorn.conf", "-b", ":8000", "main:app"]
