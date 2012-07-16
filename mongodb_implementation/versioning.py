from elements.section import Section
from elements.property import Property
from elements.value import Value
from elements.oldRoot import oldRoot

class Version:

    def save_root(self, source_root):
        r = OldRoot()

        r.author     = source_root.author
        r.date       = source_root.date
        r.repository = source_root.repository
        r.version    = source_root.version

        for sec in source_root.sections:
            r.sections.append(self.save_section(sec))
            
    def save_section(self, source_section):
        #create new section
        s = Section()

        s.name       = source_section.name
        s.type_name  = source_section.type_name
        s.reference  = source_section.reference
        s.definition = source_section.definition
        s.repository = source_section.repository
        s.mapping    = source_section.mapping
        s.link       = source_section.link
        s.include    = source_section.include

        self.rewrite_properties(section, s)
    
        # recursively add subsections
        print "---+++"

        for sec in source_section.subsections:
            # print sec
            print sec.__class__
            s.subsections.append(self.save_section(sec))
        
        print "+++---"

        return s


    def rewrite_properties(self, source_section, target_section):
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
            self.rewrite_values(pro, p)

            # add new property to target section
            target_section.properties.append(p)

    def rewrite_values(self, source_property, target_property):
        for value in source_property.values:
            # create new value object (embedded document)
            v = Value()

            # copy value related fields
            v.value       = value.value      
            v.uncertainty =  value.uncertainty
            v.unit        =  value.unit       
            v.type_name   =  value.type_name
            v.definition  =  value.definition 
            v.reference   =  value.reference  
            v.filename    =  value.filename   
            v.encoder     =  value.encoder    
            v.checksum    =  value.checksum

            # add new object to target property values collection
            target_property.values.append(v) 