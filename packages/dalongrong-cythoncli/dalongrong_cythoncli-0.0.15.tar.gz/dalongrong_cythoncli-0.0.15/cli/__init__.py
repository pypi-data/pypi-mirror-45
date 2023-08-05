import click

import add_app

@click.command()
@click.option("--scale", default=1, help="Number to scale.")
@click.option("--pod", prompt="pod name",
              help="The Pod counts.")
def apply(scale, pod):
    """Simple program that scale pod."""
    results = add_app.py_add(scale,10)
    print("pod scale with counts",pod,results)

if __name__ == '__main__':
    apply()