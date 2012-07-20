from odml.tools.xmlparser import load

from elements.value import Value
from elements.property import Property
from elements.section import LatestSection
from elements.root import Root

# class for mapping from odml file to documents in mongodatabase
# it needs working connection to database (mongod process)
class Mapper():
    def to_database(self, source_file):
        # create root document
        r = Root()
        
        # load odml file using python-odml module
        odml_root = load(source_file)

        # rewrite root fields
        r.author     = odml_root.author
        r.date       = odml_root.date
        r.repository = odml_root.repository
        r.version    = odml_root.version

        r.previous   = None

        # add sections to 'section' ccollection
        for section in odml_root.sections:
            s = self._save_section(section, None)
            r.sections.append(s)

        # save new object in database
        r.save()

    def _save_section(self, source_section, parent):
        # create new section document
        s = LatestSection()

        # set parent for that section
        # None means that it is section at the top of the hierarchy
        s.parent = parent

        # rewrite section related fields
        s.name       = source_section.name
        s.type_name  = source_section.type
        s.reference  = source_section.reference
        s.definition = source_section.definition
        s.repository = source_section.repository
        s.mapping    = source_section.mapping
        s.link       = source_section.link
        s.include    = source_section.include
        s.isLatest   = True
        
        # use external method for rewriting properties
        self._rewrite_properties(source_section, s)   

        # recursively add subsections
        for section in source_section.sections:
            s.subsections.append(self._save_section(section, None))

        # initialize identity hash for that section
        s.sid()

        # parent hash changed after subsections were added
        # so parent hash need to be updated for every subsection
        for section in s.subsections:
            temp = Section.objects(object_id=section)[0]
            temp.parent = s.sid()
            temp.save()   

        # save section in database
        s.save()

        # return section hash - id
        return s.sid()

    def _rewrite_properties(self, source_section, target_section):
        # copy all properties from given section
        for pro in source_section.properties:
            # create new property object (embedded document)
            p = Property()
            
            # rewirite properites relateed fields
            p.name            = pro.name 
            p.definition      = pro.definition
            p.mapping         = pro.mapping 
            p.dependency        = pro.dependency
            p.dependencyValue   = pro.dependency
            
            # use external method for rewriting values
            self._rewrite_values(pro, p)

            # add new property to target section
            target_section.properties.append(p)

    def _rewrite_values(self, source_property, target_property):
        for value in source_property.values:
            # create new value object (embedded document)
            v = Value()

            # copy value related fields
            v.value       = value._value      
            v.uncertainty =  value._uncertainty
            v.unit        =  value._unit       
            v.type_name   =  value.dtype 
            v.definition  =  value._definition 
            v.reference   =  value._reference  
            v.filename    =  value._filename   
            v.encoder     =  value._encoder    
            v.checksum    =  value.checksum

            # add new object to target property values collection
            target_property.values.append(v)     