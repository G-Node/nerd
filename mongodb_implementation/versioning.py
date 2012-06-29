from elements.section import Section
from mapper import Mapper

class Version:

    def __init__(self)
        self.m = Mapper()

    def save_section(self, section):
    	#create new section
    	s = Section()
    
        s.name       = section.name
        s.type_name  = section.type_name
        s.reference  = section.reference
        s.definition = section.definition
        s.repository = section.repository
        s.mapping    = section.mapping
        s.link       = section.link
        s.include    = section.include
        s.isLatest   = True
        
        # now that section will not appear in search results
        section.isLatest = False
    
        self.m._rewrite_properties(section, target_section)
    
        # recursively add subsections
        for section in source_section.sections:
            s.subsections.append(self.save_section(section))
            
            
        s.sid()
    
        # parent hash changed after subsections were added
        # so parent hash need to be updated for every subsection
        for section in s.subsections:
            temp = Section.objects(object_id=section)[0]
            temp.parent = s.sid()
            temp.save()   
    
        # save section in database
        s.save()    