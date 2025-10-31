from query_data import query_rag


def test_overview_services():
    assert assert_with_grade(
        question="In breve, che servizi offre Seeweb?",
        expected_keywords=["cloud", "hosting", "vps"],
        min_score=0.6,
    )


def test_cloud_managed():
    assert assert_with_grade(
        question="Quali servizi cloud gestiti offre Seeweb?",
        expected_keywords=["cloud", "vm", "scalabile"],
        min_score=0.6,
    )


def test_storage_backup():
    assert assert_with_grade(
        question="Quali opzioni di storage e backup sono disponibili?",
        expected_keywords=["storage", "backup"],
        min_score=0.6,
    )


def test_network_dns_cdn():
    assert assert_with_grade(
        question="Offrite servizi di rete come CDN o DNS gestito?",
        expected_keywords=["cdn", "dns"],
        min_score=0.6,
    )


def test_support_contact():
    assert assert_with_grade(
        question="Come posso contattare il supporto Seeweb?",
        expected_keywords=["supporto", "assistenza"],
        min_score=0.5,
    )


def grade_response(response_text: str, expected_keywords: list[str]):
    text = response_text.lower()
    expected = [k.lower() for k in expected_keywords]
    present = [k for k in expected if k in text]
    missing = [k for k in expected if k not in text]
    precision = (len(present) / len(expected)) if expected else 1.0
    recall = precision  # same set makes sense for simple keyword check
    f1 = (2 * precision * recall / (precision + recall)) if precision else 0.0
    return {
        "present": present,
        "missing": missing,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "score": precision,
    }


def format_eval_table(question: str, response_text: str, evald: dict):
    lines = []
    lines.append("| Campo | Valore |")
    lines.append("|---|---|")
    lines.append(f"| Domanda | {question} |")
    lines.append(f"| Score | {evald['score']:.2f} |")
    lines.append(f"| Precision | {evald['precision']:.2f} |")
    lines.append(f"| Recall | {evald['recall']:.2f} |")
    lines.append(f"| F1 | {evald['f1']:.2f} |")
    pres = ", ".join(evald["present"]) or "-"
    miss = ", ".join(evald["missing"]) or "-"
    lines.append(f"| Presenti | {pres} |")
    lines.append(f"| Mancanti | {miss} |")
    lines.append("\nDettaglio risposta:\n")
    lines.append(response_text)
    return "\n".join(lines)


def assert_with_grade(
    question: str, expected_keywords: list[str], min_score: float
):
    result = query_rag(question)
    response_text = result['answer']
    evald = grade_response(response_text, expected_keywords)
    table = format_eval_table(question, response_text, evald)
    print(table)
    return evald["score"] >= min_score
