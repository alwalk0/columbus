from columbus.framework.validators import validate_config, validate_config_key, validate_models, validate_database, validate_api_config, validate_api
import pytest



@pytest.fixture()
def config_extra_keys():
    config = {'models': 'tests/integration/models.py', 'database': 'mock_url', 'hello':'world', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config    


@pytest.fixture()
def config_missing_keys():
    config = {'database': 'mock_url', 'hello':'world', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config    

@pytest.fixture()
def valid_config():
    config = {'models': 'tests/integration/models.py', 'database': 'mock_url', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config  


@pytest.fixture()
def missing_models_value_config():
    config = {'models': None, 'database': 'mock_url', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config       


@pytest.fixture()
def missing_models_file_config():
    config = {'models': 'foo.py', 'database': 'mock_url', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config       
                            
                     
@pytest.fixture()
def missing_database_value_config():
    config = {'models': 'foo.py', 'database': None, 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config       


@pytest.fixture()
def invalid_database_url_config():
    config = {'models': 'foo.py', 'database': 'foo', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config       
                                                                
                     
              

@pytest.fixture()
def missing_api_value_config():
    config = {'models': 'foo.py', 'database': 'foo', 'apis': None}
    yield config    

              

def test_validate_config_extra_keys(config_extra_keys):
    validated_config = validate_config(config_extra_keys)
    assert isinstance(validated_config, Exception)
    assert 'Wrong keys' in str(validated_config)
    assert 'hello' in str(validated_config)


def test_validate_config_missing_keys(config_missing_keys):
    validated_config = validate_config(config_missing_keys) 
    assert isinstance(validated_config, Exception)
    assert 'Missing keys' in str(validated_config)
    assert 'models' in str(validated_config)

def test_validate_config_valid_config(valid_config, mocker):
    mocker.patch('columbus.framework.validators.validate_config_key', return_value = 'mock_key')
    validated_config = validate_config(valid_config)
    assert validated_config == valid_config



#add parametrize
def test_validate_config_key(valid_config, mocker):
    key_value = 'models.py'
    mocker.patch('columbus.framework.validators.validate_models', return_value=key_value)
    validated_key = validate_config_key(valid_config,'models')
    assert validated_key == key_value

def test_validate_models_no_value(missing_models_value_config):  
    models_validator = validate_models(missing_models_value_config)
    assert isinstance(models_validator, Exception)
    assert 'No value for key models in config' in str(models_validator)

def test_validate_models_missing_file(missing_models_file_config):
    models_validator = validate_models(missing_models_file_config)
    assert isinstance(models_validator, Exception)
    assert 'No such file' in str(models_validator)
    assert 'foo.py' in str(models_validator)

def test_validate_models_valid_config(valid_config):
    models_validator = validate_models(valid_config)
    assert models_validator == valid_config['models']

def test_validate_database_no_value(missing_database_value_config):
    database_validator = validate_database(missing_database_value_config)
    assert isinstance(database_validator, Exception)
    assert 'No value for key database in config' in str(database_validator)
    
def test_validate_database_invalid_url(invalid_database_url_config):
    database_validator = validate_database(invalid_database_url_config)   
    assert isinstance(database_validator, Exception)
    assert 'Invalid database url' in str(database_validator)

def test_validate_api_config_no_value(missing_api_value_config):
    validated_config = validate_api_config(missing_api_value_config)
    assert isinstance(validated_config, Exception)
    assert 'No value for key apis in config'

def test_validate_api_config_valid(valid_config, mocker):
    api_config =  {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}
    mocker.patch('columbus.framework.validators.validate_api', return_value = api_config)
    validated_config = validate_api_config(valid_config)
    assert validated_config == api_config

def test_validate_api_missing_keys():
    models_file = 'tests/integration/models.py'
    api =  {'methods':['GET', 'POST', 'DELETE'] }
    validated_api = validate_api(models_file, api)
    assert isinstance(validated_api, Exception)
    assert 'Missing keys' in str(validated_api)
    assert 'table' in str(validated_api)

def test_validate_api_extra_keys():
    models_file = 'tests/integration/models.py'
    api =  {'table': 'dogs', 'foo':'bar', 'methods':['GET', 'POST', 'DELETE'] }
    validated_api = validate_api(models_file, api)
    assert isinstance(validated_api, Exception)
    assert 'Wrong keys' in str(validated_api)
    assert 'foo' in str(validated_api)


def test_validate_api_missing_value_table():
    models_file = 'tests/integration/models.py'
    api = {'table': None, 'methods':['GET', 'POST', 'DELETE'] }
    validated_api = validate_api(models_file, api)
    assert isinstance(validated_api, Exception)
    assert 'No value for key table in config' in str(validated_api)

def test_validate_api_no_db_table():
    models_file = 'tests/integration/models.py'
    api = {'table': 'foo', 'methods':['GET', 'POST', 'DELETE'] }
    validated_api = validate_api(models_file, api)
    assert isinstance(validated_api, Exception)
    assert 'No database table foo in {}'.format(models_file) in str(validated_api)

def test_validate_api_missing_value_methods():
    models_file = 'tests/integration/models.py'
    api = {'table': 'dogs', 'methods':None}
    validated_api = validate_api(models_file, api)
    assert isinstance(validated_api, Exception)
    assert 'No value for key methods in config' in str(validated_api)

def test_validate_api_invalid_methods():
    models_file = 'tests/integration/models.py'
    api = {'table': 'dogs', 'methods':['GET', 'POST', 'FOO'] }
    validated_api = validate_api(models_file, api)
    assert isinstance(validated_api, Exception)
    assert 'Invalid methods in methods key' in str(validated_api)
    assert 'FOO' in str(validated_api)



    








