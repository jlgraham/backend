import logging
import peewee
from dbschema import Waypoint, Location, database

def storage(topic, item, m2s=None):
    """
    Storage plugin for m2s. The function signature MUST match the
    above. `topic' contains the message topic (e.g. "owntracks/jpm/nexus")
    and `item' is a dict which contains the rest of the data (including
    weather and reverse geo-coding information if requested)

    This function need not return anything.
    """

    store_only = m2s.cf.store_only
    if store_only is not None:
        if topic not in store_only:
            return

    logging.debug("---- in storage: %s" % topic)

    item['tst'] = item['date_string']           # replace for database

    # Attempt to connect if not already connected. Takes care of MySQL 2006
    try:
        database.connect()
    except Exception, e:
        logging.info("Cannot connect to database: %s" % (str(e)))

    # Handle _type location/waypoint specifically

    if '_type' in item:
        if item['_type'] == 'waypoint':
            # Upsert
            try:
                try:
                    Waypoint.get(Waypoint.tst == item['tst']).delete_instance()
                except peewee.WaypointDoesNotExist:
                    pass

                waypoint = Waypoint(**item)
                waypoint.save()
            except Exception, e:
                logging.info("Cannot upsert waypoint in DB: %s" % (str(e)))

        else:
            try:
                loca = Location(**item)
                loca.save()
            except Exception, e:
                logging.info("Cannot store location in DB: %s" % (str(e)))
