from Bio import Entrez


def handler(event, context):
    """AWS Lambda function to search PubMed Central and get article details"""

    search_term = event["searchTerm"]

    # Set up Entrez email
    Entrez.email = "your_email@example.com"

    # Search PubMed Central
    handle = Entrez.esearch(db="pmc", term=search_term, retmax=10)
    record = Entrez.read(handle)
    id_list = record["IdList"]

    if not id_list:
        return {"articles": []}

    # Get article details
    handle = Entrez.efetch(db="pmc", id=id_list, rettype="xml", retmode="xml")
    article_details = Entrez.read(handle)

    # Extract article titles
    result_list = [
        article["front"]["article-meta"]["title-group"]["article-title"]
        for article in article_details
    ]

    return {
        "statusCode": 200,
        "body": result_list,
    }
