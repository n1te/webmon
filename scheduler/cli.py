import click
import psycopg
from config import SchedulerConfig


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    config = SchedulerConfig()
    with psycopg.connect(config.postgres.conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                create table if not exists sites
                (
                    id serial primary key,
                    url text not null unique,
                    regex text,
                    interval integer constraint sites_interval_check check (("interval" >= 5) AND ("interval" <= 300)),
                    next_check_at integer default 0 not null
                )
            """)
            cur.execute('create index if not exists next_check_at_idx on sites (next_check_at)')
            cur.execute("insert into sites (url, interval) values ('https://google.com', 7)")
            cur.execute("""
                insert into sites (url, interval, regex)
                values ('https://aiven.io', 5, 'The trusted open source data platform for everyone')
                """)
            conn.commit()
    click.echo('Initialized database')


@cli.command()
def dropdb():
    config = SchedulerConfig()
    with psycopg.connect(config.postgres.conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute('drop table if exists sites')
    click.echo('Dropped the database')


if __name__ == '__main__':
    cli()
