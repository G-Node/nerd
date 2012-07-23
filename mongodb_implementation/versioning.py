from elements.section import LatestSection, OldSection
from elements.property import Property
from elements.value import Value
from elements.root import Root

class Version:

    def save_root(self, root):
        r = Root()

        # rewirite primary fields
        r.author     = root.author
        r.date       = root.date
        r.repository = root.repository
        r.version    = root.version

        r.previous   = str(root.id)
        
        # copy sections for that root document
        for sec in root.sections:
            r.sections.append(self.save_section(LatestSection.objects(object_id = sec)[0]))

        r.save()

    def save_section(self, section):
        #create new section
        s = OldSection()

        s.object_id  = section.object_id
        print "OBJECT_ID: " + str(s.object_id)

        s.name       = section.name
        print "NAME: " + str(s.name)

        s.type_name  = section.type_name
        s.reference  = section.reference
        s.definition = section.definition
        s.repository = section.repository
        s.mapping    = section.mapping
        s.link       = section.link
        s.include    = section.include

        s.parent     = section.parent
    
        # COMMENTED PROPERTIES SAVE ! ! !
        self.rewrite_properties(section, s)
    
        # recursively add subsections
        print "add subsections"
        for sec in section.subsections:
            print "subsection_id" + str(sec)
            print "subsection_name" + str(LatestSection.objects(object_id = sec)[0].name)

            s.subsections.append(self.save_section(LatestSection.objects(object_id = sec)[0]))
        
        print "end. (" + str(s.sid()) + ") { " + str(s.name) + " }\n"
            
        s.sid()
    
        # parent hash changed after subsections were added
        # so parent hash need to be updated for every subsection
        for section in s.subsections:
            print "[[ " + str(LatestSection.objects(object_id=section)) + " ]]"
            temp = LatestSection.objects(object_id=section)[0]
            temp.parent = s.sid()
            temp.save()   

        # save section in database
        print "SID! for: " + str(s.name)
        print s.sid()
        print "END!\n\n"

        s.save()

        #return id
        return s.sid()


    def rewrite_properties(self, source_section, target_section):
        # copy all properties from given section
        for pro in source_section.properties:
            # create new property object (embedded document)
            p = Property()
            
            # rewirite properites relateed fields
            p.name              = pro.name 
            p.definition        = pro.definition
            p.mapping           = pro.mapping 
            p.dependency        = pro.dependency
            p.dependencyValue   = pro.dependencyValue
            
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