import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
import unicodedata

def clean_text(text):
    """
    Remplace les caractères non-latin1 par des équivalents simples.
    """
    text = unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    return text

BASE_URL = "https://assistance.free.fr/articles/{}"
START_ID = 1
END_ID = 2000
SLEEP_SECONDS = 1
OUTPUT_PDF = "free_assistance_articles.pdf"


def detect_variant(soup: BeautifulSoup):
    """Variant detection disabled - always returns None."""
    return None


def fetch_article(article_id):
    """
    Tente de récupérer le titre d'un article donné par son ID.
    Retourne (titre, url) si succès, sinon None.
    """
    url = BASE_URL.format(article_id)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        # Recherche dynamique du titre
        title = None
        if soup.h1 and soup.h1.get_text(strip=True):
            title = soup.h1.get_text(strip=True)
        elif soup.title and soup.title.get_text(strip=True):
            title = soup.title.get_text(strip=True)
        else:
            # Recherche d'autres balises titres
            for tag in ["h2", "h3"]:
                t = soup.find(tag)
                if t and t.get_text(strip=True):
                    title = t.get_text(strip=True)
                    break
        if title and len(title) > 3:
            return (title, url)
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        # Ignore uniquement les erreurs réseau ou de timeout
        print(f"[!!] Erreur réseau pour l'article {article_id}: {e}")
    return None


def scrape_articles(start_id=START_ID, end_id=END_ID):
    """
    Parcourt les articles et retourne une liste de tuples (titre, url).
    """
    articles = []
    for article_id in range(start_id, end_id + 1):
        result = fetch_article(article_id)
        if result:
            title, url = result
            print(f"[OK] {article_id}: {title}")
            articles.append((title, url))
        else:
            print(f"[--] {article_id}: Not found or no title.")
        time.sleep(SLEEP_SECONDS)
    return articles


def generate_pdf(articles, output_file=OUTPUT_PDF):
    """
    Génère un PDF listant tous les articles trouvés.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for idx, (title, url) in enumerate(articles, 1):
        # Écrit le titre comme texte cliquable menant à l'URL
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 255)
        # Affiche le titre (et son index) comme lien vers l'article
        pdf.write(8, f"{idx}. {clean_text(title)}", link=url)
        pdf.ln(8)
        pdf.set_text_color(0, 0, 0)
        # Ajoute l'URL en petit (optionnel)
        pdf.set_font("Arial", size=8)
        pdf.multi_cell(0, 5, url)
        pdf.ln(2)
    pdf.output(output_file)
    print(f"PDF généré : {output_file}")


def main():
    print("Scraping des articles Free Assistance...")
    articles = scrape_articles()
    if articles:
        generate_pdf(articles)
    else:
        print("Aucun article valide trouvé.")


if __name__ == "__main__":
    main()
