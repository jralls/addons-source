#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2016 John Ralls <jralls@ceridwen.us>
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

from gramps.gen.lib import (Person, Family, Event, EventRoleType, EventType,
                            Source, Place, Citation, Note, NoteType, Date, Tag)
from gramps.gen.datehandler import displayer as date_displayer
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.simple import SimpleDoc
from gramps.version import VERSION_TUPLE
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.gettext

if VERSION_TUPLE[0] < 5:
    class HandleError(Exception):
        pass
class SourceNote:
    def __init__(self, db, source):
        self.db = db
        if not source:
            raise RunTimeError("Citation has no source reference.")
        if isinstance(source, str):
            try:
                source = db.get_source_from_handle(source)
                if not source:
                    raise RunTimeError("Citation source handle invalid.")
            except HandleError:
                raise RunTimeError("Citation source handle invalid.")
        self.source = source
        self.first_ref = True

    def format(self):
        '''
        Return a full citation for the first use and a short citation (the
        abbrev field if it's not empty, otherwise the title) for subsequent
        uses.
        '''
        retval = ''
        if self.first_ref:
            retval = '{auth}, "{title}", {pub}'
            retval = retval.format(auth=self.source.get_author(),
                                   title=self.source.get_title(),
                                   pub=self.source.get_publication_info())
            self.first_ref = False
        elif self.source.get_abbreviation():
            retval = self.source.get_abbreviation()
        else:
            retval = '"{title}"'.format(title=self.source.get_title())

        return retval

class CitationNote:
    def __init__(self, db, cite, sourcenote):
        if not cite:
            raise RunTimeError("Can't init CitationNote with null citation.")
        if isinstance(cite, str):
            try:
                cite = db.get_citation_from_handle(cite)
                if not cite:
                    raise RunTimeError("Invalid Citation Handle.")
            except HandleError:
                raise RunTimeError("Invalid Citation Handle.")
        self.cite = cite
        self.source = sourcenote
        self.first_ref = True

    def format(self):
        '''
        Create a named ref element with the citation contents for the
        first use and just the name attribute for subsequent uses.
        '''
        retval = ''
        source = None

        if self.first_ref:
            retval = '<ref name={id}>{source}, {page}</ref>'.format(
                id=self.cite.get_gramps_id(), source=self.source.format(),
                page=self.cite.get_page())
            self.first_ref = False
        else:
            retval = '<ref name={id}/>'.format(id=self.cite.get_gramps_id())
        return retval

class NoteNote:
    def __init__(self, db, note):
        if not note:
            return None
        if isinstance(note, str):
            try:
                note = db.get_note_from_handle(note)
                if not note:
                    return None
            except HandleError:
                return None
        self.note = note

    def format(self):
        return self.note.get()

class EventNote:
    def __init__(self, db, event, summary):
        if not event:
            raise RunTimeError("Can't init EventNote with null event.")
        if isinstance(event, str):
            try:
                event = db.get_event_from_handle(event)
                if not event:
                    raise RunTimeError("Invalid Event Handle.")
            except HandleError:
                raise RunTimeError("Invalid Event Handle.")
        self.event = event
        self.db = db
        self.citations = []
        self.notes = []
        self.description = event.get_description()
        for cite in event.get_citation_list():
            citation = summary.add_citation(cite)
            if citation is not None:
                self.citations.append(citation)

        for note_h in event.get_note_list():
            note = NoteNote(db, note_h)
            if note is not None:
                self.notes.append(note)

    def get_type(self):
        return self.event.get_type()

    def get_description(self):
        return self.event.get_description()

    def format(self, event_str):
        '''
        Create a string describing an event with source.
        '''
        retval = ''
        date = 'unknown'
        place = 'unknown'
        date_obj = self.event.get_date_object()
        place_h = self.event.get_place_handle()
        if date_obj:
            date = date_displayer.display(date_obj)
        try:
            if place_h:
                place_obj = self.db.get_place_from_handle(place_h)
                if place_obj:
                    place = place_displayer.display(self.db, place_obj)
        except HandleError:
            pass

        retval = _(' {e_str} on {e_date} at {e_place}.').format(e_str=event_str,
                                                                e_date=date,
                                                                e_place=place)
        for source in self.citations:
            retval += source.format()
        # Translation note: The single quotes are for wiki
        # markup. Include them in your msgstr.
        retval += '\n'.join([_("'Note: {_note}'").format(_note=note.format()) for note in self.notes])

        return retval

def find_event(event_list, type):
    events = [e for e in event_list if e.type == type]
    if not events:
        return None
    return events[0]

