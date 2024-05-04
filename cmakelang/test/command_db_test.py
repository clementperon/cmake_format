
import unittest
import subprocess

from cmakelang.parse.funs import get_parse_db

IGNORE_LIST = [
    "endforeach",
    "endfunction",
    "endmacro",
    # FIXME: Support this new functions / macro
    "add_link_options",
    "block",
    "cmake_file_api",
    "cmake_language",
    "cmake_path",
    "endblock",
    "target_link_directories",
    "target_link_options",
    "target_precompile_headers"
]


class TestCommandDatabase(unittest.TestCase):
  """
  Execute cmake and ensure that all cmake commands are in the database
  """

  def test_all_commands_in_db(self):
    missing_commands = []
    proc = subprocess.Popen(
        ["cmake", "--help-command-list"],
        stdout=subprocess.PIPE)

    parse_db = get_parse_db()

    ignore = IGNORE_LIST
    with proc.stdout as infile:
      for line in infile:
        command = line.strip().decode("utf-8")
        if command not in parse_db and command not in ignore:
          missing_commands.append(command)
    proc.wait()

    message = "Missing commands:\n  " + "\n  ".join(sorted(missing_commands))
    self.assertFalse(bool(missing_commands), msg=message)


if __name__ == "__main__":
  unittest.main()
