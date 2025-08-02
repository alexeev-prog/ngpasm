import orjson as json
import pytest
import toml
import yaml

from ngpasm.loader import (
    ConfigReader,
    ConfigType,
    detect_config_type_by_extension,
    detect_config_type_by_filename,
)

EXTENSION_TEST_CASES = [
    ("json", ConfigType.JSON),
    (".json", ConfigType.JSON),
    ("JSON", ConfigType.JSON),
    (".JsOn", ConfigType.JSON),
    ("yaml", ConfigType.YAML),
    (".yaml", ConfigType.YAML),
    ("yml", ConfigType.YAML),
    (".yml", ConfigType.YAML),
    ("YML", ConfigType.YAML),
    ("toml", ConfigType.TOML),
    (".toml", ConfigType.TOML),
    ("", ConfigType.JSON),
    ("unknown", ConfigType.JSON),
    (".conf", ConfigType.JSON),
]

FILENAME_TEST_CASES = [
    ("config.json", ConfigType.JSON),
    (".config.json", ConfigType.JSON),
    ("/path/to/config.json", ConfigType.JSON),
    ("config.yaml", ConfigType.YAML),
    ("config.yml", ConfigType.YAML),
    ("config.toml", ConfigType.TOML),
    ("no_extension", ConfigType.JSON),
    (".hidden", ConfigType.JSON),
    ("config.YML", ConfigType.YAML),
]

CONFIG_READER_VALID_CASES = [
    (ConfigType.JSON, {"name": "test", "value": 42}, '{"name":"test","value":42}'),
    (
        ConfigType.YAML,
        {"server": {"host": "localhost", "port": 8080}},
        "server:\n  host: localhost\n  port: 8080",
    ),
    (
        ConfigType.TOML,
        {"title": "Example", "owner": {"name": "Alice"}},
        'title = "Example"\n\n[owner]\nname = "Alice"',
    ),
]

CONFIG_READER_INVALID_CASES = [
    (ConfigType.JSON, "invalid json", ".json", json.JSONDecodeError),
    (ConfigType.YAML, "invalid: [", ".yaml", yaml.YAMLError),
    (ConfigType.TOML, "invalid toml =", ".toml", toml.TomlDecodeError),
]

NON_DICT_ERROR_CASES = [
    (ConfigType.JSON, '["item1", "item2"]', ".json"),
    (ConfigType.YAML, "- item1\n- item2", ".yaml"),
]

SCALAR_ERROR_CASES = [
    (ConfigType.JSON, "42", ".json"),
    (ConfigType.JSON, '"string"', ".json"),
    (ConfigType.JSON, "null", ".json"),
    (ConfigType.YAML, "42", ".yaml"),
    (ConfigType.YAML, "string", ".yaml"),
    (ConfigType.YAML, "null", ".yaml"),
]


@pytest.mark.parametrize("extension, expected", EXTENSION_TEST_CASES)
def test_detect_config_type_by_extension(extension, expected):
    assert detect_config_type_by_extension(extension) == expected


@pytest.mark.parametrize("filename, expected", FILENAME_TEST_CASES)
def test_detect_config_type_by_filename(filename, expected):
    assert detect_config_type_by_filename(filename) == expected


@pytest.fixture
def tmp_config_file(tmp_path):
    def _create_file(content, extension):
        file = tmp_path / f"test_config{extension}"
        file.write_text(content)
        return file

    return _create_file


@pytest.mark.parametrize(
    ("config_type", "config_data", "content"), CONFIG_READER_VALID_CASES
)
def test_config_reader_valid_content(
    tmp_config_file, config_type, config_data, content
):
    config_file = tmp_config_file(
        content,
        {
            ConfigType.JSON: ".json",
            ConfigType.YAML: ".yaml",
            ConfigType.TOML: ".toml",
        }[config_type],
    )
    reader = ConfigReader(str(config_file), config_type)
    assert reader.config == config_data
    reader_auto = ConfigReader(str(config_file))
    assert reader_auto.config == config_data


def test_config_reader_nonexistent_file():
    reader = ConfigReader("non_existent.json")
    assert reader.config == {}


@pytest.mark.parametrize(
    ("config_type", "content", "extension", "exception"), CONFIG_READER_INVALID_CASES
)
def test_config_reader_invalid_content(
    tmp_config_file, config_type, content, extension, exception
):
    config_file = tmp_config_file(content, extension)
    with pytest.raises(exception):
        ConfigReader(str(config_file), configtype=config_type)


@pytest.mark.parametrize(("config_type", "content", "extension"), NON_DICT_ERROR_CASES)
def test_config_reader_non_dict_error(tmp_config_file, config_type, content, extension):
    config_file = tmp_config_file(content, extension)
    with pytest.raises(TypeError):
        ConfigReader(str(config_file), configtype=config_type)


@pytest.mark.parametrize(("config_type", "content", "extension"), SCALAR_ERROR_CASES)
def test_config_reader_scalar_error(tmp_config_file, config_type, content, extension):
    config_file = tmp_config_file(content, extension)
    with pytest.raises(TypeError):
        ConfigReader(str(config_file), configtype=config_type)


def test_config_reader_empty_file(tmp_config_file):
    json_file = tmp_config_file("", ".json")
    with pytest.raises(json.JSONDecodeError):
        ConfigReader(str(json_file))
    yaml_file = tmp_config_file("", ".yaml")
    with pytest.raises(TypeError):
        reader = ConfigReader(str(yaml_file))
        assert reader.config == {}
    toml_file = tmp_config_file("", ".toml")
    reader = ConfigReader(str(toml_file))
    assert reader.config == {}


def test_config_reader_no_extension_json(tmp_config_file):
    content = '{"test": "value"}'
    config_file = tmp_config_file(content, "")
    reader = ConfigReader(str(config_file))
    assert reader.config == {"test": "value"}


def test_config_reader_no_extension_invalid(tmp_config_file):
    config_file = tmp_config_file("invalid content", "")
    with pytest.raises(json.JSONDecodeError):
        ConfigReader(str(config_file))


def test_config_reader_scalar_json_content(tmp_config_file):
    json_file = tmp_config_file("42", ".json")
    with pytest.raises(TypeError):
        ConfigReader(str(json_file))
