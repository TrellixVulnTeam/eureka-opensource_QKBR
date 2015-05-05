# -*- coding: utf-8 -*-
# =-
# Copyright Solocal Group (2015)
#
# eureka@solocal.com
#
# This software is a computer program whose purpose is to provide a full
# featured participative innovation solution within your organization.
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# =-

import os
import sys
import textwrap
from optparse import OptionParser

import eureka
import nagare
import pkg_resources
from eureka.infrastructure import filesystem


def set_options(optparser):
    optparser.usage = " [application] ..."
    optparser.add_option('-H', '--fcgi-host', dest='fastcgi_host',
                         default='127.0.0.1', help='FastCGI host')
    optparser.add_option('-P', '--fcgi-port', dest='fastcgi_port',
                         default='9001', help='FastCGI port')
    optparser.add_option('-m', '--memcached-host', dest='memcached_host',
                         default='127.0.0.1', help='memcached host')
    optparser.add_option('-p', '--memcached-port', dest='memcached_port',
                         default='11211', help='memcached port')


def _validate(options):
    if options.fastcgi_host is None:
        raise ValueError('fastcgi_host not given')
    if options.fastcgi_port is None:
        raise ValueError('fastcgi_port not given')
    if options.memcached_host is None:
        raise ValueError('memcached_host not given')
    if options.memcached_port is None:
        raise ValueError('memcached_port not given')


def generate_publisher_config():
    """Outputs a generated Nagare FastCGI
        + memcached configuration for your Eureka
    In:
      - ``parser`` -- the optparse.OptParser object used
            to parse the configuration file
      - ``options`` -- options in the command lines
      - ``args`` -- arguments in the command lines
    """
    parser = OptionParser(usage='Usage: %prog [options]',
                          description=generate_publisher_config.__doc__)
    set_options(parser)
    (__, __) = parser.parse_args()
    options = parser.values
    _validate(options)

    eureka_egg_dir = os.path.dirname(os.path.dirname(eureka.__file__))
    with open(os.path.join(eureka_egg_dir, 'contrib/fastcgi.conf.template')
              ) as template_file:
        template = template_file.read()
        publisher_conf = template.format(
            fastcgi_host=options.fastcgi_host,
            fastcgi_port=options.fastcgi_port,
            memcached_host=options.memcached_host,
            memcached_port=options.memcached_port,
        )

    return publisher_conf

print(generate_publisher_config())
