from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import fix_statecraft_common_asr_entities as fix  # noqa: E402

def test_apply_replacements_fixes_selected_entity_families() -> None:
    text = (
        "Xiinping met Wangi near Bundra Abbas while Judge Andrew Npalitano listened to Witgo.\n"
        "A second report mentioned Witoff near Karg Island and later Karg itself.\n"
        "Netanyao deferred to Ayatah Ham while Wit Gulf waited nearby.\n"
        "Foreign Minister Arachi briefed President Peskin and later Abbas Araqchi met them.\n"
        "The ship moved through the straight of Hermoose.\n"
        "Another report said the trade of Hermuz and the straight of her moose were decisive.\n"
        "Pete Hexath, Pete Hegs, Hexa, Hacket, and heg Seth all spoke.\n"
    )

    updated, counts = fix.apply_replacements(text)

    assert "Xiinping" not in updated
    assert "Wangi" not in updated
    assert "Bundra Abbas" not in updated
    assert "Npalitano" not in updated
    assert "Witgo" not in updated
    assert "Witoff" not in updated
    assert "Karg Island" not in updated
    assert "Netanyao" not in updated
    assert "Ayatah Ham" not in updated
    assert "Wit Gulf" not in updated
    assert "Arachi" not in updated
    assert "Araqchi" not in updated
    assert "Peskin" not in updated
    assert "straight of Hermoose" not in updated
    assert "trade of Hermuz" not in updated
    assert "straight of her moose" not in updated
    assert "Hexath" not in updated
    assert "Pete Hegs," not in updated
    assert "Hexa" not in updated
    assert "Hacket" not in updated
    assert "heg Seth" not in updated
    assert "Xi Jinping" in updated
    assert "Wang Yi" in updated
    assert "Bandar Abbas" in updated
    assert "Judge Andrew Napolitano" in updated
    assert updated.count("Witkoff") == 3
    assert updated.count("Kharg") == 2
    assert "Netanyahu" in updated
    assert "Ayatollah Khamenei" in updated
    assert updated.count("Araghchi") == 2
    assert "Pezeshkian" in updated
    assert updated.count("Strait of Hormuz") == 3
    assert updated.count("Hegseth") >= 5
    assert counts["xi_jinping"] == 1
    assert counts["wang_yi"] == 1
    assert counts["bandar_abbas"] == 1
    assert counts["napolitano_name"] == 1
    assert counts["witkoff_name"] == 3
    assert counts["kharg_island"] == 2
    assert counts["netanyahu_name"] == 1
    assert counts["khamenei_title_name"] == 1
    assert counts["araghchi_name"] == 2
    assert counts["pezeshkian_name"] == 1
    assert counts["hormuz_proper_noun_family"] == 3
    assert counts["hegseth_hexath"] == 1
    assert counts["hegseth_hegs"] == 1
    assert counts["hegseth_hexa"] == 1
    assert counts["hegseth_hacket"] == 1
    assert counts["hegseth_split"] == 1

