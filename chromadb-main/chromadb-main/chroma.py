import chromadb
import requests
import time


#7OOYZDM6H53OW8L8 : 1st
#YQBAK9042LP6L4W6 : 2nd
#E2BGLXNMJ7P0G7NS : 3rd
#use vpn to switch between servers and ip addresses.

def add_ticker_to_chroma(ticker: str) -> None:
    transcript_dict: dict = {}
    year = 2025
    quarter = 4

    potential_id = f"{ticker}_0"
    
    if potential_id in collection.get(ids=[potential_id])["ids"]:
        print(f"{ticker} earnings call already exists in ChromaDB.")
        return None

    while len(transcript_dict) == 0 and transcript_dict is not None:

        query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={year}Q{quarter}&apikey=KCMNKODOBZ1L8YW7'
        response = requests.get(query_url)

        if response.status_code != 200:
            print(f"Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")

        else:
            data: dict = response.json()
            try:
                transcript_dict: dict = data["transcript"]

                if len(transcript_dict) == 0:
                    quarter -= 1
                    if quarter == 0:
                        quarter = 4
                        year -= 1

                    if year == 2024 and quarter < 3:
                        print(f"No transcript found for {ticker} in any recent quarter.")
                        return None
            
            except Exception as e:
                print(f"No transcript found for {ticker}. Probably API rate limit exceeded.")
                return None
            
    documents = []
    metadatas = []
    ids = []

    for i, entry in enumerate(transcript_dict):
        speaker: str = entry["speaker"]
        speaker_title: str = entry["title"]
        content: str = entry["content"]
        sentiment: str = entry["sentiment"]

        documents.append(content)
        metadatas.append({"speaker": speaker, "title": speaker_title, "sentiment": sentiment})
        ids.append(f"{ticker}_{i}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Added {len(documents)} entries to ChromaDB for {ticker} in quarter {year}Q{quarter}.")

    return None
            

    

if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chroma")
    collection = client.get_collection("database")

    for col in client.list_collections():
        print(col)

    tickers = ["IBM", "ORCL", "XOM", "JPM", "CSCO",
               "GOOGL", "RACE", "WMT", "MSFT", "INTC",
               "AVGO", "TSLA", "NVDA", "AMD", "META", "COST",
               "PEP", "AMZN", "AAPL"]

    # tickers = ["NFLX"]

    # allIDS = collection.get()["ids"]

    # ticker_ids = [id for id in allIDS if id.split("_")[0] in tickers]
    # tickers = []
    # for id in ticker_ids:
    #     tickers.append(id.split("_")[0])


    # for i, ticker in enumerate(tickers):
    #     try:
    #         collec = client.get_or_create_collection(f"{ticker}")
    #         print("")
    #         collec.add(
    #             documents=[collection.get(ids=[ticker_ids[i]])["documents"][0]],
    #             metadatas=[collection.get(ids=[ticker_ids[i]])["metadatas"][0]],
    #             ids=[ticker_ids[i]]
    #         )
    #         print(f"Added {ticker_ids[i]} to {ticker} collection. {i}")
    #     except Exception as e:
    #         print(f"Failed to add {ticker_ids[i]} to {ticker} collection. {e}")
    #         continue

