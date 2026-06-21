import glob
import py_compile


def test_backend_source_compiles() -> None:
    files = glob.glob("src/backend/**/*.py", recursive=True)
    for file_path in files:
        py_compile.compile(file_path, doraise=True)
