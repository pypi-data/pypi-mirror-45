#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import unittest
import mock
from io import StringIO
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "lib"))
import insult

class TestWordList(unittest.TestCase):
    def test_ctor(self):
        wl = insult.WordList("name")
        self.assertEqual(wl.name, "name")
        self.assertFalse(wl.words)

        wl = insult.WordList("name", ["hello", "world"])
        self.assertEqual(wl.name, "name")
        self.assertIn("hello", wl.words)
        self.assertIn("world", wl.words)

    def test_add_word(self):
        wl = insult.WordList("name")
        self.assertEqual(wl.name, "name")
        self.assertNotIn("hello", wl.words)
        wl.add_word("hello")
        self.assertIn("hello", wl.words)

    def test_get(self):
        wl = insult.WordList("name", ["a", "b", "c", "d"])
        self.assertEqual(len(wl.get()), 1)
        self.assertIn(wl.get()[0], wl.words)
        self.assertEqual(len(wl.get(3)), 3)
        self.assertEqual(len(wl.get(10)), 4)
        self.assertLessEqual(len(wl.get(3, 2)), 3)
        self.assertGreaterEqual(len(wl.get(3, 2)), 2)

    def test_word_list_id_class(self):
        wl1 = insult.WordList("1")
        wl2 = insult.WordList("2")
        id = insult.WordListId("1")
        self.assertTrue(id.check(wl1))
        self.assertFalse(id.check(wl2))

    def test_word_list_id_def(self):
        wli = insult.word_list_id("hello")
        self.assertIsInstance(wli, insult.WordListId)
        self.assertEqual(wli.name, "hello")
        self.assertEqual(wli.flags, 0)

        wli = insult.word_list_id("hello", 42)
        self.assertIsInstance(wli, insult.WordListId)
        self.assertEqual(wli.name, "hello")
        self.assertEqual(wli.flags, 42)

        wli = insult.word_list_id(("hello", 42))
        self.assertIsInstance(wli, insult.WordListId)
        self.assertEqual(wli.name, "hello")
        self.assertEqual(wli.flags, 42)

        wli = insult.word_list_id(insult.WordListId("hello", 42))
        self.assertIsInstance(wli, insult.WordListId)
        self.assertEqual(wli.name, "hello")
        self.assertEqual(wli.flags, 42)

        self.assertRaises(TypeError, lambda: insult.word_list_id(1, 2, 3, 4))
        self.assertRaises(TypeError, lambda: insult.word_list_id((1, 2, 3, 4)))


