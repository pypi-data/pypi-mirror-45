"""

This module is not yet ready to be used for adapters.

Here the logic should be placed that allows the application to draw already
existing relationships on the diagram when a model element is added (e.g.
by drag and drop).
"""

from zope import component


###class AssociationRelationship(Relationship):
###    """Relationship for associations.
###    """
###    def relationship(self, line, head_subject = None, tail_subject = None):
###        # First check if we do not already contain the right subject:
###        if line.subject:
###            end1 = line.subject.memberEnd[0]
###            end2 = line.subject.memberEnd[1]
###            if (end1.type is head_type and end2.type is tail_type) \
###               or (end2.type is head_type and end1.type is tail_type):
###                return
###
###        # Find all associations and determine if the properties on the
###        # association ends have a type that points to the class.
###        Association = UML.Association
###        for assoc in resource(UML.ElementFactory).itervalues():
###            if isinstance(assoc, Association):
###                #print 'assoc.memberEnd', assoc.memberEnd
###                end1 = assoc.memberEnd[0]
###                end2 = assoc.memberEnd[1]
###                if (end1.type is head_type and end2.type is tail_type) \
###                   or (end2.type is head_type and end1.type is tail_type):
###                    # check if this entry is not yet in the diagram
###                    # Return if the association is not (yet) on the canvas
###                    for item in assoc.presentation:
###                        if item.canvas is line.canvas:
###                            break
###                    else:
###                        return assoc
###        return None
