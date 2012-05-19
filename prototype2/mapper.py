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

    def _save_section(self, source_section, parent):

        s = Section()

        s.parent = parent

        s.name       = source_section.name
        s.type_name  = source_section.type
        s.reference  = source_section.reference
        s.definition = source_section.definition
        s.repository = source_section.repository
        s.mapping    = source_section.mapping
        s.link       = source_section.link
        s.include    = source_section.include

        for section in source_section.sections:
            s.subsections.append(self._save_section(section, None))
            # print "$$ in"

        s.sid()

        for section in s.subsections:
            Section.objects.count() # FOR DEBUG
            temp = Section.objects(object_id=section)[0]
            temp.parent = s.sid()
            temp.save()
            # print "$$ " + s.name +  s.sid()

        self._rewrite_properties(source_section, s)        

        s.save()

        return s.sid()

    def _rewrite_properties(self, source_section, target_section):
        print "IN!!!!"
        for pro in source_section.properties:
            p = Property()

            p.name            = pro.name 
            p.definition      = pro.definition
            p.mapping         = pro.mapping 
            # dependency      = pro.dependency
            # dependencyValue = pro.dependency
            
            # self._rewrite_values(pro, p)

            target_section.properties.append(p)

    def _rewrite_values(self, source_property, target_property):
        for value in source_property.values:
            v = Value()

            v.value       = value._value      
            v.uncertainty =  value._uncertainty
            v.unit        =  value._unit       
            v.type_name   =  value.dtype 
            v.definition  =  value._definition 
            v.reference   =  value._reference  
            v.filename    =  value._filename   
            v.encoder     =  value._encoder    
            v.checksum    =  value.checksum 

            target_property.values.append(v)     