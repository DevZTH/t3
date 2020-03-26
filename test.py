import pytest
from runit import db_adapter

def test_db1():
    db = db_adapter(":memory")
    assert db.sp_SaveData(1, 'user@example.com', 'fio') == True
    assert db.sp_SaveData(0, 'user@example.com', 'fio') == False
    with pytest.raises(ValueError):
        db.sp_SaveData(0, 'user@example', 'fio')
    with pytest.raises(ValueError):
        db.sp_SaveData(0, 'user@example.com', 'русский текст')
    with pytest.raises(TypeError):
        db.sp_SaveData("incorrect number", 'user@example.com', 'fio')
    with pytest.raises(ValueError):
        db.sp_SaveData(11, 'user@example.com', 'fio')
        
test_db1()