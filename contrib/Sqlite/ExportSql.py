# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2008 Douglas S. Blank <doug.blank@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: ExportSql.py 508 2010-08-16 01:48:01Z dsblank $
#

"Export to SQLite Database"

#------------------------------------------------------------------------
#
# Standard Python Modules
#
#------------------------------------------------------------------------

import sqlite3 as sqlite
import time

#------------------------------------------------------------------------
#
# Set up logging
#
#------------------------------------------------------------------------
import logging
log = logging.getLogger(".ExportSql")

#------------------------------------------------------------------------
#
# GRAMPS modules
#
#------------------------------------------------------------------------
from gramps.gen.utils.id import create_id
from gramps.gen.constfunc import cuni
from gramps.gen.const import GRAMPS_LOCALE as glocale
try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext
ngettext = _trans.ngettext

#-------------------------------------------------------------------------
#
# Export functions
#
#-------------------------------------------------------------------------
def lookup(index, event_ref_list):
    """
    Get the unserialized event_ref in an list of them and return it.
    """
    if index < 0:
        return None
    else:
        count = 0
        for event_ref in event_ref_list:
            (private, note_list, attribute_list, ref, role) = event_ref
            if index == count:
                return ref
            count += 1
        return None

def makeDB(db):
    db.query("""drop table note;""")
    db.query("""drop table person;""")
    db.query("""drop table event;""")
    db.query("""drop table family;""")
    db.query("""drop table repository;""")
    db.query("""drop table repository_ref;""")
    db.query("""drop table date;""")
    db.query("""drop table place;""") 
    db.query("""drop table citation;""") 
    db.query("""drop table source;""") 
    db.query("""drop table media;""")
    db.query("""drop table name;""")
    db.query("""drop table surname;""")
    db.query("""drop table link;""")
    db.query("""drop table markup;""")
    db.query("""drop table event_ref;""")
    db.query("""drop table child_ref;""")
    db.query("""drop table person_ref;""")
    db.query("""drop table lds;""")
    db.query("""drop table media_ref;""")
    db.query("""drop table address;""")
    db.query("""drop table location;""")
    db.query("""drop table attribute;""")
    db.query("""drop table url;""")
    db.query("""drop table datamap;""")
    db.query("""drop table tag;""")

    db.query("""CREATE TABLE note (
                  handle CHARACTER(25) PRIMARY KEY,
                  gid    CHARACTER(25),
                  text   TEXT,
                  format INTEGER,
                  note_type1   INTEGER,
                  note_type2   TEXT,
                  change INTEGER,
                  tags TEXT,
                  private BOOLEAN);""")

    db.query("""CREATE TABLE name (
                  handle CHARACTER(25) PRIMARY KEY,
                  primary_name BOOLEAN,
                  private BOOLEAN, 
                  first_name TEXT, 
                  suffix TEXT, 
                  title TEXT, 
                  name_type0 INTEGER, 
                  name_type1 TEXT, 
                  group_as TEXT, 
                  sort_as INTEGER,
                  display_as INTEGER, 
                  call TEXT,
                  nick TEXT,
                  famnick TEXT);""")

    db.query("""CREATE TABLE surname (
                  handle CHARACTER(25),
                  surname TEXT, 
                  prefix TEXT, 
                  primary_surname BOOLEAN, 
                  origin_type0 INTEGER,
                  origin_type1 TEXT,
                  connector TEXT);""")

    db.query("""CREATE INDEX idx_surname_handle ON 
                  surname(handle);""")

    db.query("""CREATE TABLE date (
                  handle CHARACTER(25) PRIMARY KEY,
                  calendar INTEGER, 
                  modifier INTEGER, 
                  quality INTEGER,
                  day1 INTEGER, 
                  month1 INTEGER, 
                  year1 INTEGER, 
                  slash1 BOOLEAN,
                  day2 INTEGER, 
                  month2 INTEGER, 
                  year2 INTEGER, 
                  slash2 BOOLEAN,
                  text TEXT, 
                  sortval INTEGER, 
                  newyear INTEGER);""")

    db.query("""CREATE TABLE person (
                  handle CHARACTER(25) PRIMARY KEY,
                  gid CHARACTER(25), 
                  gender INTEGER, 
                  death_ref_handle TEXT, 
                  birth_ref_handle TEXT, 
                  change INTEGER, 
                  tags TEXT, 
                  private BOOLEAN);""")

    db.query("""CREATE TABLE family (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 father_handle CHARACTER(25), 
                 mother_handle CHARACTER(25), 
                 the_type0 INTEGER, 
                 the_type1 TEXT, 
                 change INTEGER, 
                 tags TEXT, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE place (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 title TEXT, 
                 main_location CHARACTER(25),
                 long TEXT, 
                 lat TEXT, 
                 change INTEGER, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE event (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 the_type0 INTEGER, 
                 the_type1 TEXT, 
                 description TEXT, 
                 change INTEGER, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE citation (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 confidence INTEGER,
                 page CHARACTER(25),
                 source_handle CHARACTER(25),
                 change INTEGER,
                 private BOOLEAN);""")

    db.query("""CREATE TABLE source (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 title TEXT, 
                 author TEXT, 
                 pubinfo TEXT, 
                 abbrev TEXT, 
                 change INTEGER,
                 private BOOLEAN);""")

    db.query("""CREATE TABLE media (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 path TEXT, 
                 mime TEXT, 
                 desc TEXT,
                 change INTEGER, 
                 tags TEXT, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE repository_ref (
                 handle CHARACTER(25) PRIMARY KEY,
                 ref CHARACTER(25), 
                 call_number TEXT, 
                 source_media_type0 INTEGER,
                 source_media_type1 TEXT,
                 private BOOLEAN);""")

    db.query("""CREATE TABLE repository (
                 handle CHARACTER(25) PRIMARY KEY,
                 gid CHARACTER(25), 
                 the_type0 INTEGER, 
                 the_type1 TEXT,
                 name TEXT, 
                 change INTEGER, 
                 private BOOLEAN);""")

    # One link to link them all
    db.query("""CREATE TABLE link (
                 from_type CHARACTER(25), 
                 from_handle CHARACTER(25), 
                 to_type CHARACTER(25), 
                 to_handle CHARACTER(25));""")

    db.query("""CREATE INDEX idx_link_to ON 
                  link(from_type, from_handle, to_type);""")

    db.query("""CREATE TABLE markup (
                 handle CHARACTER(25) PRIMARY KEY,
                 markup0 INTEGER, 
                 markup1 TEXT, 
                 value TEXT, 
                 start_stop_list TEXT);""")

    db.query("""CREATE TABLE event_ref (
                 handle CHARACTER(25) PRIMARY KEY,
                 ref CHARACTER(25), 
                 role0 INTEGER, 
                 role1 TEXT, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE person_ref (
                 handle CHARACTER(25) PRIMARY KEY,
                 description TEXT,
                 private BOOLEAN);""")

    db.query("""CREATE TABLE child_ref (
                 handle CHARACTER(25) PRIMARY KEY,
                 ref CHARACTER(25), 
                 frel0 INTEGER,
                 frel1 CHARACTER(25),
                 mrel0 INTEGER,
                 mrel1 CHARACTER(25),
                 private BOOLEAN);""")

    db.query("""CREATE TABLE lds (
                 handle CHARACTER(25) PRIMARY KEY,
                 type INTEGER, 
                 place CHARACTER(25), 
                 famc CHARACTER(25), 
                 temple TEXT, 
                 status INTEGER, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE media_ref (
                 handle CHARACTER(25) PRIMARY KEY,
                 ref CHARACTER(25),
                 role0 INTEGER,
                 role1 INTEGER,
                 role2 INTEGER,
                 role3 INTEGER,
                 private BOOLEAN);""")

    db.query("""CREATE TABLE address (
                handle CHARACTER(25) PRIMARY KEY,
                private BOOLEAN);""")

    db.query("""CREATE TABLE location (
                 handle CHARACTER(25) PRIMARY KEY,
                 street TEXT, 
                 locality TEXT,
                 city TEXT, 
                 county TEXT, 
                 state TEXT, 
                 country TEXT, 
                 postal TEXT, 
                 phone TEXT,
                 parish TEXT);""")

    db.query("""CREATE TABLE attribute (
                 handle CHARACTER(25) PRIMARY KEY,
                 the_type0 INTEGER, 
                 the_type1 TEXT, 
                 value TEXT, 
                 private BOOLEAN);""")

    db.query("""CREATE TABLE url (
                 handle CHARACTER(25) PRIMARY KEY,
                 path TEXT, 
                 desc TXT, 
                 type0 INTEGER,
                 type1 TEXT,                  
                 private BOOLEAN);
                 """)

    db.query("""CREATE TABLE datamap (
                 handle CHARACTER(25) PRIMARY KEY,
                 key_field   TEXT, 
                 value_field TXT);
                 """)

    db.query("""CREATE TABLE tag (
                 handle CHARACTER(25) PRIMARY KEY,
                 name TEXT,
                 color TEXT,
                 priority INTEGER,
                 change INTEGER);
                 """)

