import yaml


def generate_overview():
    with open("meta.yml", "r") as f:
        members = yaml.safe_load(f)

    if not (isinstance(members, dict) and "members" in members):
        raise ValueError('Malformed meta.yml file, expected top-level "members" key')

    print('<div class="member-list">')
    for member in members["members"]:
        print(
            f"""<div class="member-item">
            <div class="member-photo"><img src="{member['photo']}"/></div>
            <div class="member-info">
                <div class="member-name">{member['name']}</div>
                <div class="member-topic">{member['topic']}</div>
            </div>
        </div>"""
        )
    print("</div>")


if __name__ == "__main__":
    import sys

    if "list" in sys.argv:
        generate_overview()
    else:
        print(f"unknown command: {sys.argv}")
