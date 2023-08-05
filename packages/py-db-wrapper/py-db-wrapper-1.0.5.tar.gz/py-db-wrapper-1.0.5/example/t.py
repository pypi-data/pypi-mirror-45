import sys
sys.path.insert(0, "../")

from py_db_wrapper import types 
from py_db_wrapper import dialects

print(types.BIGINT.TYPES[dialects.Mysql])

print(types.BIGINT.TYPES.__len__())

# print(types.get_base_type_from_string(dialects.Mysql, 'BIGINT'))

# mssql = types.convert_type_string('BIGINT', dialects.Mysql, dialects.Mssql)
# print(mssql)