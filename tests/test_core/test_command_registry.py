import unittest
from packages.core.command_registry import CommandRegistry

class TestCommandRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = CommandRegistry()

    def test_register_and_execute_success(self):
        def sample_callback(*args):
            return f"Received: {','.join(args)}"
        
        self.registry.register("test_cmd", sample_callback, "Help text here")
        
        # Test exact match execution
        res = self.registry.execute("test_cmd arg1 arg2")
        self.assertEqual(res, "Received: arg1,arg2")
        
        # Test case-insensitivity
        res_upper = self.registry.execute("TEST_CMD arg3")
        self.assertEqual(res_upper, "Received: arg3")

    def test_execute_empty_line(self):
        res = self.registry.execute("   ")
        self.assertEqual(res, "")

    def test_execute_unregistered_command(self):
        res = self.registry.execute("unknown_cmd")
        self.assertIn("unrecognized. Type 'help'", res)

    def test_execute_with_exception(self):
        def buggy_callback(*args):
            raise ValueError("Buggy callback failure")
            
        self.registry.register("buggy", buggy_callback, "Buggy command")
        res = self.registry.execute("buggy")
        self.assertIn("Execution Error: Buggy callback failure", res)

    def test_get_help_list(self):
        def cb():
            return "ok"
        self.registry.register("cmd1", cb, "help 1")
        self.registry.register("cmd2", cb, "help 2")
        
        help_map = self.registry.get_help_list()
        self.assertEqual(help_map.get("cmd1"), "help 1")
        self.assertEqual(help_map.get("cmd2"), "help 2")

if __name__ == "__main__":
    unittest.main()
