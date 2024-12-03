# Tool-OSINT-Linkedin-Scraper
Scraper Linkedin che genera automaticamente una lista mail di dipendenti di una determinata azienda.

import argparse
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def estrai_nome_azienda_da_dominio(dominio):
    nome_azienda = dominio.split('.')[0]
    print(f"Nome azienda estratto dal dominio {dominio}: {nome_azienda}")
    return nome_azienda

def costruisci_query(dominio, scan_mode="fast"):
    nome_azienda = estrai_nome_azienda_da_dominio(dominio)

    if scan_mode == "fast":
        queries = [
            f"site:linkedin.com/in \"{nome_azienda}\"",
            f"site:linkedin.com/in \"lavoro presso {nome_azienda}\"",
        ]
    elif scan_mode == "full":
        queries = [
            f"site:linkedin.com/in \"{nome_azienda}\"",
            f"site:linkedin.com/in \"lavoro presso {nome_azienda}\"",
            f"site:linkedin.com/in \"{nome_azienda} team\"",
            f"site:linkedin.com/in \"{nome_azienda} manager\"",
            f"site:linkedin.com/in \"{nome_azienda} developer\"",
            f"site:linkedin.com/in \"{nome_azienda} engineer\"",
            f"site:linkedin.com/in \"{nome_azienda} marketing\"",
            f"site:linkedin.com/in \"{nome_azienda} sales\"",
            f"site:linkedin.com/in \"{nome_azienda} human resources\"",
            f"site:linkedin.com/in \"progetto presso {nome_azienda}\"",
            f"site:linkedin.com/in \"team di {nome_azienda}\"",
            f"site:linkedin.com/in \"sede di {nome_azienda}\"",
        ]
    else:
        raise ValueError("Modalità di scansione non valida. Usa 'fast' o 'full'.")

    print(f"Query generate per il dominio {dominio} (modalità {scan_mode}): {queries}")
    return queries

def estrai_nomi_cognomi(link):
    link = re.sub(r"https?://[a-z]{2,3}\.linkedin\.com/in/", "", link)
    parts = link.split('-')
    if len(parts) >= 2:
        nome = parts[0]
        cognome = parts[1]
        print(f"Estratto nome: {nome}, cognome: {cognome} da {link}")
        return f"{nome}.{cognome}@".lower()
    print(f"Impossibile estrarre nome e cognome da {link}")
    return None

def cerca_duckduckgo(query, max_pages=10):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    print(f"Avviando WebDriver per la query: {query}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://duckduckgo.com/")

    try:
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        links = []
        current_page = 0

        while current_page < max_pages:
            print(f"Raccogliendo risultati dalla pagina {current_page + 1}...")
            results = driver.find_elements(By.XPATH, "//a[@href]")
            for result in results:
                link = result.get_attribute("href")
                if "linkedin.com/in" in link:
                    links.append(link)

            current_page += 1
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "button#more-results")
                next_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"Fine delle pagine o errore: {e}")
                break

        print(f"Link raccolti: {links}")
        return links

    except Exception as e:
        print(f"Errore durante l'esecuzione di cerca_duckduckgo: {e}")
        return []

    finally:
        driver.quit()

def cerca_con_query_multiple(dominio, max_pages=5, scan_mode="fast"):
    queries = costruisci_query(dominio, scan_mode)
    tutti_i_risultati = set()

    for query in queries:
        print(f"\nEseguendo ricerca con query: {query}")
        try:
            risultati = cerca_duckduckgo(query, max_pages)
            if risultati:
                print(f"Risultati trovati per la query: {risultati}")
                tutti_i_risultati.update(risultati)

            delay = random.uniform(4, 8)
            print(f"Attesa di {delay:.2f} secondi prima della prossima query...")
            time.sleep(delay)

        except Exception as e:
            print(f"Errore durante la ricerca con query '{query}': {e}")

    print(f"Tutti i risultati trovati: {list(tutti_i_risultati)}")
    return list(tutti_i_risultati)

def genera_mail(nome_completo, dominio):
    email = f"{nome_completo}{dominio}".lower()
    print(f"Generata email: {email}")
    return email

def salva_email_in_file(profili, dominio):
    print(f"Salvando email nel file...")
    try:
        with open("email_dipendenti.txt", "w") as file:
            for profilo in profili:
                nome_completo = estrai_nomi_cognomi(profilo)
                if nome_completo:
                    email = genera_mail(nome_completo, dominio)
                    file.write(f"{email}\n")
                    print(f"Email salvata: {email}")
    except Exception as e:
        print(f"Errore durante il salvataggio delle email: {e}")

def main():
    parser = argparse.ArgumentParser(description="Ricerca profili LinkedIn e genera email associate.")
    parser.add_argument("-d", "--dominio", required=True, help="Dominio dell'azienda (es. nomeazienda.com)")
    parser.add_argument("-s", "--scan", choices=["fast", "full"], default="fast", help="Modalità di scansione: 'fast' o 'full' (default: fast)")
    args = parser.parse_args()

    dominio = args.dominio
    scan_mode = args.scan

    print(f"Cercando profili LinkedIn per il dominio: {dominio} (modalità {scan_mode})")

    try:
        profili = cerca_con_query_multiple(dominio, max_pages=5, scan_mode=scan_mode)

        if not profili:
            print("\nNessun profilo trovato.")
        else:
            print("\nProfili trovati e email generate:")
            salva_email_in_file(profili, dominio)

    except Exception as e:
        print(f"Errore durante l'esecuzione principale: {e}")

if __name__ == "__main__":
    main()
