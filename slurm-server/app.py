import click
import subprocess
from flask import Flask

app = Flask(__name__)


@app.route('/cluster', methods=['GET'])
def get_cluster():
    return subprocess.run("sinfo", stdout=subprocess.PIPE).stdout.decode("utf-8")


@app.route('/nodes', methods=['GET'])
@app.route('/nodes/<name>', methods=['GET'])
def get_nodes(name=None):
    os_cmd = ["scontrol", "show", "node"]
    if name is not None:
        os_cmd.append(name)

    return subprocess.run(os_cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")


@app.route('/partitions', methods=['GET'])
@app.route('/partitions/<name>', methods=['GET'])
def get_partitions(name=None):
    os_cmd = ["scontrol", "show", "partition"]
    if name is not None:
        os_cmd.append(name)

    return subprocess.run(os_cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")


@click.command()
@click.option('--host', '-h')
@click.option('--port', '-p', default=5000)
def run(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    run()
