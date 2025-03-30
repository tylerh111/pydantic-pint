from __future__ import annotations

import argparse
import os.path
from pathlib import Path
from typing import Any, Mapping, Sequence

import nox
import setuptools_scm

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["lint", "test"]

PACKAGE = "pydantic-pint"
REPO = "pypi"
DIST = Path("dist")
DOCS = Path("docs")
SITE = Path("site")
REPORTS = Path("reports")


def _get_package():
    return PACKAGE


def _get_version():
    return setuptools_scm.get_version(version_scheme="no-guess-dev")


def _add_args_if(
    test: bool,
    *args: str,
):
    """Usage: `*_add_args_if(...)`"""
    return args if test else ()


def _parse_args(
    session: nox.Session,
    args: Sequence[str],
    name: str,
    *options: Mapping[str, Any],
    description: str | None = None,
    epilog: str | None = None,
    command: str | None = None,
    add_ellipse_to_usage: bool = True,
):
    """Usage: _parser_args(session.posargs, <name>, <argument>, ...)"""

    class EllipsisHelpFormatter(argparse.RawTextHelpFormatter):
        @staticmethod
        def _add_ellipse_to_usage(usage: str):
            if not add_ellipse_to_usage:
                return usage
            has_newline = usage.endswith("\n")
            usage = usage.rstrip("\n")
            usage = (usage + " ...") if not usage.endswith("...") else usage
            usage = (usage + "\n") if has_newline else usage
            return usage

        def format_help(self):
            help = super().format_help()
            if help:
                usage, *help = help.splitlines(keepends=True)
                usage = self._add_ellipse_to_usage(usage)
                help = "".join((usage, *help))
            return help

    if not command:
        command = "underlying command(s)"

    if not epilog:
        epilog = f"remaining:\n  passed to {command}"

    parser = argparse.ArgumentParser(
        prog=name,
        description=description,
        formatter_class=EllipsisHelpFormatter,
        epilog=epilog,
    )
    for option in options:
        names = option.pop("args")
        names = [names] if isinstance(names, str) else names
        parser.add_argument(*names, **option)

    try:
        return parser.parse_known_intermixed_args(args)
    except SystemExit:
        session.error()


# =============================================================================
#  sessions
# =============================================================================


@nox.session(name="version")
def version(session: nox.Session):
    """Show version"""
    package = _get_package()
    version = _get_version()
    session.log(f"{package} {version}")


@nox.session(name="lint")
def lint(session: nox.Session):
    """Run linter"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s lint",
        dict(
            args=["-o", "--output"],
            type=Path,
            default=REPORTS,
            help="output directory for generated reports",
        ),
        dict(
            args=["--report"],
            action=argparse.BooleanOptionalAction,
            default=False,
            help="generate report",
        ),
        command="`ruff check`",
    )

    output: Path = args.output
    report: bool = args.report

    if report:
        output.mkdir(exist_ok=True)

    def ruff_check_command():
        return [
            "ruff",
            "check",
            "--exit-zero",
            *_add_args_if(
                report,
                "--output-file", f"{output / 'ruff.txt'}",
            ),
            ".",
        ]  # fmt: skip

    session.install("-e", ".[lint]")
    session.log(f"# Running ruff")
    session.run(*ruff_check_command(), *remaining)


@nox.session(name="format")
def format(session: nox.Session):
    """Run formatter"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s format",
        dict(
            args=["--fix"],
            action=argparse.BooleanOptionalAction,
            default=True,
            help="fix formatting and linting warnings",
        ),
        command="`ruff format`",
    )

    fix: bool = args.fix

    def ruff_check_command():
        return [
            "ruff",
            "check",
            "--fix",
            *_add_args_if(not fix, "--no-fix", "--diff"),
            ".",
        ]  # fmt: skip

    def ruff_format_command():
        return [
            "ruff",
            "format",
            *_add_args_if(not fix, "--check", "--diff"),
            ".",
        ]  # fmt: skip

    session.install("-e", ".[lint]")
    session.log(f"# Running ruff")
    session.run(*ruff_check_command(), success_codes=(0, 1))
    session.run(*ruff_format_command(), *remaining, success_codes=(0, 1))


