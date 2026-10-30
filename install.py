#!/usr/bin/env python3
"""Install reviewed Skill folders into one project's .agents/skills. Stdlib only."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
PROFILES = {
    'core': ['grill-me', 'grilling', 'verification-before-completion'],
    'ui': ['grill-me', 'grilling', 'verification-before-completion', 'frontend-design'],
    'all': ['grill-me', 'grilling', 'verification-before-completion',
            'frontend-design', 'diagnosing-bugs', 'api-tester', 'api-and-interface-design'],
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(folder: Path) -> dict[str, str]:
    result = {}
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlinked Skill resources are not installed: ' + str(path))
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = sha256(path)
    return result

def inside(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(parent.resolve())
    return resolved

def load_manifest() -> dict:
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    names = [item['name'] for item in manifest['skills']]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate Skill names in manifest')
    for name in names:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ValueError('Invalid Skill name: ' + name)
    return manifest

def choose(manifest: dict, requested: list[str]) -> list[dict]:
    by_name = {item['name']: item for item in manifest['skills']}
    ordered, visiting = [], set()
    def visit(name: str):
        if name not in by_name:
            raise ValueError('Unknown Skill: ' + name)
        if name in visiting:
            raise ValueError('Cyclic Skill dependency: ' + name)
        if name in ordered:
            return
        visiting.add(name)
        for dep in by_name[name].get('dependencies', []):
            visit(dep)
        visiting.remove(name)
        ordered.append(name)
    for name in requested:
        visit(name)
    return [by_name[name] for name in ordered]

def plan(project: Path, selected: list[dict]) -> list[dict]:
    project = project.resolve()
    if not project.is_dir():
        raise ValueError('Project must be an existing directory: ' + str(project))
    for parent in [project / '.agents', project / '.agents/skills']:
        if parent.is_symlink():
            raise ValueError('Do not replace or follow a managed Skill directory: ' + str(parent))
    destination = inside(project / '.agents/skills', project)
    planned = []
    for item in selected:
        name = item['name']
        raw_source = ROOT / 'skills' / name
        if raw_source.is_symlink():
            raise ValueError('Symlinked Skill source is not installed: ' + name)
        source = inside(raw_source, ROOT / 'skills')
        expected = item['files']
        for rel in expected:
            parts = PurePosixPath(rel)
            if parts.is_absolute() or '..' in parts.parts or '\\' in rel or ':' in rel:
                raise ValueError('Unsafe resource path: ' + rel)
        if inventory(source) != expected:
            raise ValueError('Source resource hashes do not match manifest: ' + name)
        if 'SKILL.md' not in expected:
            raise ValueError('Missing SKILL.md: ' + name)
        raw_target = destination / name
        if raw_target.is_symlink():
            raise ValueError('Do not follow an existing Skill symlink: ' + name)
        target = inside(raw_target, project)
        if target.exists():
            if not target.is_dir() or inventory(target) != expected:
                raise FileExistsError('Different existing Skill preserved, no overwrite: ' + str(target))
            action = 'already_identical'
        else:
            action = 'install'
        planned.append({'name': name, 'source': str(source), 'target': str(target),
                        'action': action, 'files': expected})
    return planned

def apply_plan(project: Path, planned: list[dict]) -> None:
    # All source hashes and destination conflicts were checked before the first write.
    for item in planned:
        target = Path(item['target'])
        if item['action'] == 'already_identical':
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.moonskill-stage-', dir=str(project)) as stage:
            staged = Path(stage) / item['name']
            shutil.copytree(item['source'], staged)
            if inventory(staged) != item['files']:
                raise ValueError('Staged file verification failed: ' + item['name'])
            if target.exists():
                raise FileExistsError('Destination appeared during install; preserved: ' + str(target))
            staged.rename(target)
        if inventory(target) != item['files']:
            raise ValueError('Installed file verification failed: ' + item['name'])

def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List packaged Skills; no installation')
    parser.add_argument('--project', help='Existing task project; never a global Skill directory')
    parser.add_argument('--profile', choices=PROFILES, default=None)
    parser.add_argument('--skills', nargs='+', help='Explicit names; dependencies are included')
    parser.add_argument('--apply', action='store_true', help='Copy after preflight; otherwise dry run')
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest()
        if args.list:
            print(json.dumps({'version': manifest['version'], 'skills': [
                {'name': s['name'], 'role': s['role'], 'dependencies': s.get('dependencies', [])}
                for s in manifest['skills']]}, ensure_ascii=False, indent=2))
            return 0
        if not args.project:
            parser.error('--project is required for a dry run or install')
        profile = args.profile or manifest['default_profile']
        selected = choose(manifest, args.skills or PROFILES[profile])
        project = Path(args.project).expanduser().resolve()
        planned = plan(project, selected)
        if args.apply:
            apply_plan(project, planned)
        print(json.dumps({'mode': 'installed_and_hash_verified' if args.apply else 'dry_run',
            'project': str(project), 'skills': [
                {k: v for k, v in item.items() if k not in ('files', 'source')} for item in planned],
            'codex_discovery_verified': False,
            'next': 'Check /skills or $ in a fresh provided Codex session; file copy is not invocation.'},
            ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc), 'complete': False}, ensure_ascii=False), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
