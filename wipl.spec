Summary:	Make statistics on basis of packets seen on a LAN.
Name:		wipl
Version:	020601
Release:	1
Copyright:	GNU
Group:		Applications/Networking
Source0:	http://wipl-wrr.sourceforge.net/tgz-wipl/%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The wipl program package is able to maintain and display statistics
based on packets seen by a network card.

The program package contains a daemon which maintains the statistics.
For each packet seen by the network card the daemon executes a small
user supplied program. This program can update the statistics using
information about the package. The program must be written in a very
simple build-in programming language.

The program package also contains several client programs which are
able to retreview or modify the statistics maintained by the daemon.
One of them is able to display tables with values evaluated from user
supplied expressions which can refer to the statistics maintained by
the daemon. These tables can be written to HTML or XML files allowing
easy publication from web pages.

On the wipl home page an extension is available which makes it
possible for wipl to cooperate with proxyservers such as Squid and a
socks5 server.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d -o 0 -g 0 $RPM_BUILD_ROOT/%{_sysconfdir}/init.d $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
install -o 0 -g 0 support/wipld.conf $RPM_BUILD_ROOT/%{_sysconfdir}/wipld.conf
install -o 0 -g 0 redhat/wipld $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/wipld
install -o 0 -g 0 redhat/logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/wipld

%post
chkconfig --add wipld

%preun
if [ -e /%{_localstatedir}/run/wipld.pid ]; then
  /%{_sysconfdir}/init.d/wipld stop
fi
chkconfig --del wipld

%postun
rm -f %{_localstatedir}/log/wipld.*
rm -f %{_localstatedir}/run/wipld.pid

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/wipld
%attr(755,root,root) %{_sbindir}/wiplcInetd
%attr(755,root,root) %{_bindir}/wiplc
%attr(755,root,root) %{_bindir}/wiplcSimple
%attr(755,root,root) %{_bindir}/wiplcExec
%{_sysconfdir}/init.d/wipld
%{_sysconfdir}/logrotate.d/wipld
%{_mandir}/man?/*
%config %{_sysconfdir}/wipld.conf
%doc wipl.lsm ChangeLog AUTHORS README NEWS FAQ support wiplJava
