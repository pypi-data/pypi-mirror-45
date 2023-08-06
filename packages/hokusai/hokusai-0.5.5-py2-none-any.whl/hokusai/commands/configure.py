import os
import urllib
import shutil
import tempfile

from distutils.dir_util import mkpath

import boto3

from hokusai.lib.command import command
from hokusai.lib.common import print_green, get_region_name
from hokusai.lib.exceptions import HokusaiError

@command()
def configure(kubectl_version, bucket_name, key_name, config_file, platform, install_to, install_config_to):
  if not ((bucket_name and key_name) or config_file):
    raise HokusaiError("Must define bucket_name and key_name or config_file")

  print_green("Downloading and installing kubectl...", newline_before=True, newline_after=True)
  tmpdir = tempfile.mkdtemp()
  urllib.urlretrieve("https://storage.googleapis.com/kubernetes-release/release/v%s/bin/%s/amd64/kubectl" % (kubectl_version, platform), os.path.join(tmpdir, 'kubectl'))
  os.chmod(os.path.join(tmpdir, 'kubectl'), 0755)
  shutil.move(os.path.join(tmpdir, 'kubectl'), os.path.join(install_to, 'kubectl'))
  shutil.rmtree(tmpdir)

  print_green("Configuring kubectl...", newline_after=True)
  if not os.path.isdir(install_config_to):
    mkpath(install_config_to)

  if bucket_name and key_name:
    client = boto3.client('s3', region_name=get_region_name())
    client.download_file(bucket_name, key_name, os.path.join(install_config_to, 'config'))
  else:
    shutil.copy(config_file, os.path.join(install_config_to, 'config'))
