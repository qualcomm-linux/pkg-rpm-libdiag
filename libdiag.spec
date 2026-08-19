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

# Prebuilt aarch64 ELF binaries only; building on another arch would mislabel
# the RPM. Skip auto debuginfo extraction: there is no matching source tree
# for find-debuginfo to pair with these prebuilt binaries.
ExclusiveArch:  aarch64
%global debug_package %{nil}

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
# Verified against the real tarball fetched from Source0: the Debian-multiarch
# tree uses usr/lib/aarch64-linux-gnu (not usr/lib64), and libdiag.so.1's real
# target is libdiag.so.1.0.3 even though the package version is 1.0.4. The
# tarball ships no top-level LICENSE/README.md (Debian-style per-component
# doc/copyright files instead), so %license/%doc below point at those.
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_bindir} %{buildroot}%{_includedir}
cp -a data/qcom-libdiag/arm64/usr/lib/aarch64-linux-gnu/. %{buildroot}%{_libdir}/
cp -a data/qcom-diag/arm64/usr/bin/. %{buildroot}%{_bindir}/
cp -a data/qcom-libdiag-dev/arm64/usr/include/. %{buildroot}%{_includedir}/
cp -a data/qcom-libdiag-dev/arm64/usr/lib/aarch64-linux-gnu/pkgconfig %{buildroot}%{_libdir}/

%files
%license data/qcom-diag/arm64/usr/share/doc/qcom-diag/copyright
%doc data/qcom-diag/arm64/usr/share/doc/qcom-diag/changelog.gz
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*

%changelog
* Wed Aug 19 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.4-1
- Initial RPM packaging, ported from the Debian packaging in
  qualcomm-linux/pkg-libdiag (qcom/ubuntu/resolute branch).
