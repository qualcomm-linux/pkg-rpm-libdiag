<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# libdiag (Diagnostic library)

**This is the branch for CentOS 10 Stream (`c10s`).** It holds the `libdiag` RPM's spec file
and `sources` pointer, plus the CI workflows that build and publish them.

Following the Fedora/CentOS **dist-git** convention, each distro stream gets its
own branch, and the packaging files live at the branch root:

| Branch | Stream | Contents |
|---|---|---|
| `main` | — | Template docs, onboarding guide, community files. Nothing is built here. |
| **`c10s`** | CentOS 10 Stream | **This branch.** `libdiag.spec` + `sources` + workflows. |

Full onboarding guide, configuration reference, and troubleshooting live on
[`main`](../../tree/main) — see its `README.md` and `docs/workflows.md`.

---

## Layout

```
libdiag.spec              # RPM spec for the Qualcomm diag framework library/tools
sources                   # dist-git checksum pointer for the qcom-diag prebuilt tarball
.github/workflows/        # build-on-pr.yml, pkg-release.yml
```

This RPM packages the same Artifactory-published prebuilt binary tarball as
the Debian packaging in
[`qualcomm-linux/pkg-libdiag`](https://github.com/qualcomm-linux/pkg-libdiag):
the Qualcomm diagnostic (diag) shared library and command-line tools, used to
route diagnostic messages between the host and MSM.

The current `sources` file contains the SHA512 checksum for
`diag-1.0.5_1.el10.aarch64.tar.gz`. Keep the `Source0:` filename in
[`libdiag.spec`](libdiag.spec) and the filename in `sources` synchronized when
updating the package.

## Package contents

The spec produces three RPMs from the prebuilt payload:

| Package | Contents | Use when you need |
|---|---|---|
| `qcom-libdiag` | Versioned `libdiag.so.1*` runtime library and license | Applications that use the diag shared library at runtime. |
| `qcom-diag` | Command-line tools and sample applications | The diag utilities; this package requires `qcom-libdiag`. |
| `qcom-libdiag-devel` | Headers, the unversioned `libdiag.so` symlink, and `diag.pc` | Building applications against libdiag; this package requires `qcom-libdiag`. |

The payload contains prebuilt **aarch64** binaries, so the package is restricted
to that architecture.

---
