# ==============================================================================
# settings
# ==============================================================================

_version_fallback := "0.4"
_version := if shell("which setuptools-scm || true") != "" {
    shell("setuptools-scm")
} else {
    _version_fallback
}

_default_package_repo := "pypi"
_default_package_name := "pydantic_pint"

_default_dist_dir := "dist"
_default_docs_dir := "docs"
_default_site_dir := "site"

# ==============================================================================
# general
# ==============================================================================

[default]
[doc("shows available recipes")]
[group("general")]
recipes:
    @just --list

[doc("shows version of code")]
[group("general")]
version:
    @echo {{ _version }}

# ==============================================================================
# development
# ==============================================================================

[doc("run formatter")]
[group("dev")]
format:
    ruff format

[private]
[doc("run formatter (check)")]
[group("dev")]
format-check:
    ruff format --check

[doc("run linter")]
[group("dev")]
lint:
    ruff check --fix

[private]
[doc("run linter (check)")]
[group("dev")]
lint-check:
    ruff check --no-fix --diff --exit-zero

[doc("run test")]
[group("dev")]
test:
    pytest

[private]
[doc("run test (verbose)")]
[group("dev")]
test-check:
    pytest -v

# ==============================================================================
# documentation
# ==============================================================================

[doc("build documentation")]
[group("documentation")]
build-docs:
    zensical build

[doc("serve documentation")]
[group("documentation")]
serve-docs:
    zensical serve

[doc("release documentation")]
[group("documentation")]
[arg("no-push", long, value="true")]
release-docs no-push="false":
    mike deploy \
        --branch site \
        --remote site \
        --update-aliases \
        {{ if no-push == "true" { "" } else { "--push" } }} \
        {{ _version }} \
        dev

# ==============================================================================
# release
# ==============================================================================

[doc("build wheel package")]
[group("release")]
build-wheel:
    python -m build .

[doc("prepare code for release")]
[group("release")]
[arg("bump")]
[arg("dry", long, short="n", value="true")]
release-prepare bump dry="false":
    #!/usr/bin/env bash
    set -eux -o pipefail

    if [ "{{ dry }}" == "false" ] && [ -n "{{ `git status --porcelain` }}" ]; then
        echo "error: working directory not clean: aborting"
        exit 1
    fi

    bump-my-version bump \
        {{ if dry == "true" { "-n -v" } else { "" } }} \
        --allow-dirty \
        --no-commit \
        --no-tag \
        {{ bump }}

    towncrier build \
        {{ if dry == "true" { "--draft" } else { "" } }} \
        "--yes"

    if [ "{{ dry }}" == "false" ]; then
        new_version=$(bump-my-version show current_version 2> /dev/null)
        git add .
        git commit -m "releaes version $new_version"
        git tag -m "$new_version" "$new_version"
    fi

[private]
[doc("(wip) release package to artifactory")]
[group("release")]
release-build:
    twine upload \
        -r {{ _default_package_repo }} \
        {{ _default_dist_dir + "/" + _default_package_name + "-" + _version + "-py3-none-any.whl" }} \
        {{ _default_dist_dir + "/" + _default_package_name + "-" + _version + ".tar.gz" }}

# ==============================================================================
# helpers
# ==============================================================================

[private]
[doc("clean package builds from dist folder")]
[group("helpers")]
clean-dist-folder:
    rm dist/*
