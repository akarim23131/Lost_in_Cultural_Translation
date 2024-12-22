import re
import string
import json

def build_entities_map(entities_identified_list):
    entities_map = {}
    for line in entities_identified_list:
        if ":" in line:
            category, values = line.split(":", 1)
            category = category.strip()
            # Split by comma for multiple entities
            entity_list = [v.strip() for v in values.split(",") if v.strip()]
            entities_map[category] = entity_list
    return entities_map

def is_placeholder(tok):
    return tok.startswith("{") and tok.endswith("}")

def placeholder_category(tok):
    ph_type = re.findall(r"\{([^}]+)\}", tok)
    return ph_type[0] if ph_type else None

def clean_token(tok):
    if is_placeholder(tok):
        return tok
    punctuation_to_remove = string.punctuation.replace("'", "")
    return tok.strip(punctuation_to_remove)

def regex_tokenize(text):
    pattern = r"\{[^}]+\}|[A-Za-z0-9']+|\S"
    return re.findall(pattern, text)

def tokens_match(s, o, is_placeholder_func, match_score, mismatch_score, placeholder_match_score):
    if is_placeholder_func(s):
        return placeholder_match_score
    return match_score if s.lower() == o.lower() else mismatch_score

def try_fix_possessive(tok, cat, entities_map):
    # If category is "Person name" and token ends with "'s", try removing it
    if cat == "Person name" and tok.lower().endswith("'s"):
        base = tok[:-2] if len(tok) > 2 else tok
        # Check if base is known person name
        if any(base.lower() == e.lower() for e in entities_map.get("Person name", [])):
            return base
    return tok

def try_multi_word_entity(cat, o_i, orig_tokens, entities_map):
    # If there are multi-word entities for this category, try to find them near o_i
    if cat in entities_map:
        multi_ent_list = [e for e in entities_map[cat] if " " in e]
        if not multi_ent_list:
            return None

        search_range = 2
        for ent in multi_ent_list:
            ent_words = ent.split()
            length = len(ent_words)
            start_min = max(0, o_i - search_range)
            end_max = min(len(orig_tokens)-length+1, o_i + search_range + 1)
            for start_idx in range(start_min, end_max):
                segment = orig_tokens[start_idx:start_idx+length]
                if len(segment) == length and all(segment[k].lower() == ent_words[k].lower() for k in range(length)):
                    return " ".join(segment)
    return None

def align_and_map(original_question, symbolic_question, entities_identified):
    entities_map = build_entities_map(entities_identified)

    # Remove "Question:\n" if exists
    symbolic_question = symbolic_question.replace("Question:\n", "")

    orig_raw = regex_tokenize(original_question)
    sym_raw = regex_tokenize(symbolic_question)

    orig_tokens = [clean_token(t) for t in orig_raw if t.strip()]
    sym_tokens = [clean_token(t) for t in sym_raw if t.strip()]

    # Scoring scheme
    match_score = 2
    mismatch_score = -1
    gap_score = -1
    placeholder_match_score = 1

    def is_ph(s):
        return is_placeholder(s)

    n = len(sym_tokens)
    m = len(orig_tokens)
    dp = [[0]*(m+1) for _ in range(n+1)]
    trace = [[None]*(m+1) for _ in range(n+1)]

    # Initialize DP
    for i in range(1, n+1):
        dp[i][0] = dp[i-1][0] + gap_score
        trace[i][0] = ('up', i-1, 0)
    for j in range(1, m+1):
        dp[0][j] = dp[0][j-1] + gap_score
        trace[0][j] = ('left', 0, j-1)

    # Fill DP
    for i in range(1, n+1):
        for j in range(1, m+1):
            s_tok = sym_tokens[i-1]
            o_tok = orig_tokens[j-1]

            diag_score = dp[i-1][j-1] + tokens_match(s_tok, o_tok, is_ph, match_score, mismatch_score, placeholder_match_score)
            up_score = dp[i-1][j] + gap_score
            left_score = dp[i][j-1] + gap_score

            best = diag_score
            direction = ('diag', i-1, j-1)
            if up_score > best:
                best = up_score
                direction = ('up', i-1, j)
            if left_score > best:
                best = left_score
                direction = ('left', i, j-1)

            dp[i][j] = best
            trace[i][j] = direction

    # Trace back
    aligned_pairs = []
    i, j = n, m
    while i > 0 or j > 0:
        dir_type, pi, pj = trace[i][j]
        if dir_type == 'diag':
            aligned_pairs.append((i-1, j-1))
            i, j = pi, pj
        elif dir_type == 'up':
            aligned_pairs.append((i-1, None))
            i, j = pi, pj
        else:
            aligned_pairs.append((None, j-1))
            i, j = pi, pj

    aligned_pairs.reverse()

    placeholder_alignments = []
    for pair in aligned_pairs:
        s_i, o_i = pair
        if s_i is not None and s_i < len(sym_tokens) and is_placeholder(sym_tokens[s_i]):
            if o_i is not None and o_i < len(orig_tokens):
                placeholder_alignments.append((s_i, sym_tokens[s_i], orig_tokens[o_i], o_i))
            else:
                placeholder_alignments.append((s_i, sym_tokens[s_i], "<no token>", None))

    corrected_alignments = []
    for (s_i, ph, ot, o_i) in placeholder_alignments:
        cat = placeholder_category(ph)
        if ot == "<no token>" or o_i is None:
            corrected_alignments.append((s_i, ph, ot))
            continue

        # Fix possessive
        ot_fixed = try_fix_possessive(ot, cat, entities_map)

        # Try multi-word entity
        if cat in entities_map and any(" " in e for e in entities_map[cat]):
            multi_ent = try_multi_word_entity(cat, o_i, orig_tokens, entities_map)
            if multi_ent:
                corrected_alignments.append((s_i, ph, multi_ent))
                continue

        corrected_alignments.append((s_i, ph, ot_fixed))

    return corrected_alignments

def process_questions_in_batches(all_questions, batch_size=100):
    """
    Processes all questions in batches. Each batch of questions is aligned and the results
    are saved into a separate JSON file named 'batch_output_<batch_index>.json'.
    """

    for batch_index in range(0, len(all_questions), batch_size):
        batch = all_questions[batch_index:batch_index+batch_size]
        batch_results = []
        for q in batch:
            original_q = q["question"]
            symbolic_q = q["gsm_symbolic"]
            entities = q["entities_identified"]
            problem_num = q["problem_number"]

            corrected_alignments = align_and_map(original_q, symbolic_q, entities)

            output_entry = {
                "problem_number": problem_num,
                "mappings": [
                    {"index": idx, "placeholder": ph, "entity": ot}
                    for (idx, ph, ot) in corrected_alignments
                ]
            }
            batch_results.append(output_entry)

        filename = f"batch_output_{batch_index // batch_size}.json"
        with open(filename, "w") as f:
            json.dump(batch_results, f, indent=4)

        print(f"Saved batch {batch_index // batch_size} to {filename}")


############################################
# Reading the input file and processing    #
############################################

# Load the questions from an input JSON file. Adjust the path as needed.
with open("input file path", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Now process all the questions in batches of 100 (you can change the batch size if needed)
process_questions_in_batches(all_questions, batch_size=100)
