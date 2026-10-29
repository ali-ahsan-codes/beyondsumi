"""Tests for the model-free Studio launcher defaults."""
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('studio_launcher', ROOT / 'install.py')
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


class StudioLauncherTests(unittest.TestCase):
    def test_no_arguments_parse_as_model_free_studio(self):
        args = launcher.build_parser().parse_args([])
        self.assertIsNone(args.skills_root)
        self.assertEqual(args.port, 8765)
        self.assertFalse(args.no_browser)

    def test_main_without_arguments_launches_studio(self):
        with patch.object(launcher, 'launch_studio') as launch:
            launcher.main([])
        launch.assert_called_once_with(ROOT, 8765, open_browser=True)

    def test_studio_server_uses_loopback_and_closes_after_interrupt(self):
        events = []

        class Server:
            server_port = 8765

            def __init__(self, address, handler):
                events.append(('bind', address))

            def serve_forever(self):
                events.append(('serve',))
                raise KeyboardInterrupt

            def server_close(self):
                events.append(('close',))

        with patch.object(launcher.http.server, 'ThreadingHTTPServer', Server), \
             patch.object(launcher.webbrowser, 'open', return_value=True) as open_browser, \
             patch('sys.stdout', new_callable=io.StringIO) as output:
            launcher.launch_studio(ROOT, open_browser=True)

        self.assertIn(('bind', ('127.0.0.1', 8765)), events)
        self.assertIn(('serve',), events)
        self.assertIn(('close',), events)
        open_browser.assert_called_once_with('http://127.0.0.1:8765/', new=2)
        self.assertIn('does not use an AI model', output.getvalue())
        self.assertIn('server stopped', output.getvalue())

    def test_default_port_falls_back_to_an_available_local_port(self):
        events = []

        class Server:
            def __init__(self, address, handler):
                events.append(address)
                if len(events) == 1:
                    raise OSError('port in use')
                self.server_port = 49821

            def serve_forever(self):
                raise KeyboardInterrupt

            def server_close(self):
                events.append('closed')

        with patch.object(launcher.http.server, 'ThreadingHTTPServer', Server), \
             patch.object(launcher.webbrowser, 'open') as open_browser, \
             patch('sys.stdout', new_callable=io.StringIO) as output:
            launcher.launch_studio(ROOT, open_browser=True)

        self.assertEqual(events[:2], [('127.0.0.1', 8765), ('127.0.0.1', 0)])
        open_browser.assert_called_once_with('http://127.0.0.1:49821/', new=2)
        self.assertIn('using an available local port', output.getvalue())

    def test_explicit_port_error_does_not_silently_change_port(self):
        with patch.object(launcher.http.server, 'ThreadingHTTPServer', side_effect=OSError('busy')):
            with self.assertRaisesRegex(ValueError, 'port 9000'):
                launcher.launch_studio(ROOT, port=9000, open_browser=False)

    def test_windows_launchers_run_only_the_local_studio(self):
        start = (ROOT / 'start.bat').read_text().lower()
        install = (ROOT / 'install.bat').read_text().lower()
        self.assertIn('cd /d "%~dp0"', start)
        self.assertIn('py -3 install.py', start)
        self.assertIn('python install.py', start)
        self.assertIn('sys.version_info >= (3, 8)', start)
        self.assertNotIn('pip install', start)
        self.assertNotIn('--skills-root', start)
        self.assertIn('call "%~dp0start.bat"', install)
        self.assertIn('no ai model', install)
        self.assertNotIn('pip install', install)


if __name__ == '__main__':
    unittest.main()
