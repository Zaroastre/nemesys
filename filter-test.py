from time import perf_counter;

def test_filter_by_name():
    usernames: list[str] = ["Pierre", "Thierry", "Aurélie", "Hermine", "Nicolas", "Nicolas", "Clélia", "JF", "Thibaud", "Mathieu", "Samuel"];
    
    start = perf_counter()
    alias_end_by_e: list[str] = [];
    for alias in usernames:
        if (alias.endswith("e")):
            alias_end_by_e.append(alias);

    start = perf_counter();
    alias_end_by_d = [alias for alias in usernames if alias.endswith("e")];
    print(round(perf_counter() - start, 8));

if (__name__ == "__main__"):
    test_filter_by_name();