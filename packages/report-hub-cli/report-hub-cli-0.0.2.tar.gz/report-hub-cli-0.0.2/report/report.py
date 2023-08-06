import shutil
import click
import requests


def create_archive(report_folder):

    shutil.make_archive(report_folder, 'zip', report_folder)


@click.group()
def cli():
    """
    Cli for ReportHub server
    """


@cli.command(name='allure', help='Send allure folder to ReportHub')
@click.option('-h', '--host', 'host', envvar='REPORT_HUB_HOST', help='Your ReportHub server host', required=True)
@click.option('-p', '--project', 'project', help='Your ReportHub project', required=True)
@click.option('-m', '--module', 'module', help='Your ReportHub module', required=True)
@click.option('-f',
              '--report-folder',
              'report_folder',
              help='Your allure report folder',
              required=True,
              default='allure-results',
              show_default=True)
def allure_report(host, project, module, report_folder):

    url = '{0}/api/{1}/{2}/report'.format(host, project, module)

    create_archive(report_folder=report_folder)

    requests.post(url=url,
                  files={'allure-results': open('{0}.zip'.format(report_folder), 'rb')},
                  timeout=120)
