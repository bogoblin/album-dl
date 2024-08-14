def best_suffix(strings: list[str]):
    suffixes = dict()
    for string in strings:
        for offset in range(len(string)):
            suffix = string[offset:]
            current_count = suffixes.get(suffix) or 0
            suffixes[suffix] = current_count + 1

    suffix_scores = {suffix: len(suffix) * count for suffix, count in suffixes.items() if count > 1}
    try:
        return max(suffix_scores, key=suffix_scores.get)
    except ValueError:
        return ''