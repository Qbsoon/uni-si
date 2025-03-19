import pandas as pd
import rdflib

#Wymagana zmiana do zachowania formatu oryginalnego to dodanie w rdf_to_csv index=False w .to_csv(), aby wynikowy csv nie miał zapisanych indeksów, tak samo jak oryginał.

dmap = {"cap-diameter": rdflib.XSD.int, "cap-shape": rdflib.XSD.int, "gill-attachment": rdflib.XSD.int, "gill-color": rdflib.XSD.int, "stem-height": rdflib.XSD.float, "stem-width": rdflib.XSD.int, "stem-color": rdflib.XSD.int, "season": rdflib.XSD.float, "class": rdflib.XSD.int}

def csv_to_rdf(csv_file, rdf_file, dtype_mapping=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Create an RDF graph
    g = rdflib.Graph()

    # Define a base URI for our RDF graph
    base_uri = rdflib.URIRef("http://example.org/")

    # Iterate over the DataFrame and create RDF triples
    for i, row in df.iterrows():
        row_uri = rdflib.URIRef(f"{base_uri}row{i}")
        for column in df.columns:
            predicate = rdflib.URIRef(f"{base_uri}{column}")
            if column in dtype_mapping:
                object_value = rdflib.Literal(row[column], datatype=dtype_mapping[column])
            else:
                print("type missing in map")
                object_value = rdflib.Literal(row[column])
            g.add((row_uri, predicate, object_value))

    # Serialize the RDF graph to a file (Turtle format)
    g.serialize(destination=rdf_file, format="turtle")
    print(f"RDF graph has been saved to {rdf_file}")


def rdf_to_csv(rdf_file, csv_file):
    # Create an RDF graph and parse the RDF file
    g = rdflib.Graph()
    g.parse(rdf_file, format="turtle")

    # Initialize a dictionary to hold rows for the CSV
    rows = {}

    # Iterate over the RDF triples to build the CSV structure
    for subject, predicate, obj in g:
        if isinstance(subject, rdflib.URIRef) and isinstance(predicate, rdflib.URIRef):
            # Extract the row index from the subject URI (e.g., "row0", "row1", ...)
            row_index = str(subject).split('/')[-1]
            column_name = str(predicate).split('/')[-1]

            # Initialize the row if it doesn't exist
            if row_index not in rows:
                rows[row_index] = {}

            # Add the object value to the corresponding row and column
            rows[row_index][column_name] = obj

    # Convert the dictionary of rows into a DataFrame
    df = pd.DataFrame.from_dict(rows, orient='index')
    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)
    print(f"CSV file has been saved to {csv_file}")


csv_to_rdf('mushroom_cleaned.csv', 'mushroom.ttl', dmap)

rdf_to_csv('mushroom.ttl', 'mushroom_rdf.csv')