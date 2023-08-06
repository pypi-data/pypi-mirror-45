import os
from filecmp import dircmp
from tempfile import TemporaryDirectory
from operatorcourier.nest import nest_bundles


def test_nest_default():
    with TemporaryDirectory() as registry_dir:
        expected_result = "tests/test_files/bundles/nest/bundle1result"
        folder_to_nest = "tests/test_files/bundles/nest/bundle1"

        yaml_files = []
        for filename in os.listdir(folder_to_nest):
            with open(folder_to_nest + "/" + filename) as f:
                yaml_files.append(f.read())

        with TemporaryDirectory() as temp_dir:
            nest_bundles(yaml_files, registry_dir, temp_dir)

        dcmp = dircmp(registry_dir, expected_result)
        assert(len(dcmp.diff_files) == 0)


def test_nest_no_crds():
    with TemporaryDirectory() as registry_dir:
        expected_result = "tests/test_files/bundles/nest/bundle2result"
        folder_to_nest = "tests/test_files/bundles/nest/bundle2"

        yaml_files = []
        for filename in os.listdir(folder_to_nest):
            with open(folder_to_nest + "/" + filename) as f:
                yaml_files.append(f.read())

        with TemporaryDirectory() as temp_dir:
            nest_bundles(yaml_files, registry_dir, temp_dir)

        dcmp = dircmp(registry_dir, expected_result)
        assert(len(dcmp.diff_files) == 0)
