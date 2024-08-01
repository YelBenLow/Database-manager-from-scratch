import os
import random

currentPath = os.getcwd()+'\\'+'Databases'+'\\'

adatbazisok = ['személyek', 'városok', 'állatok']
for db in adatbazisok:
    if not os.path.exists(currentPath+db):
        os.mkdir(currentPath+db)


def szemelyek_db():
    gyerek_columns = 'id vezetekNev keresztNev kor email szulhely testverekSzama'
    szemelyek_vezeteknevek = ["Kovács", "Nagy", "Tóth", "Szabó", "Horváth", "Kiss", "Molnár", "Varga", "Farkas", "Balogh", "Vass"]
    szemelyek_keresztnevek = ['Bence', 'Martin', 'László', 'Péter', 'Patrik', 'Lívia', 'Natália', 'Dávid', 'Ákos', 'Noémi', 'Attila']
    szemelyek_szülhelyek = ['Nyíregyháza', 'Budapest', 'Debrecen', 'Eger', 'Miskolc', 'Győr', 'Pécs', 'Kecskemét', 'Nagyvárad']
    szemelyek_emailek = ['gmail', 'freemail', 'citromail', 'business']


    with open(currentPath+'személyek\\gyerek.txt', 'w', encoding = 'utf-8') as f:
        f.write(gyerek_columns+'\n')
        for i in range(random.randint(50, 100)):
            randomvezeteknev = random.choice(szemelyek_vezeteknevek)
            randomkeresztnev = random.choice(szemelyek_keresztnevek)
            randomszulhely = random.choice(szemelyek_szülhelyek)
            randomkor = random.randint(10, 30)
            r_ema = random.choice(szemelyek_emailek)
            randomemail = f'{randomvezeteknev}{randomkeresztnev}{randomkor}@{r_ema}.com'
            randomtestverszam = random.randint(0, 10)

            sor = f'{i} {randomvezeteknev} {randomkeresztnev} {randomkor} {randomemail} {randomszulhely} {randomtestverszam}\n'

            f.write(sor)


    szulo_columns = 'id vezetekNev keresztNev kor szulhely'

    with open(currentPath+'személyek\\szulo.txt', 'w', encoding = 'utf-8') as f:
        f.write(szulo_columns+'\n')
        for i in range(random.randint(50, 100)):
            randomvezeteknev = random.choice(szemelyek_vezeteknevek)
            randomkeresztnev = random.choice(szemelyek_keresztnevek)
            randomszulhely = random.choice(szemelyek_szülhelyek)
            randomkor = random.randint(10, 30)

            sor = f'{i} {randomvezeteknev} {randomkeresztnev} {randomkor} {randomszulhely}\n'

            f.write(sor)

    hobbi_columns = 'id szemelyid hobbinev hobbileiras'

    HobbiLista = ["Horgászat", "Főzés", "Futás", "Fotózás", "Utazás"]

    HobbiLeirasLista = [
        "Horgászat_a_természetben",
        "Kreatív_főzés_és_finom_ételek",
        "Egészséges_életmód_és_futás",
        "Fontos_pillanatok_fotózása",
        "Világ_felfedezése_utazás_közben"
    ]



    with open(currentPath+'személyek\\hobbi.txt', 'w', encoding = 'utf-8') as f:
        f.write(hobbi_columns+'\n')
        for i in range(random.randint(50, 100)):
            randomszemelyid = random.randint(0, 100)
            randomhobbi = random.choice(HobbiLista)
            randomhobbileiras = HobbiLeirasLista[HobbiLista.index(randomhobbi)]

            sor = f'{i} {randomszemelyid} {randomhobbi} {randomhobbileiras}\n'

            f.write(sor)


