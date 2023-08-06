from collections import OrderedDict
import yaml

from hokusai.lib.command import command
from hokusai.lib.exceptions import HokusaiError
from hokusai.lib.common import print_green, clean_string
from hokusai.lib.constants import YAML_HEADER

@command()
def create_new_app_yaml(source_file, app_name):
  with open(source_file, 'r') as stream:
    try:
      yaml_content = list(yaml.load_all(stream))
    except yaml.YAMLError as exc:
      raise HokusaiError("Cannot read source yaml file %s." % source_file)

  for c in yaml_content: update_namespace(c, clean_string(app_name))

  new_namespace = OrderedDict([
      ('apiVersion', 'v1'),
      ('kind', 'Namespace'),
      ('metadata', {
        'name': clean_string(app_name)
      })
    ])
  yaml_content = [new_namespace] + yaml_content

  with open("hokusai/%s.yml" % app_name, 'w') as output:
    output.write(YAML_HEADER)
    yaml.safe_dump_all(yaml_content, output, default_flow_style=False)

  print_green("Created hokusai/%s.yml" % app_name)

def update_namespace(yaml_section, destination_namespace):
  if 'apiVersion' in yaml_section:
    if 'metadata' in yaml_section:
      yaml_section['metadata']['namespace'] = destination_namespace
    else:
      yaml_section['metadata'] = { 'namespace': destination_namespace }
