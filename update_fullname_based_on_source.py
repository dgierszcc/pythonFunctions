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

  '''
  Use this block if you have need to use a different source to match
  # Create dictionary to store source_field1 values and corresponding source_field2 values
  source_value_dict = {}
  for row in source1_cursor:
    source_value_dict[row.getValue(source_field1)] = row.getValue(source_field2)
  del source1_cursor  # Close unnecessary cursor
  '''
  #Built in dictionary source
  source_value_dict = {'Aly': 'Alley', 'Anx': 'Anex', 'Arc': 'Arcade', 'Ave': 'Avenue',
  'Byu': 'Bayou', 'Bch': 'Beach', 'Bnd': 'Bend', 'Blf': 'Bluff', 'Blfs': 'Bluffs',
  'Btm': 'Bottom', 'Blvd': 'Boulevard', 'Br': 'Branch', 'Brg': 'Bridge', 'Brk': 'Brook',
  'Brks': 'Brooks', 'Bg': 'Burg', 'Bgs': 'Burgs', 'Byp': 'Bypass', 'Cp': 'Camp',
  'Cyn': 'Canyon', 'Cpe': 'Cape', 'Cswy': 'Causeway', 'Ctr': 'Center', 'Ctrs': 'Centers',
  'Cir': 'Circle', 'Cirs': 'Circles', 'Clf': 'Cliff', 'Clfs': 'Cliffs', 'Clb': 'Club',
  'Cmn': 'Common', 'Cmns': 'Commons', 'Coll': 'Collector', 'Conn': 'Connector',
  'Cor': 'Corner', 'Cors': 'Corners', 'Crse': 'Course', 'Ct': 'Court', 'Cts': 'Courts',
  'Cv': 'Cove', 'Cvs': 'Coves', 'Crk': 'Creek', 'Cres': 'Crescent', 'Crst': 'Crest',
  'Xing': 'Crossing', 'Xrd': 'Crossroad', 'Xrds': 'Crossroads', 'Curv': 'Curve',
  'Dl': 'Dale', 'Dm': 'Dam', 'Dv': 'Divide', 'Dr': 'Drive', 'Drs': 'Drives',
  'Est': 'Estate', 'Ests': 'Estates', 'Expy': 'Expressway', 'Ext': 'Extension',
  'Exts': 'Extensions', 'Fall': 'Fall', 'Fls': 'Falls', 'Fry': 'Ferry', 'Fld': 'Field',
  'Flds': 'Fields', 'Flt': 'Flat', 'Flts': 'Flats', 'Frd': 'Ford', 'Frds': 'Fords',
  'Frst': 'Forest', 'Frg': 'Forge', 'Frgs': 'Forges', 'Frk': 'Fork', 'Frks': 'Forks',
  'Ft': 'Fort', 'Fwy': 'Freeway', 'Gdn': 'Garden', 'Gdns': 'Gardens', 'Gtwy': 'Gateway',
  'Gln': 'Glen', 'Glns': 'Glens', 'Grn': 'Green', 'Grns': 'Greens', 'Grv': 'Grove',
  'Grvs': 'Groves', 'Hbr': 'Harbor', 'Hbrs': 'Harbors', 'Hvn': 'Haven', 'Hts': 'Heights',
  'Hwy': 'Highway', 'Hl': 'Hill', 'Hls': 'Hills', 'Holw': 'Hollow', 'Inlt': 'Inlet',
  'Is': 'Island', 'Iss': 'Islands', 'Isle': 'Isle', 'Jct': 'Junction', 'Jcts': 'Junctions',
  'Ky': 'Key', 'Kys': 'Keys', 'Knl': 'Knoll', 'Knls': 'Knolls', 'Lk': 'Lake', 'Lks': 'Lakes',
  'Land': 'Land', 'Lndg': 'Landing', 'Ln': 'Lane', 'Lgt': 'Light', 'Lgts': 'Lights',
  'Lf': 'Loaf', 'Lck': 'Lock', 'Lcks': 'Locks', 'Ldg': 'Lodge', 'Loop': 'Loop',
  'Mall': 'Mall', 'Mnr': 'Manor', 'Mnrs': 'Manors', 'Mdw': 'Meadow', 'Mdws': 'Meadows',
  'Mews': 'Mews', 'Ml': 'Mill', 'Mls': 'Mills', 'Msn': 'Mission', 'Mtwy': 'Motorway',
  'Mt': 'Mount', 'Mtn': 'Mountain', 'Mtns': 'Mountains', 'Nck': 'Neck', 'Ofrp': 'Offramp',
  'Onrp': 'Onramp', 'Orch': 'Orchard', 'Oval': 'Oval', 'Opas': 'Overpass', 'Park': 'Park',
  'Parks': 'Parks', 'Pkwy': 'Parkway', 'Pkwys': 'Parkways', 'Pass': 'Pass',
  'Psge': 'Passage', 'Path': 'Path', 'Pike': 'Pike', 'Pne': 'Pine', 'Pnes': 'Pines',
  'Pl': 'Place', 'Pln': 'Plain', 'Plns': 'Plains', 'Plz': 'Plaza', 'Pt': 'Point',
  'Pts': 'Points', 'Prt': 'Port', 'Prts': 'Ports', 'Pr': 'Prairie', 'Radl': 'Radial',
  'Ramp': 'Ramp', 'Rnch': 'Ranch', 'Rpd': 'Rapid', 'Rpds': 'Rapids', 'Rst': 'Rest',
  'Rdg': 'Ridge', 'Rdgs': 'Ridges', 'Riv': 'River', 'Rd': 'Road', 'Rds': 'Roads',
  'Rte': 'Route', 'Row': 'Row', 'Rue': 'Rue', 'Run': 'Run', 'Shl': 'Shoal',
  'Shls': 'Shoals', 'Shr': 'Shore', 'Shrs': 'Shores', 'Skwy': 'Skyway', 'Spg': 'Spring',
  'Spgs': 'Springs', 'Spur': 'Spur', 'Spurs': 'Spurs', 'Sq': 'Square', 'Sqs': 'Squares',
  'Sta': 'Station', 'Stra': 'Stravenue', 'Strm': 'Stream', 'St': 'Street',
  'Sts': 'Streets', 'Smt': 'Summit', 'Ter': 'Terrace', 'Trwy': 'Throughway',
  'Trce': 'Trace', 'Trak': 'Track', 'Trfy': 'Trafficway', 'Trl': 'Trail', 'Trlr': 'Trailer',
  'Tunl': 'Tunnel', 'Tpke': 'Turnpike', 'Upas': 'Underpass', 'Un': 'Union', 'Uns': 'Unions',
  'Vly': 'Valley', 'Vlys': 'Valleys', 'Via': 'Viaduct', 'Vw': 'View', 'Vws': 'Views',
  'Vlg': 'Village', 'Vlgs': 'Villages', 'Vl': 'Ville', 'Vis': 'Vista', 'Walk': 'Walk',
  'Walks': 'Walks', 'Wall': 'Wall', 'Way': 'Way', 'Ways': 'Ways', 'Wl': 'Well', 'Wls': 'Wells'}

  # Update features in the update feature class
  cnt = 0                                           #create a counter variable
  newName = ''                                      #create new name variable
  for row in update_cursor:
    existName = row.getValue(match_field)           #get the existing value
    if existName is None:                           #check for nulls
        continue                                    #skip if null    
    else:           
        splitName = existName.split()               #else split it into a list
    i = False                                       #create a flag variable
    for n in reversed(splitName):                   #flip the name list to check from the nd
        if n in source_value_dict and i == False:   #check if the name list item is in the source dictionary and check if it's the first one found
            name = source_value_dict[n]             #grab the value using the key
            newName = name + ' ' + newName          #start building the new name
            i = True                                #flip the flag to skip all other parts of the name list
        else:
            newName = n + ' ' + newName             #if it's not in the source dictionary add to the new name as is
    newName = newName.strip()                       #get rid of any extraneous whitespace
    row.setValue(match_field,newName)               #set the match field to the new name
    update_cursor.updateRow(row)                    #udpate the row
    newName = ''                                    #reset the new name
    #cnt +=1                                        #optional counter, does not always work as expected
    #print(cnt, end='\r')                           #print counter

  # Delete cursors                              
  del update_cursor
  del source2_cursor

  print("Field update complete.")
