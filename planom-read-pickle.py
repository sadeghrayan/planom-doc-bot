import pickle

def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

if __name__ == "__main__":
    # Load data from the pickle file
    scraped_data = load_data_from_pickle('scraped_data10.pickle')

    print("Scraped data:")
    print(scraped_data)
