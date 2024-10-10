def check_for_selection(layer_name):
    """
    Checks if a layer has any selected features.
    
    Args:
    layer_name (str): Layer to be checked for active selection.
    """
    
    desc = arcpy.Describe(layer_name)
    if desc.FIDSet:
        return True
    else:
        return False
