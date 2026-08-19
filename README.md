<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# Package branch — CentOS 10 Stream (`c10s`)

**This is the branch you work on.** It holds the `libdiag` RPM's spec file
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
[`qualcomm-linux/pkg-libdiag`](https://github.com/qualcomm-linux/pkg-libdiag)
(`qcom/ubuntu/resolute` branch, `upstream.conf`): the Qualcomm diagnostic
(diag) shared library and command-line tools, used to route diagnostic
messages between the host and modem. Debian splits this into three packages
(`qcom-libdiag`, `qcom-libdiag-dev`, `qcom-diag`); this spec bundles the
runtime library/tools into `libdiag` and the headers/pkg-config files into
`libdiag-devel`, matching the RPM `-devel` subpackage convention.

[`pkg-rpm-diag-router`](https://github.com/qualcomm-linux/pkg-rpm-diag-router)
packages the companion `qcom-diag-router` daemon and depends on this package.

> **Known gap:** the upstream tarball at `Source0` lives behind
> `qartifactory-edge.qualcomm.com`, which returned 401/403 on anonymous access
> while authoring this spec — the same access gap already tracked for
> `qmi-framework` in
> [`pkg-rpm-time-services`](https://github.com/qualcomm-linux/pkg-rpm-time-services)'s
> README. The `sources` file therefore holds a **placeholder checksum** and
> the `%install` layout (which directory in the tarball maps to which RPM
> file) is inferred from the Debian packaging's `debian/rules`, not verified
> against the real archive. Both must be confirmed/corrected once the tarball
> is fetchable.

---

## Getting started

### Update the version

Two edits, every time:

1. Bump `Version:` in [`libdiag.spec`](libdiag.spec) (and the `Source0:` URL's
   `TAG`/filename if the upstream Artifactory path changed — see
   `upstream.conf` in `pkg-libdiag` for the current `TAG`/`PACKAGE_NAME`).
2. Recompute the checksum:
   ```bash
   sha512sum --tag qcom-diag_<newversion>_arm64.tar.gz > sources
   ```

Commit both, open a PR against this branch, merge, then run **Release**. The
first release fetches the new upstream tarball, verifies it, and caches it back
automatically.

### Open a PR

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM.
Download it from the run's **Artifacts**.

### Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer
approves the `pkg-release-approval` gate, then the RPM publishes to
Artifactory.
