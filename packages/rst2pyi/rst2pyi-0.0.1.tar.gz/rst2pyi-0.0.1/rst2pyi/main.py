# Copyright 2019 John Reese
# Licensed under the MIT license

import click


@click.command(help="convert reStructuredText annotations to python type stubs")
@click.argument(
    "source_dir", type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.argument(
    "dest_dir",
    type=click.Path(exists=False, file_okay=False, writable=True, resolve_path=True),
)
def main(source_dir, dest_dir):
    print(source_dir, dest_dir)


if __name__ == "__main__":
    main()