def test_apply_replacements_fixes_residual_hegseth_context_variants() -> None:
    text = (
        "Pete Haga and Pete Hax stood next to Peter Hexith.\n"
        "Pete Haxet, Pete Hexit, and Pete Hexet joined them.\n"
        "Pete Hexed, Pete Hexeth, and Pete Het arrived after that.\n"
        "Later Pete Hgse, Pete Hegsth, and Pete Hagsth talked.\n"
        "Pete Heg says the strike will continue, and Pete Hex's head may roll.\n"
        "Secretary of War Hagel said the operation was on track.\n"
        "Hegath, Hegathth, Hagseth, Hexth, Hegth, Hegsef, and Hgsith were quoted again the next day.\n"
    )

    updated, counts = fix.apply_replacements(text)

    assert "Pete Haga" not in updated
    assert "Pete Hax" not in updated
    assert "Pete Haxet" not in updated
    assert "Pete Hexit" not in updated
    assert "Pete Hexet" not in updated
    assert "Pete Hexed" not in updated
    assert "Pete Hexeth" not in updated
    assert "Pete Het" not in updated
    assert "Peter Hexith" not in updated
    assert "Pete Hgse" not in updated
    assert "Pete Hegsth" not in updated
    assert "Pete Hagsth" not in updated
    assert "Pete Heg says" not in updated
    assert "Pete Hex's head" not in updated
    assert "Secretary of War Hagel said" not in updated
    assert "Hegath" not in updated
    assert "Hegathth" not in updated
    assert "Hagseth" not in updated
    assert "Hexth" not in updated
    assert "Hegth" not in updated
    assert "Hegsef" not in updated
    assert "Hgsith" not in updated
    assert updated.count("Pete Hegseth") >= 12
    assert "Pete Hegseth says" in updated
    assert "Pete Hegseth's head" in updated
    assert "Secretary of War Hegseth said" in updated
    assert counts["hegseth_pete_variant"] == 9
    assert counts["hegseth_pete_phrase"] == 2
    assert counts["hegseth_title_phrase"] == 1
    assert counts["hegseth_hegath"] == 1
    assert counts["hegseth_tail_token"] == 9

def test_apply_replacements_fixes_eu_iran_negotiation_cluster() -> None:
    text = (
        "Keith Stormer and Kayak Kalas met while Kayakalas spoke.\n"
        "theuou and noou were discussed; the theou was planned; sign theou later.\n"
        "Lean River and Leani River; Benavir; in the EES; Enquury; Tatari government.\n"
    )

    updated, counts = fix.apply_replacements(text)

    assert "Keith Stormer" not in updated
    assert "Kayak Kalas" not in updated
    assert "Kayakalas" not in updated
    assert "theuou" not in updated
    assert "noou" not in updated
    assert "the theou was" not in updated
    assert "sign theou" not in updated
    assert "Lean River" not in updated
    assert "Leani River" not in updated
    assert "Benavir" not in updated
    assert "in the EES" not in updated
    assert "Enquury" not in updated
    assert "Tatari government" not in updated
    assert "Keith Starmer" in updated
    assert updated.count("Kaja Kallas") == 2
    assert "MOU" in updated
    assert updated.count("Litani River") == 2
    assert "Netanyahu" in updated
    assert "in the EEAS" in updated
    assert "Anchorage" in updated
    assert "Qatar government" in updated
    assert counts["starmer_keith_stormer"] == 1
    assert counts["kallas_kayak_kalas"] == 1
    assert counts["kallas_kayakalas"] == 1
    assert counts["mou_theuou"] == 1
    assert counts["mou_noou"] == 1
    assert counts["litani_lean_river"] == 1
    assert counts["litani_leani_river"] == 1

def test_apply_replacements_skips_markdown_link_paths_and_urls() -> None:
    line = (
        "- [source-mercouris-oil-crisis-aragchi-russia-2026-03-06.md]"
        "(2026-03-06/source-mercouris-oil-crisis-aragchi-russia-2026-03-06.md) "
        "— Aragchi met Xiinping; see https://example.com/path/kyiv-story"
    )

    updated, counts = fix.apply_replacements(line)

    assert "aragchi" in updated
    assert "Araghchi" in updated
    assert "Xi Jinping" in updated
    assert "https://example.com/path/kyiv-story" in updated
    assert counts["araghchi_name"] == 1
    assert counts["xi_jinping"] == 1
    assert counts.get("kiev_kyiv_canonical", 0) == 0