class Database(object):
    """
    The db connection.
    """
    def __init__(self, database):
        self.batch = False
        self.database = database
        self.db = sqlite.connect(self.database)
        self.cursor = self.db.cursor()

    def query(self, q, *args):
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], str):
                args[i] = cuni(args[i])
        if q.strip().upper().startswith("DROP"):
            try:
                self.cursor.execute(q, args)
                self.db.commit()
            except:
                "WARN: no such table to drop: '%s'" % q
        else:
            try:
                self.cursor.execute(q, args)
                if not self.batch:
                    self.db.commit()
            except:
                print "ERROR: query :", q
                print "ERROR: values:", args
                raise
            return self.cursor.fetchall()

    def close(self):
        """ Closes and writes out tables """
        self.cursor.close()
        self.db.close()

def export_location_list(db, from_type, from_handle, locations):
    for location in locations:
        export_location(db, from_type, from_handle, location)

def export_url_list(db, from_type, from_handle, urls):
    for url in urls:
        # (False, u'http://www.gramps-project.org/', u'loleach', (0, u'kaabgo'))
        (private, path, desc, type) = url
        handle = create_id()
        db.query("""insert INTO url (
                 handle,
                 path, 
                 desc, 
                 type0,                  
                 type1,                  
                 private) VALUES (?, ?, ?, ?, ?, ?);
                 """,
                 handle,
                 path,
                 desc,
                 type[0],
                 type[1],
                 private)
        # finally, link this to parent
        export_link(db, from_type, from_handle, "url", handle)

