import requests
from bs4 import BeautifulSoup
from dadata import Dadata

address = 'Москва ' + input('Введите ваше местоположение... ')
price = input('Максимальная сумма чека... ')

#тут, я думаю, можно, чтоб вводить все параметры, а можно иногда "пропуск"

#ниже я все переменные указываю, чтоб не запутаться, и словари тоже

names, addresses, metro = [],[],[]
req = 'https://msk.allcafe.ru/catalog/?query='

dic_Districts = {'академический':'akademicheskiy','алексеевский':'alekseevskiy','алтуфьевский':'altufevskiy','арбат':'arbat','аэропорт':'aeroport',
                 'бабушкинский':'babushkinskiy','басманный':'basmannyy','беговой':'begovoy','бескудниковский':'beskudnikovskiy','бибирево':'bibirevo',
                 'бирюлево восточное':'biryulevo-vostochnoe','бирблево западное':'biryulevo-zapadnoe','богородское':'bogorodskoe','братеево':'brateevo',
                 'бутырский':'butyrskiy','вешняки':'veshnyaki','войковский':'voykovskiy','восточное дегунино':'vostochnoe-degunino','восточное измайлово':'vostochnoe-izmaylovo',
                 'выхино':'vykhino','головинский':'golovinskiy','гагаринский':'gagarinskiy','Голяново':'golyanovo','даниловский':'danilovskiy','дмитровский':'dmitrovskiy',
                 'донской':'donskoy','дорогомилово':'dorogomilovo','загородный':'zagorodnyy','замоскворечье':'zamoskvoreche','западное дегунино':'zapadnoe-degunino',
                 'зюзино':'zyuzino','зябликово':'zyablikovo','ивановское':'ivanovskoe','измайлово':'izmaylovo','капотня':'kapotnya','китай-город':'kitay-gorod',
                 'коньково':'konkovo','коптево':'koptevo','косино-ухтомксий':'kosino-ukhtomskiy','котловка':'kotlovka','красносельский':'krasnoselskiy','крылатское':'krylatskoe',
                 'кузьминки':'kuzminki','кунцево':'kuntsevo','куркино':'kurkino','кутузовский':'kutuzovskiy','левобережный':'levoberezhnyy','левортово':'lefortovo',
                 'лианозово':'lianozovo','ломоносовский':'lomonosovskiy','лосиноостровский':'losinoostrovskiy','люблино':'lyublino','марфино':'marfino','марьина роща':'marina-roshcha',
                 'марьино':'marino','мещанский':'meshchanskiy','митино':'mitino','можайский':'mozhayskiy','молжаниновский':'molzhaninovskiy','москворечье - сабурово':'moskvoreche-saburovo',
                 'мосфильмовский':'mosfilmovskiy','нагатино - садовники':'nagatino-sadovniki','нагорный':'nagornyy','нижегородский':'nizhegorodskiy','ново-переделкино':'novo-peredelkino',
                 'новогиреево':'novogireevo','новокосино':'novokosino','новомосковский административный округ':'novomoskovskiy-administrativnyy-okrug','обручевский':'obruchevskiy',
                 'орехово-борисово северное':'orekhovo-borisovo-severnoe','орехово-борисово южное':'orekhovo-borisovo-yuzhnoe','останкинский':'ostankinskiy','отрадное':'otradnoe',
                 'очаково-матвеевское':'ochakovo-matveevskoe','перово':'perovo','печатники':'pechatniki','покровское-стрешнево':'pokrovskoe-streshnevo','преображенское':'preobrazhenskoe',
                 'пресненский':'presnenskiy','проспект вернадского':'prospekt-vernadskogo','раменки':'ramenki','ростокино':'rostokino','рязанский':'ryazanskiy','савеловский':'savelovskiy',
                 'свиблово':'sviblovo','северное бутово':'severnoe-butovo','северное измайлово':'severnoe-izmaylovo','северное медведково':'severnoe-medvedkovo',
                 'северное тушино':'severnoe-tushino','северный':'severnyy','симоновский':'simonovskiy','сокол':'sokol','соколиная гора':'sokolinaya-gora','сокольники':'sokolniki',
                 'солнцево':'solntsevo','строгино':'strogino','таганский':'taganskiy','тверской':'tverskoy','текстильники':'tekstilshchiki','теплый стан':'teplyy-stan',
                 'тимирязевский':'timiryazevskiy','тропарево-никулино':'troparevo-nikulino','филевский парк':'filevskiy-park','фили-давыдково':'fili-davydkovo','хамовники':'khamovniki',
                 'ховрино':'khovrino','хорошево-мневники':'khoroshevo-mnevniki','хорошевский':'khoroshevskiy','царицыно':'tsaritsyno','черемушки':'cheremushki',
                 'чертаново северное':'chertanovo-severnoe','чертаново центральное':'chertanovo-tsentralnoe','чертаново южное':'chertanovo-yuzhnoe','шереметьевский':'sheremetevskiy',
                 'щукино':'shchukino','южное бутово':'yuzhnoe-butovo','южное медведково':'yuzhnoe-medvedkovo','южное тушино':'yuzhnoe-tushino','южнопортовый':'yuzhnoportovyiy',
                 'южный порт':'yuzhnyy-port','якиманка':'yakimanka','ярославский':'yaroslavskiy','яснево':'yasenevo'}

