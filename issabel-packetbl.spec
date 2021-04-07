%define modname packetbl

Summary: Packet Blacklist
Name: issabel-packetbl
Version: 1.0
Release: 1
License: GPL
Group: System
Url: http://www.issabel.org
Source0: issabel-%{modname}-%{version}.tar.gz
Source1: libpool.h
Source2: libpool.a
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires:	dotconf-devel
BuildRequires:  /usr/include/dotconf.h
BuildRequires:	libnetfilter_queue-devel
BuildRequires:	libnfnetlink-devel
BuildRequires:  openssl-devel
Buildrequires:  ldns-devel

Requires:       libnetfilter_queue
Requires:       fail2ban-server


%description
Packetbl checks IP addresses of incoming connections against RBLs
and uses Netfilter/iptables to block them if they're listed.

%prep
%setup -n %{name}-%{version}
cp %{SOURCE1} /usr/include
cp %{SOURCE2} /usr/lib64

%build
%configure --with-cache --with-stats 
mkdir bin
%__make

%install
rm -rf %{buildroot}
%__make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/etc/fail2ban/action.d
mkdir -p %{buildroot}/etc/systemd/system
mkdir -p %{buildroot}/etc/sysconfig
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/packetbl

cp issabel/issabelrbl.conf %{buildroot}/%{_sysconfdir}/fail2ban/action.d
cp issabel/iptables-multiport-issabelrbl.conf %{buildroot}/etc/fail2ban/action.d
cp packetbl.service %{buildroot}/%{_sysconfdir}/systemd/system
cp packetbl.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/packetbl

%clean
rm -rf %{buildroot}

%post
if [ -f /etc/fail2ban/jail.local ]; then
grep "START packetbl" /etc/fail2ban/jail.local &>/dev/null
if [ $? -eq 1 ]; then
cat >> /etc/fail2ban/jail.local <<'ISSABELJAILLOCAL'
#START packetbl
[asterisk]
banaction = iptables-multiport-issabelrbl
action    = %%(banaction)s[name=%%(__name__)s-tcp, port="%%(port)s", protocol="tcp", chain="%%(chain)s", actname=%%(banaction)s-tcp]
            %%(banaction)s[name=%%(__name__)s-udp, port="%%(port)s", protocol="udp", chain="%%(chain)s", actname=%%(banaction)s-udp]
            %%(mta)s-whois[name=%%(__name__)s, dest="%%(destemail)s"]
            issabelrbl
#END packetbl
ISSABELJAILLOCAL
fi
else
cat >> /etc/fail2ban/jail.local <<'ISSABELJAILLOCAL'
#START packetbl
[asterisk]
banaction = iptables-multiport-issabelrbl
action    = %%(banaction)s[name=%%(__name__)s-tcp, port="%%(port)s", protocol="tcp", chain="%%(chain)s", actname=%%(banaction)s-tcp]
            %%(banaction)s[name=%%(__name__)s-udp, port="%%(port)s", protocol="udp", chain="%%(chain)s", actname=%%(banaction)s-udp]
            %%(mta)s-whois[name=%%(__name__)s, dest="%%(destemail)s"]
            issabelrbl
#END packetbl
ISSABELJAILLOCAL

fi

%postun
sed -i '/#START packetbl/,/#END packetbl/d' /etc/fail2ban/jail.local

%preun
systemctl stop packetbl

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/packetbl/packetbl.conf
%{_sysconfdir}/systemd/system/packetbl.service
%{_sysconfdir}/sysconfig/packetbl
%{_bindir}/packetbl
%{_bindir}/packetbl_getstat
%{_sysconfdir}/fail2ban/action.d/issabelrbl.conf
%{_sysconfdir}/fail2ban/action.d/iptables-multiport-issabelrbl.conf

%changelog
