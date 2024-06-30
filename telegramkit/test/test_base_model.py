import pytest
from telegramkit.base_model import BaseModel

class MockClient:
    pass

def test_base_model_init():
    client = MockClient()
    base_model = BaseModel(client, 1)
    assert base_model.client == client
    assert base_model.id == 1

def test_base_model_from_dict():
    client = MockClient()
    base_model = BaseModel(client, 1)
    data = {'attr1': 'value1', 'attr2': 'value2'}
    base_model.from_dict(data)
    assert base_model.attr1 == 'value1'
    assert base_model.attr2 == 'value2'

@pytest.mark.asyncio
async def test_base_model_to_dict():
    client = MockClient()
    base_model = BaseModel(client, 1)
    base_model.attr1 = 'value1'
    base_model.attr2 = 'value2'
    data = await base_model.to_dict()
    assert data['attr1'] == 'value1'
    assert data['attr2'] == 'value2'
