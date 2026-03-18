
create_vegobjekt = """CREATE TABLE vegobjekt (
                    id BIGINT PRIMARY KEY,
                    href TEXT,
                    type_id INT,
                    type_navn VARCHAR(100),
                    versjon INT,
                    startdato DATE,
                    sist_modifisert TIMESTAMP
                );"""
    
create_vegobjekt_egenskap = """CREATE TABLE vegobjekt_egenskap (
                            vegobjekt_id BIGINT ,
                        
                            egenskap_id INT,
                            navn VARCHAR(100),
                            verdi_text TEXT,
                            verdi_int INT,
                            enum_id INT,
                            egenskapstype VARCHAR(50),
                            
                            PRIMARY KEY (vegobjekt_id, egenskap_id),
                            FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)
                        );"""


create_vegobjekt_lokasjon = """CREATE TABLE vegobjekt_lokasjon (
                            id SERIAL PRIMARY KEY,
                            vegobjekt_id BIGINT,
                            lengde DOUBLE PRECISION,
                            FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)
                        );"""
    

create_vegobjekt_kommune = """CREATE TABLE vegobjekt_lokasjon_kommune (
                                lokasjon_id INT REFERENCES vegobjekt_lokasjon(id),
                                kommune INT,
                                vegobjekt_id BIGINT,
                                PRIMARY KEY (lokasjon_id, kommune),
                                FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)
                            );"""



create_vegobjekt_vegsystemreferanse = """CREATE TABLE vegobjekt_vegsystemreferanse (
                            id SERIAL PRIMARY KEY,
                            lokasjon_id INT REFERENCES vegobjekt_lokasjon(id),
                        
                            vegkategori CHAR(1),
                            fase CHAR(1),
                            vegnummer INT,
                        
                            strekning INT,
                            delstrekning INT,
                            arm BOOLEAN,
                            adskilte_lop VARCHAR(10),
                            trafikantgruppe CHAR(1),
                            retning VARCHAR(10),
                            fra_meter DOUBLE PRECISION,
                            til_meter DOUBLE PRECISION,
                        
                            metrert_retning VARCHAR(10),
                        
                            kortform VARCHAR(50),
                            vegobjekt_id BIGINT,
                            FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)
                            
                        );"""


create_vegobjekt_stedfesting = """CREATE TABLE vegobjekt_stedfesting (
                                id SERIAL PRIMARY KEY,
                                lokasjon_id INT REFERENCES vegobjekt_lokasjon(id),
                            
                                type VARCHAR(20),
                                veglenkesekvensid BIGINT,
                                startposisjon DOUBLE PRECISION,
                                sluttposisjon DOUBLE PRECISION,
                                retning VARCHAR(10),
                                kortform VARCHAR(50),
                                vegobjekt_id BIGINT,
                                FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)
                            );"""


create_vegobjekt_vegsegment = """CREATE TABLE vegobjekt_vegsegment (
                                id SERIAL PRIMARY KEY,
                                vegobjekt_id BIGINT,
                            
                                veglenkesekvensid BIGINT,
                                startposisjon DOUBLE PRECISION,
                                sluttposisjon DOUBLE PRECISION,
                                lengde DOUBLE PRECISION,
                                retning VARCHAR(10),
                            
                                veglenketype VARCHAR(50),
                                detaljnivaa VARCHAR(100),
                                typeveg VARCHAR(100),
                                typeveg_sosi VARCHAR(100),
                            
                                startdato DATE,
                            
                                kommune INT,
                                fylke INT,
                                FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)

                            );"""


vegobjekt_vegsegment_vegsystemreferanse = """CREATE TABLE vegobjekt_vegsegment_vegsystemreferanse (
                                vegsegment_id INT PRIMARY KEY REFERENCES vegobjekt_vegsegment(id),
                            
                                vegkategori CHAR(1),
                                fase CHAR(1),
                                vegnummer INT,
                            
                                strekning INT,
                                delstrekning INT,
                                arm BOOLEAN,
                                adskilte_lop VARCHAR(10),
                                trafikantgruppe CHAR(1),
                                retning VARCHAR(10),
                                fra_meter DOUBLE PRECISION,
                                til_meter DOUBLE PRECISION,
                            
                                kortform VARCHAR(50),
                                vegobjekt_id BIGINT,
                                FOREIGN KEY (vegobjekt_id) REFERENCES vegobjekt(id)
                            );"""
    
    
    

def create_database_case1(mydb):
    mydb_cursor.execute(create_vegobjekt)
    print(mydb_cursor.fetchall())

    mydb_cursor.execute(create_vegobjekt_egenskap)
    print(mydb_cursor.fetchall())

    mydb_cursor.execute(create_vegobjekt_lokasjon)
    print(mydb_cursor.fetchall())
    
    mydb_cursor.execute(create_vegobjekt_kommune)
    print(mydb_cursor.fetchall())

    
    mydb_cursor.execute(create_vegobjekt_vegsystemreferanse)
    print(mydb_cursor.fetchall())
    
    mydb_cursor.execute(create_vegobjekt_vegsegment)
    print(mydb_cursor.fetchall())

    mydb_cursor.execute(create_vegobjekt_stedfesting)
    print(mydb_cursor.fetchall())

    mydb_cursor.execute(vegobjekt_vegsegment_vegsystemreferanse)
    mydb_cursor.execute("SHOW TABLES")
    print(mydb_cursor.fetchall())