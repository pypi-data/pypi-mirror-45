# -*- coding: utf-8 -*-

"""Console script for test_earlybirds."""
import sys
import click
from test_earlybirds.app import execute


@click.command()
@click.option('--k', default=5, prompt='the number of the neighbors')
@click.option('--output', prompt='the output path')
@click.option('--learn', prompt='the input path of the train set')
@click.option('--evaluation', prompt='the input path of the evaluation set')
@click.option('--user_limit', default=20, prompt='limit the number of user to evaluate')
def main(learn, evaluation, output, k, user_limit):
    execute(learn_path=learn, eval_path=evaluation, output_path=output, k=k, user_limit=user_limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
