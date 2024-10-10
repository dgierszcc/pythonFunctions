def removeAttributeValue(layer,fields,value):
  """
  Takes the provided layer, checks the provided field for the provided value.
  If the layer has the value in any of the fields, it sets null.

  Args:
    layer (str): Layer to be checked.
    fields(list): List of fields to be checked.
    value(string): Value to be checked for.
  """

  for field in fields:
      arcpy.management.SelectLayerByAttribute(
          in_layer_or_view=layer,
          selection_type="NEW_SELECTION",
          where_clause=field + " = " + value,
          invert_where_clause=None
      )
      if check_for_selection(layer):
          print(f'Selected all {layer}s with a {field} value of {value}, setting value to None.')
          arcpy.management.CalculateField(
              in_table=cleStreets,
              field=field,
              expression="None",
              expression_type="PYTHON3",
              code_block="",
              field_type="TEXT",
              enforce_domains="NO_ENFORCE_DOMAINS"
          )
          print(f'CalculateField for {layer} attribute {field} complete.')
      else:
          print(f'{layer} has no selection. CalculateField not performed.')
