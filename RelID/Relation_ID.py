#
# Gramps - a GTK+/GNOME based genealogy program
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

"""
Display person objects
"""

#-------------------------------------------------------------------------
#
# gramps modules
#
#-------------------------------------------------------------------------

from gramps.gen.lib import Person
from gen.display.name import displayer as name_displayer
from gen.plug import Gramplet
from gramps.gen.relationship import get_relationship_calculator
import number

#------------------------------------------------------------------------
#
# The Gramplet
#
#------------------------------------------------------------------------
class IDGramplet(Gramplet):

    def init(self):
        self.set_use_markup(True)
        self.set_tooltip("Double-click on object for details")
        self.set_text("No Family Tree loaded.")

    def db_changed(self):
        self.dbstate.db.connect('person-rebuild', self.update)

    def main(self):
        self.set_text("Processing..." + "\n")
        yield True
        self.set_text("Person objects" + "\n")
        count = 0
        default_person = self.dbstate.db.get_default_person()
        plist = self.dbstate.db.get_person_handles(sort_handles=True)
        total = len(plist)
        home = name_displayer.display(default_person)
        if home:
            count += 1
            root_str = str(home) + "\n"
            self.set_text(root_str)
        
        #now determine the relation
        relationship = get_relationship_calculator()
        relationship.connect_db_signals(self.dbstate)
        
        for handle in plist:
            person = self.dbstate.db.get_person_from_handle(handle)
            name = name_displayer.display(person)
            #self.set_text("%s/%s\n" % (count + 1, total))
            if person and person != default_person and person.gender == Person.FEMALE:
                #rank, handle person, rel_str_orig, rel_fam_orig, rel_str_other, rel_fam_str
                dist = relationship.get_relationship_distance_new(
                      self.dbstate.db, default_person, person, only_birth=True)
                rel_a = dist[0][2]
                Ga = len(rel_a)
                rel_b = dist[0][4]
                Gb = len(rel_b)
                yield True
                kekule = number.get_number(Ga, Gb, rel_a, rel_b)
                value = name

                mothers = []
                mothers.append((kekule, value, Ga))
                n = 3 # starting key (mother value on sosa/kekule)
                max_level = 4 # number of generations
                # sequence = from n to wall
                wall = n * (max_level + 1) - 1 # max key
                for (key, value, level) in mothers:
                    if key != "u" and key != "0":
                        for i in range(1, max_level):
                            if level == i:
                                self.append_text("\nAncestor: ")
                                self.link(str(value) + key, 'Person', handle)
                    if key == "0": # cousines
                        self.append_text("\nAunt or Cousine: ")
                        self.link(str(value) + key , 'Person', handle)
                if kekule.startswith('-'):
                    self.append_text("\n")
                    value = "Descendant[%s] on level[%s] index n°: %s" % (kekule, Gb, count)
                    self.link(str(value) , 'Person', handle)
                    #yield False
                ## pseudo rel IDs
                #value = value + "[%s]: " % kekule + "[%s]" % Ga + kekule + "[%s]" % Gb
                count += 1
                ## title, handletype, handle
                #self.link(str(value) , 'Person', handle)
                self.append_text("", scroll_to='begin')
                if count == int(total/max_level):
                    #self.set_text("Too large database for such test")
                    yield False
