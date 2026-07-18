from app.utils.text import normalize_name, parse_name_list, sanitize_filename, strip_list_prefix


def test_normalize_name_removes_accents_case_and_punctuation() -> None:
    assert normalize_name("  Grandioso És Tu! ") == "grandioso es tu"


def test_strip_list_prefix_accepts_common_numbering() -> None:
    assert strip_list_prefix("02 - Porque Ele Vive") == "Porque Ele Vive"
    assert strip_list_prefix("• Alvo Mais Que a Neve") == "Alvo Mais Que a Neve"


def test_parse_list_reports_and_removes_normalized_duplicates() -> None:
    result = parse_name_list("Grandioso És Tu\ngrandioso es tu; Porque Ele Vive")
    assert result.items == ("Grandioso És Tu", "Porque Ele Vive")
    assert result.duplicates == ("grandioso es tu",)


def test_parse_list_can_keep_duplicates() -> None:
    result = parse_name_list("Hino; hÍno", remove_duplicates=False)
    assert result.items == ("Hino", "hÍno")


def test_sanitize_filename_handles_windows_reserved_and_invalid_names() -> None:
    assert sanitize_filename("CON") == "_CON"
    assert sanitize_filename('Hino: 01 / "Paz"') == "Hino_ 01 _ _Paz_"
