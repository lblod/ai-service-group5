import os
import datetime
from string import Template
from escape_helpers import (
    sparql_escape_uri,
    sparql_escape_datetime,
    sparql_escape_string,
    sparql_escape,
)
from helpers import generate_uuid, logger
import traceback

MU_APPLICATION_GRAPH = os.environ.get("MU_APPLICATION_GRAPH")

STATUS_BUSY = "http://redpencil.data.gift/id/concept/JobStatus/busy"
STATUS_SCHEDULED = "http://redpencil.data.gift/id/concept/JobStatus/scheduled"
STATUS_SUCCESS = "http://redpencil.data.gift/id/concept/JobStatus/success"
STATUS_FAILED = "http://redpencil.data.gift/id/concept/JobStatus/failed"


def attach_task_results_container(task, results, graph=MU_APPLICATION_GRAPH):
    CONTAINER_URI_PREFIX = 'http://redpencil.data.gift/id/container/'
    container_uuid = generate_uuid()
    container_uri = CONTAINER_URI_PREFIX + container_uuid

    container_query_template = Template("""
PREFIX cogs: <http://vocab.deri.ie/cogs#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
PREFIX nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
PREFIX mu: <http://mu.semte.ch/vocabularies/core/>
PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>

INSERT {
    GRAPH ?graph {
        $task task:resultsContainer $container .
        $container a nfo:DataContainer ;
            mu:uuid $container_uuid ;
            task:hasFile $results .
    }
}
WHERE {
    GRAPH ?graph {
        $task a task:Task .
    }
}""")
    container_query_string = container_query_template.substitute(
        graph=sparql_escape_uri(graph) if graph else "?g",
        task=sparql_escape_uri(task),
        container_uuid=sparql_escape_string(container_uuid),
        container=sparql_escape_uri(container_uri),
        results=", ".join([sparql_escape_uri(result) for result in results]),
    )
    return container_query_string


def update_task_status(task, status, graph=MU_APPLICATION_GRAPH):
    time = datetime.datetime.now()

    query_template = Template("""
PREFIX adms: <http://www.w3.org/ns/adms#>
PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
PREFIX dct: <http://purl.org/dc/terms/>

DELETE {
    GRAPH ?g {
        $task adms:status ?old_status ;
            dct:modified ?old_modified .
    }
}
INSERT {
    GRAPH ?g {
        $task adms:status $new_status ;
            dct:modified $modified .
    }
}
WHERE {
  GRAPH ?g {
      $task a task:Task ;
            adms:status ?old_status .
      OPTIONAL { ?task dct:modified ?old_modified }

  }
}""")
    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph) if graph else "?g",
        task=sparql_escape_uri(task),
        new_status=sparql_escape_uri(status),
        modified=sparql_escape_datetime(time),
    )
    return query_string


def verify_actionable_task(task_uri, graph=MU_APPLICATION_GRAPH):
    query_template = Template("""
PREFIX mu: <http://mu.semte.ch/vocabularies/core/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX cogs: <http://vocab.deri.ie/cogs#>
PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
PREFIX adms: <http://www.w3.org/ns/adms#>
PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>

SELECT (?uuid as ?id) ?status ?created ?used ?operation WHERE {
    GRAPH ?g {
        $task_uri a task:Task ;
            dct:created ?created ;
            adms:status <http://redpencil.data.gift/id/concept/JobStatus/scheduled> ;
            task:operation ?operation ;
            mu:uuid ?uuid .
        OPTIONAL { $task_uri task:inputContainer/task:hasFile ?used }
    }
}
ORDER BY ASC(?created)
LIMIT 1
""")
    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph) if graph else "?g",
        task_uri=sparql_escape_uri(task_uri),
    )
    return query_string


def find_actionable_task_of_type(task_type, graph):
    query_template = Template("""
PREFIX mu: <http://mu.semte.ch/vocabularies/core/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX cogs: <http://vocab.deri.ie/cogs#>
PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
PREFIX adms: <http://www.w3.org/ns/adms#>
PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>

SELECT (?task as ?uri) (?uuid as ?id) ?created ?used ?operation WHERE {
    graph ?g {
        ?task a task:Task ;
            dct:created ?created ;
            adms:status <http://redpencil.data.gift/id/concept/JobStatus/scheduled> ;
            task:operation ?operation ;
            mu:uuid ?uuid .
        OPTIONAL { ?task task:inputContainer/task:hasFile ?used }
        VALUES ?operation {$task_type}
    }
}
ORDER BY ASC(?created)
LIMIT 1
""")
    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph) if graph else "?g",
        task_type=sparql_escape_uri(task_type),
    )
    return query_string



def get_input_contents_task(task_uri, graph):
    query_template = Template("""
PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>

SELECT ?content WHERE {
    GRAPH ?g {
        $task_uri a task:Task ;
                  task:inputContainer/task:hasFile ?content.
    }
}
""")
    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph) if graph else "?g",
        task_uri=sparql_escape_uri(task_uri),
    )
    return query_string


def run_task(task_uri, graph, runner_func, sparql_query, sparql_update):
    task_q = verify_actionable_task(task_uri, graph)
    task_res = sparql_query(task_q)
    if task_res["results"]["bindings"]:
        used = [
            binding["used"]["value"]
            for binding in task_res["results"]["bindings"]
            if "used" in binding
        ]
    else:
        raise Exception(f"Didn't find actionable task for <{task_uri}>")

    logger.info(f"Started running task {task_uri}")

    sparql_update(update_task_status(task_uri, STATUS_BUSY, graph))
    try:
        generated = runner_func(used)
        if generated:
            logger.info(
                f"Running task <{task_uri}> with source <{used[0]}> generated <{generated[0]}>"
            )
            for task in task_uri:
                sparql_update(attach_task_results_container(task, generated, graph))
        sparql_update(update_task_status(task_uri, STATUS_SUCCESS, graph))
        return generated
    except Exception as e:
        traceback.print_exc()
        sparql_update(update_task_status(task_uri, STATUS_FAILED, graph))

    # end_time = time.time()
    # logger.info(
    # f"Finished running job at {start_time}, took {end_time - start_time} seconds"
    # )