def export_person_ref_list(db, from_type, from_handle, person_ref_list):
    for person_ref in person_ref_list:
        (private, 
         citation_list,
         note_list,
         handle,
         desc) = person_ref
        db.query("""INSERT INTO person_ref (
                    handle,
                    description,
                    private) VALUES (?, ?, ?);""",
                 handle,
                 desc,
                 private
                 )
        export_list(db, "person_ref", handle, "note", note_list)
        export_citation_list(db, "person_ref", handle, citation_list)
        # And finally, make a link from parent to new object
        export_link(db, from_type, from_handle, "person_ref", handle)

def export_lds(db, from_type, from_handle, data):
    (lcitation_list, lnote_list, date, type, place,
     famc, temple, status, private) = data
    lds_handle = create_id()
    db.query("""INSERT into lds (handle, type, place, famc, temple, status, private) 
             VALUES (?,?,?,?,?,?,?);""",
             lds_handle, type, place, famc, temple, status, private)
    export_link(db, "lds", lds_handle, "place", place)
    export_list(db, "lds", lds_handle, "note", lnote_list)
    export_date(db, "lds", lds_handle, date)
    export_citation_list(db, "lds", lds_handle, lcitation_list)
    # And finally, make a link from parent to new object
    export_link(db, from_type, from_handle, "lds", lds_handle)
    
def export_citation_ref(db, from_type, from_handle, citation_handle):
    export_link(db, from_type, from_handle, "citation", citation_handle)

def export_source(db, handle, gid, title, author, pubinfo, abbrev, change, 
                  private):
    db.query("""INSERT into source (
             handle, 
             gid, 
             title, 
             author, 
             pubinfo, 
             abbrev, 
             change,
             private
             ) VALUES (?,?,?,?,?,?,?,?);""",
             handle, 
             gid, 
             title, 
             author, 
             pubinfo, 
             abbrev, 
             change,
             private)

