



def insert_vegobjekt(mydb, data):

    sql = """
    INSERT INTO vegobjekt (
        id,
        href,
        type_id,
        type_navn,
        versjon,
        startdato,
        sist_modifisert
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    mydb_cursor = mydb.cursor()
    
    values = (
        data["id"],
        data.get("href"),
        data["metadata"]["type"]["id"],
        data["metadata"]["type"]["navn"],
        data["metadata"]["versjon"],
        data["metadata"]["startdato"],
        data["metadata"]["sist_modifisert"][:-1]
    )

    mydb_cursor.execute(sql, values)
    mydb.commit()

    mydb_cursor.close()
    

def insert_vegobjekt_egenskap(mydb, data,vegobjekt_id):
                                
    
    sql = """
    INSERT INTO vegobjekt_egenskap (
        vegobjekt_id,
        egenskap_id,
        navn,
        verdi_text,
        verdi_int,
        enum_id,
        egenskapstype
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    mydb_cursor = mydb.cursor()

    if data["egenskapstype"] == 'Heltall':
        values = (
            vegobjekt_id,
            data["id"],
            data["navn"],
            None,
            data["verdi"],
            data.get('enum_id'),
            data["egenskapstype"],
        )
    else:
        values = (
            vegobjekt_id,
            data["id"],
            data["navn"],
            data["verdi"],
            None,
            data.get('enum_id'),
            data["egenskapstype"],
        )

    mydb_cursor.execute(sql, values)
    mydb.commit()

    mydb_cursor.close()


# insert_vegobjekt(mydb,objekter[0])
# for e in objekter[0]['egenskaper']:
#     insert_vegobjekt_egenskap(mydb,e,objekter[0]['id'])
def insert_vegobjekt_lokasjon(mydb, data,vegobjekt_id):

    sql = """
    INSERT INTO vegobjekt_lokasjon (
        vegobjekt_id,
        lengde
    )
    VALUES (%s, %s)
    """
    mydb_cursor = mydb.cursor()
    
    values = (
        vegobjekt_id,
        data.get("lengde"),
    )

    mydb_cursor.execute(sql, values)
    mydb.commit()

    mydb_cursor.execute('SELECT LAST_INSERT_ID()')
    lokasjon_id = mydb_cursor.fetchone()[0]
    
    mydb_cursor.close()

    insert_vegobjekt_vegsystemreferanse(mydb, data,lokasjon_id,vegobjekt_id)
    
    insert_vegobjekt_stedfesting(mydb, data,lokasjon_id,vegobjekt_id)

# for e in objekter[0]['egenskaper']:
#     insert_vegobjekt_egenskap(mydb,e,objekter[0]['id'])
# insert_vegobjekt_lokasjon(mydb,objekter[0]['lokasjon'],objekter[0]['id'])




def insert_vegobjekt_vegsystemreferanse(mydb, data,lokasjon_id,vegobjekt_id):

    mydb_cursor = mydb.cursor()
    # mydb_cursor.execute('SELECT LAST_INSERT_ID()')
    # lokasjon_id = mydb_cursor.fetchone()[0]

    sql = """
    INSERT INTO vegobjekt_vegsystemreferanse (
        lokasjon_id,
        vegkategori,
        fase,
        vegnummer,
        strekning,
        delstrekning,
        arm,
        adskilte_lop,
        trafikantgruppe,
        retning,
        fra_meter,
        til_meter,
        metrert_retning,
        kortform,
        vegobjekt_id
        
        
        
    )
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)
    """

    
    for veg_ref in data['vegsystemreferanser']:
        vegsystem = veg_ref['vegsystem']
        strekning = veg_ref['strekning']
        values = (
            lokasjon_id,
            vegsystem.get("vegkategori"),
            vegsystem.get("fase"),
            vegsystem.get("nummer"),
            strekning.get('strekning'),
            strekning.get('delstrekning'),
            strekning.get('arm'),
            strekning.get('adskilte_løp'),
            strekning.get('trafikantgruppe'),
            strekning.get('retning'),
            strekning.get('fra_meter'),
            strekning.get('til_meter'),
            veg_ref['metrertLokasjon'].get('retning'),
            veg_ref.get('kortform'),
            vegobjekt_id
        )

    
        mydb_cursor.execute(sql, values)
        
    mydb.commit()

    mydb_cursor.close()


# insert_vegobjekt_lokasjon(mydb,objekter[0]['lokasjon'],objekter[0]['id'])

def insert_vegobjekt_stedfesting(mydb, data,lokasjon_id,vegobjekt_id):

    mydb_cursor = mydb.cursor()
    # mydb_cursor.execute('SELECT LAST_INSERT_ID()')
    # last_id = mydb_cursor.fetchone()[0]

    sql = """
    INSERT INTO vegobjekt_stedfesting (
        lokasjon_id,
        type,
        veglenkesekvensid,
        startposisjon,
        sluttposisjon,
        retning,
        kortform,
        vegobjekt_id  
    )
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s)
    """

    
    stedfestinger = data['stedfestinger']
    for sted in stedfestinger:
        
        values = (
            lokasjon_id,
            sted.get('type'),
            sted.get("veglenkesekvensid"),
            sted.get("startposisjon"),
            sted.get('sluttposisjon'),
            sted.get('retning'),
            sted.get('kortform'),
            vegobjekt_id
        )

    
        mydb_cursor.execute(sql, values)
        
    mydb.commit()

    mydb_cursor.close()



def insert_vegobjekt_vegsegment(mydb, data,vegobjekt_id):

    mydb_cursor = mydb.cursor()
    # mydb_cursor.execute('SELECT LAST_INSERT_ID()')
    # last_id = mydb_cursor.fetchone()[0]
    vegobjekt_vegsegment_id = []
    sql = """
    INSERT INTO vegobjekt_vegsegment (
        vegobjekt_id,
        veglenkesekvensid,
        startposisjon,
        sluttposisjon,
        lengde,
        retning,
        veglenketype,
        detaljnivaa,
        typeveg,
        typeveg_sosi,
        startdato,
        kommune,
        fylke
        
    )
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
    for veg in data:
        values = (
            vegobjekt_id,
            veg.get('veglenkesekvensid'),
            veg.get("startposisjon"),
            veg.get('sluttposisjon'),
            veg.get('lengde'),
            veg.get('retning'),
            veg.get('veglenkeType'),
            veg.get('detaljnivå'),
            veg.get('typeVeg'),
            veg.get('typeVeg_sosi'),
            veg.get('startdato'),
            veg.get('kommune'),
            veg.get('fylke')

        )

    
        mydb_cursor.execute(sql, values)
        
        mydb.commit()
    
        mydb_cursor.execute('SELECT LAST_INSERT_ID()')
        last_id = mydb_cursor.fetchone()[0]
        vegobjekt_vegsegment_id.append(last_id)
    
    mydb_cursor.close() 
    insert_vegobjekt_vegsegment_vegsystemreferanse(mydb,data,vegobjekt_vegsegment_id,vegobjekt_id)

    

# insert_vegobjekt_vegsegment(mydb, objekter[0]['vegsegmenter'],objekter[0]['id'])


def insert_vegobjekt_vegsegment_vegsystemreferanse(mydb, data,vegobjekt_vegsegment_id,vegobjekt_id):

    mydb_cursor = mydb.cursor()
    # mydb_cursor.execute('SELECT LAST_INSERT_ID()')
    # last_id = mydb_cursor.fetchone()[0]

    sql = """
    INSERT INTO vegobjekt_vegsegment_vegsystemreferanse (
        vegsegment_id,
        vegkategori,
        fase,
        vegnummer,
        strekning,
        delstrekning,
        arm,
        adskilte_lop,
        trafikantgruppe,
        retning,
        fra_meter,
        til_meter,
        kortform,
        vegobjekt_id
        
        
    )
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s)
    """


    
    for veg_ref,vegsegment_id in zip(data,vegobjekt_vegsegment_id):
        vegsystem = veg_ref['vegsystemreferanse']['vegsystem']
        strekning = veg_ref['vegsystemreferanse']['strekning']
        values = (
            vegsegment_id,
            vegsystem.get("vegkategori"),
            vegsystem.get("fase"),
            vegsystem.get("nummer"),
            strekning.get('strekning'),
            strekning.get('delstrekning'),
            strekning.get('arm'),
            strekning.get('adskilte_løp'),
            strekning.get('trafikantgruppe'),
            strekning.get('retning'),
            strekning.get('fra_meter'),
            strekning.get('til_meter'),
            veg_ref['vegsystemreferanse'].get('kortform'),
            vegobjekt_id
        )

        mydb_cursor.execute(sql, values)
        
    mydb.commit()

    mydb_cursor.close() 
