from postgresAPI import PostgresAPI
import argparse
import pandas as pd
import sys
import os

def main(args):
    # Create a postgresAPI object
    db = PostgresAPI(dbname=args.database, user=args.user, password=args.password, host=args.host, port=args.port)

    positive_triples = db.get_samples(label = "Positive", project_name = "triple classification")
    negative_triples = db.get_samples(label = "Negative", project_name = "triple classification")

    print("Positive triples: ", len(positive_triples))
    print("Negative triples: ", len(negative_triples))

    # Create a new dataset
    dataset_name = "triple classification"
    dataset_description = "Dataset for triple classification"
    full_dataset = pd.concat([positive_triples, negative_triples])

    # Create a test set with 10% of the data
    test_set = full_dataset.sample(frac=0.1, random_state=42)
    # Remove the test set from the full dataset
    full_dataset = full_dataset.drop(test_set.index)

    # Create a validation set with 10% of the data but balanced distribution
    n = min(len(positive_triples), len(negative_triples))
    p = int(n * 0.1)
    pos_set = full_dataset[full_dataset['label'] == 'Positive'].sample(n=p, random_state=42)
    neg_set = full_dataset[full_dataset['label'] == 'Negative'].sample(n=p, random_state=42)

    validation_set = pd.concat([pos_set, neg_set])

    # Remove the validation set from the full dataset
    full_dataset = full_dataset.drop(validation_set.index)

    # Create a training set with the remaining data
    training_set = full_dataset

    # save the datasets as csv files
    # create empty datasets if they don't exist
    if not os.path.exists(os.path.join(args.output, args.dataset)):
        os.makedirs(os.path.join(args.output, args.dataset))
    
    training_set.to_csv(os.path.join(args.output, args.dataset, "training_set.csv"), index=False)
    validation_set.to_csv(os.path.join(args.output, args.dataset, "validation_set.csv"), index=False)
    test_set.to_csv(os.path.join(args.output, args.dataset, "test_set.csv"), index=False)
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=str, default="5432")
    parser.add_argument("--user", type=str, default="postgres")
    parser.add_argument("--password", type=str, default="postgres")
    parser.add_argument("--database", type=str, default="postgres")
    parser.add_argument("--dataset", type=str, default="triple")
    parser.add_argument("--output", type=str, default="data/triple/")
    args = parser.parse_args()
    main(args)