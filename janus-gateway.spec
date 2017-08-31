Name:    janus-gateway
Version: 0.2.3
Release: 5%{?dist}
Summary: General purpose WebRTC gateway
Group: Network
License: GPLv2
Source0: https://github.com/meetecho/janus-gateway/archive/master.tar.gz
Source1: janus-gateway.service
BuildRequires: libmicrohttpd-devel, jansson-devel, libnice-devel, openssl-devel, libsrtp-devel, glib-devel, opus-devel, libogg-devel, libcurl-devel, pkgconfig, gengetopt, libtool, autoconf, automake, libwebsockets-devel, doxygen, graphviz
BuildRequires: sofia-sip
Requires: libmicrohttpd, jansson, libnice, openssl, libsrtp, glib, sofia-sip libwebsockets
Requires: libsrtp15

%description
Janus is an open source, general purpose, WebRTC gateway designed and developed by Meetecho.

%prep
%autosetup -n janus-gateway-master

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