def varosok_db():
    varos_column = 'id varosNev orszag'

    VarosNev = [
        "Budapest", "Debrecen", "Szeged", "New_York", "Los_Angeles", "Chicago", "Tokió", "Osaka", "Nagoya", "Párizs",
        "Lyon", "Nice", "Róma", "Milánó", "Firenze", "London", "Manchester", "Birmingham", "Berlin", "München",
        "Hamburg", "Sydney", "Melbourne", "Brisbane", "Rio_de_Janeiro", "Sao_Paulo", "Brasília", "Dubai",
        "Abu_Dhabi", "Sharjah", "Peking", "Shanghai", "Guangzhou", "Moszkva", "Szentpétervár", "Novoszibirszk",
        "Delhi", "Mumbai", "Bangalore", "Bangkok", "Phuket", "Pattaya", "Káhira", "Alexandria", "Luxor", "Prága",
        "Brünn", "Ostrava", "Stockholm", "Göteborg", "Malmö", "Bécs", "Salzburg", "Innsbruck", "Istanbul", "Ankara",
        "Izmir"
    ]

    Orszag = [
        "Magyarország", "Magyarország", "Magyarország", "Egyesült_Államok", "Egyesült_Államok", "Egyesült_Államok",
        "Japán", "Japán", "Japán", "Franciaország", "Franciaország", "Franciaország", "Olaszország", "Olaszország",
        "Olaszország", "Egyesült_Királyság", "Egyesült_Királyság", "Egyesült_Királyság", "Németország", "Németország",
        "Németország", "Ausztrália", "Ausztrália", "Ausztrália", "Brazília", "Brazília", "Brazília",
        "Egyesült_Arab_Emírségek",
        "Egyesült_Arab_Emírségek", "Egyesült_Arab_Emírségek", "Kína", "Kína", "Kína", "Oroszország", "Oroszország",
        "Oroszország", "India", "India", "India", "Thaiföld", "Thaiföld", "Thaiföld", "Egyiptom", "Egyiptom",
        "Egyiptom", "Csehország", "Csehország", "Csehország", "Svédország", "Svédország", "Svédország", "Ausztria",
        "Ausztria", "Ausztria", "Törökország", "Törökország", "Törökország"
    ]

    with open(currentPath+'városok\\varos.txt', 'w', encoding = 'utf-8') as f:
        f.write(varos_column+'\n')
        for i in range(random.randint(50, 100)):
            randomvaros = random.choice(VarosNev)
            orszag = Orszag[VarosNev.index(randomvaros)]
            sor = f'{i} {randomvaros} {orszag}\n'

            f.write(sor)


    HelyNev = [
        "Hősök_tere", "Városliget", "Széchenyi_fürdő",  # Budapest
        "Central_Park", "Times_Square", "Empire_State_Building",  # New_York
        "Szenso-ji_templom", "Ueno_Park", "Skytree",  # Tokió
        "Louvre_Múzeum", "Notre-Dame_Székesegyház", "Montmartre",  # Párizs
        "Colosseum", "Spanyol_lépcsők", "Pantheon",  # Róma
        "British_Múzeum", "Londoni_Tower", "Westminster_Palota",  # London
        "Brandenburgi_Kapu", "Reichstag", "Múzeumsziget",  # Berlin
        "Sydney_Operaház", "Bondi_Beach", "Taronga_Állatkert",  # Sydney
        "Ipanema_Beach", "Cristo_Redentor", "Santa_Teresa_negyed",  # Rio_de_Janeiro
        "Dubai_Mall", "Burj_Khalifa", "Palm_Jumeirah",  # Dubai
        "Copacabana", "Corcovado-hegy", "Tijuca_Nemzeti_Park"  # Rio_de_Janeiro
    ]
    helyVarosNev = [
        "Budapest", "Budapest", "Budapest",  # Budapest
        "New_York", "New_York", "New_York",  # New_York
        "Tokió", "Tokió", "Tokió",  # Tokió
        "Párizs", "Párizs", "Párizs",  # Párizs
        "Róma", "Róma", "Róma",  # Róma
        "London", "London", "London",  # London
        "Berlin", "Berlin", "Berlin",  # Berlin
        "Sydney", "Sydney", "Sydney",  # Sydney
        "Rio_de_Janeiro", "Rio_de_Janeiro", "Rio_de_Janeiro",  # Rio_de_Janeiro
        "Dubai", "Dubai", "Dubai",  # Dubai
        "Rio_de_Janeiro", "Rio_de_Janeiro", "Rio_de_Janeiro"  # Rio_de_Janeiro
    ]
    Elmeny = {'Hősök_tere':
                  ['Nagyszerű_emlékek_a_híres_szobrok_között.',
                   'Lenyűgöző_volt_a_környező_épületek_látványa.',
                   'Kellemes_naplementét_láttam_a_teret_átszelő_séta_során.'],

              'Városliget': ['Sétálgatás_a_tó_partján_és_csónakázás_a_Vajdahunyad_vára_előtt.',
                             'A_Nagyréti_tavon_szörföztem_és_piknikeztem.',
                             'Szép_idő_volt,_jó_volt_piknikezni_a_zöld_fűben.'],

              'Széchenyi_fürdő': ['Kiváló_pihenés_és_fürdés_a_termálvizes_medencékben.',
                                  'A_szaunákban_feltöltődtem_és_ellazultam.',
                                  'Szuper_időtöltés_a_barátokkal_a_szabadtéri_medencékben.'],

              'Central_Park': ['Hosszú_séták_a_parkban_és_a_tó_partján.',
                               'Pihenés_a_fák_árnyékában_a_forró_napon.',
                               'Szuper_volt_a_futás_a_parkban_a_reggeli_órákban.'],

              'Times_Square': ['Az_éjszaka_fényei_és_a_sok_ember_nagyon_látványos_volt.',
                               'Rengeteg_üzletet_és_éttermet_néztem_meg.',
                               'Kedvenc_emlékem_az_óriás_LED_kijelzők_ragyogása_volt.'],

              'Empire_State_Building': ['Gyönyörű_kilátás_a_városra_a_tetejéről.',
                                        'A_szélvédett_kilátóról_minden_látnivalót_szemügyre_vettem.',
                                        'Az_estei_városfények_csodálatosak_voltak.'],

              'Szenso-ji_templom': ['Békés_légkörű_hely,_sok_imádkozóval.',
                                    'A_környező_piacokon_sokféle_érdekes_dolgot_találtam.',
                                    'Az_óriási_lampionok_lenyűgözőek_voltak_az_esti_fényben.'],

              'Ueno_Park': ['Sétáltam_a_parkban_és_sok_szép_növényt_láttam.',
                            'A_tavon_csónakáztam_és_a_madarakat_etettem.',
                            'A_múzeumokban_sok_érdekes_dolgot_tanultam_a_japán_kultúráról.'],

              'Skytree': ['Fantasztikus_kilátás_a_városra_a_magasságból.',
                          'A_környező_üzletekben_sok_ajándékot_vásároltam.',
                          'Az_üvegfalú_lift_látványos_élmény_volt.'],

              'Louvre_Múzeum': ['Csodálatos_műalkotásokat_láttam_a_múzeumban.',
                                'A_Mona_Lisa_hihetetlenül_lenyűgöző_volt_élőben.',
                                'Sokféle_stílusú_művészeti_alkotásban_gyönyörködtem.'],

              'Notre-Dame_Székesegyház': ['A_katedrális_lenyűgözően_szép_és_impozáns.',
                                          'Felmentem_a_toronyba_és_lenyűgöző_volt_a_kilátás.',
                                          'A_belső_tér_hangulata_igazán_megkapó_volt.'],

              'Montmartre': ['A_művészek_sora_és_a_művészeti_hangulat_lenyűgöző.',
                             'A_Sacré-Cœur_bazilika_csodálatos_épület.',
                             'A_kávézók_hangulata_magával_ragadó_volt.'],

              'Colosseum': ['Az_ókori_amfiteátrum_történelmi_jelentősége_magával_ragadó_volt.',
                            'Sétáltam_a_felső_szinteken_és_élveztem_a_kilátást.',
                            'Sokat_tanultam_a_gladiátorok_életéről_és_küzdelmeiről.'],

              'Spanyol_lépcsők': ['A_tér_sok_turistával_volt_zsúfolt,_de_mégis_nagyszerű_volt.',
                                  'A_lépcsőkön_ülve_élveztem_a_naplementét.',
                                  'A_művészek_alkotásait_nézve_idővel_elszállt_az_idő.'],

              'Pantheon': ['Az_ókori_templom_építészeti_csodája_lenyűgöző_volt.',
                           'A_kupola_alatt_való_sétálgatás_felemelő_érzés_volt.',
                           'A_híres_emberek_sírjait_megtekintve_sokat_tanultam_a_történelemről.'],

              'British_Múzeum': ['A_múzeum_hatalmas_és_elképesztő_mennyiségű_kiállítást_tartalmaz.',
                                 'A_múlt_kultúráinak_lenyomatai_lenyűgözőek_voltak.',
                                 'Sok_érdekességet_hallottam_a_múzeum_vezetett_túráján.'],

              'Londoni_Tower': ['A_vár_történelmi_jelentősége_magával_ragadó_volt.',
                                'A_Beefeater_csoport_vezetése_szórakoztató_és_informatív_volt.',
                                'A_koronázási_ékszerek_gyönyörűek_és_lenyűgözőek.'],

              'Westminster_Palota': ['A_parlament_épülete_impozáns_és_gyönyörű.',
                                     'A_Thames_folyó_partján_sétálva_élveztem_a_kilátást.',
                                     'A_Big_Ben_harangja_hatalmas_és_lenyűgöző.'],

              'Brandenburgi_Kapu': ['A_kapu_történelmi_szimbólumként_fontos_és_látványos.',
                                    'A_teret_körülölelő_oszlopok_lenyűgözőek_voltak.',
                                    'A_híres_helyen_sokféle_előadást_néztem_meg.'],

              'Reichstag': ['A_német_parlament_épülete_modern_és_impozáns.',
                            'A_tetején_található_kupolából_fantasztikus_a_kilátás.',
                            'Az_épület_történelmi_fontossága_érezhető_minden_szegletében.'],

              'Múzeumsziget': ['A_múzeumok_sokfélesége_lenyűgöző_volt.',
                               'A_műalkotások_között_eltöltött_idő_felejthetetlen_volt.',
                               'Sok_érdekességet_tanultam_a_művészetről_és_a_történelemről.'],

              'Sydney_Operaház': ['Az_Operaház_lenyűgöző_látvány_a_kikötőben.',
                                  'A_belső_térben_koncertet_hallgattam_és_élveztem_a_zenei_élményt.',
                                  'A_kilátás_a_tetejéről_fantasztikus_volt.'],

              'Bondi_Beach': ['A_tengerparti_hangulat_feledhetetlen_volt.',
                              'A_habokban_pancsolva_kikapcsolódtam_a_forró_napon.',
                              'A_szörfösök_ügyességét_figyelve_szórakoztam.'],

              'Taronga_Állatkert': ['A_sokféle_állat_megfigyelése_nagyszerű_élmény_volt.',
                                    'A_kilátás_a_kikötőre_fantasztikus.',
                                    'A_különböző_állatfajokról_sok_érdekes_információt_hallottam.'],

              'Ipanema_Beach': ['A_tengerpart_hangulata_és_a_zenélő_emberek_feledhetetlenek_voltak.',
                                'A_homokban_pihenve_élveztem_a_napfényt.',
                                'A_naplementét_nézve_felejthetetlen_pillanatokat_éltem_át.'],

              'Cristo_Redentor': ['A_szobor_hatalmas_és_lenyűgöző.',
                                  'A_városi_panoráma_a_magasból_gyönyörű_volt.',
                                  'Az_ég_felé_nyújtózó_karok_üzenete_nagyon_megható_volt.'],

              'Santa_Teresa_negyed': ['A_negyed_hangulatos_utcái_és_a_művészeti_szellemiség_lenyűgöző_volt.',
                                      'A_színes_házak_és_az_utcazenészek_sokszínűsége_felejthetetlen.',
                                      'A_fák_árnyékában_sétálva_sok_érdekességre_bukkantam.'],

              'Dubai_Mall': ['A_bevásárlóközpont_óriási_és_szinte_végtelen_lehetőségekkel.',
                             'A_szökőkutak_látványa_megkapó_volt.',
                             'Az_óriási_akvárium_lenyűgöző_és_izgalmas_volt.'],

              'Burj_Khalifa': ['A_torony_méretei_hihetetlenek_és_elképesztőek.',
                               'A_tetejéről_a_város_a_lábam_előtt_terült_el.',
                               'Az_emelkedés_a_lifttel_egy_különleges_élmény_volt.'],

              'Palm_Jumeirah': ['A_mesterséges_sziget_felemelő_látvány_volt.',
                                'A_tengerparton_pihenve_kikapcsolódtam.',
                                'A_luxusszálloda_kényelmes_szállást_biztosított.'],

              'Copacabana': ['A_tengerpart_hosszú_és_gyönyörű.',
                             'A_homokos_partszakasz_kényelmes_volt_a_napozáshoz.',
                             'A_strandbárban_élveztem_a_koktélokat_és_a_zenét.'],

              'Corcovado-hegy': ['Fantasztikus_kilátás_a_városra_és_a_tengerre.',
                                 'A_szobor_közelről_is_lenyűgöző_látvány_volt.',
                                 'A_hegyi_út_sok_szép_növényt_rejtett.'],

              'Tijuca_Nemzeti_Park': ['Sokféle_növény-_és_állatfajtával_találkoztam.',
                                      'A_vízesések_gyönyörűek_voltak_a_dzsungelben.',
                                      'A_túra_során_rengeteg_érdekességet_hallottam_a_parkról.']}


    helycolumn = 'id varos hely elmeny'

    with open(currentPath+'városok\\latogatok.txt', 'w', encoding = 'utf-8') as f:
        f.write(helycolumn+'\n')
        for i in range(random.randint(40, 100)):
            randomhely = random.choice(HelyNev)
            varos = helyVarosNev[HelyNev.index(randomhely)]
            randomelmeny = random.choice(Elmeny[randomhely])
            sor = f'{i} {varos} {randomhely} {randomelmeny}\n'

            f.write(sor)


def allatok_db():

    allat_columns = 'id faj nev kor'
    allatok = [
        "Bengáli_tigris", "Sarki_róka", "Koala", "Panda", "Tigris", "Lion",
        "Elefánt", "Fehér_cápa", "Polar_medve", "Szumátrai_orangután",
        "Zebra", "Narvál", "Levélállat", "Pengőke", "Denevér"
    ]

    allatok_neve = [
        "Simba", "Zara", "Baloo", "Luna", "Max", "Mia",
        "Charlie", "Bella", "Leo", "Lily", "Rocky", "Molly",
        "Oliver", "Lola", "Buddy"
    ]

    with open(currentPath + 'állatok\\allat.txt', 'w', encoding='utf-8') as f:
        f.write(allat_columns + '\n')
        for i in range(random.randint(50, 100)):
            randomfaj = random.choice(allatok)
            randomnev = random.choice(allatok_neve)
            sor = f'{i} {randomfaj} {randomnev} {random.randint(1, 20)}\n'

            f.write(sor)


szemelyek_db()
varosok_db()
allatok_db()
