from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import logging, re


# Initialize the logger
logging.basicConfig(format='%(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fetch_data(sql_query, config):
    # Check and modify the SQL query for LIMIT clause
    if not re.search(r"LIMIT \d+", sql_query, re.IGNORECASE) or int(re.search(r"LIMIT (\d+)", sql_query, re.IGNORECASE).group(1)) > 5:
        sql_query = re.sub(r"LIMIT \d+", "LIMIT 5", sql_query, flags=re.IGNORECASE)

    transport = AIOHTTPTransport(
      url=config["API_URL"],
      headers={"X-API-Key": config["API_TOKEN"]}
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # `IssueQuery` is a nickname for the query. You can fully omit it.
    issue_query = gql(
        """
        mutation IssueQuery($sql: String!) {
            executeDataLakeQuery(input: { sql: $sql }) {
                id
            }
        }
        """
    )

    # `GetQueryResults` is a nickname for the query. You can fully omit it.
    get_query_results = gql(
        """
        query GetQueryResults($id: ID!, $cursor: String) {
            dataLakeQuery(id: $id) {
                message
                status
                results(input: { cursor: $cursor }) {
                    edges {
                        node
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """
    )

    # an accumulator that holds all results that we fetch from all pages
    all_results = []
    # a helper to know when to exit the loop.
    has_more = True
    # the pagination cursor
    cursor = None

    # Issue a Data Lake (Data Explorer) query
    mutation_data = client.execute(
        issue_query,
        variable_values={
            "sql": sql_query
        }
    )

    # Start polling the query until it returns results. From there,
    # keep fetching pages until there are no more left
    while has_more:
        query_data = client.execute(
            get_query_results,
            variable_values = {
                "id": mutation_data["executeDataLakeQuery"]["id"],
                "cursor": cursor
            }
        )
        
        # if it's still running, print a message and keep polling
        if query_data["dataLakeQuery"]["status"] == "running":
            logger.info('Retrieving events from Data Lake...')
        
        # if it's not running & it's not completed, then it's
        # either cancelled or it has errored out. In this case,
        # throw an exception
        if query_data["dataLakeQuery"]["status"] != "succeeded":
            raise Exception(query_data["dataLakeQuery"]["message"])

        all_results.extend([edge["node"] for edge in query_data["dataLakeQuery"]["results"]["edges"]])
        has_more = query_data["dataLakeQuery"]["results"]["pageInfo"]["hasNextPage"]
        cursor = query_data["dataLakeQuery"]["results"]["pageInfo"]["endCursor"]

    return all_results