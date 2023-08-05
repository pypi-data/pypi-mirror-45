def verbose_results(results):
    text = ""
    for (source, amount, destination) in results:
        text += f"{source} → {destination}: {amount}\n"
    return text
