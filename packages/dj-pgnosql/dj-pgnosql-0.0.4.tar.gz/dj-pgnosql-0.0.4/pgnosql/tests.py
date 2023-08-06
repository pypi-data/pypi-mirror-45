from django.test import TestCase
from .models import KV
class KVTestCase(TestCase):

    databases = {'default', 'pgnosql'}

    def setUp(self):
        pass

    def test_set_kv(self):
        key = KV.set('foo', {"bar": "baz"})
        self.assertIsInstance(key, KV)
        self.assertEqual(
            KV.objects.count(),
            1,
            'Create a key'
        )

    def test_set_will_update_if_key_already_exists(self):
        key = KV.set('foo', {"bar": "baz"})
        self.assertEqual(
            KV.get("foo").get("bar"),
            "baz"
        )

        key = KV.set('foo', {"bar": "bus"})
        self.assertEqual(KV.get("foo").get("bar"), "bus")

    def test_get_kv(self):
        KV.set('foo', {"bar": "baz"})
        got = KV.get('foo')
        self.assertEqual(
            got.get('bar'),
            "baz"
        )

    def test_get_returns_none_if_key_does_not_exist(self):
        self.assertIsNone(KV.get('nope'))

    def test_can_delete(self):
        KV.set('foo', {"bar": "baz"})
        self.assertIsNotNone(KV.get("foo"))
        KV.delete_key("foo")
        self.assertIsNone(KV.get("foo"))



