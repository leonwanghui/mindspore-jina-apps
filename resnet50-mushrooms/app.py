__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
import string
import random
import click
from jina.flow import Flow

RANDOM_SEED = 15


def config():
    os.environ['JINA_PARALLEL'] = str(1)
    os.environ['JINA_SHARDS'] = str(2)
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))
    os.environ['JINA_DATA_DIR'] = os.environ.get('JINA_DATA_DIR', '/root/jina/mushrooms')
    os.environ['JINA_WORKSPACE'] = os.environ.get('JINA_WORKSPACE', get_random_ws(os.environ['JINA_DATA_DIR']))


def get_random_ws(workspace_path, length=8):
    random.seed(RANDOM_SEED)
    letters = string.ascii_lowercase
    dn = ''.join(random.choice(letters) for i in range(length))
    return os.path.join(workspace_path, dn)


@click.command()
@click.option('--task', '-t')
@click.option('--num_docs', '-n', default=1000)
def main(task, num_docs):
    config()
    data_path = os.path.join(os.environ['JINA_DATA_DIR'], 'train/**/*.jpg')
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
