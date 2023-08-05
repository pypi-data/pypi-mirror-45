import asyncpg
import asyncio
import click
import hashlib
from pganonymizer.dsn import makeDSN
import os
from csj_parser.csj import Csj
import base64

async def convert_byte_to_int(input):
    return int.from_bytes(input, byteorder='big')

async def hash_month_date(date, hasher):
    date_array = str(date).split("-")
    hasher.update(date_array[1].encode("utf-8"))
    month = int.from_bytes(hasher.digest()[28:], byteorder='big') % 13
    hasher.update(date_array[2].encode("utf-8"))
    date = int.from_bytes(hasher.digest()[28:], byteorder='big') % 29
    return "{}-{}-{}".format(date_array[0], month if month else month + 1, date if date else date + 1)

async def hash_phone_number(phone_number, hasher):
    country_code = phone_number[:3]
    pure_number = phone_number[3:]
    len_to_be_hashed = len(pure_number)
    hasher.update(pure_number.encode("utf-8"))
    result = await convert_byte_to_int(hasher.digest()[31-len_to_be_hashed:]) % int("9"*len_to_be_hashed)
    result = country_code + (str(result) if len(str(result)) == len_to_be_hashed else str(result) + "0" * (len_to_be_hashed - len(str(result))))
    return result

async def hashRecord(record, rule):
    hasher = hashlib.sha256()
    if rule == "hash":
        hasher.update(record.encode("utf-8"))
        result = base64.b32encode(hasher.digest()).decode()[:16]

    elif rule == "date": #YMD
        result = await hash_month_date(record, hasher)

    elif rule == "phone": #+CCX~ 
        result = await hash_phone_number(record, hasher)

    return result

async def loadcsj(filename):
    with open(filename) as f:
        lines = f.read()
        json_dict = Csj.to_dict(lines)
        return json_dict

async def run_anonymizer(dsn, schemafile):
    conn = await asyncpg.connect(dsn)
    schema = await loadcsj(schemafile)
    async with conn.transaction(isolation='serializable'):
        for each_row in schema:
            table_name = each_row.get('table')
            column_name = each_row.get('column')
            rule = each_row.get('rule')
            await conn.execute("ALTER TABLE {} DISABLE TRIGGER ALL;".format(table_name))
            records = await conn.fetch("SELECT {} FROM {}".format(column_name, table_name))          
            for each_record in records:
                hashed_record = await hashRecord(each_record.get(column_name), rule)
                await conn.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(table_name, column_name, hashed_record, column_name, each_record.get(column_name)))
            await conn.execute("ALTER TABLE {} ENABLE TRIGGER ALL;".format(table_name))

@click.command()
@click.option('-h', nargs=1, required=False, help="Postgres host")
@click.option('-d', nargs=1, required=False, help="Database name")
@click.option('-u', '-U', nargs=1, required=False, help="Database username (role)")
@click.option('-p', nargs=1, required=False, help="Database port")
@click.option('-password', '-P', nargs=1, required=False, help="Database password (Not recommended, use environment variable PGPASSWORD instead)")
@click.option('--schema', nargs=1, required=False, help="Path to yml file")
def main(h, d, u, p, password, schema):
    cnx_destination = {
        '-h': h,
        '-d': d,
        '-U': u,
        '-p': p,
        '-P': password
    }
    dsn = makeDSN(cnx_destination)
    if schema:
        asyncio.get_event_loop().run_until_complete(run_anonymizer(dsn, schema))


if __name__ == "__main__":
    main()