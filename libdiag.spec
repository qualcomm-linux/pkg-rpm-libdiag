# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
Name:           libdiag
Version:        1.0.4
Release:        1%{?dist}
Summary:        Qualcomm diagnostic framework shared library and tools

License:        BSD-3-Clause
URL:            https://github.com/qualcomm-linux/pkg-libdiag
# Prebuilt binary tarball published to Artifactory (same artifact used by the
# Debian packaging in qualcomm-linux/pkg-libdiag, see its upstream.conf).
# %{name} and %{version} are NOT expanded here because the upstream tarball's
# own naming ("qcom-diag_<ver>_arm64") doesn't match this package's Name:.
Source0:        https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/core-technologies.qclinux.0.0/260513/prebuilt_resolute/qcom-diag_1.0.4_arm64.tar.gz

%description
Shared library and command-line tools for the Qualcomm diagnostic (diag)
framework, used to route diagnostic messages between the host and modem.
This package bundles what the Debian packaging in qualcomm-linux/pkg-libdiag
splits into qcom-libdiag, qcom-libdiag-dev, and qcom-diag.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Headers, static libraries, and pkg-config files for %{name}.

%prep
%setup -q -c -n %{name}-%{version}

%build
# Prebuilt binaries only; nothing to compile.

%install
rm -rf %{buildroot}
# NOTE: the tarball's internal layout could not be verified while packaging
# this spec (Artifactory returns 401/403 on anonymous access — same gap noted
# in pkg-rpm-time-services/README.md for qmi-framework). This mirrors the
# Debian packaging's arm64 install layout in qualcomm-linux/pkg-libdiag
# (debian/rules: data/qcom-libdiag/arm64, data/qcom-libdiag-dev/arm64,
# data/qcom-diag/arm64) and MUST be verified/adjusted once the real tarball
# is fetchable.
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_bindir} %{buildroot}%{_includedir}
cp -a data/qcom-libdiag/arm64/usr/lib64/* %{buildroot}%{_libdir}/ 2>/dev/null || :
cp -a data/qcom-diag/arm64/usr/bin/* %{buildroot}%{_bindir}/ 2>/dev/null || :
cp -a data/qcom-libdiag-dev/arm64/usr/include/* %{buildroot}%{_includedir}/ 2>/dev/null || :
cp -a data/qcom-libdiag-dev/arm64/usr/lib64/pkgconfig %{buildroot}%{_libdir}/ 2>/dev/null || :

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*

%changelog
* Wed Aug 19 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.4-1
- Initial RPM packaging, ported from the Debian packaging in
  qualcomm-linux/pkg-libdiag (qcom/ubuntu/resolute branch).
