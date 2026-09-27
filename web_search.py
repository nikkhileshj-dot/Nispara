from importlib import import_module


def _get_ddgs():
    try:
        return import_module("ddgs").DDGS
    except (ImportError, AttributeError) as exc:
        raise RuntimeError(
            "The 'ddgs' package is required. Install it with: pip install ddgs"
        ) from exc


def search_web(query, max_results=5):

    if not query or not query.strip():
        return []

    try:
        results = []

        with _get_ddgs()() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                title = result.get("title", "")
                body = result.get("body", "")
                url = result.get("href", "")

                if title and body:
                    results.append({
                        "title": title,
                        "body": body,
                        "url": url
                    })

        return results

    except Exception as e:

        print(
            "❌ Web search error:",
            type(e).__name__,
            "-",
            e
        )

        return []