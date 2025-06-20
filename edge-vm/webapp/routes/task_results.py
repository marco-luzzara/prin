from typing import Generator, Any

from flask import (
    Blueprint, current_app, render_template, jsonify
)

from .middlewares.authenticated import authenticated
from .. import _kafka_consumer

bp = Blueprint('task-results', __name__, url_prefix='/task-results')

## Test Kafka notification with:
#
# BROKER=kafka-broker-0:9092
# TOPIC=devprin.task.result
# 
# ./kafka-console-producer.sh \
#   --broker-list $BROKER \
#   --topic      $TOPIC \
#   --property  parse.key=true \
#   --property  key.separator=";" <<EOF
# {"group_name":"researcher_user1"};{"taskType":"training","taskTimestamp":"$(date "+%Y-%m-%dT%H:%M:%SZ")","group":"researcher_user1","fileName":"data.csv","preSignedUrl":"https://..."}
# EOF


def poll_kafka_records() -> Generator[Any, None, None]:
    # Changed from https://github.com/dpkp/kafka-python/blob/e4e6fcf353184af36226397d365cce1ee88b4a3a/kafka/consumer/group.py#L1160C9-L1175C29
    record_map = _kafka_consumer.poll(timeout_ms=10000, update_offsets=False)
    for tp, records in iter(record_map.items()):
        for record in records:
            if not _kafka_consumer._subscription.is_fetchable(tp):
                current_app.logger.debug("Not returning fetched records for partition %s"
                            " since it is no longer fetchable", tp)
                break
            yield record


def map_kafka_record_to_task_result(record):
    task_result = record.value
    return {
        'timestamp': task_result['taskTimestamp'],
        'type': task_result['taskType'],
        'filename': task_result['fileName'],
        'url': task_result['preSignedUrl']
    }


@bp.get('/')
@authenticated
def view_task_results():
    return render_template('task-results.html')


@bp.get('/poll')
@authenticated
def poll_task_results():
    task_results = [map_kafka_record_to_task_result(r) for r in poll_kafka_records()]
    current_app.logger.info(f'Task results after polling: {len(task_results)}')

    return jsonify(task_results)
