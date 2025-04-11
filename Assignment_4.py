#!/usr/bin/env python3
import argparse
import os
import sys

from openai import OpenAI

client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable

def get_text_from_url(url):
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Asenna 'requests' ja 'beautifulsoup4'-kirjastot, jotta HTML-sivujen käsittely onnistuu.")
        sys.exit(1)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Virhe haettaessa URL-osoitetta {url}: {response.status_code}")
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    # Palautetaan sivun teksti, rivinvaihdot erotellaan
    return soup.get_text(separator="\n")

def get_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_text_from_csv(filepath):
    import csv
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(", ".join(row))
    return "\n".join(rows)

def get_text_from_docx(filepath):
    try:
        import docx
    except ImportError:
        print("Asenna 'python-docx'-kirjasto, jotta .docx-tiedostojen käsittely onnistuu.")
        sys.exit(1)
    doc = docx.Document(filepath)
    paragraphs = [para.text for para in doc.paragraphs]
    return "\n".join(paragraphs)

def get_text_from_pdf(filepath):
    try:
        import PyPDF2
    except ImportError:
        print("Asenna 'PyPDF2'-kirjasto, jotta PDF-tiedostojen käsittely onnistuu.")
        sys.exit(1)
    text = []
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text.append(extracted)
    return "\n".join(text)

def get_content(source):
    """Päätellään lähteen tyyppi ja palautetaan sisältöä vastaava teksti."""
    if source.startswith("http://") or source.startswith("https://"):
        return get_text_from_url(source)
    elif os.path.isfile(source):
        ext = os.path.splitext(source)[1].lower()
        if ext == ".txt":
            return get_text_from_txt(source)
        elif ext == ".csv":
            return get_text_from_csv(source)
        elif ext == ".docx":
            return get_text_from_docx(source)
        elif ext == ".pdf":
            return get_text_from_pdf(source)
        else:
            # Jos tiedostopääte ei ole tunnistettu, kokeillaan lukea se tekstinä
            return get_text_from_txt(source)
    else:
        print(f"Lähdettä '{source}' ei löydy tai se ei ole kelvollinen URL.")
        return ""

def dummy_llm_process(content, query, include_citations=False, include_source=False):
    # Create prompt based on whether a custom query was provided
    if not query:
        prompt = f"Tiivistä seuraava sisältö lyhyesti:\n\n{content}"
    else:
        prompt = f"{query}\n\nSisältö:\n{content}"

    try:
        # Call OpenAI API to process the content
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "Olet avulias avustaja asiakirjojen käsittelyssä."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000  # Limit response length
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Yksinkertainen komentorivityökalu teksti-, html-, CSV-, .docx- ja PDF-tiedostojen yhteenvetoon.",
        usage="""%(prog)s [optiot] arg1 [arg2 ...]
Esimerkit:
  python %(prog)s -r .\\little_red_cap.txt
  python %(prog)s -r "https://www.bbc.com/news/articles/cj620yl96kzo"
  python %(prog)s -r .\\plato_apology_pg1656.txt -f plato.txt
  python %(prog)s -r .\\BashTutorial.docx -q "luettelo kaikki tässä asiakirjassa löytyvät bash-komennot"
"""
    )
    # Positiiviset argumentit: yksi tai useampi lähde
    parser.add_argument("sources", nargs="+", help="Tiedoston nimi, kelvollinen html URL, .docx, PDF- tai CSV-tiedosto")
    parser.add_argument("-f", "--file", metavar="TIEDOSTONIMI", help="Kirjoita tuloste tiedostoon TIEDOSTONIMI")
    parser.add_argument("-c", "--sitaatit", action="store_true", help="Lisää mahdolliset viittaukset (sitaatit) tulosteeseen")
    parser.add_argument("-q", "--query", metavar="QUERY", help="Kehote, joka annetaan kielimallille (oletuksena yhteenveto)")
    # -r: nollaa tiedoston sisältö, jos tulosteen ohjaus on tiedostoon; muussa tapauksessa lisää olemassa olevaan
    parser.add_argument("-r", "--reset", action="store_true", help="Nollaa tulostetiedoston sisältö, jos tiedostoon kirjoitetaan")
    parser.add_argument("-v", "--verbose", action="store_true", help="Tulosta syötteiden lähdetiedot tulosteeseen")
    args = parser.parse_args()

    # Kootaan kaikkien lähteiden sisältö yhteen
    aggregated_content = ""
    for source in args.sources:
        content = get_content(source)
        if args.verbose:
            print(source)
            aggregated_content += f"\n\n--- Sisältö lähteestä: {source} ---\n\n"
        aggregated_content += content

    # print(aggregated_content)
    # Kutsutaan simuloivaa LLM-käsittelyfunktiota
    output = dummy_llm_process(aggregated_content, args.query, include_citations=args.sitaatit, include_source=args.verbose)

    # Tulostetaan joko stdout:iin tai kirjoitetaan tiedostoon
    if args.file:
        mode = "w" if args.reset else "a"
        with open(args.file, mode, encoding="utf-8") as f:
            f.write(output)
        print(f"Tuloste kirjoitettu tiedostoon: {args.file}")
    else:
        print(output)

if __name__ == "__main__":
    main()