class TestInsulter(unittest.TestCase):
    def test_ctor(self):
        ins = insult.Insulter()
        self.assertFalse(ins.word_lists)
        self.assertIsNone(ins.max_count)
        self.assertFalse(ins.list_max_count)

    def test_word_list(self):
        ins = insult.Insulter()
        self.assertRaises(Exception, lambda: ins.word_list("a"))
        self.assertIsInstance(ins.word_list("a", True), insult.WordList)
        self.assertEqual(ins.word_list("a").name, "a")

    @mock.patch("os.listdir", return_value=["foo", "bar", "lol.jpg", insult.Insulter.rules_file])
    @mock.patch("os.path.isfile", return_value=True)
    def test_load_directory(self, *args, **kwargs):
        def fake_open(file, mode=""):
            if file == "foo/foo":
                contents = "foo\nbar\n"
            elif file == "foo/bar":
                contents = "hello\nworld\n\n"
            elif file == "foo/rules.json":
                contents = '{"test":[{"hello":"world"}]}'
            elif file == "bar/rules.json":
                contents = 'invalid json'
            elif file.startswith("bar/"):
                contents = ""
            else:
                raise Exception("Wrong file open: %s" % file)
            io = StringIO(contents)
            io.__enter__ = lambda *a, **k: io
            io.__exit__ = lambda *a, **k: None
            return io

        with mock.patch("insult.open", side_effect=fake_open):
            ins = insult.Insulter()
            ins.load_directory("foo")
            self.assertSetEqual(set(["foo", "bar"]), ins.word_list("foo").words)
            self.assertSetEqual(set(["hello", "world"]), ins.word_list("bar").words)
            self.assertRaises(Exception, lambda: ins.word_list("lol.jpg"))
            self.assertEqual(ins.rules["test"], [{"hello": "world"}])

            ins = insult.Insulter()
            try:
                ins.load_directory("bar")
            except Exception:
                self.fail("load_directory shouldn't fail")

    def test_add_words(self):
        ins = insult.Insulter()
        ins.word_list("a", True)
        ins.add_words("a", ["hello"])
        self.assertIn("hello", ins.word_list("a").words)

        ins.add_words("b", ["world"])
        self.assertIn("world", ins.word_list("b").words)

    def test_get(self):
        ins = insult.Insulter()
        ins.add_words("name", ["a", "b", "c", "d"])
        self.assertEqual(len(ins.get("name")), 1)
        self.assertEqual(len(ins.get("name", 3)), 3)
        self.assertEqual(len(ins.get("name", 10)), 4)
        self.assertLessEqual(len(ins.get("name", 3, 2)), 3)
        self.assertGreaterEqual(len(ins.get("name", 3, 2)), 2)

    def test_set_max(self):
        ins = insult.Insulter()
        ins.add_words("name", ["a", "b", "c", "d", "e"])
        self.assertEqual(len(ins.get("name", 5)), 5)

        ins.set_max(4)
        self.assertEqual(len(ins.get("name", 5)), 4)

        ins.set_max(3, "name")
        self.assertEqual(len(ins.get("name", 5)), 3)

        ins.set_max(2)
        self.assertEqual(len(ins.get("name", 5)), 2)

        ins.set_max(None)
        self.assertEqual(len(ins.get("name", 5)), 3)

        ins.set_max(None, "name")
        self.assertEqual(len(ins.get("name", 5)), 5)

        self.assertIsNone(ins.set_max(None, "name"))

    def test_format(self):
        ins = insult.Insulter()
        ins.set_rules("article", [
            {"target": "^[aeiouAEIOU8].*",  "result": r"an "},
            {"target": ".*",                "result": r"a "}
        ])
        phrase = "You are <article target='adj1' /><adjective id='adj1' count='3' /> <animal />"

        ins.word_lists = []
        ins.add_words("animal", ["pig"])
        ins.add_words("adjective", ["ugly"])
        self.assertEqual(ins.format(phrase), "You are an ugly pig")

        ins.word_lists = []
        ins.add_words("animal", ["pig"])
        ins.add_words("adjective", ["ignorant", "ugly", "awful"])
        formatted = ins.format(phrase)
        self.assertTrue(formatted.startswith("You are an "))
        self.assertIn("ignorant", formatted)
        self.assertIn("ugly", formatted)
        self.assertIn("awful", formatted)
        self.assertTrue(formatted.endswith("pig"))

        ins.word_lists = []
        ins.add_words("animal", ["pig"])
        ins.add_words("adjective", ["dastardly", "grotesque", "smelly"])
        formatted = ins.format(phrase)
        self.assertTrue(formatted.startswith("You are a "))
        self.assertIn("dastardly", formatted)
        self.assertIn("grotesque", formatted)
        self.assertIn("smelly", formatted)
        self.assertTrue(formatted.endswith("pig"))

        phrase = "You are <article target='adj1' /><adjective id='adj1' max='3' /> <animal />"
        ins.word_lists = []
        ins.add_words("animal", ["pig"])
        ins.add_words("adjective", ["ignorant", "ugly", "awful"])
        formatted = ins.format(phrase)
        self.assertTrue(formatted.startswith("You are an "))
        self.assertIn("ignorant", formatted)
        self.assertIn("ugly", formatted)
        self.assertIn("awful", formatted)
        self.assertTrue(formatted.endswith("pig"))

        self.assertEqual(ins.format("You are <foobar/>here"), "You are here")
        infref = "You are<article target='a' id='b'/> <article target='b' id='a'/>here"
        self.assertEqual(ins.format(infref), "You are here")
        ins.set_rules("article", [])

        ins.word_lists = []
        ins.add_words("animal", ["pig"])
        ins.add_words("adjective", ["smelly"])
        ins.set_rules("article", [])
        self.assertEqual(ins.format("<article target='a'><animal id='a'>"), "pig")