def export_note(db, data):
    (handle, gid, styled_text, format, note_type,
     change, tags, private) = data
    text, markup_list = styled_text
    db.query("""INSERT into note (
                  handle,
                  gid,
                  text,
                  format,
                  note_type1,
                  note_type2,
                  change,
                  tags,
                  private) values (?, ?, ?, ?,
                                   ?, ?, ?, ?, ?);""", 
             handle, gid, text, format, note_type[0],
             note_type[1], change, ",".join(tags), private)
    for markup in markup_list:
        markup_code, value, start_stop_list = markup
        export_markup(db, "note", handle, markup_code[0], markup_code[1], value, 
                      str(start_stop_list)) # Not normal form; use eval

def export_markup(db, from_type, from_handle,  markup_code0, markup_code1, value, 
                  start_stop_list):
    markup_handle = create_id()
    db.query("""INSERT INTO markup (
                 handle, 
                 markup0, 
                 markup1, 
                 value, 
                 start_stop_list) VALUES (?,?,?,?,?);""",
             markup_handle, markup_code0, markup_code1, value, 
             start_stop_list)
    # And finally, make a link from parent to new object
    export_link(db, from_type, from_handle, "markup", markup_handle)

def export_event(db, data):
    (handle, gid, the_type, date, description, place_handle, 
     citation_list, note_list, media_list, attribute_list,
     change, private) = data
    db.query("""INSERT INTO event (
                 handle, 
                 gid, 
                 the_type0, 
                 the_type1, 
                 description, 
                 change, 
                 private) VALUES (?,?,?,?,?,?,?);""",
             handle, 
             gid, 
             the_type[0], 
             the_type[1], 
             description, 
             change, 
             private)
    export_date(db, "event", handle, date)
    export_link(db, "event", handle, "place", place_handle)
    export_list(db, "event", handle, "note", note_list)
    export_attribute_list(db, "event", handle, attribute_list)
    export_media_ref_list(db, "event", handle, media_list)
    export_citation_list(db, "event", handle, citation_list)

def export_event_ref(db, from_type, from_handle, event_ref):
    (private, note_list, attribute_list, ref, role) = event_ref
    handle = create_id()
    db.query("""insert INTO event_ref (
                 handle, 
                 ref, 
                 role0, 
                 role1, 
                 private) VALUES (?,?,?,?,?);""",
             handle, 
             ref, 
             role[0], 
             role[1], 
             private) 
    export_list(db, "event_ref", handle, "note", note_list)
    export_attribute_list(db, "event_ref", handle, attribute_list)
    # finally, link this to parent
    export_link(db, from_type, from_handle, "event_ref", handle)

def export_person(db, person):
    (handle,        #  0
     gid,          #  1
     gender,             #  2
     primary_name,       #  3
     alternate_names,    #  4
     death_ref_index,    #  5
     birth_ref_index,    #  6
     event_ref_list,     #  7
     family_list,        #  8
     parent_family_list, #  9
     media_list,         # 10
     address_list,       # 11
     attribute_list,     # 12
     urls,               # 13
     lds_ord_list,       # 14
     pcitation_list,       # 15
     pnote_list,         # 16
     change,             # 17
     tags,             # 18
     private,           # 19
     person_ref_list,    # 20
     ) = person
    db.query("""INSERT INTO person (
                  handle, 
                  gid, 
                  gender, 
                  death_ref_handle, 
                  birth_ref_handle, 
                  change, 
                  tags, 
                  private) values (?, ?, ?, ?, ?, ?, ?, ?);""",
             handle, 
             gid, 
             gender, 
             lookup(death_ref_index, event_ref_list),
             lookup(birth_ref_index, event_ref_list),
             change, 
             ",".join(tags), #TO_FIX: TypeError: sequence item 0: expected string, NoneType found
             private)
    
    # Event Reference information
    for event_ref in event_ref_list:
        export_event_ref(db, "person", handle, event_ref)
    export_list(db, "person", handle, "family", family_list) 
    export_list(db, "person", handle, "parent_family", parent_family_list)
    export_media_ref_list(db, "person", handle, media_list)
    export_list(db, "person", handle, "note", pnote_list)
    export_attribute_list(db, "person", handle, attribute_list)
    export_url_list(db, "person", handle, urls) 
    export_person_ref_list(db, "person", handle, person_ref_list)
    export_citation_list(db, "person", handle, pcitation_list)
    
    # -------------------------------------
    # Address
    # -------------------------------------
    for address in address_list:
        export_address(db, "person", handle, address)
        
    # -------------------------------------
    # LDS ord
    # -------------------------------------
    for ldsord in lds_ord_list:
        export_lds(db, "person", handle, ldsord)

    # -------------------------------------
    # Names
    # -------------------------------------
    export_name(db, "person", handle, True, primary_name)
    map(lambda name: export_name(db, "person", handle, False, name), 
        alternate_names)

