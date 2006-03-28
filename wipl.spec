Summary:	Make statistics on basis of packets seen on a LAN
Summary(pl):	Tworzenie statystyk na bazie pakietów zauwa¿onych w sieci lokalnej
Name:		wipl
Version:	020601
Release:	1
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://wipl-wrr.sourceforge.net/tgz-wipl/%{name}-%{version}.tar.gz
# Source0-md5:	ccd8895d8297c98bcf8e02a4d1911e66
URL:		http://wipl-wrr.sourceforge.net/wipl.html
BuildRequires:	flex
BuildRequires:	libpcap-devel
BuildRequires:	libstdc++-devel
BuildRequires:	perl-base
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
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

%description -l pl
Program wipl potrafi prowadziæ i wy¶wietlaæ statystyki bazuj±c na
pakietach zauwa¿onych przez kartê sieciow±.

Pakiet zawiera demona, który prowadzi statystyki. Dla ka¿dego pakietu
zauwa¿onego przez kartê sieciow± demon wykonuje ma³y program wskazany
przez u¿ytkownika. Program ten mo¿e uaktualniaæ statystyki u¿ywaj±c
informacji o pakiecie. Musi byæ napisany w bardzo prostym, wbudowanym
jêzyku programowania.

Pakiet zawiera tak¿e kilka programów klienckich, które mog± odczytywaæ
lub modyfikowaæ statystyki prowadzone przez demona. Te tabele mog± byæ
zapisane do plików HTML lub XML, co pozwala na ³atw± publikacjê na
stronach WWW.

Na stronie projektu wipl dostêpne jest rozszerzenie pozwalaj±ce
programowi wspó³pracowaæ z serwerami proxy takimi jak Squid i socks5.

%prep
%setup -q

%build
%{__perl} -pi -e 's/net\/bpf.h/pcap-bpf.h/g' configure
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,logrotate.d},%{_sysconfdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install support/wipld.conf $RPM_BUILD_ROOT%{_sysconfdir}/wipld.conf
install redhat/wipld $RPM_BUILD_ROOT/etc/rc.d/init.d/wipld
install redhat/logrotate $RPM_BUILD_ROOT/etc/logrotate.d/wipld

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add wipld

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/run/wipld.pid ]; then
		/etc/rc.d/init.d/wipld stop
	fi
	/sbin/chkconfig --del wipld
	rm -f /var/run/wipld.pid
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ README support wiplJava
%attr(755,root,root) %{_sbindir}/wipld
%attr(755,root,root) %{_sbindir}/wiplcInetd
%attr(755,root,root) %{_bindir}/wiplc
%attr(755,root,root) %{_bindir}/wiplcSimple
%attr(755,root,root) %{_bindir}/wiplcExec
%attr(754,root,root) /etc/rc.d/init.d/wipld
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/wipld
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wipld.conf
%{_mandir}/man?/*
