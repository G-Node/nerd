from elements.section import LatestSection, OldSection, TempSection
from elements.property import Property
from elements.value import Value
from elements.root import Root

class Version:

    def __init__(self):
        self.to_delete = []

    def clear_trash(self):
        
        for s in self.to_delete:
            s.delete()

        self.to_delete = []

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
            r.sections.append(self.save_section(LatestSection.objects(object_id = sec)[0], "old"))

        r.save()

    def save_section(self, section, section_type):
        #create new section
        if (section_type == "latest"):
            s = LatestSection()
            print "[[[LATEST]]]"
        elif (section_type == "old"):
            s = OldSection()
            print "{{{OLD}}}"
        else:
            s = TempSection()
            print "(((TEMP)))"

        s.object_id  = section.object_id
        # print "OBJECT_ID: " + str(s.object_id)

        s.name       = section.name
        # print "NAME: " + str(s.name)

        s.type_name  = section.type_name
        s.reference  = section.reference
        s.definition = section.definition
        s.repository = section.repository
        s.mapping    = section.mapping
        s.link       = section.link
        s.include    = section.include

        s.parent     = section.parent
    
        # PROPERTIES SAVE
        self.rewrite_properties(section, s)
    
        # recursively add subsections
        # print "add subsections"
        for sec in section.subsections:
            # print "subsection_id =>  " + sec
            
            if (section_type == "latest"):

                section = TempSection.objects(object_id = sec)[0]
                # print "subsection_name : " + str(section)

                s.subsections.append(self.save_section(section, "latest"))
            
            elif (section_type == "old"):
                # print "subsection_name" + str(LatestSection.objects(object_id = sec)[0].name)
                s.subsections.append(self.save_section(LatestSection.objects(object_id = sec)[0], "old"))

            else:
                # print "subsection_name" + str(OldSection.objects(object_id = sec)[0].name)
                s.subsections.append(self.save_section(OldSection.objects(object_id = sec)[0], "temp"))

        
        # print "end. (" + str(s.sid()) + ") { " + str(s.name) + " }\n"
            
        s.sid()
    
        # parent hash changed after subsections were added
        # so parent hash need to be updated for every subsection
        for subsection in s.subsections:
            # print "[[ " + str(LatestSection.objects(object_id=section)) + " ]]"
            if (section_type == "latest"):
                temp = LatestSection.objects(object_id=subsection)[0]
            elif (section_type == "old"):
                temp = OldSection.objects(object_id=subsection)[0]
            else:
                temp = TempSection.objects(object_id=subsection)[0]

            temp.parent = s.sid()
            temp.save()   

        # save section in database
        # print "SID! for: " + str(s.name)
        # print s.sid()
        # print "END!\n\n"

        s.save()

        #return id
        self.to_delete.append(section)
        print s.name + " --> DEL"
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

class VersionManager:

    def version_history(self, root_id):
        
        # extract root from 
        r = Root.objects(id=root_id)[0]
        
        print "FIRST = " + str(r.id)

        history = []
        prev = r.previous

        while (prev != None and prev != ""):
            history.append(prev)
            root = Root.objects(id=prev)[0]
            prev = root.previous

        return history

    def switch_to_last(self, root_id):

        print "\n --------------------- VERSION MANAGER ----------------------- \n"
        v = Version() 

        # take root object
        root = Root.objects(id=root_id)[0]

        # take it ancestor (as object)
        previous_root = Root.objects(id=root.previous)[0]

        # list for sections storage
        current_sections = []
        old_sections = []

        temp_collection = root.sections

        # add sections to temporary lists, recursively!
        while (len(temp_collection) != 0):
            next_collection = []
            
            for sec in temp_collection:
                current_sections.append(LatestSection.objects(object_id=sec)[0])

                for s in (LatestSection.objects(object_id=sec)[0]).subsections:
                    next_collection.append(s)

            temp_collection = next_collection

        # the same operation for ancestor

        temp_collection = previous_root.sections

        while (len(temp_collection) != 0):
            next_collection = []
            
            for sec in temp_collection:
                old_sections.append(OldSection.objects(object_id=sec)[0])

                for s in (OldSection.objects(object_id=sec)[0]).subsections:
                    next_collection.append(s)

            temp_collection = next_collection


        # old code, delete
        # for sec in previous_root.sections:
        #     old_sections.append(OldSection.objects(object_id=sec)[0])

        # move sections from old to temp

        old_counter = 0
        for s in old_sections: 
            if (TempSection.objects(object_id = s.object_id)).count() == 0:
                print "[ " + s.name + " -> TEMP]"
                v.save_section(s, "temp")
                # s.delete()
                # print "latest del"
                old_counter += 1

        # move sections from latest to old

        current_counter = 0
        for s in current_sections:
            if (OldSection.objects(object_id = s.object_id)).count() == 0:
                print "[ " + s.name + " -> OLD]"
                v.save_section(s, "old")
                # s.delete()
                # print "old del"
                current_counter += 1

        # move sections from temp to latest
        for x in range(0,7):
            print "----------------------"

        temp_counter = 0
        for sec in TempSection.objects():
            print str(sec.id) + " : " + str(sec.name) + " : " + str(sec.object_id)
            for subsec in sec.subsections:
                print "sub:  " + subsec
            print " "
            temp_counter += 1

        print "~~~ \n"
        print "old_counter == " + str(old_counter)
        print "current_counter == " + str(current_counter)
        print "temp_counter == " + str(temp_counter)
        print "current_sections == " + str(len(old_sections))
        print "old_sections == " + str(len(current_sections))

        for s in TempSection.objects():
            # print "s.name == " + str(s.name)
            if (LatestSection.objects(object_id = s.object_id)).count() == 0:
                print "[ " + s.name + " -> LATEST]"
                v.save_section(s, "latest")
                # s.delete()
                # print "temp del"
        
        v.clear_trash()