import contextlib
import datetime
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import render_pdf


class ConvertTests(unittest.TestCase):
    def test_headings(self) -> None:
        out = render_pdf.convert("# One\n\n## Two\n\n### Three")
        self.assertIn('<h1 dir="auto">One</h1>', out)
        self.assertIn('<h2 dir="auto">Two</h2>', out)
        self.assertIn('<h3 dir="auto">Three</h3>', out)

    def test_bold_italic_and_inline_code(self) -> None:
        out = render_pdf.convert("A **strong** and *soft* word with `x < y`.")
        self.assertIn("<strong>strong</strong>", out)
        self.assertIn("<em>soft</em>", out)
        self.assertIn("<code>x &lt; y</code>", out)

    def test_nested_list_with_continuation(self) -> None:
        source = "- first\n  continues here\n  - inner one\n  - inner two\n- second\n"
        out = render_pdf.convert(source)
        self.assertEqual(out.count("<ul"), 2)
        self.assertEqual(out.count("<li"), 4)
        self.assertIn("first<br>\ncontinues here", out)
        self.assertIn("inner one", out.split("first", 1)[1].split("second")[0])

    def test_ordered_list_keeps_its_start_number(self) -> None:
        out = render_pdf.convert("3. third\n4. fourth")
        self.assertIn('<ol dir="auto" start="3">', out)

    def test_multi_paragraph_blockquote(self) -> None:
        out = render_pdf.convert("> First paragraph.\n>\n> Second paragraph.\n\nAfter.")
        quote = out.split("<blockquote", 1)[1].split("</blockquote>")[0]
        self.assertEqual(quote.count("<p "), 2)
        self.assertIn('<p dir="auto">After.</p>', out.split("</blockquote>")[1])

    def test_table(self) -> None:
        source = "| Name | Count |\n| :--- | ---: |\n| a | 1 |\n| b | 2 |\n"
        out = render_pdf.convert(source)
        self.assertIn("<thead>", out)
        self.assertEqual(out.count("<th "), 2)
        self.assertEqual(out.count("<td "), 4)
        self.assertIn('style="text-align:end"', out)

    def test_fenced_code_block_is_literal(self) -> None:
        out = render_pdf.convert("```\n<b>raw</b> **not bold** [slot]\n```")
        self.assertIn("&lt;b&gt;raw&lt;/b&gt; **not bold** [slot]", out)
        self.assertNotIn("<strong>", out)
        self.assertNotIn('class="slot"', out)

    def test_horizontal_rule(self) -> None:
        self.assertIn("<hr>", render_pdf.convert("above\n\n---\n\nbelow"))

    def test_html_is_escaped(self) -> None:
        out = render_pdf.convert("<script>alert(1)</script> & <b>x</b>")
        self.assertNotIn("<script", out)
        self.assertIn("&lt;script&gt;", out)
        self.assertIn("&amp;", out)

    def test_unsafe_link_scheme_is_dropped(self) -> None:
        out = render_pdf.convert("[click](javascript:alert(1)) and [ok](https://example.test/a)")
        self.assertNotIn("javascript:", out)
        self.assertIn('<a href="https://example.test/a">ok</a>', out)

    def test_bare_url_becomes_a_link(self) -> None:
        out = render_pdf.convert("See https://example.test/page.")
        self.assertIn('<a href="https://example.test/page">https://example.test/page</a>.', out)

    def test_bracket_slot_is_highlighted(self) -> None:
        out = render_pdf.convert("Led a team of [number of people] engineers.")
        self.assertIn('<span class="slot">[number of people]</span>', out)

    def test_slot_not_applied_inside_links_or_code(self) -> None:
        out = render_pdf.convert("[docs](https://example.test) and `[kept]`")
        self.assertNotIn('class="slot"', out)
        self.assertIn("<code>[kept]</code>", out)

    def test_non_latin_text_passes_through(self) -> None:
        for sample in ("Colaboração e posição", "日本語のテキスト", "مرحبا بالعالم"):
            with self.subTest(sample=sample):
                out = render_pdf.convert("## " + sample + "\n\n" + sample)
                self.assertEqual(out.count(sample), 2)
        self.assertIn('<p dir="auto">', out)


class DocumentTests(unittest.TestCase):
    def test_lang_and_title_block(self) -> None:
        document = render_pdf.build_document("<p>x</p>", "A & B", "pt-BR", "2026-01-02")
        self.assertIn('<html lang="pt-BR">', document)
        self.assertIn("<title>A &amp; B</title>", document)
        self.assertIn("2026-01-02", document)

    def test_first_heading_is_taken_as_title(self) -> None:
        title, rest = render_pdf.take_first_heading(["intro", "# My **Report**", "body"])
        self.assertEqual(title, "My Report")
        self.assertEqual(rest, ["intro", "body"])

    def test_heading_inside_fence_is_ignored(self) -> None:
        title, _ = render_pdf.take_first_heading(["```", "# not a title", "```"])
        self.assertIsNone(title)


class MainTests(unittest.TestCase):
    def run_main(self, markdown: str, *extra: str) -> "tuple[int, str, Path]":
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(directory, ignore_errors=True))
        report = directory / "notes.md"
        report.write_text(markdown, encoding="utf-8")
        out = directory / "out.pdf"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            status = render_pdf.main([str(report), "-o", str(out), *extra], engines=())
        return status, stdout.getvalue(), out.with_suffix(".html")

    def test_no_engine_writes_html_and_returns_three(self) -> None:
        status, printed, html_path = self.run_main("# Title\n\nBody [slot].", "--lang", "pt-BR")
        self.assertEqual(status, 3)
        self.assertTrue(html_path.is_file())
        self.assertIn("No PDF engine was found", printed)
        document = html_path.read_text(encoding="utf-8")
        self.assertIn('<html lang="pt-BR">', document)
        self.assertIn(datetime.date.today().isoformat(), document)
        self.assertEqual(document.count("<h1"), 1)

    def test_explicit_title_keeps_the_body_heading(self) -> None:
        _, _, html_path = self.run_main("# Body heading\n\ntext", "--title", "Given")
        document = html_path.read_text(encoding="utf-8")
        self.assertIn("<title>Given</title>", document)
        self.assertIn("Body heading", document)

    def test_file_name_is_the_last_resort_title(self) -> None:
        _, _, html_path = self.run_main("just text")
        self.assertIn("<title>notes</title>", html_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