class WikiTreeSummary:
    '''
    Master class that collects the elements and formats the report.
    '''
    def __init__(self, db, person):
        self.db = db
        self.name = 'unknown'
        self.given = 'unknown'
        self.person = person
        self.sources = dict()
        self.citations = dict()
        self.birth = None
        self.death = None
        self.marriages = []
        self.other_events = []
        self.notes = []
        if person.primary_name:
            self.name = name_displayer.display(person)
            self.given = name_displayer.display_given(person)

        families = person.get_family_handle_list()
        for event_ref in person.get_event_ref_list():
            event = self.db.get_event_from_handle(event_ref.ref)
            event_note = EventNote(db, event, self)
            if event.type == EventType.BIRTH:
                self.birth = event_note
            elif event.type == EventType.DEATH:
                self.death = event_note
            else:
                role = event_ref.get_role()
                self.other_events.append([role, EventNote(db, event, self)])
        self.pronoun = _('He')
        self.possessive = _('His')
        if person.get_gender() == person.FEMALE:
            self.pronoun = _('She')
            self.possessive = _('Her')

        for family in families:
            marriage = self.create_marriage_event(family)
            if marriage:
                self.marriages.append(marriage)

        for note_h in self.person.get_note_list():
            note = NoteNote(db, note_h)
            if note is not None:
                self.notes.append(note)


    def add_citation(self, cite):
        '''
        We maintain master lists of citations and sources so that common
        citations generate a single footnote and subsequent uses of a
        source don't repeat the whole thing.

        '''
        if isinstance(cite, str):
            try:
                cite = self.db.get_citation_from_handle(cite)
                if not cite:
                    raise RunTimeError("Invalid Citation Handle.")
            except HandleError:
                raise RunTimeError("Invalid Citation Handle.")
        citeid = cite.get_gramps_id()
        if citeid not in self.citations:
            source = cite.get_reference_handle()
            if isinstance(source, str):
                try:
                    source = self.db.get_source_from_handle(source)
                    if not source:
                        raise RunTimeError("Citation source handle invalid.")
                except HandleError:
                    raise RunTimeError("Citation source handle invalid.")
            sourceid = source.get_gramps_id()
            if sourceid not in self.sources:
                self.sources[sourceid] = SourceNote(self.db, source)
            self.citations[citeid] = CitationNote(self.db, cite,
                                                  self.sources[sourceid]);
            return self.citations[citeid]
        return None

    def create_marriage_event(self, family_handle):
        try:
            family = self.db.get_family_from_handle(family_handle)
            if family is None:
                return None # No family, no marriage.
            father_h = family.get_father_handle()
            mother_h = family.get_mother_handle()
            if mother_h is None or father_h is None:
                return None # No marriage if there arent' two spouses.
            father = self.db.get_person_from_handle(father_h)
            mother = self.db.get_person_from_handle(mother_h)
            if father is None or mother is None:
                return None # One's a bad handle, bail out.
        except HandleError:
            return
        spouse = father
        if father == self.person:
            spouse = mother
        family_events = [self.db.get_event_from_handle(h)
                         for h in [ref.ref for ref in family.get_event_ref_list()]]
        marriage = find_event(family_events, EventType.MARRIAGE)
        if marriage:
            return spouse, EventNote(self.db, marriage, self)

    def format(self, sdoc):
        if self.birth:
            birth_str = self.birth.format(_('was born'))
        else:
            birth_str = _(' birth date and place are unknown')

        if self.marriages:
            marriage_str = self.pronoun + _(' married ') + ', '.join([m.format('{s_name}'.format(s_name=name_displayer.display(s))) for s,m in self.marriages])
        else:
            marriage_str = _(' had no known marriages')

        if self.death:
            death_str = self.death.format(_('died'))
        else:
            death_str = _(' death date and place are unknown')

        sdoc.title(_('WikiTree Summary for {name}').format(name=self.name))
        sdoc.paragraph("")
        sdoc.paragraph(_(
            '{name} {b_str}.{pp} {m_str}.{gn}{d_str}').format(name=self.name,
                                                        b_str=birth_str,
                                                        m_str=marriage_str,
                                                        pp=self.pronoun,
                                                        gn=self.given,
                                                        d_str=death_str))
        for role, event in self.other_events:
            type = glocale.get_type(event.get_type())
            desc = event.get_description()
            if role in (EventRoleType.PRIMARY, EventRoleType.FAMILY):
                event_str = _('{pp} {type} was').format(pp=self.possessive,
                                                        type=type)
            else:
                event_str = _('{pp} did {role} in {type} {desc}')
                event_str = event_str.format(pp=self.pronoun, role=role,
                                             type=type, desc=desc)
            sdoc.paragraph(event.format(event_str))

        if self.notes:
            sdoc.paragraph('')
            sdoc.paragraph('=== NOTES ===')
            sdoc.paragraph('')
            for note in self.notes:
                sdoc.paragraph(note.format())
                sdoc.paragraph('')

def run(db, doc, person):
    '''
    Write a biographical sketch with citations in WikiTree markdown.
    '''
    if not doc:
        raise RunTimeError("Can't create summary with no document to write to.")
    sdoc = SimpleDoc(doc)
    if db is None:
        sdoc.title("Error")
        sdoc.paragraph(_('Attempting to report from an invalid database!'))

    if isinstance(person, str):
        person = db.get_person_from_handle(person)
    if person is None or not isinstance(person, Person):
        sdoc.title("Error")
        sdoc.paragraph(_("No person selected to report upon."))
        raise RunTimeError("Person invalid")

    name_displayer.set_default_format(2)
    summary = WikiTreeSummary(db, person)

    summary.format(sdoc)
