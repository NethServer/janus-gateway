%define janus_commit 1c4b1106867ffc4f49a01df02cb785996ca4fa0b

Name:    janus-gateway
Version: 0.12.3
Release: 1%{?dist}
Summary: General purpose WebRTC gateway
License: GPLv3
URL: https://github.com/NethServer/janus-gateway
Source0: https://github.com/meetecho/janus-gateway/archive/%{janus_commit}.tar.gz
Source1: janus-gateway.service
BuildRequires: gengetopt, libtool, autoconf, automake
BuildRequires: jansson-devel, openssl-devel, libsrtp23-devel, glib-devel, opus-devel, libogg-devel, libcurl-devel, libwebsockets-devel, libconfig-devel
BuildRequires: libmicrohttpd-devel >= 0.9.59
BuildRequires: sofia-sip-devel
BuildRequires: libnice-devel >= 0.1.16, lua-devel
BuildRequires: systemd

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: jansson, openssl, glib, sofia-sip, libwebsockets
Requires: libsrtp23
Requires: libnice >= 0.1.16
Requires: libmicrohttpd >= 0.9.59
%description
Janus is an open source, general purpose, WebRTC gateway designed and developed by Meetecho.

%prep
%autosetup -n janus-gateway-%{janus_commit}

%build
./autogen.sh
./configure --prefix=/opt/janus %{?dbgflags:CFLAGS="%{dbgflags}" LDFLAGS="%{dbgflags}"}
make %{?_smp_mflags}

%install
DESTDIR=%buildroot make install
DESTDIR=%buildroot make configs
mkdir -p  %{buildroot}%{_unitdir}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/janus-gateway.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license COPYING
%config(noreplace) /opt/janus/etc/janus/*
%doc /opt/janus/share/doc/*
%doc /opt/janus/share/man/*
/opt/janus/share/janus/
/opt/janus/bin
/opt/janus/include
/opt/janus/lib
%{_unitdir}/janus-gateway.service

%post
%systemd_post ${name}.service

%preun
%systemd_preun ${name}.service

%postun
# As this RPM is released for NethServer, the nethserver-janus
# configuration package takes care of restarting the service
# when needed. We could revert this decision in the future
# by using the following macro instead:
# %%systemd_postun_with_restart ${name}.service
%systemd_postun

%changelog
* Fri Sep 30 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 0.12.3-1
- Update Janus Gateway to 0.12.3 - nethesis/dev#6178

* Thu May 26 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 0.10.10-2
- Update from 1.5 to 2.3 - nethesis/dev#6124

* Thu Feb 18 2021 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.10.10-1
- Janus-Gateway: upgrade to 0.10.10 (7732127) - NethServer/dev#6416

* Tue Oct 20 2020 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.10.6-1
- Janus-Gateway: upgrade to 0.10.6 (cc204a5) - NethServer/dev#6313

* Tue Jul 14 2020 Davide Principi <davide.principi@nethesis.it> - 0.10.2-2
- Janus-Gateway: upgrade to 922b392 - NethServer/dev#6195
- Upgrade janus lib to 922b392 - nethesis/dev#5824
- Development builds for Janus and sofia-sip - nethesis/dev#5836


* Mon Jun 22 2020 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.10.2.1-1
- Upgrade janus-gateway to commit a46344d - NethServer/dev#6195

* Tue Jun 16 2020 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.10.1.1-1
- Upgrade janus-gateway to commit 085ed39 - NethServer/dev#6195

* Thu Mar 21 2019 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.6.3-1
- Update janus-gateway to 0.6.3 - NethServer/dev#5735

* Thu Mar 7 2019 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.6.2-1
- Update janus-gateway to 0.6.2 - NethServer/dev#5728

* Thu Feb 28 2019 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.6.1-1
- Update janus-gateway to 0.6.1 - NethServer/dev#5723

* Tue Jan 15 2019 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.6.0-1
- Update janus-gateway to 0.6.0 - NethServer/dev#5555

* Wed Nov 21 2018 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.5.0-1
- Update janus-gateway to 0.5.0 - NethServer/dev#5648

* Tue Sep 25 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.4.3-2
- Update to upstream commit ef8477e6081c4015e244fbce37d9930e73b83412

* Tue Jul 24 2018 Alessandro Polidori <alessandro.polidori@gmail.com> - 0.4.3-1
- Update janus-gateway to 0.4.3 - NethServer/dev#5511

* Thu May 31 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.4.1
- Update to upstream release 0.4.1

* Thu Mar 08 2018 Stefano Fancello <stefano.fancello@nethesis.it> - 0.2.5.1-1
- janus-gateway: Janus doesn't try to restart if it fails - Bug NethServer/dev#5426

* Mon Nov 20 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.2.5-1
- janus-gateway ignores rtp_port_range option - Bug NethServer/dev#5374