def export_date(db, from_type, from_handle, data):
    if data is None: return
    (calendar, modifier, quality, dateval, text, sortval, newyear) = data
    if len(dateval) == 4:
        day1, month1, year1, slash1 = dateval
        day2, month2, year2, slash2 = 0, 0, 0, 0
    elif len(dateval) == 8:
        day1, month1, year1, slash1, day2, month2, year2, slash2 = dateval
    else:
        raise ("ERROR: date dateval format", dateval)
    date_handle = create_id()
    db.query("""INSERT INTO date (
                  handle,
                  calendar, 
                  modifier, 
                  quality,
                  day1, 
                  month1, 
                  year1, 
                  slash1,
                  day2, 
                  month2, 
                  year2, 
                  slash2,
                  text, 
                  sortval, 
                  newyear) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                   ?, ?, ?, ?, ?, ?);""",
             date_handle, calendar, modifier, quality, 
             day1, month1, year1, slash1, 
             day2, month2, year2, slash2,
             text, sortval, newyear)
    # And finally, make a link from parent to new object
    export_link(db, from_type, from_handle, "date", date_handle)

def export_surname(db, handle, surname_list):
    for data in surname_list:
        (surname, prefix, primary, origin_type, connector) = data        
        db.query("""INSERT INTO surname (
                  handle,
                  surname, 
                  prefix, 
                  primary_surname, 
                  origin_type0,
                  origin_type1,
                  connector) VALUES (?,?,?,?,?,?,?);""",
                 handle, surname, prefix, primary, origin_type[0], 
                 origin_type[1], connector)

def export_name(db, from_type, from_handle, primary, data):
    if data:
        (private, citation_list, note_list, date,
         first_name, surname_list, suffix, title,
         name_type, 
         group_as, sort_as, display_as, 
         call, nick, famnick) = data
        handle = create_id()
        db.query("""INSERT into name (
                  handle,
                  primary_name,
                  private, 
                  first_name, 
                  suffix, 
                  title, 
                  name_type0, 
                  name_type1, 
                  group_as, 
                  sort_as,
                  display_as, 
                  call,
                  nick,
                  famnick
                    ) values (?, ?, ?, ?, ?, ?, ?,  
                              ?, ?, ?, ?, ?, ?, ?);""",
                 handle, primary, private, first_name, suffix, title,
                 name_type[0], name_type[1], group_as, 
                 sort_as, display_as, call, nick, famnick)
        export_surname(db, handle, surname_list)
        export_date(db, "name", handle, date) 
        export_list(db, "name", handle, "note", note_list)
        export_citation_list(db, "name", handle, citation_list)
        # And finally, make a link from parent to new object
        export_link(db, from_type, from_handle, "name", handle)

def export_attribute(db, from_type, from_handle, attribute):
    (private, citation_list, note_list, the_type, value) = attribute
    handle = create_id()
    db.query("""INSERT INTO attribute (
                 handle,
                 the_type0, 
                 the_type1, 
                 value, 
                 private) VALUES (?,?,?,?,?);""",
             handle, the_type[0], the_type[1], value, private)
    export_citation_list(db, "attribute", handle, citation_list)
    export_list(db, "attribute", handle, "note", note_list)
    # finally, link the parent to the address
    export_link(db, from_type, from_handle, "attribute", handle)

def export_citation_list(db, from_type, from_handle, citation_list):
    for citation_handle in citation_list:
        export_citation_ref(db, from_type, from_handle, citation_handle)

def export_media_ref_list(db, from_type, from_handle, media_list):
    for media in media_list:
        export_media_ref(db, from_type, from_handle, media)

