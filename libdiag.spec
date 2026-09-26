# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
Name:           qcom-libdiag
Version:        1.0.5
Release:        1%{?dist}
Summary:        Qualcomm diagnostic framework shared library and tools

License:        BSD-3-Clause
URL:            https://github.com/qualcomm-linux/pkg-libdiag

Source0:        https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/core-technologies.qclinux.0.0/260925.1/prebuilt_rpm/libdiag/diag-1.0.5_1.el10.aarch64.tar.gz

# Prebuilt aarch64 ELF binaries only; building on another arch would mislabel
# the RPM. Skip auto debuginfo extraction: there is no matching source tree
# for find-debuginfo to pair with these prebuilt binaries.
ExclusiveArch:  aarch64
%global debug_package %{nil}

%description
Shared library for the Qualcomm diagnostic (diag) framework, used to route
diagnostic messages between the host and modem.

%package -n qcom-diag
Summary:        Qualcomm diagnostic framework command-line tools
Requires:       qcom-libdiag = %{version}-%{release}

%description -n qcom-diag
Command-line tools and sample applications for the Qualcomm diagnostic (diag)
framework.

%package -n qcom-libdiag-devel
Summary:        Development files for %{name}
Requires:       qcom-libdiag = %{version}-%{release}

%description -n qcom-libdiag-devel
Headers, unversioned library symlink, and pkg-config files for qcom-libdiag.

%prep
%setup -q -n diag-%{version}

%build
# Prebuilt binaries only; nothing to compile.

%install
rm -rf %{buildroot}
# The archive contains a prebuilt RPM-style filesystem rooted at usr/.
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_bindir} %{buildroot}%{_includedir}
cp -a usr/lib64/. %{buildroot}%{_libdir}/
cp -a usr/bin/. %{buildroot}%{_bindir}/
cp -a usr/include/. %{buildroot}%{_includedir}/
cp -a usr/lib64/pkgconfig %{buildroot}%{_libdir}/

%files
%license usr/share/licenses/diag/LICENSE.qcom-2
%{_libdir}/libdiag.so.1*

%files -n qcom-diag
%doc usr/share/doc/diag/CHANGES
%{_bindir}/*

%files -n qcom-libdiag-devel
%{_includedir}/diag
%{_libdir}/libdiag.so
%{_libdir}/pkgconfig/diag.pc

%changelog
* Sat Sep 26 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.5-1
- Split the prebuilt diag payload into library, tools, and development RPMs.

* Wed Aug 19 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.4-1
- Initial RPM packaging, ported from the Debian packaging in
  qualcomm-linux/pkg-libdiag (qcom/ubuntu/resolute branch).
