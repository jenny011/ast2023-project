def extract_queries(fname):
    dml = []
    queries = []
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            if line[:2] == "--":
                continue

            line = line.strip()
            lines = line.split(";")
            for j, l in enumerate(lines):
                lines[j] = lines[j].strip()
                lines[j] = lines[j] + ";"
            for l in lines:
                if l[:2] == "--":
                    continue
                if len(l) > 1 and l[-1] == ';':
                    if "--" in line:
                        dml.append(l)
                    else:
                        queries.append(l)
    return queries

