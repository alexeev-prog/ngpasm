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

# Test data for parametrization
EXTENSION_TEST_CASES = [
    ('json', ConfigType.JSON),
    ('.json', ConfigType.JSON),
    ('JSON', ConfigType.JSON),
    ('.JsOn', ConfigType.JSON),
    ('yaml', ConfigType.YAML),
    ('.yaml', ConfigType.YAML),
    ('yml', ConfigType.YAML),
    ('.yml', ConfigType.YAML),
    ('YML', ConfigType.YAML),
    ('toml', ConfigType.TOML),
    ('.toml', ConfigType.TOML),
    ('', ConfigType.JSON),
    ('unknown', ConfigType.JSON),
    ('.conf', ConfigType.JSON),
]

FILENAME_TEST_CASES = [
    ('config.json', ConfigType.JSON),
    ('.config.json', ConfigType.JSON),
    ('/path/to/config.json', ConfigType.JSON),
    ('config.yaml', ConfigType.YAML),
    ('config.yml', ConfigType.YAML),
    ('config.toml', ConfigType.TOML),
    ('no_extension', ConfigType.JSON),
    ('.hidden', ConfigType.JSON),
    ('config.YML', ConfigType.YAML),
]

CONFIG_READER_VALID_CASES = [
    (ConfigType.JSON, {'name': 'test', 'value': 42}, '{"name":"test","value":42}'),
    (
        ConfigType.YAML,
        {'server': {'host': 'localhost', 'port': 8080}},
        'server:\n  host: localhost\n  port: 8080',
    ),
    (
        ConfigType.TOML,
        {'title': 'Example', 'owner': {'name': 'Alice'}},
        'title = "Example"\n\n[owner]\nname = "Alice"',
    ),
]

CONFIG_READER_INVALID_CASES = [
    (ConfigType.JSON, 'invalid json', '.json', json.JSONDecodeError),
    (ConfigType.YAML, 'invalid: [', '.yaml', yaml.YAMLError),
    (ConfigType.TOML, 'invalid toml =', '.toml', toml.TomlDecodeError),
]

NON_DICT_CONTENT_CASES = [
    (ConfigType.JSON, '["item1", "item2"]', '.json'),
    (ConfigType.YAML, '- item1\n- item2', '.yaml'),
]


@pytest.mark.parametrize('extension, expected', EXTENSION_TEST_CASES)  # noqa: PT006
def test_detect_config_type_by_extension(extension, expected):
    """Test detection by file extension."""
    assert detect_config_type_by_extension(extension) == expected  # noqa: S101


@pytest.mark.parametrize('filename, expected', FILENAME_TEST_CASES)  # noqa: PT006
def test_detect_config_type_by_filename(filename, expected):
    """Test detection by filename."""
    assert detect_config_type_by_filename(filename) == expected  # noqa: S101


@pytest.fixture
def tmp_config_file(tmp_path):
    """Create temporary config file for testing."""

    def _create_file(content, extension):
        file = tmp_path / f'test_config{extension}'
        file.write_text(content)
        return file

    return _create_file


@pytest.mark.parametrize(
    ('config_type', 'config_data', 'content'), CONFIG_READER_VALID_CASES
)
def test_config_reader_valid_content(
    tmp_config_file, config_type, config_data, content
):
    """Test ConfigReader with valid file content."""
    # Create temp file
    config_file = tmp_config_file(
        content,
        {
            ConfigType.JSON: '.json',
            ConfigType.YAML: '.yaml',
            ConfigType.TOML: '.toml',
        }[config_type],
    )

    # Test with explicit type
    reader = ConfigReader(str(config_file), config_type)
    assert reader.config == config_data  # noqa: S101

    # Test with type autodetection
    reader_auto = ConfigReader(str(config_file))
    assert reader_auto.config == config_data  # noqa: S101


def test_config_reader_nonexistent_file():
    """Test with non-existent config file."""
    reader = ConfigReader('non_existent.json')
    assert reader.config == {}  # noqa: S101


@pytest.mark.parametrize(
    ('config_type', 'content', 'extension', 'exception'),
    CONFIG_READER_INVALID_CASES,
)
def test_config_reader_invalid_content(
    tmp_config_file, config_type, content, extension, exception
):
    """Test with invalid file content."""
    config_file = tmp_config_file(content, extension)
    with pytest.raises(exception):
        ConfigReader(str(config_file), configtype=config_type)


@pytest.mark.parametrize(
    ('config_type', 'content', 'extension'), NON_DICT_CONTENT_CASES
)
def test_config_reader_non_dict_content(
    tmp_config_file, config_type, content, extension
):
    """Test with valid non-dict content."""
    config_file = tmp_config_file(content, extension)
    reader = ConfigReader(str(config_file), configtype=config_type)
    assert reader.config == {}  # noqa: S101


def test_config_reader_empty_file(tmp_config_file):
    """Test with empty file content."""
    # JSON should raise error on empty file
    json_file = tmp_config_file('', '.json')
    with pytest.raises(json.JSONDecodeError):
        ConfigReader(str(json_file))

    # YAML should return None -> converted to {}
    yaml_file = tmp_config_file('', '.yaml')
    reader = ConfigReader(str(yaml_file))
    assert reader.config == {}  # noqa: S101

    # TOML should return {}
    toml_file = tmp_config_file('', '.toml')
    reader = ConfigReader(str(toml_file))
    assert reader.config == {}  # noqa: S101


def test_config_reader_no_extension_json(tmp_config_file):
    """Test file without extension containing JSON."""
    content = '{"test": "value"}'
    config_file = tmp_config_file(content, '')
    reader = ConfigReader(str(config_file))
    assert reader.config == {'test': 'value'}  # noqa: S101


def test_config_reader_no_extension_invalid(tmp_config_file):
    """Test file without extension with invalid content."""
    config_file = tmp_config_file('invalid content', '')
    with pytest.raises(json.JSONDecodeError):
        ConfigReader(str(config_file))
