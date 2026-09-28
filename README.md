# Qualcomm libdiag RPM packaging

This repository contains the RPM packaging for Qualcomm's diagnostic (`diag`)
framework. The library and tools route diagnostic messages between the host and
modem.

The packaged payload is a prebuilt binary release. This repository does not
compile the diag sources; the RPM spec stages the files from the upstream
Artifactory tarball and splits them into runtime, tools, and development
packages.

The corresponding Debian packaging is maintained in
[`qualcomm-linux/pkg-libdiag`](https://github.com/qualcomm-linux/pkg-libdiag).

---

## Packages

The CentOS 10 Stream spec currently produces these RPMs:

| Package | Contents | Dependency |
|---|---|---|
| `qcom-libdiag` | Versioned `libdiag.so.1*` runtime library and license | — |
| `qcom-diag` | Diagnostic command-line tools and sample applications | `qcom-libdiag` |
| `qcom-libdiag-devel` | Headers, the unversioned `libdiag.so` linker symlink, and `diag.pc` | `qcom-libdiag` |

The prebuilt payload is currently restricted to **aarch64**. The package is
licensed under **BSD-3-Clause**. The current CentOS 10 Stream package version is
`1.0.5`.

---

## Branches

The repository follows a Fedora/CentOS dist-git-style branch layout:

| Branch | Purpose |
|---|---|
| [`main`](../../tree/main) | Repository documentation, shared workflows, and project files. |
| [`c10s`](../../tree/c10s) | CentOS 10 Stream packaging branch containing `libdiag.spec`, `sources`, and the package workflows. |

The package build and release work happens on [`c10s`](../../tree/c10s). See
that branch's [`README.md`](../../tree/c10s/README.md) for the stream-specific
maintenance instructions.

---

## Repository layout

Common repository files live on `main`:

```
README.md                  # Project overview and maintenance guidance
docs/workflows.md          # Shared CI, source-cache, and release reference
.github/workflows/         # GitHub Actions workflow callers
LICENSE.txt                # Repository license
```

The package definition lives on `c10s`:

```
libdiag.spec               # RPM spec and package split
sources                    # Source tarball checksum and filename
```

The repository intentionally tracks the spec and checksum pointer, not the
binary source tarball itself.

---

## Maintaining the package

Make package changes on the [`c10s`](../../tree/c10s) branch.

### Update the version

1. Bump `Version:` in [`libdiag.spec`](../../blob/c10s/libdiag.spec). Update the
   `Source0:` URL as well if the upstream Artifactory path changes.
2. Obtain the matching prebuilt tarball and regenerate `sources` with its exact
   filename. The current naming pattern is
   `diag-<version>_<build>.el10.aarch64.tar.gz`:

   ```bash
   sha512sum --tag diag-<newversion>_<build>.el10.aarch64.tar.gz > sources
   ```

   The filename in `sources` must match the `Source0:` basename exactly.
3. Commit the spec and `sources` changes and open a pull request against `c10s`.
   The PR build verifies the checksum and builds the RPMs.
4. After the change is merged, run **Actions → Release → Run workflow** on the
   `c10s` branch. The release workflow builds and publishes the RPMs after the
   configured approval gate.

Source tarballs are resolved from the Artifactory lookaside cache when
available. On a cache miss, the build downloads the tarball from `Source0:` and
verifies it against `sources`; release builds can cache a verified download for
future builds. See [`docs/workflows.md`](docs/workflows.md) for the shared
workflow and source-resolution details.

---

## Related documentation

- [`c10s/README.md`](../../tree/c10s/README.md) — CentOS 10 Stream package-branch instructions
- [`docs/workflows.md`](docs/workflows.md) — CI, lookaside-cache, and release behavior
- [`libdiag.spec`](../../blob/c10s/libdiag.spec) — current RPM metadata and file split
- [`sources`](../../blob/c10s/sources) — current source checksum pointer
- [`qualcomm-linux/pkg-libdiag`](https://github.com/qualcomm-linux/pkg-libdiag) — corresponding Debian packaging
