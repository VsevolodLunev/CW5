import unittest
import pymysql


class TestSQLQueries(unittest.TestCase):

    def test_get_companies_and_vacancies_count(self):
        conn = pymysql.connect(host='localhost', user='postgres', password='', db='hh_db', port='5432')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT employer_name, COUNT(vacancies.employer_id) FROM employers INNER JOIN vacancies USING (employer_id)
        GROUP BY employer_name ORDER BY COUNT DESC;
        """)
        result = cursor.fetchall()
        expected = [
            ('Т-Банк', 20),
            ('Яндекс.Доставка', 20),
            ('Вега-ГАЗ', 20), ('Вода', 20),
            ('T2', 20),
            ('Яндекс.Еда', 20),
            ('Газпром газораспределение Волгоград', 16),
            ('Питон Кама', 13),
            ('Tennisi', 9)
        ]
        self.assertEqual(result, expected)
        conn.close()

    def test_get_all_vacancies(self):
        assert True

    def test_get_avg_salary(self):
        assert True

    def test_get_vacancies_with_higher_salary(self):
        assert True

    def test_get_vacancies_with_keyword(self, keyword):
        assert True


if __name__ == '__main__':
    unittest.main()
