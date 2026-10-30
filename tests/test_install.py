from pathlib import Path
import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch

PACKAGE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('moonskill_install',PACKAGE/'install.py')
installer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='moonskill-install-test-')
        self.base=Path(self.tmp.name)
        self.project=self.base/'task';self.project.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self,*args):
        output,error=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(error):
            code=installer.main(['--project',str(self.project),*args])
        return code,output.getvalue(),error.getvalue()

    def installed(self):
        root=self.project/'.agents/skills'
        return sorted(p.name for p in root.iterdir()) if root.exists() else []

    def test_dry_run_does_not_create_project_configuration(self):
        before=sorted(self.project.rglob('*'))
        code,out,_=self.run_cli()
        self.assertEqual(code,0)
        self.assertEqual(json.loads(out)['mode'],'dry_run')
        self.assertEqual(sorted(self.project.rglob('*')),before)

    def test_core_installs_three_complete_skill_folders_only(self):
        code,out,error=self.run_cli('--apply')
        self.assertEqual(code,0,error)
        self.assertEqual(set(self.installed()),set(installer.PROFILES['core']))
        manifest=installer.load_manifest()
        for skill in installer.choose(manifest,installer.PROFILES['core']):
            self.assertEqual(installer.inventory(self.project/'.agents/skills'/skill['name']),skill['files'])
        self.assertFalse(json.loads(out)['codex_discovery_verified'])

    def test_all_profile_installs_six_independent_skills(self):
        code,_,error=self.run_cli('--profile','all','--apply')
        self.assertEqual(code,0,error)
        self.assertEqual(set(self.installed()),set(installer.PROFILES['all']))
        for name in self.installed():
            self.assertTrue((self.project/'.agents/skills'/name/'SKILL.md').is_file())

    def test_grill_entrypoint_always_includes_its_dependency(self):
        code,_,error=self.run_cli('--skills','grill-me','--apply')
        self.assertEqual(code,0,error)
        self.assertEqual(self.installed(),['grill-me','grilling'])

    def test_reinstall_identical_files_is_idempotent(self):
        self.assertEqual(self.run_cli('--apply')[0],0)
        before=installer.inventory(self.project/'.agents/skills')
        code,out,error=self.run_cli('--apply')
        self.assertEqual(code,0,error)
        self.assertEqual(before,installer.inventory(self.project/'.agents/skills'))
        self.assertTrue(all(s['action']=='already_identical' for s in json.loads(out)['skills']))

    def test_conflict_is_preserved_and_preflight_prevents_partial_install(self):
        target=self.project/'.agents/skills/grill-me';target.mkdir(parents=True)
        (target/'SKILL.md').write_text('User skill, preserve this',encoding='utf-8')
        before=installer.inventory(self.project)
        code,_,error=self.run_cli('--profile','all','--apply')
        self.assertEqual(code,1)
        self.assertIn('no overwrite',error)
        self.assertEqual(before,installer.inventory(self.project))

    def test_tampered_source_fails_before_first_project_write(self):
        package=self.base/'tampered';shutil.copytree(PACKAGE/'skills',package/'skills')
        shutil.copy2(PACKAGE/'manifest.json',package/'manifest.json')
        with (package/'skills/grilling/SKILL.md').open('a',encoding='utf-8') as f:f.write('\nmodified')
        with patch.object(installer,'ROOT',package):
            code,_,error=self.run_cli('--apply')
        self.assertEqual(code,1)
        self.assertIn('hashes do not match',error)
        self.assertFalse((self.project/'.agents').exists())

    def test_unknown_skill_fails_without_writes(self):
        code,_,error=self.run_cli('--skills','not-a-packaged-skill','--apply')
        self.assertEqual(code,1)
        self.assertIn('Unknown Skill',error)
        self.assertFalse((self.project/'.agents').exists())

    def test_nonexistent_project_is_not_silently_created(self):
        missing=self.base/'missing'
        with contextlib.redirect_stderr(io.StringIO()):
            code=installer.main(['--project',str(missing),'--apply'])
        self.assertEqual(code,1)
        self.assertFalse(missing.exists())

    def test_symlink_outside_project_is_not_followed(self):
        external=self.base/'external';external.mkdir()
        try:(self.project/'.agents').symlink_to(external,target_is_directory=True)
        except OSError:self.skipTest('OS does not allow directory symlinks in this session')
        code,_,_=self.run_cli('--apply')
        self.assertEqual(code,1)
        self.assertEqual(list(external.iterdir()),[])

    def test_list_does_not_install_or_require_a_project(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):code=installer.main(['--list'])
        self.assertEqual(code,0)
        self.assertEqual(len(json.loads(output.getvalue())['skills']),6)
        self.assertFalse((self.project/'.agents').exists())

if __name__=='__main__':unittest.main(verbosity=2)
