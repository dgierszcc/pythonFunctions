def update_fullname_based_on_source(source_fc, update_fc, update_field, source_field1, source_field2, match_field):
  """
  Updates a field in a feature class based on values from another feature class or table.
  Checks update field in reverse and only updates first value it finds.
  Originally used to change street type abbreviations to full street type.

  Args:
      workspace (str): Path to the workspace that contains the data
      source_fc (str): Path to the source feature class.
      update_fc (str): Path to the feature class with the field to update.
      update_field (str): Name of the field in update_fc to update.
      source_field1 (str): Name of the field in the source_fc to match with match_field.
      source_field2 (str): Name of the field in the source_fc to get the update value.
      match_field (str): Name of the field in update_fc to match with source_field1.
  """

  # Enable overwrite outputs
  arcpy.env.overwriteOutput = True

  # Create update cursor for the feature class to update
  update_cursor = arcpy.UpdateCursor(update_fc)

  # Create search cursors for source feature classes
  source1_cursor = arcpy.SearchCursor(source_fc)
  source2_cursor = arcpy.SearchCursor(source_fc)

  # Create dictionary to store source_field1 values and corresponding source_field2 values
  source_value_dict = {}
  for row in source1_cursor:
    source_value_dict[row.getValue(source_field1)] = row.getValue(source_field2)
  del source1_cursor  # Close unnecessary cursor

  # Update features in the update feature class
  cnt = 0
  newName = ''
  for row in update_cursor:
    existName = row.getValue(match_field)
    if existName is None:
        splitName = "None"
    else:
        splitName = existName.split()
    i = 0    
    for n in reversed(splitName):
        if n in source_value_dict and i == 0:
            name = source_value_dict[n]
            newName = name + ' ' + newName
            i += 1
        else:
            newName = n + ' ' + newName
    newName = newName.strip()
    row.setValue(match_field,newName)
    update_cursor.updateRow(row)
    newName = ''
    #cnt +=1
    #print(cnt, end='\r')

  # Delete cursors
  del update_cursor
  del source2_cursor

  print("Field update complete.")
