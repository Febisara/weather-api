from datetime import date
import copy
import unittest
from pipeline import validate

class ValidationTests(unittest.TestCase):
    def payload(self):
        return {'daily_units': {
            'temperature_2m_mean':'°C', 'precipitation_sum':'mm',
            'wind_speed_10m_max':'km/h'}, 'daily': {
            'time':['2025-01-01'], 'temperature_2m_mean':[5.0],
            'precipitation_sum':[1.2], 'wind_speed_10m_max':[20.0]}}
    def check(self,p):
        return validate(p,date(2025,1,1),date(2025,1,1))
    def test_valid(self):
        self.assertEqual(len(self.check(self.payload())),1)
    def test_missing_value(self):
        p=self.payload();p['daily']['precipitation_sum']=[None]
        with self.assertRaises(ValueError):self.check(p)
    def test_wrong_date(self):
        p=self.payload();p['daily']['time']=['2025-01-02']
        with self.assertRaises(ValueError):self.check(p)
    def test_wrong_units(self):
        p=self.payload();p['daily_units']['precipitation_sum']='inch'
        with self.assertRaises(ValueError):self.check(p)

if __name__=='__main__':
    unittest.main()
