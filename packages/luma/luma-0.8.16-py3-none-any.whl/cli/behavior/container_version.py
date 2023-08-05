from urllib.parse import urlparse
from cli import pyke
import subprocess
import click

class ContainerVersionBehavior:
  def __init__(self, profile=None):
    self.util = pyke.Util(profile=profile)
    self.object_type = 'container'

  def tail_logs(self, container, version):
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
          {'container_id': container_id, 'version_id': version_id}), data={'type': 'editor'})

    token = resp.get('payload', {}).get('data', {}).get('token')

    p = urlparse(self.util.context.get('app'))
    service_url = '{}://experience.{}'.format(p.scheme, '.'.join(p.hostname.split('.')[1:]))

    # TODO: Dynamically get integration cloud
    editor_url = '{}/ic/{}/luma-editor/logs'.format(service_url, url_ref)

    command_list = 'curl {} -H '.format(editor_url).split()
    command_list.append("Authorization: Bearer {}".format(token))
    subprocess.run(command_list)