def export_media_ref(db, from_type, from_handle, media):
    (private, citation_list, note_list, attribute_list, ref, role) = media
    # handle is the media_ref handle
    # ref is the media handle
    handle = create_id()
    if role is None:
        role = (-1, -1, -1, -1)
    db.query("""INSERT into media_ref (
                 handle,
                 ref,
                 role0,
                 role1,
                 role2,
                 role3,
                 private) VALUES (?,?,?,?,?,?,?);""",
             handle, ref, role[0], role[1], role[2], role[3], private) 
    export_list(db, "media_ref", handle, "note", note_list)
    export_attribute_list(db, "media_ref", handle, attribute_list)
    export_citation_list(db, "media_ref", handle, citation_list)
    # And finally, make a link from parent to new object
    export_link(db, from_type, from_handle, "media_ref", handle)

def export_attribute_list(db, from_type, from_handle, attr_list):
    for attribute in attr_list:
        export_attribute(db, from_type, from_handle, attribute)

def export_child_ref_list(db, from_type, from_handle, to_type, ref_list):
    for child_ref in ref_list:
        # family -> child_ref
        # (False, [], [], u'b305e96e39652d8f08c', (1, u''), (1, u''))
        (private, citation_list, note_list, ref, frel, mrel) = child_ref
        handle = create_id()
        db.query("""INSERT INTO child_ref (handle, 
                     ref, frel0, frel1, mrel0, mrel1, private)
                        VALUES (?, ?, ?, ?, ?, ?, ?);""",
                 handle, ref, frel[0], frel[1], 
                 mrel[0], mrel[1], private)
        export_citation_list(db, "child_ref", handle, citation_list)
        export_list(db, "child_ref", handle, "note", note_list)
        # And finally, make a link from parent to new object
        export_link(db, from_type, from_handle, "child_ref", handle)

def export_list(db, from_type, from_handle, to_type, handle_list):
    for to_handle in handle_list:
        export_link(db, from_type, from_handle, to_type, to_handle)
            
def export_link(db, from_type, from_handle, to_type, to_handle):
    if to_handle:
        db.query("""insert into link (
                   from_type, 
                   from_handle, 
                   to_type, 
                   to_handle) values (?, ?, ?, ?)""",
                 from_type, from_handle, to_type, to_handle)

def export_datamap_dict(db, from_type, from_handle, datamap):
    for key_field in datamap:
        handle = create_id()
        value_field = datamap[key_field]
        db.query("""INSERT INTO datamap (
                      handle,
                      key_field, 
                      value_field) values (?, ?, ?)""",
                 handle, key_field, value_field)
        export_link(db, from_type, from_handle, "datamap", handle)

def export_address(db, from_type, from_handle, address):
    (private, acitation_list, anote_list, date, location) = address
    addr_handle = create_id()
    db.query("""INSERT INTO address (
                handle,
                private) VALUES (?, ?);""", addr_handle, private)
    export_location(db, "address", addr_handle, location)
    export_date(db, "address", addr_handle, date)
    export_list(db, "address", addr_handle, "note", anote_list) 
    export_citation_list(db, "address", addr_handle, acitation_list)
    # finally, link the parent to the address
    export_link(db, from_type, from_handle, "address", addr_handle)

def export_location(db, from_type, from_handle, location):
    if location == None: return
    if len(location) == 8:
        (street, locality, city, county, state, country, postal, phone) = location 
        parish = None
    elif len(location) == 2:
        ((street, locality, city, county, state, country, postal, phone), parish) = location 
    else:
        print "ERROR: what kind of location is this?", location
        return
    handle = create_id()
    db.query("""INSERT INTO location (
                 handle,
                 street, 
                 locality,
                 city, 
                 county, 
                 state, 
                 country, 
                 postal, 
                 phone,
                 parish) VALUES (?,?,?,?,?,?,?,?,?,?);""",
             handle, street, locality, city, county, state, country, postal, phone, parish)
    # finally, link the parent to the address
    export_link(db, from_type, from_handle, "location", handle)

def export_repository_ref_list(db, from_type, from_handle, reporef_list):
    for repo in reporef_list:
        (note_list, 
         ref,
         call_number, 
         source_media_type,
         private) = repo
        handle = create_id()
        db.query("""insert INTO repository_ref (
                     handle, 
                     ref, 
                     call_number, 
                     source_media_type0,
                     source_media_type1,
                     private) VALUES (?,?,?,?,?,?);""",
                 handle, 
                 ref, 
                 call_number, 
                 source_media_type[0],
                 source_media_type[1],
                 private) 
        export_list(db, "repository_ref", handle, "note", note_list)
        # finally, link this to parent
        export_link(db, from_type, from_handle, "repository_ref", handle)

