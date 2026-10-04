import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('adapter', Path(__file__).resolve().parents[1] / 'review_runner.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class AdapterTests(unittest.TestCase):
    def test_review_limits(self):
        command = adapter.command('codex', 'review', Path('/tmp/result'))
        self.assertIn('--ignore-user-config', command)
        for flag in ('features.plugins=false', 'features.apps=false', 'features.hooks=false', 'approval_policy="never"'):
            self.assertIn(flag, command)
        self.assertIn('read-only', command)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', command)

    def test_claude_review_limits(self):
        command = adapter.command('claude', 'inspect', Path('/tmp/result'))
        for flag in ('--safe-mode', '--strict-mcp-config', 'dontAsk', 'Read,Glob,Grep'):
            self.assertIn(flag, command)

    def test_nested_snapshot_excludes_parent_and_results(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-q')
            (root / 'README.md').write_text('parent old')
            git('add', 'README.md')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
            (root / 'README.md').write_text('parent new')
            example = root / 'examples' / 'tiny'
            example.mkdir(parents=True)
            (example / 'README.md').write_text('example')
            output = example / 'output'
            output.mkdir()
            (output / 'prior.json').write_text('{}')
            snapshot = adapter.upstream.snapshot(example, 'HEAD')
            self.assertEqual([f['path'] for f in snapshot['files']], ['README.md'])
            self.assertEqual(snapshot['files'][0]['sha256'], adapter.upstream.digest(b'example'))
            diff = adapter.upstream.git(example, 'diff', '--no-ext-diff', 'HEAD', '--')
            self.assertEqual(diff, b'')


if __name__ == '__main__':
    unittest.main()
