Name:           ledmon
Version:        0.90
Release:        intel_5.4%{dist}
Group:          System/Base
License:        GPL
Vendor:         Intel Corporation
URL:            http://sourceforge.net/projects/ledmon/
Summary:        LED control application for a storage enclosure.
Source0:        %{name}.tar.gz
Source1:        ledmon.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       ledctl = %{version}-%{release}
Provides:       ledmon = %{version}-%{release}

%description
ledmon - Intel(R) LED control application for a storage enclosure.
Ledmon is an user space application designed to control LEDs associated with each slot in an enclosure or a drive bay.

%prep
%setup -q -n %{name}

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT SBIN_DIR=$RPM_BUILD_ROOT/%{_sbindir} MANDIR=$RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -m 644 %{_sourcedir}/ledmon.service $RPM_BUILD_ROOT/usr/lib/systemd/system

%clean
rm -rf $RPM_BUILD_ROOT

%preun
systemctl stop ledmon.service
systemctl disable ledmon.service

%post
systemctl daemon-reload
systemctl enable ledmon.service
systemctl start ledmon.service

%files
%defattr(-,root,root,-)
%doc README COPYING
/usr/lib/systemd/system/ledmon.service
%{_sbindir}/ledmon
%{_sbindir}/ledctl
%{_mandir}/*/*

%changelog
* Thu Feb 15 2018 Mariusz Dabrowski <mariusz.dabrowski@intel.com> - 0.90
- Possibility to list all controllers detected by ledctl.
- Configuration file for ledmon advanced features.
- Added option to ledctl for managing only listed devices.
- Documentation improvements.
- Blinking failure LED after removing disk from RAID.
- Refactoring of SES-2 protocol implementation. SES minor fixes.
- Logfile and log levels small improvements.

* Mon Nov 13 2017 Artur Paszkiewicz <artur.paszkiewicz@intel.com> - 0.81
- Handle udev events in ledmon
- Bugfixes

* Tue Sep 19 2017 Pawel Baldysiak <pawel.baldysiak@intel.com>
- Fixes ordering for SMP GPIO_TX registers
- few minor bugfixes

* Mon Jan 16 2017 Pawel Baldysiak <pawel.baldysiak@intel.com>
- Make VMD sysfs blinking method default for NVMe drives under VMD

* Fri Oct 28 2016 Pawel Baldysiak <pawel.baldysiak@intel.com> - 0.80
- Add support for NVMe under VMD domain connected to NC HSBP

* Thu Dec 4 2014 Pawel Baldysiak <pawel.baldysiak@intel.com>
- Replace sysvinit script with systemd unit file

* Fri Nov 15 2013 Lukasz Dorau <lukasz.dorau@intel.com> - 0.79
- Added support for NVME SSD devices (uses nvme/nvmhci block driver)
- Updated help info regarding reporting bugs

* Fri Jun 21 2013 Lukasz Dorau <lukasz.dorau@intel.com> - 0.78
- Make ledctl work if libahci is not a kernel module
- ledctl documentation improvements
- Minor bug fixes

* Tue Feb 05 2013 Lukasz Dorau <lukasz.dorau@intel.com> - 0.77
- Do not send LED command if state of block device has not changed

* Thu Jan 17 2013 Lukasz Dorau <lukasz.dorau@intel.com> - 0.76
- ledmon's behavior during rebuild changed

* Tue Dec 11 2012 Lukasz Dorau <lukasz.dorau@intel.com> - 0.75
- Support for the Dell PCIe SSD devices added
- Some minor fixes revealed by a coverity scan

* Thu Aug 9 2012 Lukasz Dorau <lukasz.dorau@intel.com> - 0.74
- Restart of the ledmon's internal state when an unrecoverable error occurs
  (e.g. lack of disk's location)
- Logging level for not supported patterns changed from 'warning' to 'debug'

* Mon Aug 6 2012 Lukasz Dorau <lukasz.dorau@intel.com> - 0.72
- More detailed information about device change (name changed, missing)
- Added extra checks against device presence in sysfs (device may disappear
  at anytime: during rescan, initialization, sending command)
- Pattern "locate_off" fixed

* Thu Jul 26 2012 Maciej Naruszewicz <maciej.naruszewicz@intel.com> - 0.70
- SES-2 support for enclosures
- New patterns (SES-2) in ledctl for drives in enclosures
- Several bugfixes
- Improved LED blinking and slot locations for AHCI and SCSI DA

* Fri Jul 13 2012 Maciej Naruszewicz <maciej.naruszewicz@intel.com> - 0.40
- Start logging changes
- Added sysvinit script for ledmon
- Added mising RPM data
