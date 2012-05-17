from odml.tools.xmlparser import load

from elements.value import Value
from elements.property import Property
from elements.section import Section
from elements.root import Root

class Mapper():
    def to_database(self, source_file):
        
        r = Root()

        odml_root = load(source_file)

        r.author     = odml_root.author
        r.date       = odml_root.date
        r.repository = odml_root.repository
        r.version    = odml_root.version

        for section in odml_root.sections:
            s = self._save_section(section, None)
            r.sections.append(s)
            # print "$$ root"

        r.save()

    def _save_section(self, source, parent):

        s = Section()

        s.parent = parent

        s.name       = source.name
        s.type_name  = source.type
        s.reference  = source.reference
        s.definition = source.definition
        s.repository = source.repository
        s.mapping    = source.mapping
        s.link       = source.link
        s.include    = source.include

        for section in source.sections:
            s.subsections.append(self._save_section(section, None))
            # print "$$ in"

        s.sid()

        for section in s.subsections:
            temp = Section.objects(object_id=section)[0]
            temp.parent = s.sid()
            temp.save()
            # print "$$ " + s.name +  s.sid()

        s.sid()
        s.save()

        # TODO: rewrite properties

        return s.sid()