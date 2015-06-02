#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2015 Douglas Blank <doug.blank@gmail.com>
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

plg = newplugin()
plg.id    = 'dbapi'
plg.name  = _("DB-API 2.0")
plg.name_accell  = _("DB-_API 2.0")
plg.description =  _("DB-API 2.0 Database Backend")
plg.version = '1.0'
plg.gramps_target_version = "5.0"
plg.status = STABLE
plg.fname = 'dbapi.py'
plg.ptype = DATABASE
plg.databaseclass = 'DBAPI'