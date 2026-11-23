import unittest
from pathlib import Path
from iban_validation_claim_audit.audit import audit, evidence, matches
from iban_validation_claim_audit.phrases import IBANVALIDATION, NOIBANVALIDATION, GENERIC_NAMES
ROOT = Path(__file__).resolve().parents[1]

class AuditTests(unittest.TestCase):
    def test_library_routes(self):
        cases = ['from stdnum.iban import validate as v\nv(x)', 'from stdnum.iban import is_valid as v\nv(x)', 'import stdnum\nstdnum.iban.validate(x)', 'import stdnum.iban\nstdnum.iban.is_valid(x)', 'from stdnum import iban as i\ni.validate(x)', 'from stdnum import iban\niban.is_valid(x)', 'import stdnum.iban as i\ni.validate(x)', 'from schwifty import IBAN as I\nI(x)', 'import schwifty as s\ns.IBAN(x)']
        for name in GENERIC_NAMES:
            cases += ['obj.%s(x)' % name, 'from lib import %s as v\nv(x)' % name, 'obj = make()\nobj.%s(x)' % name]
        for case in cases:
            with self.subTest(case=case): self.assertTrue(evidence(case))

    def test_not_evidence(self):
        cases = ['import stdnum.iban', 'import schwifty', 'validate(x)', 'is_valid(x)', 'IBAN(x)', 'obj.validate(x)', 'obj.is_valid(x)', 'obj.IBAN(x)', 'import stdnum.iban\nstdnum.iban.compact(x)', 'import stdnum.iban\nstdnum.iban.format(x)', 'import stdnum.iban\nstdnum.iban.calc_check_digits(x)', 'from schwifty import IBAN\nIBAN.generate(x)', 'from schwifty import BIC\nBIC(x)', 'from lib import IbanValidation\nIbanValidation(x)', 'payment.process(x)', 'extract.document(x)', 'subprocess.run(["validator", x])', '"validate iban"', '# validate iban', 'from stdnum.iban import validate', 'from schwifty import IBAN\ndef IBAN(x): pass\nIBAN(x)', 'from stdnum import iban\niban = x\niban.validate(x)', 'def validate_iban(x): pass\nobj.validate_iban(x)', 'from lib import validate_iban\nwith ctx() as validate_iban:\n validate_iban(x)', 'invalid ! syntax', 'from isbnlib import Isbn\nIsbn(x)', 'import barcode\nbarcode.get("iban", x)', 'from barcode import IBAN\nIBAN(x)', 'import barcode\nbarcode.generate("iban", x)']
        cases += ['import re\nre.%s("[A-Z]+", x)' % x for x in ('match','search','fullmatch')]
        cases += ['from urllib.parse import %s\n%s(x)' % (x,x) for x in ('urlparse','urlsplit')]
        cases += ['import validators\nvalidators.%s(x)' % x for x in ('url','ipv4','ipv6','email','card_number','domain')]
        cases += ['import isbnlib\nisbnlib.%s(x)' % x for x in ('is_isbn10','is_isbn13','notisbn')]
        cases += ['import stdnum.%s\nstdnum.%s.%s(x)' % (m,m,f) for m in ('isbn','issn') for f in ('validate','is_valid')]
        cases += ['x.%s' % x for x in ('compact','formatted','country_code','bank_code','account_code','bic','length')]
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence(case))

    def test_phrases(self):
        for phrase in IBANVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(matches(phrase)[0])
        for phrase in NOIBANVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(matches(phrase), ([], [phrase]))
        self.assertEqual(matches('```\nvalidate iban\n```'), ([], []))
        self.assertTrue(matches('`validate iban`')[0])

    def test_findings(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp); (p/'README.md').write_text('validate iban')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_x.py').write_text('obj.validate_iban(x)')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'MEDIUM')
            (p/'src.py').write_text('obj.validate_iban(x)')
            self.assertFalse(audit(p)['findings'])
            (p/'README.md').write_text('no iban validation')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')
            self.assertFalse(audit(p, ['src.py'])['findings'])

    def test_self_audit(self):
        self.assertFalse(audit(ROOT)['findings'])
        self.assertFalse(audit(ROOT/'README.md')['findings'])

    def test_limitations_prose(self):
        text = (ROOT/'README.md').read_text().split('## Limitations', 1)[1]
        self.assertEqual(matches(text), ([], []))
