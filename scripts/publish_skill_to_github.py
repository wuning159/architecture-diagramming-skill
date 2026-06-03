#!/usr/bin/env python3
"""Package a Codex skill as a GitHub repository and publish it.

This script intentionally uses only the Python standard library plus git. It
reads GitHub credentials from GITHUB_TOKEN and never writes the token to disk.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


GITHUB_API = "https://api.github.com"


def run(cmd: list[str], cwd: Path | None = None, dry_run: bool = False) -> str:
    printable = " ".join(cmd)
    if dry_run:
        print(f"[dry-run] {printable}")
        return ""
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {printable}\n{result.stdout}")
    return result.stdout.strip()


def github_request(method: str, path: str, token: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = Request(
        f"{GITHUB_API}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "codex-skill-publisher",
        },
    )
    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {method} {path} failed: {exc.code}\n{detail}") from exc


def frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 4 or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"')
    raise ValueError("SKILL.md frontmatter must include name")


def copy_tree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def write_default_readmes(repo_dir: Path, skill_name: str, description: str) -> None:
    readme = repo_dir / "README.md"
    zh = repo_dir / "README.zh-CN.md"
    en = repo_dir / "README.en.md"
    if not readme.exists():
        readme.write_text(
            f"# {skill_name}\n\n{description}\n\n"
            f"- [中文说明](README.zh-CN.md)\n"
            f"- [English README](README.en.md)\n",
            encoding="utf-8",
        )
    if not zh.exists():
        zh.write_text(
            f"# {skill_name}\n\n{description}\n\n"
            "## 安装\n\n"
            f"复制 `skills/{skill_name}` 到 Codex 全局 skills 目录。\n",
            encoding="utf-8",
        )
    if not en.exists():
        en.write_text(
            f"# {skill_name}\n\n{description}\n\n"
            "## Installation\n\n"
            f"Copy `skills/{skill_name}` into your global Codex skills directory.\n",
            encoding="utf-8",
        )


def write_license(repo_dir: Path) -> None:
    license_file = repo_dir / "LICENSE"
    if license_file.exists():
        return
    license_file.write_text(
        "MIT License\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE.\n",
        encoding="utf-8",
    )


def create_or_get_repo(token: str, repo_name: str, description: str, private: bool) -> dict:
    user = github_request("GET", "/user", token)
    owner = user["login"]
    body = {
        "name": repo_name,
        "description": description,
        "private": private,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
    }
    try:
        return github_request("POST", "/user/repos", token, body)
    except RuntimeError as exc:
        if "422" not in str(exc):
            raise
        return github_request("GET", f"/repos/{owner}/{repo_name}", token)


def github_put_contents(
    token: str,
    owner: str,
    repo_name: str,
    branch: str,
    repo_dir: Path,
) -> int:
    uploaded = 0
    for file_path in sorted(repo_dir.rglob("*")):
        if not file_path.is_file() or ".git" in file_path.parts:
            continue
        rel = file_path.relative_to(repo_dir).as_posix()
        content = file_path.read_bytes()
        encoded = __import__("base64").b64encode(content).decode("ascii")
        sha = None
        try:
            existing = github_request("GET", f"/repos/{owner}/{repo_name}/contents/{rel}?ref={branch}", token)
            sha = existing.get("sha")
        except RuntimeError as exc:
            if "404" not in str(exc) and "409" not in str(exc):
                raise
        body = {
            "message": f"Add {rel}",
            "content": encoded,
            "branch": branch,
        }
        if sha:
            body["sha"] = sha
            body["message"] = f"Update {rel}"
        github_request("PUT", f"/repos/{owner}/{repo_name}/contents/{rel}", token, body)
        uploaded += 1
    return uploaded


def build_repo(args: argparse.Namespace, work_dir: Path) -> Path:
    skill_path = args.skill_path.resolve()
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"Missing SKILL.md: {skill_md}")
    skill_name = frontmatter_name(skill_md)

    repo_dir = work_dir / args.repo_name
    repo_dir.mkdir(parents=True, exist_ok=True)

    skill_target = repo_dir / "skills" / skill_name
    copy_tree_contents(skill_path, skill_target)

    if args.project_template:
        copy_tree_contents(args.project_template.resolve(), repo_dir)
    write_default_readmes(repo_dir, skill_name, args.description)
    write_license(repo_dir)
    (repo_dir / ".gitignore").write_text(".DS_Store\nThumbs.db\n*.tmp\n*.log\n", encoding="utf-8")
    return repo_dir


def publish(args: argparse.Namespace) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token and not args.dry_run:
        raise RuntimeError("GITHUB_TOKEN is required unless --dry-run is used")

    root = Path(args.output_dir).resolve() if args.output_dir else Path(tempfile.mkdtemp())
    repo_dir = build_repo(args, root)
    print(f"Prepared repository at: {repo_dir}")

    run(["git", "init"], cwd=repo_dir, dry_run=args.dry_run)
    run(["git", "add", "."], cwd=repo_dir, dry_run=args.dry_run)
    run(["git", "commit", "-m", args.commit_message], cwd=repo_dir, dry_run=args.dry_run)

    if args.dry_run:
        print("[dry-run] Skipping GitHub repository creation and push")
        return

    repo = create_or_get_repo(token or "", args.repo_name, args.description, args.private)
    html_url = repo["html_url"]
    owner = repo["owner"]["login"]
    default_branch = repo.get("default_branch") or "main"

    uploaded = github_put_contents(token or "", owner, args.repo_name, default_branch, repo_dir)
    print(f"Published with GitHub Contents API: {html_url} ({uploaded} files)")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a Codex skill to GitHub.")
    parser.add_argument("--skill-path", required=True, type=Path, help="Path to the skill folder containing SKILL.md")
    parser.add_argument("--repo-name", required=True, help="GitHub repository name")
    parser.add_argument("--description", default="Codex skill repository", help="GitHub repository description")
    parser.add_argument("--output-dir", type=Path, help="Directory for the generated local repository")
    parser.add_argument("--project-template", type=Path, help="Optional directory with README/docs to copy into repo root")
    parser.add_argument("--commit-message", default="Initial skill release", help="Initial commit message")
    parser.add_argument("--private", action="store_true", help="Create a private repository instead of public")
    parser.add_argument("--dry-run", action="store_true", help="Prepare files and print git commands without GitHub calls")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        publish(parse_args(argv))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
