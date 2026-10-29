"""Public Android availability must not imply public plugin or active Pro billing."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicAvailability(unittest.TestCase):
    def test_public_android_import_and_approval_are_clear(self):
        for name in ['privacy.html', 'terms.html', 'support.html']:
            text = (ROOT / name).read_text(encoding='utf-8')
            for phrase in ['publicly available on Google Play in the United States',
                           '0.1.20 (30)', 'without a Pro subscription',
                           'Older releases may require an update',
                           'review and approve imported items before saving']:
                self.assertIn(phrase, text, name)
            for outdated in ['0.1.19+28', '0.1.18+27', 'not generally available',
                             'still checks Pro access', 'existing Closed testing – Alpha group']:
                self.assertNotIn(outdated, text, name)

    def test_plugin_and_billing_availability_remain_separate(self):
        privacy = (ROOT / 'privacy.html').read_text(encoding='utf-8')
        terms = (ROOT / 'terms.html').read_text(encoding='utf-8')
        support = (ROOT / 'support.html').read_text(encoding='utf-8')
        product = (ROOT / 'simple-checklist.html').read_text(encoding='utf-8')
        self.assertIn('has not yet been publicly listed', privacy)
        self.assertIn('subject to OpenAI review and publication', privacy)
        self.assertIn('private testing, not publicly listed', terms)
        self.assertIn('not publicly listed yet', support)
        self.assertIn('Planned offering, not a checkout', terms)
        self.assertIn('Pro subscriptions are planned and are not currently sold', product)
        self.assertNotIn('Android · Launch testing', product)
        for page in [privacy, terms]:
            self.assertIn('<strong>Effective date:</strong> October 27, 2026.', page)


if __name__ == '__main__':
    unittest.main()
