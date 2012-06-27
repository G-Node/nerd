from elements.section import Section
from mapper import Mapper

def save_section(section):
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

    section.isLatest = False

    m = Mapper()
    m._rewrite_properties(section, target_section)

    # recursively add subsections
    for section in source_section.sections:
        s.subsections.append(self._save_section(section, None))
        
        
    s.sid()

    # parent hash changed after subsections were added
    # so parent hash need to be updated for every subsection
    for section in s.subsections:
        temp = Section.objects(object_id=section)[0]
        temp.parent = s.sid()
        temp.save()   

    # save section in database
    s.save()    