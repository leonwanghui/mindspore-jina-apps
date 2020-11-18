__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import click
import os
from jina.flow import Flow


def config():
    os.environ['JINA_PARALLEL'] = str(1)
    os.environ['JINA_SHARDS'] = str(2)
    os.environ['JINA_DATA_DIR'] = os.environ.get('JINA_DATA_DIR', '/tmp/jina/mushrooms')
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))
    os.environ['JINA_WORKSPACE'] = os.environ.get('JINA_WORKSPACE', '/tmp/jina/workspace')


@click.command()
@click.option('--task', '-t')
@click.option('--num_docs', '-n', default=1000)
def main(task, num_docs):
    config()
    data_path = os.path.join(os.environ['JINA_DATA_DIR'], '**/*.jpg')
    if task == 'index':
        f = Flow().load_config('flow-index.yml')
        with f:
            f.index_files(data_path, batch_size=32, read_mode='rb', size=num_docs)
    elif task == 'query':
        f = Flow().load_config('flow-query.yml')
        with f:
            f.block()
    elif task == 'dryrun':
        f = Flow.load_config('flow-query.yml')
        with f:
            pass
    else:
        raise NotImplementedError(f'unknown task: {task}. A valid task is either `index`, `query` or `dryrun`.')


if __name__ == '__main__':
    main()
