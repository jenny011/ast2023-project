def extract_queries(fname):
    queries = []
    with open(fname, 'r') as f:
        query = ""
        for i, line in enumerate(f):
            line = line.strip()
            query += line
            query += ' '
            if len(line) > 1 and line[-1] == ';':
                queries.append(query)
                query = ""
    return queries

