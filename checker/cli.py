import click
import psycopg
from config import CheckerConfig


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    config = CheckerConfig()
    with psycopg.connect(config.postgres.conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                create table metrics
                    (
                        id            serial  primary key,
                        url           text    not null,
                        regex         text,
                        response_time real    not null,
                        http_code     integer,
                        regex_match   boolean,
                        error         text,
                        timestamp     integer not null
                    )
            """)
            conn.commit()
    click.echo('Initialized database')


@cli.command()
def dropdb():
    config = CheckerConfig()
    with psycopg.connect(config.postgres.conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute('drop table if exists metrics')
    click.echo('Dropped the database')


if __name__ == '__main__':
    cli()
