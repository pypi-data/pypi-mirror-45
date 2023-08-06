import json
import logging
import os
import subprocess
import uuid
from datetime import datetime
from os.path import expanduser


def run_proc(command):
  logging.debug('run_proc: %s' % command)
  proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  success = int(proc.returncode) == 0
  if not success:
    logging.warning(out)
    logging.warning(err)
  return success, out, err


def pretty_file_size(num, suffix='B'):
  for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
    if abs(num) < 1024.0:
      return "%3.1f%s%s" % (num, unit, suffix)
    num /= 1024.0
  return "%.1f%s%s" % (num, 'Yi', suffix)


def pretty_date(time=False):
  '''
  Get a datetime object or a int() Epoch timestamp and return a
  pretty string like 'an hour ago', 'Yesterday', '3 months ago',
  'just now', etc
  '''
  now = datetime.now()
  if type(time) is int or type(time) is float:
    if time is 0:
      return '-'
    diff = now - datetime.fromtimestamp(time)
  elif isinstance(time, datetime):
    diff = now - time
  elif not time:
    diff = now - now
  second_diff = diff.seconds
  day_diff = diff.days

  if day_diff < 0:
    return ''

  if day_diff == 0:
    if second_diff < 3:
      return 'just now'
    if second_diff < 60:
      return str(second_diff) + ' seconds ago'
    if second_diff < 120:
      return 'a minute ago'
    if second_diff < 3600:
      return '%.2f minutes ago' % (second_diff / 60)
    if second_diff < 7200:
      return 'an hour ago'
    if second_diff < 86400:
      return '%.2f hours ago' % (second_diff / 3600)
  if day_diff == 1:
    return 'Yesterday'
  if day_diff < 7:
    return str(day_diff) + ' days ago'
  if day_diff < 31:
    return str(int(day_diff / 7)) + ' weeks ago'
  if day_diff < 365:
    return str(int(day_diff / 30)) + ' months ago'
  return str(int(day_diff / 365)) + ' years ago'


def get_id():
  return str(uuid.uuid4())[:8]


def set_mc_config(data, filter=['gcs', 'dcs']):
  logging.debug('set_mc_config')
  success = True
  for k, v in data.items():
    try:
      t = v['type']
      if t not in filter:
        logging.info('Skip set_mc_config: %s' % t)
        continue
      command = 'mc config host add %s %s %s %s' % (
        v['type'], v['url'], v['access_key'], v['secret_key'])
      logging.debug('command: %s' % command)
      proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
      (out, err) = proc.communicate()
      if int(proc.returncode) != 0:
        success = False
    except:
      continue
  return success, 'set mc config'


def get_diff_list(src, dest):
  command = 'mc diff %s %s --json' % (src, dest)
  proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  success = int(proc.returncode) == 0
  if not success:
    logging.warning(out)
    logging.warning(err)
  msg = out.decode('utf-8').strip()
  diff_list = []
  for line in msg.split('\n'):
    if line is None or len(line) == 0:
      continue
    diff = json.loads(line)
    if 'error' not in diff:
      diff_list.append(diff)
    else:
      diff_list.append({'diff_list': [], 'diff': -1})
  return success, command, msg, diff_list


def _get_all_config():
  logging.debug('get_all_config')
  home = expanduser("~")
  try:
    file_name = os.path.join(home, '.dsms-config')
    with open(file_name, 'r') as fd:
      config = json.loads(fd.read())
      return config
  except Exception as ex:
    # logging.exception(ex)
    return {}


def get_config(kind='cli'):
  return _get_all_config()[kind]


def set_config(data):
  all_config = _get_all_config()
  kind = data['kind']
  all_config[kind] = data
  home = expanduser("~")
  file_name = os.path.join(home, '.dsms-config')
  with open(file_name, 'w') as fd:
    fd.write(json.dumps(all_config, indent=2))
