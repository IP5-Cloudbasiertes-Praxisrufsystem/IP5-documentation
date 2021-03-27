# The following lines are there to calculate the progress percentage.
with Bar('Processing .json files', max=np.shape(json_files)[0]) as bar:
    for file_name in json_files:
        file_exists = os.path.isfile(file_name)
        if file_exists:
            df = pd.read_json(file_name, lines=False)
            doctype = '42'
            publish=False
            # The following part looks for an existing 
            # identifier -> uri.  If there is none, it will not
            # go into the .ris file.
            for i in range(df.count()[0]):
                if (df.iloc[i][0]['element']=='identifier' 
                    and df.iloc[i][0]['qualifier']=='uri'):
                    publish = True
            # If the previous part gave a result and the doctype is in
            # our list, it is written out as follows:
            if (doctype in ris_types) and publish:
                # First use the right mapping
                ris_map = ris_maps[doctype]
                # First line of RIS entry
                print(ris_types[doctype],file=f)
                # The document ID is in the .json file name, we extract it
                # and write it into the RIS line M2
                ident = re.findall(match_ID,file_name)[0]
                print('M2  - Item ID: %s'%(ident,),file=f)
                # The following is necessary because without a subtitle, we
                # need to write out 'title', but with a subtitle it is 
                # 'title : subtitle'
                title = ''
                subtitle = ''
                for i in range(df.count()[0]):
                    el = '%s -> %s'%(df.loc[i][0]['element'],df.loc[i][0]['qualifier'])
                    if (el=='title -> None'):
                        title = df.loc[i][0]['text_value']
                    if (el=='subtitle -> None'):
                        subtitle = df.loc[i][0]['text_value']
                    if el in ris_map:
                        print('%s%s'%(ris_map[el],df.loc[i][0]['text_value']),
                              file=f)
                if (subtitle == ''):
                    print('TI  - %s'%(title,),file=f)
                else:
                    print('TI  - %s : %s'%(title,subtitle),file=f)
                    # some debugging: this catches the many database errors
                    # where journasl names are in the suntitle field.
                    if (doctype == '01'):
                        print('Journal name in subtitle? --- [%s : %s]'%
                              (title,subtitle),file=g)
                # Now write out which collection something belongs to, but 
                # since there are entries that do not belong to any collection
                # in the collection2id database, we have to try whether this
                # works, and if it is not in the database, catch the key error
                # and instead write N.A. as the collection ID.
                try:
                    print('M2  - Collection ID: %s'%(c2ii.loc[ident][0],),file=f)
                except KeyError: 
                    print('M2  - Collection ID: %s'%('N.A.',),file=f)
                # Then the RIS record ends with 'ER  -' and an empty line.
                # The empty line is not required, but makes it easier for 
                # humans to look at the .ris file.
                print('ER  - \n',file=f)
            # This is it, the progress bar can progress.
            bar.next()