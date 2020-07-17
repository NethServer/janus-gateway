==============
janus-gateway
==============

Janus Gateway RPM https://github.com/meetecho/janus-gateway


Configuration
=============

Example configuration files are in ``/opt/janus/etc/janus``

Install and start the service
=============================

The RPM installs a systemd unit. To enable it and start the service run :: 

    # systemctl enable --now janus-gateway

The service *is not* restarted automatically after RPM upgrades. Remember to run ::

    # systemctl restart janus-gateway


Detailed trace
==============

It is possible to build the RPM with additional libraries that send to standard output a detailed trace
and detect memory leaks and faults. This is useful for upstream developers to debug a server crash.

Run ``rpmbuild`` defining additional compilation flags. For instance: ::

    $ rpmbuild -D 'dist .ns7' -D 'dbgflags -O0 -fno-omit-frame-pointer -g3 -ggdb3 -fsanitize=address,undefined' janus-gateway.spec

The build requires a modern GCC version with libasan and libubsan dependencies. On CentOS 7 it is possible to install it from SCLo.

See also the ``.travis.yml`` in this repository for more information.

Once the RPM with additional libraries is installed:

1. Add a local systemd unit override fragment,
   by running ``systemctl edit janus-gateway.service``. ::

    [Service]
    Environment="SOFIA_DEBUG=9"
    ExecStart=
    ExecStart=/bin/bash -c 'exec /opt/janus/bin/janus -o -d 7 -L /dev/null &>/var/log/janus-trc.log.$$$$'

   As alternative copy the above fragment to
   ``/etc/systemd/system/janus-gateway.service.d/override.conf``
   and run ``systemctl daemon-reload``.

2. Check the changes are in place: ::

    systemctl cat janus-gateway

3. Restart the service (when possible): ::

    systemctl restart janus-gateway

4. Check the status. The current log file is ``/var/log/janus-trc.log.PIDNUM``, where ``PIDNUM`` is 
   the server main process PID: ::

    systemctl status janus-gateway

To clean up the above setup: ::

    rm -f /etc/systemd/system/janus-gateway.service.d/override.conf
    systemctl daemon-reload

Then restart the service.

Building a release RPM
======================

1. Ensure the release commit hash is set in the .spec file
2. Fix the .spec file Version and Release tag
3. Write the %changelog entry in the .spec file
4. Commit the above changes
5. Create a git tag that starts with a digit. Do not use any "-" (minus) sign! E.g.: 0.12.1r2
6. Push the tag and the commit to start the automated build on Travis CI

Builds started from a tagged commit are published to "updates"!

More information: https://docs.nethserver.org/projects/nethserver-devel/en/v7/building_rpms.html