@nox.session(name="test")
def test(session: nox.Session):
    """Run tests"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s test",
        dict(
            args=["-o", "--output"],
            type=Path,
            default=REPORTS,
            help="output directory for generated reports",
        ),
        dict(
            args=["--report"],
            action=argparse.BooleanOptionalAction,
            default=False,
            help="generate report",
        ),
        command="`pytest`",
    )

    output: Path = args.output
    report: bool = args.report
    package = _get_package()

    if report:
        output.mkdir(exist_ok=True)

    def pytest_command():
        return [
            "pytest",
            *_add_args_if(
                report,
                f"--cov={package}",
                f"--cov-report=xml:{output / 'coverage.xml'}"),
            "tests",
        ]  # fmt: skip

    session.install("-e", ".[tests]")
    session.log(f"# Running ruff")
    session.run(*pytest_command(), *remaining, success_codes=(0, 5))


@nox.session(name="build")
def build(session: nox.Session):
    """Build Package"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s test",
        dict(
            args=["-o", "--output"],
            type=Path,
            default=DIST,
            help="output directory for generated reports",
        ),
        dict(
            args=["-c", "--clean"],
            action=argparse.BooleanOptionalAction,
            default=True,
            help="clean output directory",
        ),
        command="`python -m build`",
    )

    dist: Path = args.output
    clean: bool = args.clean
    version = _get_version()

    if os.path.exists(dist) and clean:
        for f in dist.glob("*"):
            os.remove(f)

    if os.path.exists(dist) and os.listdir(dist):
        session.error(
            f"There are files in '{dist}'. Remove them and try again."
            f" Use `rm -rf {dist}` or `git clean -fxdi -- {dist}` to do this."
        )

    def python_build_command():
        return [
            "python",
            "-m", "build",
        ]  # fmt: skip

    session.install("-e", ".[build]")
    session.log(f"# Build package: {version}")
    session.run(*python_build_command(), *remaining)


@nox.session(name="build-docs")
def build_docs(session: nox.Session):
    """Build documentation"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s build",
        dict(
            args=["--serve"],
            action=argparse.BooleanOptionalAction,
            default=True,
            help="build and serve documentation",
        ),
        command="`mkdocs build` or `mkdocs serve`",
    )

    serve: bool = args.serve

    def mkdocs_build_command():
        return [
            "mkdocs",
            "build",
        ]  # fmt: skip

    def mkdocs_serve_command():
        return [
            "mkdocs",
            "serve",
        ]  # fmt: skip

    session.install("-e", ".[docs]")
    if serve:
        session.log("# Serving documentation")
        session.run(*mkdocs_serve_command(), *remaining)
    else:
        session.log("# Building documentation")
        session.run(*mkdocs_build_command(), *remaining)


@nox.session(name="prepare-release")
def prepare_release(session: nox.Session):
    """Prepare release"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s bump",
        dict(
            args=["-d", "--dry"],
            action=argparse.BooleanOptionalAction,
            default=False,
            help="do not modify anything, only show changes (implies `--keep`)",
        ),
        dict(
            args=["-k", "--keep"],
            action=argparse.BooleanOptionalAction,
            default=False,
            help="keep news fragments",
        ),
        command="`bumpver update`",
    )

    dry: bool = args.dry
    keep: bool = args.dry or args.keep

    if all(
        arg not in ("--major", "--minor", "--patch", "-m", "-p") for arg in remaining
    ):
        remaining.append("--minor")

    def bumpver_show_command():
        return [
            "bumpver",
            "show",
            "--environ",
            "--no-fetch",
        ]  # fmt: skip

    def bumpver_test_command(version: str):
        return [
            "bumpver",
            "test",
            version,
            "MAJOR.MINOR[.PATCH][-TAG]",
        ]

    def bumpver_update_command():
        return [
            "bumpver",
            "update",
            "--allow-dirty",  # committing change log updates
            "--no-fetch",
            *_add_args_if(dry, "--dry"),
        ]  # fmt: skip

    def towncrier_build_command(version: str):
        return [
            "towncrier",
            "build",
            "--version", version,
            *_add_args_if(not keep, "--yes"),
            *_add_args_if(keep, "--keep"),
            *_add_args_if(dry, "--draft")
        ]  # fmt: skip

    session.install("-e", ".[build]")

    # get current version
    # load environment into dictionary (split on "=")
    env: str = session.run(*bumpver_show_command(), silent=True)
    env = env.splitlines()[2:]
    env = [var.split("=", maxsplit=1) for var in env]
    env = {k: v for k, v in env}
    version = env["CURRENT_VERSION"]

    # get next version
    # use next version in towncrier since towncrier uses old version
    env_next: str = session.run(*bumpver_test_command(version), *remaining, silent=True)
    env_next = env_next.splitlines()[0]
    version_next = (
        env_next if not env_next.startswith("New Version:") else
        env_next[len("New Version:"):]
    ).strip()  # fmt: skip

    session.log("# Updating change log")
    session.run(*towncrier_build_command(version_next))

    session.log(f"# Bumping version: {version!r} -> {version_next!r}")
    session.run(*bumpver_update_command(), *remaining)


