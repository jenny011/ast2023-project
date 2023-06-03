def extract_queries(fname):
    is_dml = True
    found_dml = False
    dml = []
    queries = []
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            if line[:2] == "--":
                continue
            if is_dml and "--" in line:
                found_dml = True
            if is_dml and found_dml and "--" not in line:
                is_dml = False

            line = line.strip()
            lines = line.split(";")
            for j, l in enumerate(lines):
                lines[j] = lines[j].strip()
                lines[j] = lines[j] + ";"
            for l in lines:
                if l[:2] == "--":
                    continue
                if len(l) > 1 and l[-1] == ';':
                    if is_dml:
                        dml.append(l)
                    else:
                        queries.append(l)
    return dml, queries

