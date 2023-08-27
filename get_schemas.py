import logging, os, yaml
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


# Initialize the logger
logging.basicConfig(format='%(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fetch_and_save_schemas(config):
    transport = AIOHTTPTransport(
      url=config["API_URL"],
      headers={"X-API-Key": config["API_TOKEN"]}
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    list_schemas = gql(
      """
      query ListSchemas($input: SchemasInput!) {
        schemas(input: $input) {
          edges {
            node {
              name
              description
              spec
            }
          }
        }
      }
      """
    )

    data = client.execute(
      list_schemas,
      variable_values= {
        "input": {}
      }
    )

    # Check if the schemas directory exists, if not, create it
    if not os.path.exists("schemas"):
        os.mkdir("schemas")


    # Loop through each schema and save it as a YAML file
    for edge in data['schemas']['edges']:
      schema = edge['node']
      schema_name = schema['name']
      schema_spec_string = schema['spec'].replace('\\n', '\n')

      # Now, using yaml to beautify the content
      structured_data = yaml.safe_load(schema_spec_string)
      beautified_content = yaml.dump(structured_data, default_flow_style=False, indent=4, allow_unicode=True)

      # Define the file path
      file_path = os.path.join('schemas', f"{schema_name}.yml")

      # Log a message stating the schema file being saved.
      logger.info(f'Saving {schema_name} schema.')

      # Save the beautified YAML string to a .yml file
      with open(file_path, 'w', encoding='utf-8') as f:
          f.write(beautified_content)

    print(f"{len(data['schemas']['edges'])} schemas has been saved.")
    return data['schemas']['edges']


