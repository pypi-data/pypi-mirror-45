from urllib.parse import urlparse
from cli import pyke
import subprocess
import click
import os

class ContainerVersionBehavior:
  def __init__(self, profile=None):
    self.util = pyke.Util(profile=profile)
    self.object_type = 'container'

  def force_update (self, container, version):
    container_id = self.util.lookup_object_id(self.object_type, container)
    version_id = self.util.get_version_id(self.object_type, container, version)

    req_data = {'force': True}
    resp = self.util.cli_request('PUT',
        self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}',
          {'container_id': container_id, 'version_id': version_id}), json=req_data)

    click.echo(resp)

  def __touch(self, path):
    # Helper function
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
      os.makedirs(basedir)

    # Write an empty file into the dir
    open(path, 'a').close()

  def download_app_zip(self, container, version, path):
    if path is None:
      raise ClickException('You must provide a --path to save the zip file to')

    container_id = self.util.lookup_object_id(self.object_type, container)

    try:
      container = self.util.cli_request('GET',
          self.util.build_url('{app}/iot/v1/containers?id={id}', {'id': container_id} ))['payload']['data']
    except:
      raise click.ClickException('Container not found')

    url_ref = container[0].get('urlRef')
    version_id = self.util.get_version_id(self.object_type, container_id, version)

    resp = self.util.cli_request('POST',
        self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}/token',
          {'container_id': container_id, 'version_id': version_id}), json={'type': 'editor'})

    token = resp.get('payload', {}).get('data', {}).get('token')

    p = urlparse(self.util.context.get('app'))
    service_url = '{}://experience.{}'.format(p.scheme, '.'.join(p.hostname.split('.')[1:]))

    # TODO: Dynamically get integration cloud
    editor_url = '{}/ic/{}/luma-editor/download/application.zip'.format(service_url, url_ref)

    zip_path = '{}/application.zip'.format(path)
    self.__touch(zip_path)

    command_list = 'curl -L --output {} {} -H '.format(zip_path, editor_url).split()
    command_list.append("Authorization: Bearer {}".format(token))

    subprocess.run(command_list)

  def tail_logs(self, container, version):
    container_id = self.util.lookup_object_id(self.object_type, container)

    try:
      container = self.util.cli_request('GET',
          self.util.build_url('{app}/iot/v1/containers?id={id}', {'id': container_id} ))['payload']['data']
    except:
      raise click.ClickException('Container not found')

    url_ref = container[0].get('urlRef')
    version_id = self.util.get_version_id(self.object_type, container_id, version)
    version_res = self.util.cli_request('GET', self.util.build_url('{app}/iot/v1/containers/{container_id}/versions?id={version_id}',\
        { 'container_id': container_id, 'version_id': version_id }))['payload']['data']

    if version_res is not None and len(version_res) > 0:
      version = version_res[0]

    is_editable = version.get('isEditable')
    if not is_editable:
      return self.old_logs(container_id, version_id)

    resp = self.util.cli_request('POST',
        self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}/token',
          {'container_id': container_id, 'version_id': version_id}), json={'type': 'editor'})

    token = resp.get('payload', {}).get('data', {}).get('token')

    p = urlparse(self.util.context.get('app'))
    service_url = '{}://experience.{}'.format(p.scheme, '.'.join(p.hostname.split('.')[1:]))

    # TODO: Dynamically get integration cloud
    editor_url = '{}/ic/{}/luma-editor/logs'.format(service_url, url_ref)

    command_list = 'curl {} -H '.format(editor_url).split()
    command_list.append("Authorization: Bearer {}".format(token))
    subprocess.run(command_list)

  def old_logs(self, container_id, version_id):
    resp = self.util.cli_request('GET', self.util.build_url('{app}/iot/v1/containers/{container_id}/versions/{version_id}/logs',\
      {'container_id': container_id, 'version_id': version_id}))

    for x in resp['payload']['data']:
      click.echo(x)


