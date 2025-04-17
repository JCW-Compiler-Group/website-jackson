import yaml


def highlight_authors(authors: list[str]):
    for author in authors:
        if author == "Jackson Woodruff":
            yield "<u>Jackson Woodruff</u>"
        else:
            yield author


def generate_html_list_by_year(publications):
    current_year = None
    for pub in sorted(publications, key=lambda x: x.get("year", 0), reverse=True):
        year = pub.get("year", "Unknown")

        # If we're at a new year, print a heading
        if year != current_year:
            if current_year is not None:
                yield "</ul>\n"  # Close the previous year's list
            yield f"<h2>{year}</h2>\n"
            yield "<ul>\n"  # Start a new list for the year
            current_year = year

        authors = ", ".join(highlight_authors(pub["authors"]))
        title = pub["name"]
        venue = pub["venue"]
        links = ", ".join(
            [
                f'<a href="{url}" target="_blank">{link_type}</a>'
                for link_type, url in pub.get("links", {}).items()
            ]
        )

        # Include notes and awards if they exist
        notes = (
            f" <span class='paper-notes'>({' '.join(pub['notes'])})</span>"
            if "notes" in pub
            else ""
        )
        awards = (
            f" <span class='paper-awards'>{', '.join(pub['awards'])}</span>"
            if "awards" in pub
            else ""
        )

        yield f'<li class="paper-item"><div class="paper-title">{title}<span class="paper-venue">{venue}</span></div> <div class="paper-authors">{authors}</div> <div>{notes}{awards}</div>{links}</li>\n'

    yield "</ul>\n"  # Close the last year's list


if __name__ == "__main__":
    with open("meta.yml", "r") as f:
        meta = yaml.safe_load(f)

    if not (isinstance(meta, dict) and "publications" in meta):
        raise ValueError('Malformed meta.yml file, expected top-level "members" key')

    print("".join(generate_html_list_by_year(meta["publications"])))
