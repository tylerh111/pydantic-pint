# ==============================================================================
# settings
# ==============================================================================

_version_fallback := "0.6.0"
_version := if shell("which setuptools-scm || true") != "" {
    shell("setuptools-scm")
} else {
    _version_fallback
}

_default_package_repo := "testpypi"
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

[private]
[doc("run formatter (diff)")]
[group("dev")]
format-diff:
    ruff format --diff

[doc("run linter")]
[group("dev")]
lint:
    ruff check --fix

[private]
[doc("run linter (check)")]
[group("dev")]
lint-check:
    ruff check --no-fix

[private]
[doc("run linter (diff)")]
[group("dev")]
lint-diff:
    ruff check --no-fix --diff --exit-zero

[doc("run test")]
[group("dev")]
test:
    pytest

[private]
[doc("run test (verbose)")]
[group("dev")]
test-verbose:
    pytest -v

[private]
[doc("run tests matrix")]
[group("dev")]
test-matrix:
    UV_PROJECT_ENVIRONMENT=.venv/3.15/ uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.14/ uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.13/ uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.12/ uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.11/ uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.10/ uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.9/  uv run --no-default-groups --group test pytest -q
    UV_PROJECT_ENVIRONMENT=.venv/3.8/  uv run --no-default-groups --group test pytest -q


[private]
[doc("run tests matrix (single)")]
[group("dev")]
[arg("ver")]
test-matrix-single ver:
    UV_PROJECT_ENVIRONMENT=.venv/{{ ver }}/  uv run --no-default-groups --group test pytest -q


[doc("build package")]
[group("dev")]
build:
    python -m build .


# ==============================================================================
# environment
# ==============================================================================

[doc("environment create")]
[group("env")]
env-create:
    mkdir -p .venv/
    uv venv -p 3.15 --allow-existing .venv/3.15/
    uv venv -p 3.14 --allow-existing .venv/3.14/
    uv venv -p 3.13 --allow-existing .venv/3.13/
    uv venv -p 3.12 --allow-existing .venv/3.12/
    uv venv -p 3.11 --allow-existing .venv/3.11/
    uv venv -p 3.10 --allow-existing .venv/3.10/
    uv venv -p 3.9  --allow-existing .venv/3.9/
    uv venv -p 3.8  --allow-existing .venv/3.8/

[doc("environment sync")]
[group("env")]
env-sync:
    UV_PROJECT_ENVIRONMENT=.venv/3.15/ uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.14/ uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.13/ uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.12/ uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.11/ uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.10/ uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.9/  uv sync --group all
    UV_PROJECT_ENVIRONMENT=.venv/3.8/  uv sync --group all

# ==============================================================================
# documentation
# ==============================================================================

[doc("build documentation")]
[group("docs")]
build-docs:
    zensical build

[doc("serve documentation")]
[group("docs")]
serve-docs:
    zensical serve

# ==============================================================================
# release
# ==============================================================================

[private]
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
        git commit -m "release version $new_version"
        # git tag -m "$new_version" "$new_version"
    fi

[private]
[doc("release package to pypi")]
[group("release")]
release-build repo=_default_package_repo: clean-dist-folder build
    twine upload \
        -r {{ repo }} \
        {{ _default_dist_dir }}/*

# ==============================================================================
# helpers
# ==============================================================================

[private]
[doc("clean package builds from dist folder")]
[group("helpers")]
clean-dist-folder:
    rm -rf {{ _default_dist_dir }}
