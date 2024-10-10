#check for selection
def check_for_selection(layer_name):
    """Checks if a layer has any selected features."""
    desc = arcpy.Describe(layer_name)
    if desc.FIDSet:
        return True
    else:
        return False