dic_Metro = {'Авиамоторная':'aviamotornaya','Автозаводская':'avtozavodskaya','Академическая':'akademicheskaya','Александровский сад':'aleksandrovskiy-sad',
                 'Алексеевская':'alekseevskaya','Алтуфьево':'altufevo','Аннино':'annino','Арбатская':'arbatskaya','Аэропорт':'aeroport','Бабушкинская':'babushkinskaya',
                 'Багратионовская':'bagrationovskaya','Баррикадная':'barrikadnaya','Бауманская':'baumanskaya','Беговая':'begovaya','Белорусская':'belorusskaya','Беляево':'belyaevo',
                 'Бибирево':'bibirevo','Библиотека им. Ленина':'biblioteka-im-lenina','Битцевский парк':'bittsevskiy-park','Боровицкая':'borovitskaya','Ботанический сад':'botanicheskiy-sad',
                 'Братиславская':'bratislavskaya','Бульвар адмирала Ушакова':'bulvar-admirala-ushakova','Бульвар Дмитрия Донского':'bulvar-dmitriya-donskogo',
                 'Бульвар Рокоссовского':'bulvar-rokossovskogo','Бунинская аллея':'buninskaya-alleya','ВДНХ':'vdnkh','Варшавская':'varshavskaya','Верхние Котлы':'verhnie-kotlyi',
                 'Владыкино':'vladykino','Водный стадион':'vodnyy-stadion','Войковская':'voykovskaya','Волгоградский проспект':'volgogradskiy-prospekt','Волжская':'volzhskaya',
                 'Воробьевы горы':'vorobevy-gory','Выставочная':'vystavochnaya','Выхино':'vykhino','Деловой центр':'delovoy-tsentr','Динамо':'dinamo','Дмитровская':'dmitrovskaya',
                 'Добрынинская':'dobryninskaya','Домодедовская':'domodedovskaya','Дубровка':'dubrovka','Жулебино':'zhulebino','Измайловская':'izmaylovskaya','Калужская':'kaluzhskaya',
                 'Кантемировская':'kantemirovskaya','Каховская':'kakhovskaya','Каширская':'kashirskaya','Киевская':'kievskaya','Китай-город':'kitay-gorod','':'kozhukhovskaya',
                 'Коломенская':'kolomenskaya','Комсомольская':'komsomolskaya','Коньково':'konkovo','Котельники':'kotelniki','Красногвардейская':'krasnogvardeyskaya',
                 'Краснопресненская':'krasnopresnenskaya','Красносельская':'krasnoselskaya','Красные ворота':'krasnye-vorota','Крестьянская застава':'krestyanskaya-zastava',
                 'Кропоткинская':'kropotkinskaya','Крылатское':'krylatskoe','Крымская':'kryimskaya','Кузнецкий мост':'kuznetskiy-most','Кузьминки':'kuzminki','Кунцевская':'kuntsevskaya',
                 'Курская':'kurskaya','Кутузовская':'kutuzovskaya','Ленинский проспект':'leninskiy-prospekt','Лермонтовский проспект':'lermontovskiy-prospekt',
                 'Ломоносовский проспект':'lomonosovskiy-prospekt','Лубянка':'lubyanka','Люблино':'lyublino','Марксистская':'marksistskaya','Марьина роща':'marina-roshcha',
                 'Марьино':'marino','Маяковская':'mayakovskaya','Медведково':'medvedkovo','международная':'mezhdunarodnaya','менделеевская':'mendeleevskaya','митино':'mitino',
                 'молодежная':'molodezhnaya','мякино':'myakinino','нагатинская':'nagatinskaya','нагорная':'nagornaya','нахимовский проспект':'nakhimovskiy-prospekt',
                 'новогиреево':'novogireevo','новокузнецкая':'novokuznetskaya','новослободская':'novoslobodskaya','новокосино':'novokosino','новые черемушки':'novye-cheremushki',
                 'октябрьская':'oktyabrskaya','октябрьское поле':'oktyabrskoe-pole','орехово':'orekhovo','отрадное':'otradnoe','охотный ряд':'okhotnyy-ryad','павелецкая':'paveletskaya',
                 'парк культуры':'park-kultury','парк победы':'park-pobedy','партизанская - измайловский парк':'partizanskaya-izmaylovskiy-park','первомайская':'pervomayskaya',
                 'перово':'perovo','петровско-разумовская':'petrovsko-razumovskaya','печатники':'pechatniki','пионерская':'pionerskaya','планерная':'planernaya',
                 'площадь ильича':'ploshchad-ilicha','площадь революции':'ploshchad-revolyutsii','полежаевская':'polezhaevskaya','полянка':'polyanka','пражская':'prazhskaya',
                 'преображенская площадь':'preobrazhenskaya-ploshchad','пролетарская':'proletarskaya','проспект вернадского':'prospekt-vernadskogo','проспект мира':'prospekt-mira',
                 'профсоюзная':'profsoyuznaya','пушкинская':'pushkinskaya','раменка':'ramenka','речной вокзал':'rechnoy-vokzal','рижская':'rizhskaya','римская':'rimskaya',
                 'румянцево':'rumyantsevo','рязанский проспект':'ryazanskiy-prospekt','савеловская':'savelovskaya','саларево':'salarevo','свиблово':'sviblovo',
                 'севастопольская':'sevastopolskaya','семеновская':'semenovskaya','серпуховская':'serpukhovskaya','славянский бульвар':'slavyanskiy-bulvar','смоленская':'smolenskaya',
                 'сокол':'sokol','сокольники':'sokolniki','спортивная':'sportivnaya','сретенский бульвар':'sretenskiy-bulvar','строгино':'strogino','студенческая':'studencheskaya',
                 'сухаревская':'sukharevskaya','сходненская':'skhodnenskaya','таганское':'taganskaya','тверская':'tverskaya','театральная':'teatralnaya','текстильники':'tekstilshchiki',
                 'телецентр':'teletsentr','теплый стан':'teplyy-stan','технопарк':'tekhnopark','тимирязевская':'timiryazevskaya','тертьяковская':'tretyakovskaya','трубная':'trubnaya',
                 'тульская':'tulskaya','тургеневская':'turgenevskaya','тушинская':'tushinskaya','улица 1905 года':'ulitsa-1905-goda','улица академика королева':'ulitsa-akademika-koroleva',
                 'улица академика янгеля':'ulitsa-akademika-yangelya','улица горчакова':'ulitsa-gorchakova','улица милашенкова':'ulitsa-milashenkova','улица подбельского':'ulitsa-podbelskogo',
                 'улица сергея эйзенштейна':'ulitsa-sergeya-eyzenshteyna','улица скобелевская':'ulitsa-skobelevskaya','улица старокачаловская':'ulitsa-starokachalovskaya',
                 'университет':'universitet','филевский парк':'filevskiy-park','фили':'fili','фонвизинская':'fonvizinskaya','фрузнзенская':'frunzenskaya','ховрино':'hovrino',
                 'цска':'tsska','царицыно':'tsaritsyno','цветной бульвар':'tsvetnoy-bulvar','черкизовская':'cherkizovskaya','чертановская':'chertanovskaya','чеховская':'chekhovskaya',
                 'чистые пруды':'chistye-prudy','чкаловская':'chkalovskaya','шаболовская':'shabolovskaya','шалапиха':'shelepiha','шипиловская':'shipilovskaya',
                 'шоссе энтузиастов':'shosse-entuziastov','шелковская':'shchelkovskaya','щукинская':'shchukinskaya','электрозаводская':'elektrozavodskaya','юго-западная':'yugo-zapadnaya',
                 'южная':'yuzhnaya','ясенево':'yasenevo'}

