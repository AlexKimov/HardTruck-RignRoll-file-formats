# О проекте

Описание бинарных форматов игр  **Дальнобойщики 1**, **Дальнобойщики 2** (версия 8) и **Дальнобойщики 3**. Для каждого формата доступен (в процессе) шаблон шестнадцатиричного редактора **010 Editor**, который описывает структуры формата, а также есть дополнительные скрипты для работы с форматами. 

Текущий прогресс по исследованию структуры форматов [Projects/Formats](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/projects/1). Описание форматов [Вики страница](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki).

| b3D | MSK | PLM | RMP | TXR | RES | TECH | RAW | WAY | WMD |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | 
| >50% | 100% | 100% | >95% | 100% | 100% | >85% | 100% | 100% | 5% |

####  Дополнительные ссылки
[Группа ВК](https://vk.com/rnr_mods)

#### Текущие планы

###### Дальнобойщики 1/2
1. [Формат b3D](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/2)

2. Импорт/экспорт форматов.

3. Документации на форматы.

## Ответы на частые вопросы (FAQ)

    1. Где скачать плагины для карты, моделей и т.п. Дальнобойщиков 1/2?

Здесь https://github.com/aleko2144/Hard-Truck-1-2-Blender-plugins

    2. Где скачать плагины для карты, моделей и т.п. Дальнобойщиков 3?
    
Здесь https://github.com/aleko2144/RigNRoll-Blender-plugins

    3. Какие есть еще проекты по Дальнобойщикам?
    
Дальнобойщики 2 + редактор локаций на движке Unity https://github.com/Duude92/KOTRunity. 

Direct3D-враппер для запуска на современных системах https://github.com/REDPOWAR/D2GI

Расширение возможностей игры https://github.com/aleko2144/SEMod_AsiPlugin

Программа для работы с b3d файлами Дальнобойщики 1/2 https://github.com/Duude92/B3DBlockEditor

    4. Как пользоваться скриптами и плагинами?
    
Ищите в группе ВК. Ссылка выше.

    5. Где скачать игру Дальнобойщики 2? Не запускаются Дальнобойщики 2.
Игра на gog.com https://www.gog.com/game/hard_truck_2_king_of_the_road

## Форматы файлов

Описание форматов файлов сделано в виде шаблонов для программы **010Editor**. Шаблоны в формате .bt хранят структуры в стиле языка C, если открыть файл в 010Editor и применить шаблон, то программа отобразит дерево структур файла, в котором удобно изменять значения хранимых переменных и совершать другие манипуляции.

#### Дальнобойщики 1 (1998)

| № | Формат | Прогресс  | Шаблон (010 Editor) | Описание | О формате |
| :-- | :------- | :-- | :-- | :-- | :-- |
|  **1**  |  .b3D**  |   [b3D](https://github.com/AlexKimov/HT2-RnR-tools/issues/2)  | [b3D.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/B3D.bt) | [Wiki](https://github.com/AlexKimov/HT2-RnR-tools/wiki/b3D-File-Format-Rus) | 3D объекты и объекты игровой логики (модели коллизий, порталы, объекты освещения и т.п.) |
|  **2**  | .MSK | [MSK](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/1) |  [MSK.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/MSK.bt) | [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/MSK-File-Format-Rus)  | 8 битные файлы масок, хранятся в архиве .RMP | 
|  **3**  | .PLM | [PLM](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/7) |  [PLM.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/PLM.bt) |  [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/PLM-File-Format-Rus) | Палитра и что-то еще, хранятся в архиве .RMP | 
|  **4**  | .RMP* | [RMP](https://github.com/AlexKimov/HT2-RnR-tools/issues/3) |  [RES.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/RES.bt) | [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/RES-RMP-File-Format-RUS)  | Архив ресурсов (звуки, текстуры) | 
| **5**  | .TXR | [TXR](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/6) |  [TXR.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/TXR.bt) | [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/TXR-File-Format-RUS)  | Текстура | 

    * Формат аналогичен формату RES из второй части игры (Дальнобойщики 2)
    ** Формат аналогичен формату b3D из второй части игры (Дальнобойщики 2), ну или наоборот

#### Дальнобойщики 2 (версия 8)

| № | Формат | Прогресс  | Шаблон (010 Editor) | Описание | О формате |
| :-- | :------- | :-- | :-- | :-- | :-- |
|  **1**  |  .b3D  |   [b3D](https://github.com/AlexKimov/HT2-RnR-tools/issues/2)  | [b3D.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/B3D.bt) | [Wiki](https://github.com/AlexKimov/HT2-RnR-tools/wiki/b3D-File-Format-Rus) | 3D объекты и объекты игровой логики (модели коллизий, порталы, объекты освещения и т.п.) |
|  **2**  | .MSK | [MSK](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/1) |  [MSK.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/MSK.bt) | [Вики](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/MSK-File-Format-Rus)  | 8/16 битные файлы масок, хранятся в архиве .RES | 
|  **3**  | .PLM | [PLM](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/7) |  [PLM.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/PLM.bt) |  [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/PLM-File-Format-Rus) | Палитра, хранится в архиве .RES | 
|  **4**  | .RAW | [RAW](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/8) |  | [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/RAW-File-Format-RUS)  |  Карты высот | 
|  **5**  | .RES | [RES](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/3) |  [RES.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/RES.bt) | [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/RES-RMP-File-Format-RUS)  | Архив ресурсов (звуки, текстуры) | 
|  **6**  | .TECH | [TECH](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/9) |  [TECH.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/TECH.bt) |   | Параметры транспортных средств | 
|  **7**  | .TXR | [TXR](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/6)  |  [TXR.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/TXR.bt) |   [WIKI](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/wiki/TXR-File-Format-RUS) | Текстура | 
|  **8**  | .WAY | [WAY](https://github.com/AlexKimov/HT2-RnR-tools/issues/4)  | [WAY.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/WAY.bt) |  | Пути для транспорта под управлением ИИ | 

#### Дальнобойщики 3
| № | Формат | Прогресс  | Шаблон |  Описание   |
| :-- | :------- | :-- | :-- | :-- |
|  **1**  |  .WMD  |     | [WMD.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/WDB.bt) | 3D объекты и объекты игровой логики (модели коллизий, порталы, объекты освещения и т.п.) |

## Скрипты

#### 3dsMax
* [raw_to_level_surface.ms]() - скрипт создания поверхности уровня из игры Дальнобойщики 2 на основе файлов **.raw**;
* [raw_export.ms]() - скрипт экспорта в формат **.raw** игры Дальнобойщики 2;
* [raw_import.ms]() - скрипт для импорта данных карты высот **.raw** игры Дальнобойщики 2;
* [material_to_txr_msk.ms]() - скрипт для создания материала из файлов формата **.txr** и **.msk** игры Дальнобойщики 1/2;

#### 010 Editor
* [UnpackResource.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/UnpackResource.1sc) - скрипт для распаковки файлов из игровых ресурсов (**.RES/.RMP**) 
* [mskConversion.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/mskConversion.1sc) - скрипт для конвертирования файлов масок **.msk** игры **Дальнобойщики 1/2** в формат **.tga** или **.bmp**. 
* [PLMtoTGA.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/PLMtoTGA.1sc) - скрипт для конвертирования **.plm** файлов игры Дальнобойщики 1 в формат **.tga**. 
* [TXRtoBMP.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/TXRtoBMP.1sc) - скрипт для конвертирования **.txr** файлов игры **Дальнобойщики 2** в формат **.bmp**. 
* [RawToBMP.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/RawToBMP.1sc) - скрипт конвертирует **.RAW** (карта высот) файл в 8 битное изображение (оттенки серого) в формате **bmp**.
* [RawToObj.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/RawToObj.1sc) - скрипт конвертирует **.RAW** (карта высот) файл в **.obj**.
* [decodeSCH.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/decodeSCH.1sc) - скрипт для расшифровки зашифрованных **SCH** и **CNF** файлов.
* [KeyGenerator.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/KeyGenerator.1sc) - скрипт для генерации файла ключа для расшифровки **SCH** файлов.
* [b3dToobj.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/b3dToobj.1sc) - скрипт для конвертирования **B3D** файлов в набор файлов формата **.obj** (в работе).
* [TechToTCH.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/TechToTCH.1sc) - скрипт конвертирования данных из vehicle.tech в исходную текстовую форму.
* [REStoPRO.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/REStoPRO.1sc) - скрипт конвертирования файлов ресурсов **.res** в **.pro**.

#### Noesis
* [fmt_ht_txr_msk.py](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/noesis/fmt_ht_txr_msk.py) - скрипт для открытия и сохранения **.txr** и **.msk** файлов
* [fmt_ht_rmp_res.py](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/noesis/fmt_ht_rmp_res.py) - скрипт для распковки **.res** и **.rmp** архивов
* [fmt_ht_raw.py](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/noesis/fmt_ht_raw.py) - скрипт для просмотра .raw файлов (карта высот)

## Спасибо
Юрий Гладышенко

* * * 
# About
Hard Truck 1 (1998), Hard Truck 2 King of the Road 1.3 and RignRoll (2010) games file formats. Current progress status [see Issues](https://github.com/AlexKimov/HT2-RnR-tools/issues). 

Formats description will be [there (Wiki)](https://github.com/AlexKimov/HT2-RnR-tools/wiki).

#### Roadmap

###### Hard Truck 1/2
1. **b3D** format, evereything else is ready to use (almost).

2. Formats documentation in english.

3. Conversion to other formats.

#### Hard Truck 1 (1998)

| № | Format/Ext | Progress   | Template (010 Editor) |  Description   |
| :-- | :------- | :-- | :-- | :-- | 
|  **1**  |  .b3D**  |   [b3D](https://github.com/AlexKimov/HT2-RnR-tools/issues/2)  | [b3D.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/B3D.bt) | Game logic and 3D objects |
|  **2**  | .RMP* | [RMP](https://github.com/AlexKimov/HT2-RnR-tools/issues/3) |  [RES.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/RES.bt) | Resource archive: sounds, textures | 
|  **3**  | .PLM | [PLM](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/7) | [PLM.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/PLM.bt) |   Palette | 
|  **4**  | .MSK | [MSK](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/1)  |  [MSK.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/MSK.bt) |    Texture Masks, 8-bit with palette | 
|  **5**  | .TXR | [TXR](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/6) |  [TXR.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/TXR.bt) |    Texture file |

    *  almost the same as RES format from Hard Truck 2
    **  b3D format from Hard Truck 2 has the same structure, but there are some differences

#### Hard Truck 2 King of the Road (2002)
| № | Format/Ext | Progress   | Template (010 Editor) |  Description   |
| :-- | :------- | :-- | :-- | :-- |
|  **1**  | .b3D |   [b3D](https://github.com/AlexKimov/HT2-RnR-tools/issues/2)  | [b3D.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/B3D.bt) | Game logic and 3D objects |
|  **2**  | .MSK | [MSK](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/1) |  [MSK.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/MSK.bt) |    Mask files stored in .RES | 
|  **3**  | .PLM | [PLM](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/7) |  [PLM.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/PLM.bt) |    Palette file in .RES | 
|  **4**  | .RAW | [RAW](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/8) |   [RAW.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/RAW.bt) |  Heightmaps | 
|  **5**  | .RES | [RES](https://github.com/AlexKimov/HT2-RnR-tools/issues/3)   | [RES.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/RES.bt) | Resource archive: sounds, textures | 
|  **6**  | .TECH | [TECH](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/9)  |  [TECH.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/TECH.bt) |   Vehicle params | 
|  **7**  | .TXR | [TXR](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/issues/6) |  [TXR.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/TXR.bt) |   Texture file |
|  **8**  | .WAY | [WAY](https://github.com/AlexKimov/HT2-RnR-tools/issues/4)   | [WAY.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/WAY.bt) | AI waypoints | 

#### RignRoll (2010)
| № | Format/Ext | Progress   | Template (010 Editor) |  Description   |
| :-- | :------- | :-- | :-- | :-- |
|  **1**  |  .WMD  |   WIP  | [WMD.bt](https://github.com/AlexKimov/HT2-modding-tools/blob/master/formats/templates/WDB.bt) | Game logic and 3D objects |

### Scripts

#### 010Editor
* [UnpackResource.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/UnpackResource.1sc) - unpack files from (**.RES/.RMP**) game archives (010 Editor)
* [mskConversion.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/mskConversion.1sc) - **.msk** to **.tga** conversion script (010 Editor) 
* [PLMtoTGA.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/PLMtoTGA.1sc) - **.plm** to **.tga** conversion script (010 Editor) 
* [TXRtoBMP.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/TXRtoBMP.1sc) - **.txr* to **.bmp* conversion script (010 Editor) 
* [RawToBMP.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/RawToBMP.1sc) - **.raw* (HeightMap) to **.bmp** conversion script (010 Editor) 
* [RawToObj.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/RawToObj.1sc) -  **.raw* (HeightMap) to **.obj* conversion script (010 Editor) 
* [decodeSCH.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/decodeSCH.1sc) - decode encrypted **SCH** and **CNF** files, about key file see below.
* [KeyGenerator.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/KeyGenerator.1sc) - key file generation script.
* [b3dToobj.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/b3dToobj.1sc) - convert **B3D** file to set of **.obj** files (WIP).
* [TechToTCH.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/TechToTCH.1sc) - convert data from vehicle.tech to source text data.
* [REStoPRO.1sc](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/010editor/REStoPRO.1sc) - **.res** files to **.pro** format.

#### Noesis
* [fmt_ht_txr_msk.py](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/noesis/fmt_ht_txr_msk.py) - open, save (wip) **.txr**, **.msk** files 
* [fmt_ht_rmp_res.py](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/noesis/fmt_ht_rmp_res.py) - unpack **.res** and **.rmp**
* [fmt_ht_raw.py](https://github.com/AlexKimov/HardTruck-RignRoll-file-formats/blob/master/scripts/noesis/fmt_ht_raw.py) - script to view .raw (heightmaps)