class TestNotQuiteXml(unittest.TestCase):
    def test_ctor(self):
        nqx = insult.NotQuiteXml()
        self.assertFalse(nqx.contents)

    def test_parse_just_text(self):
        nqx = insult.NotQuiteXml("Hello world")
        self.assertEqual(nqx.contents, ["Hello world"])
        self.assertFalse(nqx.elements_with_id)
        self.assertEqual(str(nqx), "Hello world")

    def test_parse_entities(self):
        nqx = insult.NotQuiteXml("Hello &lt;world&gt; &amp;amp;")
        self.assertEqual(nqx.contents, ["Hello <world> &amp;"])

    def test_parse_single_element(self):
        nqx = insult.NotQuiteXml("<hello/>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertIsNone(nqx.contents[0].id)
        self.assertFalse(nqx.contents[0].attrs)

        nqx = insult.NotQuiteXml("<hello>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertIsNone(nqx.contents[0].id)
        self.assertFalse(nqx.contents[0].attrs)

        nqx = insult.NotQuiteXml("<hello foo='bar'/>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertIsNone(nqx.contents[0].id)
        self.assertEqual(nqx.contents[0].attrs["foo"], "bar")

        nqx = insult.NotQuiteXml("<hello foo=bar/>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertIsNone(nqx.contents[0].id)
        self.assertEqual(nqx.contents[0].attrs["foo"], "bar")

        nqx = insult.NotQuiteXml("<hello foo='bar'>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertIsNone(nqx.contents[0].id)
        self.assertEqual(nqx.contents[0].attrs["foo"], "bar")

        nqx = insult.NotQuiteXml("<hello foo='bar'   bar=\"foo\" foobar hello= />")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertIsNone(nqx.contents[0].id)
        self.assertEqual(nqx.contents[0].attrs["foo"], "bar")
        self.assertEqual(nqx.contents[0].attrs["bar"], "foo")
        self.assertEqual(nqx.contents[0].attrs["foobar"], "foobar")
        self.assertEqual(nqx.contents[0].attrs["hello"], "")

        nqx = insult.NotQuiteXml("<hello foo='bar' id='hello1'/>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertEqual(nqx.contents[0].id, "hello1")
        self.assertEqual(nqx.contents[0].attrs["foo"], "bar")
        self.assertNotIn("id", nqx.contents[0].attrs)

        nqx = insult.NotQuiteXml("<hello id/>")
        self.assertEqual(len(nqx.contents), 1)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIs(nqx.contents[0].document, nqx)
        self.assertEqual(nqx.contents[0].tag_name, "hello")
        self.assertFalse(nqx.contents[0].attrs)
        self.assertNotIn("id", nqx.contents[0].attrs)
        self.assertIsNone(nqx.contents[0].id)

    def test_parse_mixed(self):
        nqx = insult.NotQuiteXml("Hello <world><foo/>bar")
        self.assertEqual(len(nqx.contents), 4)
        self.assertEqual(str(nqx), "Hello bar")
        self.assertIsInstance(nqx.contents[0], str)
        self.assertIsInstance(nqx.contents[1], insult.NotQuiteXmlElement)
        self.assertIsInstance(nqx.contents[2], insult.NotQuiteXmlElement)
        self.assertIsInstance(nqx.contents[3], str)

        nqx = insult.NotQuiteXml("<foo bar=1><foo bar=2>")
        self.assertEqual(len(nqx.contents), 2)
        self.assertIsInstance(nqx.contents[0], insult.NotQuiteXmlElement)
        self.assertIsInstance(nqx.contents[1], insult.NotQuiteXmlElement)
        self.assertEqual(nqx.contents[0].attrs["bar"], "1")
        self.assertEqual(nqx.contents[1].attrs["bar"], "2")

    def test_element_by(self):
        nqx = insult.NotQuiteXml("<foo bar=1><foo id=1 bar=2><bar bar=2 foo=''><bar id=1>")
        self.assertEqual(nqx.element_by_id("1").bar, "2")
        self.assertEqual(nqx.element_by_id("1").tag_name, "foo")
        self.assertEqual(len(nqx.elements_by_tag_name("foo")), 2)
        self.assertEqual(len(nqx.elements_by_attribute("bar", "2")), 2)
        self.assertEqual(len(nqx.elements_by_attribute("foo", "")), 1)

    def test_repr(self):
        nqx = insult.NotQuiteXml("hello <foo><foo bar=1>")
        self.assertEqual(repr(nqx), 'hello <foo/><foo bar=\"1\"/>')

    def test_element_document(self):
        nqx = insult.NotQuiteXml("<hello foo='bar' id='hello1'/>")
        element = nqx.contents[0]

        self.assertIs(element.document, nqx)
        def foo(): element.document = 0
        self.assertRaises(AttributeError, foo)
        self.assertIs(element.document, nqx)

    def test_element_tag_name(self):
        nqx = insult.NotQuiteXml("<hello foo='bar' id='hello1'/>")
        element = nqx.contents[0]

        self.assertEqual(element.tag_name, "hello")
        def foo(): element.tag_name = 0
        self.assertRaises(AttributeError, foo)
        self.assertEqual(element.tag_name, "hello")

    def test_element_id(self):
        nqx = insult.NotQuiteXml("<hello foo='bar' id='hello1'/><world/>")
        element = nqx.contents[0]

        self.assertEqual(element.id, "hello1")
        self.assertIs(nqx.elements_with_id["hello1"], element)
        element.id = "hello2"
        self.assertEqual(element.id, "hello2")
        self.assertNotIn("hello1", nqx.elements_with_id)
        self.assertIs(nqx.elements_with_id["hello2"], element)

        try:
            element.id = "hello2"
        except KeyError:
            self.fail("Should not fail on same id assignment")

        def foo(): nqx.contents[1].id = "hello2"
        self.assertRaises(KeyError, foo)

        element.id = None
        self.assertNotIn("hello2", nqx.elements_with_id)
        element.id = "hello1"
        self.assertIn("hello1", nqx.elements_with_id)
        del element.id
        self.assertNotIn("hello1", nqx.elements_with_id)
        del element.id

    def test_element_attrs(self):
        nqx = insult.NotQuiteXml("<hello foo='bar' id='hello1'/>")
        element = nqx.contents[0]

        self.assertEqual(element.foo, "bar")
        del element.foo
        self.assertNotIn("foo", element.attrs)
        element.foo = "baz"
        self.assertEqual(element.attrs["foo"], "baz")
        def foo(): del element.notattr
        self.assertRaises(AttributeError, foo)

        element.attrs["foo"] = "bar"
        self.assertEqual(element["foo"], "bar")
        del element["foo"]
        self.assertNotIn("foo", element.attrs)
        element["foo"] = "baz"
        self.assertEqual(element.attrs["foo"], "baz")

        element.attrs["foo"] = "bar"
        self.assertEqual(element.attrs["foo"], "bar")
        del element.attrs["foo"]
        self.assertNotIn("foo", element.attrs)
        element.attrs["foo"] = "baz"
        self.assertEqual(element.attrs["foo"], "baz")

    def test_to_string(self):
        nqx = insult.NotQuiteXml("Hello <world> <foo/>bar", lambda x: x.tag_name)
        self.assertEqual(str(nqx), "Hello world foobar")



unittest.main()
