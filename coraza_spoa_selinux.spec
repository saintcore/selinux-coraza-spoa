# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/sbin/coraza-spoa; \

%define selinux_policyver 38.1.53-5

Name:   coraza_spoa_selinux
Version:        1.1.0
Release:        1%{?dist}
Summary:        SELinux policy module for coraza_spoa

Group:  System Environment/Base
License:        AGPL-3.0-only
# This is an example. You will need to change it.
# For a complete guide on packaging your policy
# see https://fedoraproject.org/wiki/SELinux/IndependentPolicy
URL:            https://github.com/saintcore/selinux-coraza-spoa
Source0:        coraza_spoa.pp
Source1:        coraza_spoa.if
Source2:        coraza_spoa_selinux.8


Requires: policycoreutils-python-utils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for coraza_spoa.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/coraza_spoa_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/coraza_spoa.pp

if [ $1 -eq 1 ]; then

fi
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then

    semodule -n -r coraza_spoa
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/coraza_spoa.pp
%{_datadir}/selinux/devel/include/contrib/coraza_spoa.if
%{_mandir}/man8/coraza_spoa_selinux.8.*


%changelog
* Sat Nov 15 2025 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version
