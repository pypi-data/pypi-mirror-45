import glob
import os, os.path
import psycopg2
from astropy.io import ascii


def initialize_SolarSystem_db():
    """Add Solar System information to the database
    Currently the solar system data is in a hand-made table, but it would
    be great to get this information directly from the SPICE kernels
    """

    # Read in current config file if it exists
    configfile = os.path.join(os.environ['HOME'], '.nexoclom')
    config = {}
    if os.path.isfile(configfile):
        for line in open(configfile, 'r').readlines():
            key, value = line.split('=')
            config[key.strip()] = value.strip()
    else:
        assert 0, 'Config file not found.'

    database = config['database']

    print('Populating the database with Solar System objects')

    with psycopg2.connect(host='localhost', database=database) as con:
        # Drop the old table (if necessary) and create a new one
        con.autocommit = True
        cur = con.cursor()
        try:
            cur.execute('drop table solarsystem')
        except:
            pass

        con.autocommit = True
        cur = con.cursor()

        # Create SSObject datatype
        try:
            cur.execute('''CREATE TYPE SSObject
                           as ENUM (
                                'Milky Way',
                                'Sun',
                                'Mercury',
                                'Venus',
                                'Earth',
                                'Mars',
                                'Jupiter',
                                'Saturn',
                                'Uranus',
                                'Neptune',
                                'Ceres',
                                'Pluto',
                                'Moon',
                                'Phobos',
                                'Deimos',
                                'Io',
                                'Europa',
                                'Ganymede',
                                'Callisto',
                                'Mimas',
                                'Enceladus',
                                'Tethys',
                                'Dione',
                                'Rhea',
                                'Titan',
                                'Hyperion',
                                'Iapetus',
                                'Phoebe',
                                'Charon',
                                'Nix',
                                'Hydra')''')
        except:
            pass

        # Create the database table
        cur.execute('''CREATE TABLE SolarSystem (
                         Object SSObject UNIQUE,
                         orbits SSObject,
                         radius float,
                         mass float,
                         a float,
                         e float,
                         tilt float,
                         rotperiod float,
                         orbperiod float)''')

        planfile = glob.glob('**/PlanetaryConstants.dat', recursive=True)
        plantable = ascii.read(planfile[0], delimiter=':', comment='#')

        for row in plantable:
            cur.execute('''INSERT into SolarSystem VALUES
                               (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               tuple(row))

        # Insert naifids into database
        try:
            cur.execute('DROP table naifids')
        except:
            pass
        cur.execute('''CREATE table naifids (id int, object text)''')

        naifid_file = glob.glob('**/naif_ids.dat', recursive=True)[0]
        for line in open(naifid_file, 'r').readlines():
            if ':' in line:
                line2 = line.split(':')
                id = int(line2[0].strip())
                object = line2[1].strip()
                cur.execute(f"INSERT into naifids values ({id}, '{object}')")

if __name__ == '__main__':
    initialize_SolarSystem_db()