@nox.session(name="release")
def release(session: nox.Session):
    """Upload package"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s release",
        dict(
            args=["-o", "--output"],
            type=Path,
            default=DIST,
            help="output directory for generated reports",
        ),
        dict(
            args=["-r", "--repository"],
            type=str,
            default=REPO,
            help="repository to upload package to",
        ),
        command="`twine upload`",
        description="requires `nox -s build`",
    )

    dist: Path = args.output
    repo: str = args.repository
    package = _get_package().replace("-", "_")
    version = _get_version()

    dist_files = {*dist.glob("*")}
    session.log(f"# Distribution files: {', '.join(f.name for f in dist_files)}")

    # make sure only 2 distribution files
    count = len(dist_files)
    if count != 2:
        session.error(
            f"Expected 2 distribution files for upload, got {count}."
            f" Remove '{dist}' and run `nox -s build`."
        )

    # make sure files are correctly named
    dist_files_expected = {
        dist / f"{package}-{version}-py3-none-any.whl",
        dist / f"{package}-{version}.tar.gz",
    }
    if dist_files != dist_files_expected:
        session.error(
            f"Distribution files do not seem to be for {package}_{version} release."
        )

    def twine_upload_command():
        return [
            "twine",
            "upload",
            "--repository", repo,
            *dist_files,
        ]  # fmt: skip

    session.install("-e", ".[build]")
    session.log(f"# Uploading package: {package} {version}")
    session.run(*twine_upload_command(), *remaining)


@nox.session(name="release-docs")
def release_docs(session: nox.Session):
    """Upload documentation"""
    args, remaining = _parse_args(
        session,
        session.posargs,
        "nox -s release",
        dict(
            args=["-n", "--name"],
            default="dev",
        ),
        dict(
            args=["-p", "--push"],
            action=argparse.BooleanOptionalAction,
            default=True,
            help="upload changes",
        ),
        command="`mike deploy`",
        description="does not requires `nox -s build-docs`",
    )

    name: str = args.name
    push: bool = args.push
    package = _get_package()
    version = _get_version()

    def mike_deploy_command():
        return [
            "mike",
            "deploy",
            *_add_args_if(push, "--push"),
            name,
        ]  # fmt: skip

    session.install("-e", ".[docs]")
    session.log(f"# Uploading documentation: {package} {version}")
    session.run(*mike_deploy_command(), *remaining)
