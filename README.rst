==============
janus-gateway
==============

Janus Gateway RPM https://github.com/meetecho/janus-gateway


Configuration
--------------

Example configuration files are in ``/opt/janus/etc/janus``

Run
----

The RPM installs a systemd unit. To enable and start the service run :: 

    # systemctl enable --now janus-gateway

The service *is not* restarted automatically after RPM upgrades. Remember to run ::

    # systemctl restart janus-gateway

It is possible to tweak the service startup arguments 
by creating the file ``/opt/janus/etc/janus.env``.