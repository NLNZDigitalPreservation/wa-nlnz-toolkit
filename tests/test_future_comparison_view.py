from wa_nlnz_toolkit._future_comparison_view import highlight_phrases


def test_highlight_phrases_matches_slash_delimited_phrase():
    source = (
        "Vaccination is recommended for those over 65 and/or immunocompromised adults."
    )
    comparison = source

    highlighted = highlight_phrases(source, comparison)

    assert (
        "<mark>Vaccination is recommended for those over 65 and/or immunocompromised adults.</mark>"
        in highlighted
    )


def test_highlight_phrases_allows_whitespace_around_slash():
    source = "Vaccination is recommended for those over 65 and / or immunocompromised adults."
    comparison = (
        "Vaccination is recommended for those over 65 and/or immunocompromised adults."
    )

    highlighted = highlight_phrases(source, comparison)

    assert (
        "<mark>Vaccination is recommended for those over 65 and / or immunocompromised adults.</mark>"
        in highlighted
    )
