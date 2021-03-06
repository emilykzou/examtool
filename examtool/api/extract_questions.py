from examtool.api.scramble import is_compressible_group


def extract_questions(exam, extract_public_bool: bool = True, top_level: bool = True, include_groups: bool = False):
    def group_questions(group):
        out = _group_questions(group)
        try:
            first = next(out)
        except StopIteration:
            return
        first["text"] = group["name"] + "\n\n" + group["text"] + "\n\n" + first["text"]
        yield first
        yield from out

    def _group_questions(group):
        for i, element in enumerate(group.get("elements", []) + group.get("questions", [])):
            element["index"] = f"{group.get('index', 0)}{i + 1}."
            if element.get("type") == "group":
                if include_groups:
                    yield element
                out = group_questions(element)
                yield from out
            else:
                yield element

    if extract_public_bool:
        yield from extract_public(exam)
    if top_level:
        for i, group in enumerate(exam["groups"]):
            group["index"] = str(i + 1) + "."
            if include_groups:
                yield group
            yield from group_questions(group)
    else:
        yield from group_questions(exam)


def extract_public(exam):
    if exam.get("public"):
        yield from extract_questions(exam["public"], extract_public_bool=False, top_level=False)


def extract_groups(group):
    for g in group["groups"]:
        if is_compressible_group(g):
            for g2 in g["elements"]:
                yield g2
        else:
            yield g
