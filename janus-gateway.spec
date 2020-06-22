%define janus_release 0.10.2.1
%define janus_commit a46344dccb5b45e5644ba9645e83a39e927f6915

Name:    janus-gateway
Version: %{janus_release}
Release: 1%{?dist}
Summary: General purpose WebRTC gateway
Group: Network
License: GPLv2
Source0: https://github.com/meetecho/janus-gateway/archive/%{janus_commit}.tar.gz
Source1: janus-gateway.service
BuildRequires: jansson-devel, openssl-devel, libsrtp15-devel, glib-devel, opus-devel, libogg-devel, libcurl-devel, pkgconfig, gengetopt, libtool, autoconf, automake, libwebsockets-devel, doxygen, graphviz, libconfig-devel
BuildRequires: libmicrohttpd-devel >= 0.9.59
BuildRequires: sofia-sip
BuildRequires: libnice-devel >= 0.1.16, lua-devel
Requires: jansson, openssl, glib, sofia-sip libwebsockets
Requires: libsrtp15
Requires: libnice >= 0.1.16
Requires: libmicrohttpd >= 0.9.59
%description
Janus is an open source, general purpose, WebRTC gateway designed and developed by Meetecho.

%prep
%autosetup -n janus-gateway-%{janus_commit}

%build
./autogen.sh
./configure --prefix=/opt/janus
make

%install
DESTDIR=%buildroot make install
DESTDIR=%buildroot make configs
mkdir -p  %{buildroot}%{_unitdir}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/janus-gateway.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) /opt/janus/etc/janus/*
%doc /opt/janus/share/doc/*
%doc /opt/janus/share/man/*
/opt/janus/share/janus/
/opt/janus/bin
/opt/janus/include
/opt/janus/lib
%{_unitdir}/janus-gateway.service

%changelog
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


