"""Pure offline SEC discovery parser tests. No network or real financial claims."""
import pathlib
import sys
import unittest
from unittest import mock

SCRIPTS = pathlib.Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import sec_filing_discovery as s


class SecDiscoveryTests(unittest.TestCase):
    def test_recent_and_archived_page_shapes(self):
        rows={
          'accessionNumber':['0000000123-26-000001','0000000123-18-000002'],
          'form':['10-K','10-Q'],
          'filingDate':['2026-02-13','2018-09-10'],
          'reportDate':['2025-12-31','2018-06-30'],
          'primaryDocument':['form10k.htm','form10q.htm'],
          'acceptanceDateTime':['2026-02-13T12:00:00.000Z','']
        }
        a=s.filings_from_page({'filings':{'recent':rows}},'0000000123','fin:sample','Synthetic',{'10-K','10-Q'},2019)
        b=s.filings_from_page(rows,'0000000123','fin:sample','Synthetic',{'10-K','10-Q'},2019)
        self.assertEqual(a,b)
        self.assertEqual(len(a),1)
        self.assertEqual(a[0]['id'],'finfil:sec:0000000123:000000012326000001')
        self.assertEqual(a[0]['period_end'],'2025-12-31')
        self.assertEqual(a[0]['url'],'https://www.sec.gov/Archives/edgar/data/123/000000012326000001/form10k.htm')

    def test_path_traversal_and_wrong_forms_filtered(self):
        rows={'accessionNumber':['0000000123-26-000001','0000000123-26-000002'],
              'form':['10-K','8-K'],'filingDate':['2026-02-13','2026-04-01'],
              'primaryDocument':['../unsafe.html','event.htm']}
        self.assertEqual(s.filings_from_page(rows,'0000000123','fin:sample','Synthetic',{'10-K'},2019),[])

    def test_sec_ticker_ambiguity_requires_cik(self):
        with mock.patch.object(s,'get_json',return_value={'0':{'ticker':'TST','cik_str':123},
                                                        '1':{'ticker':'TST','cik_str':456}}):
            with self.assertRaisesRegex(ValueError,'ambiguous'):
                s.resolve_cik('TST','Synthetic contact@example.org')


if __name__=='__main__':unittest.main()
