#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template
import sys
import local_config as config

'''Generate an .ovpn file from a set of user keys
to be used with an ovpn client.
'''

try:
  username = sys.argv[1]
except:
  print('Error: Supply a username!')
  sys.exit()

try:
  server = config.OVPN_SERVER_ADDRESS
  port = config.OVPN_SERVER_PORT
except AttributeError:
    try:
        server = sys.argv[2]
        port = sys.argv[3] 
    except:
        print('Error: Need an ip and port "12.34.56.78 1194" or set up a local_config.py as demonstrated in local_config.py.sample')
        sys.exit()

#'/etc/openvpn/easy-rsa'
ovpn_name = config.OVPN_FILENAME_PREFIX + username + config.OVPN_FILENAME_SUFFIX
ca = config.EASYRSA_CERT_FILE

tlsauth = False
if config.OVPN_TLS_AUTH_ENABLED:
    tlsauth = config.OVPN_TLS_AUTH_FILE

usercert = config.EASYRSA_CLIENT_CERT_DIR + ovpn_name + '.crt'
userkey = config.EASYRSA_CLIENT_KEY_DIR + ovpn_name + '.key'
ovpn_filename = config.OVPN_FILE_DESTINATION + ovpn_name + '.ovpn'
local_ovpn_template = config.OVPN_TEMPLATE


try:    
    ovpn_template = config.OVPN_TEMPLATE
except AttributeError:
    ovpn_template = 'templates/ovpn.template'


try:
    with open(ovpn_template) as ovpntemplate, \
        open(usercert) as certfile, \
        open(userkey) as keyfile, \
        open(ca) as cafile, \
        open(tlsauth) as tafile, \
        open(ovpn_filename, 'w') as outfile:

        context = {
            'cacert': cafile.read(),
            'usercert': certfile.read(),
            'userkey': keyfile.read(),
            'tlsauth': tafile.read(),
            'server_port': config.OVPN_SERVER_PORT,
            'server_proto': config.OVPN_SERVER_PROTO,
            'server_address': config.OVPN_SERVER_ADDRESS,
         }

        model = Template(ovpntemplate.read())
        outfile.write(model.render(context))
        print(model.render(context))
        print('OVPN file generated: ' + ovpn_filename)

except IOError as e:
    print(e)
