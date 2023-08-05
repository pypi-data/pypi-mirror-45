#
# (C) Copyright IBM Corp. 2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import logging
import zipfile
from pywren_ibm_cloud import wrenconfig
from pywren_ibm_cloud.utils import version_str
from pywren_ibm_cloud.storage import storage
from pywren_ibm_cloud.cf_connector import CloudFunctions

logger = logging.getLogger(__name__)

ZIP_LOCATION = os.path.join(os.getcwd(), 'ibmcf_pywren.zip')


def _get_pywren_location():
    my_location = os.path.dirname(os.path.abspath(__file__))
    pw_location = os.path.join(my_location, '..')
    return pw_location


def _create_zip_action():

    def add_folder_to_zip(zip_file, full_dir_path, sub_dir=''):
        for file in os.listdir(full_dir_path):
            full_path = os.path.join(full_dir_path, file)
            if os.path.isfile(full_path):
                zip_file.write(full_path, os.path.join('pywren_ibm_cloud', sub_dir, file), zipfile.ZIP_DEFLATED)
            elif os.path.isdir(full_path) and '__pycache__' not in full_path:
                add_folder_to_zip(zip_file, full_path, os.path.join(sub_dir, file))

    try:
        pywren_location = _get_pywren_location()

        with zipfile.ZipFile(ZIP_LOCATION, 'w') as ibmcf_pywren_zip:
            main_file = os.path.join(pywren_location, 'action', '__main__.py')
            ibmcf_pywren_zip.write(main_file, '__main__.py', zipfile.ZIP_DEFLATED)
            add_folder_to_zip(ibmcf_pywren_zip, pywren_location)
    except Exception:
        raise Exception('Unable to create the {} action package'.format(ZIP_LOCATION))


def _extract_modules(image_name, memory, cf_client, config):
    # Extract installed Python modules from docker image
    # And store them into storage

    # Create storage_handler to upload modules file
    storage_config = wrenconfig.extract_storage_config(config)
    internal_storage = storage.InternalStorage(storage_config)

    pywren_location = _get_pywren_location()
    action_location = os.path.join(pywren_location, "runtime", "extract_modules.py")

    with open(action_location, "r") as action_py:
        action_code = action_py.read()

    modules_action_name = '{}_modules'.format(image_name.replace('/', '@').replace(':', '_'))

    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    cf_client.create_action(modules_action_name, image_name, code=action_code, is_binary=False)
    sys.stdout = old_stdout

    memory = cf_client.default_runtime_memory if not memory else memory
    runtime_name = '{}_{}'.format(image_name, memory)
    runtime_meta = cf_client.invoke_with_result(modules_action_name)
    internal_storage.put_runtime_info(runtime_name, runtime_meta)
    cf_client.delete_action(modules_action_name)


def _create_blackbox_runtime(image_name, memory, cf_client):
    # Create runtime_name from image_name
    memory = cf_client.default_runtime_memory if not memory else memory
    action_name = image_name.replace('/', '@').replace(':', '_')
    action_name = '{}_{}'.format(action_name, memory)

    # Upload zipped PyWren action
    with open(ZIP_LOCATION, "rb") as action_zip:
        action_bin = action_zip.read()
    cf_client.create_action(action_name, image_name, code=action_bin, memory=memory)


def create_runtime(image_name, memory=None, config=None):
    print('Creating a new docker image from the Dockerfile')
    print('Docker image name: {}'.format(image_name))

    cmd = 'docker build -t {} .'.format(image_name)
    res = os.system(cmd)
    if res != 0:
        exit()

    cmd = 'docker push {}'.format(image_name)
    res = os.system(cmd)
    if res != 0:
        exit()

    if config is None:
        config = wrenconfig.default()
    else:
        config = wrenconfig.default(config)

    cf_config = wrenconfig.extract_cf_config(config)
    cf_client = CloudFunctions(cf_config)
    cf_client.create_package()
    _create_zip_action()
    _extract_modules(image_name, memory, cf_client, config)
    _create_blackbox_runtime(image_name, memory, cf_client)


def clone_runtime(image_name, memory=None, config=None):
    print('Cloning docker image {}'.format(image_name))

    if config is None:
        config = wrenconfig.default()
    else:
        config = wrenconfig.default(config)

    cf_config = wrenconfig.extract_cf_config(config)
    cf_client = CloudFunctions(cf_config)
    cf_client.create_package()
    _create_zip_action()
    _extract_modules(image_name,  memory, cf_client, config)
    _create_blackbox_runtime(image_name, memory, cf_client)


def update_runtime(image_name, memory=None, config=None):
    print('Updating runtime: {}'.format(image_name))
    if config is None:
        config = wrenconfig.default()
    else:
        config = wrenconfig.default(config)

    cf_config = wrenconfig.extract_cf_config(config)
    cf_client = CloudFunctions(cf_config)

    _create_zip_action()
    _create_blackbox_runtime(image_name, memory, cf_client)


def delete_runtime(image_name, memory=None, config=None):
    print('Deleting runtime: {}'.format(image_name))

    if config is None:
        config = wrenconfig.default()
    else:
        config = wrenconfig.default(config)

    storage_config = wrenconfig.extract_storage_config(config)
    storage_client = storage.InternalStorage(storage_config)
    cf_config = wrenconfig.extract_cf_config(config)
    cf_client = CloudFunctions(cf_config)

    memory = cf_client.default_runtime_memory if not memory else memory

    runtime_name = '{}_{}'.format(image_name, memory)
    storage_client.delete_runtime_info(runtime_name)

    action_name = runtime_name.replace('/', '@').replace(':', '_')
    cf_client.delete_action(action_name)


def deploy_default_runtime(memory=None, config=None):
    this_version_str = version_str(sys.version_info)
    print('Updating default Python {} runtime'.format(this_version_str))
    if config is None:
        config = wrenconfig.default()
    else:
        config = wrenconfig.default(config)

    if this_version_str == '3.5':
        image_name = wrenconfig.RUNTIME_DEFAULT_35
    elif this_version_str == '3.6':
        image_name = wrenconfig.RUNTIME_DEFAULT_36
    elif this_version_str == '3.7':
        image_name = wrenconfig.RUNTIME_DEFAULT_37

    cf_config = wrenconfig.extract_cf_config(config)
    cf_client = CloudFunctions(cf_config)
    cf_client.create_package()

    _create_zip_action()
    _extract_modules(image_name, memory, cf_client, config)
    _create_blackbox_runtime(image_name, memory, cf_client)
