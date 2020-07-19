import json
from typing import List

from elasticsearch import Elasticsearch
from elasticsearch.client.sql import SqlClient
from elasticsearch.helpers import scan

if __name__ == '__main__':
    es = Elasticsearch()
    sql = SqlClient(es)

    # Use the direct counting API

    response = es.count(
        index='shakespeare'
    )

    print(f'How many lines are in '
          f'Shakespeare\'s plays: {response["count"]}')

    # Use an SQL query with a COUNT function
    
    response = sql.query(
        body={
            "query": "SELECT COUNT(*) FROM shakespeare"
        }
    )
    print(f'Again, as SQL: {response["rows"][0][0]}')

    # Manually count in python (less recommended)

    response = scan(  # https://elasticsearch-py.readthedocs.io/en/master/helpers.html#scan
        client=es,
        index='shakespeare',
        query={
            'size': 0
        }
    )

    print(f'Again, using scan(): {len([row for row in response])}')  # low performance

    # Get the top 3 longest plays
    
    response = es.search(
        index='shakespeare',
        body={
            'size': 0,
            'aggs': {
                'unique_play_name': {
                    'terms': {
                        'field': 'play_name',
                        'size': 3
                    }
                }
            }
        }
    )

    buckets: List[dict] = response['aggregations']['unique_play_name']['buckets']
    print(f'Which are Shakespeare\'s longest plays '
          f'(top 3): {[play["key"] for play in buckets]}')

    # Now using an SQL query

    response = sql.query(
        body={
            "query": "SELECT play_name FROM shakespeare GROUP BY play_name ORDER BY Count(*) DESC"
        }
    )
    print(f'Again, as SQL: {response["rows"][:3]}')

    # Get full line information regarding the famous line: "To be, or not to be: that is the question"

    response = es.search(
        index='shakespeare',
        body={
            'size': 1,
            'query': {
                'match_phrase': {
                    'text_entry': 'To be, or not to be: that is the question'
                }
            }
        }
    )

    print(f'The line number where Hamlet says '
          f'"To be, or not to be: that is the question" '
          f'(full line information): {json.dumps(response["hits"]["hits"][0], indent=2)}')

    # Find the top 3 characters with most lines
    
    response = es.search(
        index='shakespeare',
        body={
            'size': 0,
            'aggs': {
                'unique_play_name': {
                    'terms': {
                        'field': 'speaker',
                        'size': 3
                    }
                }
            }
        }
    )

    buckets: List[dict] = response['aggregations']['unique_play_name']['buckets']
    characters = [character["key"] for character in buckets]
    print(f'The 3 most talkative characters in '
          f'Shakespeare\'s plays: {characters}')

    # Find all of the plays of the character with the most lines (found in the query above)

    response = es.search(
        index='shakespeare',
        body={
            'size': 0,
            'query': {
                'term': {
                    'speaker': {
                        'value': characters[0]
                    }
                }
            },
            'aggs': {
                'unique_play_name': {
                    'terms': {
                        'field': 'play_name'
                    }
                }
            }
        }
    )

    buckets: List[dict] = response['aggregations']['unique_play_name']['buckets']
    print(f'The most talkative character ({characters[0]}) was in '
          f'Shakespeare\'s plays: {[play["key"] for play in buckets]}')
