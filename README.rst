==============
janus-gateway
==============

Janus Gateway RPM https://github.com/meetecho/janus-gateway


Configuration
--------------

Example configuration files are in ``/opt/janus/etc/janus``

Install and start the service
-----------------------------

The RPM installs a systemd unit. To enable it and start the service run :: 

    # systemctl enable --now janus-gateway

The service *is not* restarted automatically after RPM upgrades. Remember to run ::

    # systemctl restart janus-gateway


Detailed trace
--------------

It is possible to build the RPM with additional libraries that send to standard output a detailed trace
and detect memory leaks and faults. This is useful for upstream developers to debug a server crash.

Run ``rpmbuild`` defining additional compilation flags. For instance: ::

    $ rpmbuild -D 'dist .ns7' -D 'dbgflags -O0 -fno-omit-frame-pointer -g3 -ggdb3 -fsanitize=address,undefined' janus-gateway.spec

The build requires a modern GCC version with libasan and libubsan dependencies. On CentOS 7 it is possible to install it from SCLo.

See also the ``.travis.yml`` in this repository for more information.

Once the RPM with additional libraries is installed:

1. Add a local systemd unit override fragment, by copying the following 
   contents to ``/etc/systemd/system/janus-gateway.service.d/override.conf``
   or run ``systemctl edit janus-gateway.service``. ::

    [Service]
    ExecStart=
    ExecStart=/bin/bash -c '\
    export SOFIA_DEBUG=9; \
    logfile=/var/log/janus-dbg-$(/bin/date +%%s).log ; \
    echo OUT/ERR sent to $$logfile ; \
    exec /opt/janus/bin/janus -o -d 7 -L /dev/null &>$$logfile'

2. Check the changes are in place: ::

    systemctl cat janus-gateway

3. Restart the service (when possible): ::

    systemctl restart janus-gateway

4. Check the status. The current log file should be visible in the unit journal excerpt: ::

    systemctl status janus-gateway

Remember to remove ``/etc/systemd/system/janus-gateway.service.d/override.conf`` and restart the service when
the trace is no longer needed.
