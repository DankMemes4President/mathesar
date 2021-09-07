import pytest
from sqlalchemy.exc import NoSuchTableError

from db.tables.ddl.create import create_mathesar_table
from db.tables.ddl.update import rename_table
from db.tables import utils as table_utils
from db.tests.tables import utils as test_utils


def test_rename_table(engine_with_schema):
    engine, schema = engine_with_schema
    table_name = "test_rename_table"
    new_table_name = "test_rename_table_new"
    old_table = create_mathesar_table(table_name, schema, [], engine)
    old_oid = table_utils.get_oid_from_table(old_table.name, old_table.schema, engine)

    rename_table(table_name, schema, engine, new_table_name)
    new_table = table_utils.reflect_table(new_table_name, schema, engine)
    new_oid = table_utils.get_oid_from_table(new_table.name, new_table.schema, engine)

    assert old_oid == new_oid
    assert new_table.name == new_table_name

    with pytest.raises(NoSuchTableError):
        table_utils.reflect_table(table_name, schema, engine)


def test_rename_table_foreign_key(engine_with_schema):
    engine, schema = engine_with_schema
    table_name = "test_rename_table_foreign_key"
    new_table_name = "test_rename_table_foreign_key_new"
    related_table_name = "test_rename_table_foreign_key_related"

    table = create_mathesar_table(table_name, schema, [], engine)
    related_table = test_utils.create_related_table(related_table_name, table, schema, engine)

    rename_table(table_name, schema, engine, new_table_name)

    related_table = table_utils.reflect_table(related_table_name, schema, engine)
    fk = list(related_table.foreign_keys)[0]
    assert fk.column.table.name == new_table_name