def converter_google_sheets(link):
    if "docs.google.com/spreadsheets" not in link:
        raise Exception("O link inserido não é um Google-Sheets")

    link_csv = link.replace("/edit?", "/export?format=csv&")

    return link_csv