def exportData(database, filename, err_dialog=None, option_box=None, 
               callback=None):
    if not callable(callback): 
        callback = lambda percent: None # dummy

    if option_box:
        option_box.parse_options()
        database = option_box.get_filtered_database(database)

    start = time.time()
    total = (len(database.get_note_handles()) + 
             len(database.get_person_handles()) +
             len(database.get_event_handles()) + 
             len(database.get_family_handles()) +
             len(database.get_repository_handles()) +
             len(database.get_place_handles()) +
             len(database.get_media_object_handles()) +
             len(database.get_tag_handles()) +
             len(database.get_citation_handles()) +
             len(database.get_source_handles()))
    count = 0.0

    db = Database(filename)
    makeDB(db)

    db.batch = True # don't commit till end
    # ---------------------------------
    # Notes
    # ---------------------------------
    for note_handle in database.iter_note_handles():
        data = database.get_note_from_handle(note_handle)
        if data is None:
            continue
        export_note(db, data.serialize())
        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Event
    # ---------------------------------
    for event_handle in database.iter_event_handles():
        data = database.get_event_from_handle(event_handle)
        if data is None:
            continue
        export_event(db, data.serialize())
        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Person
    # ---------------------------------
    for person_handle in database.iter_person_handles():
        person = database.get_person_from_handle(person_handle)
        if person is None:
            continue
        export_person(db, person.serialize())
        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Family
    # ---------------------------------
    for family_handle in database.iter_family_handles():
        family = database.get_family_from_handle(family_handle)
        if family is None:
            continue
        (handle, gid, father_handle, mother_handle,
         child_ref_list, the_type, event_ref_list, media_list,
         attribute_list, lds_seal_list, citation_list, note_list,
         change, tags, private) = family.serialize()
        # father_handle and/or mother_handle can be None
        db.query("""INSERT INTO family (
                 handle, 
                 gid, 
                 father_handle, 
                 mother_handle,
                 the_type0, 
                 the_type1, 
                 change, 
                 tags, 
                 private) values (?,?,?,?,?,?,?,?,?);""",
                 handle, gid, father_handle, mother_handle,
                 the_type[0], the_type[1], change, ",".join(tags), 
                 private)

        export_child_ref_list(db, "family", handle, "child_ref", child_ref_list)
        export_list(db, "family", handle, "note", note_list)
        export_attribute_list(db, "family", handle, attribute_list)
        export_citation_list(db, "family", handle, citation_list)
        export_media_ref_list(db, "family", handle, media_list)

        # Event Reference information
        for event_ref in event_ref_list:
            export_event_ref(db, "family", handle, event_ref)
            
        # -------------------------------------
        # LDS 
        # -------------------------------------
        for ldsord in lds_seal_list:
            export_lds(db, "family", handle, ldsord)

        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Repository
    # ---------------------------------
    for repository_handle in database.iter_repository_handles():
        repository = database.get_repository_from_handle(repository_handle)
        if repository is None:
            continue
        (handle, gid, the_type, name, note_list,
         address_list, urls, change, private) = repository.serialize()

        db.query("""INSERT INTO repository (
                 handle, 
                 gid, 
                 the_type0, 
                 the_type1,
                 name, 
                 change, 
                 private) VALUES (?,?,?,?,?,?,?);""",
                 handle, gid, the_type[0], the_type[1],
                 name, change, private)
        
        export_list(db, "repository", handle, "note", note_list)
        export_url_list(db, "repository", handle, urls)

        for address in address_list:
            export_address(db, "repository", handle, address)

        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Place 
    # ---------------------------------
    for place_handle in database.iter_place_handles():
        place = database.get_place_from_handle(place_handle)
        if place is None:
            continue
        (handle, gid, title, long, lat,
         main_loc, alt_location_list,
         urls,
         media_list,
         citation_list,
         note_list,
         change, private) = place.serialize()

        db.query("""INSERT INTO place (
                 handle, 
                 gid, 
                 title, 
                 long, 
                 lat, 
                 change, 
                 private) values (?,?,?,?,?,?,?);""",
                 handle, gid, title, long, lat,
                 change, private)

        export_url_list(db, "place", handle, urls)
        export_media_ref_list(db, "place", handle, media_list)
        export_citation_list(db, "place", handle, citation_list)
        export_list(db, "place", handle, "note", note_list) 

        # Main Location with parish:
        # No need; we have the handle, but ok:
        export_location(db, "place_main", handle, main_loc)
        # But we need to link these:
        export_location_list(db, "place_alt", handle, alt_location_list)

        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Citation
    # ---------------------------------
    for citation_handle in database.iter_citation_handles():
        citation = database.get_citation_from_handle(citation_handle)
        if citation is None:
            continue
        #(handle, gid, title,
        # author, pubinfo,
        # note_list,
        # media_list,
        # abbrev,
        # change, datamap,
        # reporef_list,
        # private) 
        (handle,                           #  0
         gid,                        #  1
         date, #  2
         page,                    #  3
         confidence,                       #  4
         source_handle,                    #  5
         note_list,              #  6
         media_list,             #  7
         datamap,                          #  8
         change,                           #  9
         private) = citation.serialize()
        db.query("""INSERT into citation (
                 handle, 
                 gid, 
                 source_handle,
                 confidence,
                 page,
                 change,
                 private
                 ) VALUES (?,?,?,?,?,?,?);""",
                 handle, 
                 gid,
                 source_handle,
                 confidence,
                 page,
                 change,
                 private)
        export_datamap_dict(db, "citation", handle, datamap)
        export_date(db, "citation", handle, date)
        export_list(db, "citation", handle, "note", note_list) 
        export_media_ref_list(db, "citation", handle, "media", media_list) 
        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Source
    # ---------------------------------
    for source_handle in database.iter_source_handles():
        source = database.get_source_from_handle(source_handle)
        if source is None:
            continue
        (handle, gid, title,
         author, pubinfo,
         note_list,
         media_list,
         abbrev,
         change, datamap,
         reporef_list,
         private) = source.serialize()

        export_source(db, handle, gid, title, author, pubinfo, abbrev, change, private)
        export_list(db, "source", handle, "note", note_list) 
        export_media_ref_list(db, "source", handle, media_list)
        export_datamap_dict(db, "source", handle, datamap)
        export_repository_ref_list(db, "source", handle, reporef_list)
        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Media
    # ---------------------------------
    for media_handle in database.iter_media_object_handles():
        media = database.get_object_from_handle(media_handle)
        if media is None:
            continue
        (handle, gid, path, mime, desc,
         attribute_list,
         citation_list,
         note_list,
         change,
         date,
         tags,
         private) = media.serialize()

        db.query("""INSERT INTO media (
            handle, 
            gid, 
            path, 
            mime, 
            desc,
            change, 
            tags, 
            private) VALUES (?,?,?,?,?,?,?,?);""",
                 handle, gid, path, mime, desc, 
                 change, ",".join(tags), private)
        export_date(db, "media", handle, date)
        export_list(db, "media", handle, "note", note_list) 
        export_citation_list(db, "media", handle, citation_list)
        export_attribute_list(db, "media", handle, attribute_list)
        count += 1
        callback(100 * count/total)

    # ---------------------------------
    # Tags
    # ---------------------------------
    for tag_handle in database.iter_tag_handles():
        tag_object = database.get_tag_from_handle(tag_handle)
        if tag_object is None:
            continue
        (handle, name, color, priority, change) = tag_object.serialize()
        db.query("""INSERT INTO tag (
            handle, 
            name,
            color,
            priority,
            change) VALUES (?,?,?,?,?);""",
                 handle, name, color, priority, change)
        count += 1
        callback(100 * count/total)

    db.batch = False # turn off batch processing
    db.db.commit() # commit all changes

    total_time = time.time() - start
    msg = ngettext('Export Complete: %d second','Export Complete: %d seconds', total_time ) % total_time
    print msg
    return True

# Future ideas
# Also include meta:
#   Bookmarks
#   Header - researcher info
#   Name formats
#   Namemaps?
#   GRAMPS Version #, date, exporter
