# Elasticsearch Python Example

This is a simple python script for running simple queries against the example [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) [Shakespeare DB](https://www.elastic.co/guide/en/kibana/7.1/tutorial-load-dataset.html).

Make sure you set up Elasticsearch and load up the example dataset before running this.

## How to run

Just run `run_locally.sh` and you should see something like that:
```
How many lines are in Shakespeare's plays: 111396
Again, as SQL: 111396
Again, using scan(): 111396
Which are Shakespeare's longest plays (top 3): ['Hamlet', 'Coriolanus', 'Cymbeline']
Again, as SQL: [['Hamlet'], ['Coriolanus'], ['Cymbeline']]
The line number where Hamlet says "To be, or not to be: that is the question" (full line information): {
  "_index": "shakespeare",
  "_type": "_doc",
  "_id": "34229",
  "_score": 25.40203,
  "_source": {
    "type": "line",
    "line_id": 34230,
    "play_name": "Hamlet",
    "speech_number": 19,
    "line_number": "3.1.64",
    "speaker": "HAMLET",
    "text_entry": "To be, or not to be: that is the question:"
  }
}
The 3 most talkative characters in Shakespeare's plays: ['GLOUCESTER', 'HAMLET', 'IAGO']
The most talkative character (GLOUCESTER) was in Shakespeare's plays: ['Richard III', 'King Lear', 'Henry VI Part 2', 'Henry VI Part 3', 'Henry VI Part 1', 'Henry V']

```

## Original queries

The following are the original queries implemented here with python.
Once you have the Elasticsearch all set up, you should be able to use
[Kibana](https://www.elastic.co/downloads/kibana) ([Dev Tools](https://www.elastic.co/guide/en/kibana/current/devtools-kibana.html)) - usually found at http://localhost:5601/, to test these queries and make sure the database is set correctly.

```
GET /shakespeare/_count
```
```
GET /shakespeare/_search
{
  "size": 0, 
  "aggs": {
    "unique_play_name": {
      "terms": {
        "field": "play_name",
        "size": 3
      }
    }
  }
}
```
```
GET /shakespeare/_search
{
  "query": {
    "match_phrase": {
      "text_entry": "To be, or not to be: that is the question"
    }
  }
}
```
```
GET /shakespeare/_search
{
  "size": 0, 
  "aggs": {
    "unique_play_name": {
      "terms": {
        "field": "speaker",
        "size": 3
      }
    }
  }
}
```
```
GET /shakespeare/_search
{
  "query": {
    "term": {
      "speaker": {
        "value": "GLOUCESTER"
      }
    }
  },
  "size": 0,
  "aggs": {
    "unique_play_name": {
      "terms": {
        "field": "play_name"
      }
    }
  }
}
```
```
POST /_sql?format=txt
{
    "query": "SELECT COUNT(*) FROM shakespeare"
}
```
```
POST /_sql?format=txt
{
    "query": "SELECT play_name FROM shakespeare GROUP BY play_name ORDER BY Count(*) DESC"
}
```