import unittest

# import sys
# sys.path.insert(0, "../")
# more comments
from py_db_wrapper import types, dialects, exceptions

class TestStringMethods(unittest.TestCase):

    def test_convert_type_string(self):
        conversions = {
            dialects.Mysql:[
                {'input_value':'BIGINT', 'expected_value':'bigint', 'convert_to_dialect':dialects.Mssql}
            ],
            dialects.Mssql:[
                {'input_value':'bigint1', 'expected_value':'BIGINT', 'convert_to_dialect':dialects.Mysql}
            ],            
        }

        # check that an unknown type string raises TYPE_NOT_DEFINED error
        with self.assertRaises(exceptions.TYPE_NOT_DEFINED):
            types.convert_type_string('foo', dialects.Mssql, dialects.Mysql)
       
        for key, values in conversions.items():
            for case in values:
                self.assertEqual(types.convert_type_string(case['input_value'],key, case['convert_to_dialect']), case['expected_value'])
                # self.assertEqual(types.convert_type_string(case['expected_value'], case['convert_to_dialect'], key ), case['input_value'])


if __name__ == '__main__':
    unittest.main() 