def clip(text:str, max_length:'int > 0'=80) -> str:
    end = None
    if len(text) > max_length:
        space_before = text.rfind(' ', 0, max_length)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.find(' ', max_length)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()