def test_fix_root_only_touches_transcript_like_files(tmp_path: Path) -> None:
    transcript = tmp_path / "source-archive" / "statecraft" / "2026-05-31" / "transcript-example.md"
    transcript.parent.mkdir(parents=True)
    transcript.write_text(
        "---\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "---\n\n"
        "# Title\n\n"
        "Xiinping discussed the straight of Hermus near Bund Abbas while Judge Andrew Npalitano watched Witgov near Karg Island as Arachi briefed Peskan and Netanyao quoted Ayatah Ham.\n",
        encoding="utf-8",
    )
    note = tmp_path / "source-archive" / "statecraft" / "note.md"
    note.write_text("Xiinping should stay untouched here.\n", encoding="utf-8")

    result = fix.fix_root(tmp_path / "source-archive" / "statecraft", write=True)

    assert result["changed_files"] == 1
    body = transcript.read_text(encoding="utf-8")
    assert "Xi Jinping" in body
    assert "Strait of Hormuz" in body
    assert "Bandar Abbas" in body
    assert "Judge Andrew Napolitano" in body
    assert "Witkoff" in body
    assert "Kharg Island" in body
    assert "Netanyahu" in body
    assert "Ayatollah Khamenei" in body
    assert "Araghchi" in body
    assert "Pezeshkian" in body
    assert note.read_text(encoding="utf-8") == "Xiinping should stay untouched here.\n"

def test_apply_replacements_fixes_khairullin_mercouris_asr_cluster() -> None:
    text = (
        "Marat Kulin on Substack; Marat Khulin and Kyuin compared notes.\n"
        "Kyuin's map; Kulin puts troops at 3,000. Kharkov/Khulin Konstantinovka.\n"
        "Marat Kaiin confirmed; Marad Khulin laid out Odessa. Hulu said fall by year-end.\n"
    )
    updated, counts = fix.apply_replacements(text)
    assert "Kulin" not in updated
    assert "Khulin" not in updated
    assert "Kyuin" not in updated
    assert "Kaiin" not in updated
    assert "Marad Khulin" not in updated
    assert "Hulu said" not in updated
    assert updated.count("Khairullin") >= 6
    assert updated.count("Marat Khairullin") >= 3
    assert "Kharkov/Khairullin" in updated
    assert counts["khairullin_marat_full"] >= 2
    assert counts["khairullin_surname_asr"] >= 1
    assert counts["khairullin_kulin"] >= 1
    assert counts["khairullin_hulu_said"] == 1

def test_apply_replacements_fixes_nima_alkhorshid_display() -> None:
    text = (
        "Host Nima Alkhorshid opened. **Nima Alkhorshid:** welcome back.\n"
        "Alkorshid's guest spoke; Alkorshid thanked Carl.\n"
    )
    updated, counts = fix.apply_replacements(text)
    assert "Alkorshid" not in updated
    assert "Nima Alkhorshid" in updated
    assert "**Nima Alkhorshid:**" in updated
    assert "Alkhorshid's" in updated
    assert counts["nima_alkhorshid_display"] == 2
    assert counts["nima_alkhorshid_surname_poss"] == 1
    assert counts["nima_alkhorshid_surname_canonical"] == 1

def test_apply_replacements_fixes_martyanov_asr_family() -> None:
    text = (
        "Andre Martiano and Andrei Martanov joined Andre Martianos.\n"
        "martynaov slug typo and Martinov is a former officer.\n"
    )
    labels = {
        "martyanov_andrei_martiano",
        "martyanov_andre_martiano",
        "martyanov_andrei_martanov",
        "martyanov_andre_martanov",
        "martyanov_andre_martianos",
        "martyanov_martynaov",
        "martyanov_martinov",
        "martyanov_martanov",
    }
    specs = fix.select_specs(labels)
    updated, counts = fix.apply_replacements(text, specs)
    assert "Martiano" not in updated
    assert "Martanov" not in updated
    assert "martynaov" not in updated
    assert "Martinov" not in updated
    assert "Martianos" not in updated
    assert updated.count("Martyanov") == 5
    assert counts["martyanov_andre_martiano"] == 1
    assert counts["martyanov_andrei_martanov"] == 1
    assert counts["martyanov_andre_martianos"] == 1
    assert counts["martyanov_martynaov"] == 1
    assert counts["martyanov_martinov"] == 1
