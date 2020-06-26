%define janus_release 0.10.2.2
%define janus_commit 922b3926e3b9ed2e50b6e6f36b6f018025dadf8b

Name:    janus-gateway
Version: %{janus_release}
Release: 1.dbg%{?dist}
Summary: General purpose WebRTC gateway
Group: Network
License: GPLv2
Source0: https://github.com/meetecho/janus-gateway/archive/%{janus_commit}.tar.gz
Source1: janus-gateway.service
BuildRequires: gengetopt, libtool, autoconf, automake
BuildRequires: jansson-devel, openssl-devel, libsrtp15-devel, glib-devel, opus-devel, libogg-devel, libcurl-devel, libwebsockets-devel, libconfig-devel
BuildRequires: libmicrohttpd-devel >= 0.9.59
BuildRequires: sofia-sip-devel
BuildRequires: libnice-devel >= 0.1.16, lua-devel
BuildRequires: systemd

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: jansson, openssl, glib, sofia-sip, libwebsockets
Requires: libsrtp15
Requires: libnice >= 0.1.16
Requires: libmicrohttpd >= 0.9.59
%description
Janus is an open source, general purpose, WebRTC gateway designed and developed by Meetecho.

%prep
%autosetup -n janus-gateway-%{janus_commit}

%build
DBG_FLAGS="-O0 -fno-omit-frame-pointer -g3 -ggdb3 -fsanitize=address,undefined -frecord-gcc-switches"
./autogen.sh
./configure --prefix=/opt/janus CFLAGS="$DBG_FLAGS" LDFLAGS="$DBG_FLAGS"
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
%systemd_postun

%changelog
* Fri Jun 26 2020 Davide Principi <davide.principi@nethesis.it> - 0.10.2.2-1
- Upgrade janus-gateway to commit 922b3926e3

