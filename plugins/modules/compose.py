#!/usr/bin/python3
import subprocess
import os
import json

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'acoby GmbH'
}
DOCUMENTATION = '''
---
module: move
version_added: 1.0.0
author: Thoralf Rickert-Wendt
short_description: A small wrapper around the host specific docker compose plugin.
description:
        - This module allows managing docker compose environment with specific replacements
          for exec and run commands.
options:
        project_src:
                type: str
                required: true
                description:
                        - absolute path to the docker compose directory
        build:
                type: bool
                required: false
                default: false
                description:
                        - a flag for docker to prebuild the docker images before starting
        pull:
                type: bool
                required: false
                default: false
                description:
                        - a flag for docker to pull the docker images before starting
        remove_orphans:
                type: bool
                required: false
                default: false
                description:
                        - a flag to indicate that all orphan container should be removed
        restarted:
                type: bool
                required: false
                default: false
                description:
                        - a flag to indicate the restart the docker compose environment
        container:
                type: str
                required: false
                description:
                        - a container name within the docker compose environment
        command:
                type: str
                required: false
                description:
                        - a command that should be executed
        command_args:
                type: list
                required: false
                description:
                        - a list of arguments passed to the container command
        state:
                choices: [ "present", "absent", "execute", "run" ]
                required: false
                default: "present"
                description:
                        - a state of the docker compose environment. Be aware that "execute" and "run" are
                          not idempotent. They run commands inside the given docker comtainerd
'''

EXAMPLES = '''
- name: Move a file to a new location
    acoby.collection.compose:
        project_src: /my_project
        container: "ubuntu"
        state: exec
        command: "ls"
        command_args: ["-al","/"]
'''

RETURN = '''
msg:
    description: Message response from docker compose output
    returned: always
    type: str
'''

DOCKER_CLI = ['docker-compose']

def execute(module, cmd, workdir):
  result = {}
  result['returncode'] = -1
  try:
    my_environment = os.environ.copy()
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_environment, cwd=workdir)
    result['returncode'] = process.returncode
    result['stdout'] = process.stdout.decode("utf-8")
    result['stderr'] = process.stderr.decode("utf-8")
  except BaseException as err:
    module.fail_json(msg='Could not run cmd' % (str(err)))
  return result

def get_state(module, path):
  result = {}
  cmd = DOCKER_CLI.copy()
  # cmd.append('compose')
  cmd.append('--ansi=never')
  cmd.append('ps')
  cmd.append('--format')
  cmd.append('json')
  response = execute(module,cmd,path)
  stdout = response.get('stdout')
  if len(stdout)==0:
    return result
  # module.fail_json(msg='cmd %s result is %s' % (' '.join(cmd),stdout))
  state = json.loads(stdout)
  for container in state:
    result[container.get('Name')] = container.get('State') 
  return result

def is_running(state, container):
  for name in state:
    if name.find(container) != -1:
      if state.get(name) == 'running':
        return True
      return False
  return False

def main():
  module = AnsibleModule(
    argument_spec = dict(
      project_src    = dict(type='str', required=True),
      build          = dict(type='bool', default=False),
      pull           = dict(type='bool', default=False),
      remove_orphans = dict(type='bool', default=False),
      restarted      = dict(type='bool', default=False),
      container      = dict(type='str', required=False),
      command        = dict(type='str', required=False),
      command_args   = dict(type='list', required=False),
      state          = dict(type='str', default='present', choices=['present', 'absent', 'execute', 'run'])
    ),
    supports_check_mode=True
  )
  result = dict(changed=False, cmd='', stdout='', stderr='', msg='', diff=dict())

  path = Path(module.params.get('project_src'))
  if not path.exists():
    module.fail_json(msg='Not found or no access to project_src %s' % (path))

  composeFile = path.joinpath('docker-compose.yml')
  if not path.exists():
    module.fail_json(msg='Not found or no access to compose file %s' % (composeFile))

  if module.check_mode:
    module.exit_json(**result)

  cmd = DOCKER_CLI.copy()
  # cmd.append('compose')
  cmd.append('--ansi=never')
  
  oldstate = get_state(module,path)
  
  if module.params.get('state') == 'present':
    cmd.append('up')
    cmd.append('-d')
    
    if module.params.get('build') is True:
      cmd.append('--build')
    if module.params.get('pull') is True:
      cmd.append('--pull=always')
    if module.params.get('remove_orphans') is True:
      cmd.append('--remove-orphans')
    if module.params.get('restarted') is True:
      cmd.append('--force-recreate')
    
    response = execute(module,cmd,path)
    if response.get('returncode') != 0:
      module.fail_json(msg='Could not start project. Command %s response is %s' % (' '.join(cmd), response.get('stderr')))

    result['stdout'] = response.get('stdout')
    result['stderr'] = response.get('stderr')
  
    if response.get('stdout').find('Extracting') != -1:
      result['changed'] = True
      result['msg'] = 'New service released'
    else:
      result['msg'] = 'Service already up2date'

  elif module.params.get('state') == 'run':
    cmd.append('run')
    cmd.append('-T')
    container = module.params.get('container')

    cmd.append(container)
    cmd.append(module.params.get('command'))
    command_args = module.params.get('command_args')
    if command_args is not None:
      for command_arg in command_args:
        cmd.append(command_arg)

    response = execute(module,cmd,path)
    if response.get('returncode') != 0:
      module.fail_json(msg='Could not run command in container %s with %s' % (container, response))

    result['changed'] = True
    result['msg'] = 'Container run command passed'
    result['stdout'] = response.get('stdout')
    result['stderr'] = response.get('stderr')

  elif module.params.get('state') == 'execute':
    cmd.append('exec')
    cmd.append('-T')
    container = module.params.get('container')
    if not is_running(oldstate,container):
      module.fail_json(msg='Container %s is not running' % (container))

    cmd.append(container)
    cmd.append(module.params.get('command'))
    command_args = module.params.get('command_args')
    if command_args is not None:
      for command_arg in command_args:
        cmd.append(command_arg)

    response = execute(module,cmd,path)
    if response.get('returncode') != 0:
      module.fail_json(msg='Could not execute command in container %s with %s' % (container, response))
  
    result['changed'] = True
    result['msg'] = 'Container execute command passed'
    result['stdout'] = response.get('stdout')
    result['stderr'] = response.get('stderr')

  elif module.params.get('state') == 'absent':
    cmd.append('down')
    if module.params.get('remove_orphans') is True:
      cmd.append('--remove-orphans')

    response = execute(module,cmd,path)
    if response.get('returncode') != 0:
      module.fail_json(msg='Could not pull image. %s' % (response.get('stderr')))

    result['msg'] = 'Service absent'
    result['stdout'] = response.get('stdout')
    result['stderr'] = response.get('stderr')

  result['cmd'] = ' '.join(cmd)
  newstate = get_state(module,path)

  result['diff'] = dict(before=oldstate, after=newstate)

  if not result['changed']:
    for name in oldstate.keys():
      if name in newstate:
        if oldstate.get(name) != newstate.get(name):
          result['changed'] = True
          break
      else:
        result['changed'] = True
        break
  if not result['changed']:
    for name in newstate.keys():
      if name in oldstate:
        if oldstate.get(name) != newstate.get(name):
          result['changed'] = True
          break
      else:
        result['changed'] = True
        break

  module.exit_json(**result)


if __name__ == '__main__':
  main()
