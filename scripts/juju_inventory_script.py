#!/usr/bin/env python3.6
import base64
import json
import os
import sys
import urllib.request

inventory_url = 'http://hostname:5000/juju/inventory'


def main():
    try:
        # For no arguments, or just --list, just output the inventory.
        # This allows this script to be used as a dynamic inventory plugin.
        if not sys.argv[1:] or sys.argv[1] == '--list':
            # Build an Ansible inventory file from Juju environment status
            username = os.getenv('JUJU_USERNAME')
            password = os.getenv('JUJU_PASSWORD')
            model_uuid = os.getenv('JUJU_MODEL_UUID')

            url = '{0}?model_uuid={1}'.format(inventory_url, model_uuid)
            req = urllib.request.Request(url)
            credentials = '{0}:{1}'.format(username, password)
            encoded_credentials = base64.b64encode(credentials.encode('ascii'))
            req.add_header(
                'Authorization',
                'Basic {}'.format(encoded_credentials.decode('ascii')))
            res = urllib.request.urlopen(req).read()

            inventory = json.loads(res.decode('utf-8'))
            print(json.dumps(inventory, indent=4))
            sys.exit(0)

        elif sys.argv[1] == '--host':
            # hostvars not supported yet, exit quickly to minimize the lookup
            # cost
            print(json.dumps({}))
            sys.exit(0)

        else:
            raise Exception(
                'Unknown argument. Please use either --list or --host')
    except Exception as e:
        print('Error: {}'.format(str(e)), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