dic_Cuisine = {'авторская':'avtorskaya','азиатская':'aziatskaya','американская':'amerikanskaya','вегетарианская':'vegetarianskaya','восточная':'vostochnaya',
                 'грузинская':'gruzinskaya','еврейская':'evreyskaya','европейская':'evropeyskaya','итальянская':'italyanskaya','кавказская':'kavkazskaya',
                 'китайская':'kitayskaya','корейская':'koreyskaya','немецкая':'nemetskaya','паназиатская':'panaziatskaya','русская':'russkaya',
                 'смешанная':'smeshannaya','средиземноморская':'sredizemnomorskaya','узбекская':'uzbekskaya','французская':'frantsuzskaya','японская':'yaponskaya'}

dic_Price = {400:'do-400-rub',1000:'ot-400-do-1000-rubley',2000:'ot-1000-do-2000-rubley',3000:'ot-2000-do-3000-rubley',3001:'bolshe-3000-rub'}


if address != 'пропуск' :
    dadata = Dadata('42e5e62148b540bbf9662f1ac4076443d64fa6b9','37b7e6a312147176befc5af1e3be6c783a5ec797')
#(это я себе) выдача идет в формате:
#city_district Басманный
#metro [{'distance': 0.9, 'line': 'Сокольническая', 'name': 'Комсомольская'}, {'distance': 0.9, 'line': 'Сокольническая', 'name': 'Красные ворота'}]
    address = dadata.clean('address', address)
    district = address['city_district'].strip().lowercase()
    for i in range (len(address['metro'])) :
        metro.append (address['metro'][i]['name'].strip().lowercase())
    req += '&district[]='+dic_Districts[district]
    for i in range (len(metro)) :
        req += '&metro[]='+dic_Metro[metro[i]]

if price != 'пропуск' :
    price = int(price)
    for k in dic_Price.keys() :
        if k <= price :
            req += '&bill[]='+dic_Price[k]

#(это я опять себе) адресную строку задавать в порядке district - metro - cuisine - bill
#print (req)

html = requests.get(req).text
soup = BeautifulSoup(html,'html.parser')
for name in soup.find_all('a', {'class':'placeList_name'}) :
    a = name.text.strip()
    if a in names :
        pass
    else :
        names.append (a)
#тут надо доработать, потому что такая тема будет раблотать, если все разные метса с разными адресами,
#а если в одном доме несколько или, например, сеть с несколькими точками - все развалится
for addr in soup.find_all('span', {'class':'placeList_addr'}) :
    a = addr.text.strip()
    if a in addresses :
        pass
    else :
        while '\n' in a :
            a = a.replace('\n','')
        addresses.append (a)
for i in range (len (names)) :
    print(names[i], '\n', addresses[i])
#ну, а вообще, он пока что выводит список, и я не знаю, что делать дальше