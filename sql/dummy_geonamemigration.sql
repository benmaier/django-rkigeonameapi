-- countryinfo has to be inserted first because geonames references it
SET @@local.net_read_timeout = 3600;
SET @@local.net_write_timeout = 3600;

INSERT IGNORE INTO your_db_name.continentCodes(
    code,
    englishname,
    geonameid
) SELECT
    code,
    name,
    geonameid
FROM
    geonames.continentCodes;


-- insert countryinfo data without proper geonameid (update after geoname insert)
INSERT IGNORE INTO your_db_name.countryinfo(
     iso_alpha2
    ,iso_alpha3
    ,iso_numeric
    ,fips_code
    ,englishname
    ,capital
    ,areainsqkm
    ,population
    ,continent
    ,tld
    ,currency
    ,currencyName
    ,Phone
    ,postalCodeFormat
    ,postalCodeRegex
    ,geonameId
    ,languages
    ,neighbours
    ,equivalentFipsCode
) SELECT
     iso_alpha2
    ,iso_alpha3
    ,iso_numeric
    ,fips_code
    ,name
    ,capital
    ,areainsqkm
    ,population
    ,continent
    ,tld
    ,currency
    ,currencyName
    ,Phone
    ,postalCodeFormat
    ,postalCodeRegex
    ,geonameId
    ,languages
    ,neighbours
    ,equivalentFipsCode
FROM 
    geonames.countryinfo;


INSERT IGNORE INTO your_db_name.featureCodes(code, name, description) SELECT code, name, description FROM geonames.featureCodes;
INSERT IGNORE INTO your_db_name.featureCodes(code, name, description) VALUES ('GL', 'Global', 'contains every place on earth.');

-- remove the unnecessary class code in the table
UPDATE your_db_name.featureCodes SET code = SUBSTR(code,3) WHERE SUBSTR(code,2,1) = '.';

START TRANSACTION;
USE `your_db_name`;
UPDATE featureCodes SET searchorder_detail = 21  WHERE code = 'GL';
UPDATE featureCodes SET searchorder_detail = 20  WHERE code = 'CONT' ;
UPDATE featureCodes SET searchorder_detail = 19  WHERE code = 'RGN' ;
UPDATE featureCodes SET searchorder_detail = 18  WHERE code = 'PCLI';
UPDATE featureCodes SET searchorder_detail = 17  WHERE code = 'PPLC';
UPDATE featureCodes SET searchorder_detail = 16.5  WHERE code = 'PPL' ;
UPDATE featureCodes SET searchorder_detail = 16  WHERE code = 'PPLA';
UPDATE featureCodes SET searchorder_detail = 14  WHERE code = 'TERR';
UPDATE featureCodes SET searchorder_detail = 13  WHERE code = 'PCLX';
UPDATE featureCodes SET searchorder_detail = 12  WHERE code = 'PCLD';
UPDATE featureCodes SET searchorder_detail = 11  WHERE code = 'ADM1';
UPDATE featureCodes SET searchorder_detail = 10  WHERE code = 'ADM2';
UPDATE featureCodes SET searchorder_detail = 9  WHERE code = 'ADM3';
UPDATE featureCodes SET searchorder_detail = 8  WHERE code = 'ADM4';
UPDATE featureCodes SET searchorder_detail = 7  WHERE code = 'ADM5';
UPDATE featureCodes SET searchorder_detail = 6  WHERE code = 'ADM5';
UPDATE featureCodes SET searchorder_detail = 5  WHERE code = 'PPLX';
COMMIT;

-- explicitly name all columns because django orders them in a weird way
INSERT IGNORE INTO your_db_name.geoname(
    geonameid
    ,englishname
    ,asciiname
    ,latitude
    ,longitude
    ,fclass 
    ,cc2
    ,admin1 
    ,admin2 
    ,admin3 
    ,admin4 
    ,population
    ,elevation
    ,gtopo30 
    ,timezone 
    ,moddate 
    ,fcode
    ,country
) SELECT 
    geonameid
    ,name
    ,asciiname
    ,latitude
    ,longitude
    ,fclass 
    ,cc2
    ,admin1 
    ,admin2 
    ,admin3 
    ,admin4 
    ,population
    ,elevation
    ,gtopo30 
    ,timezone 
    ,moddate 
    ,fcode
    ,country
FROM 
    geonames.geoname
WHERE
    geonames.geoname.country <> '';

INSERT IGNORE INTO your_db_name.geoname(
    geonameid
    ,englishname
    ,asciiname
    ,latitude
    ,longitude
    ,fclass 
    ,cc2
    ,admin1 
    ,admin2 
    ,admin3 
    ,admin4 
    ,population
    ,elevation
    ,gtopo30 
    ,timezone 
    ,moddate 
    ,fcode
) SELECT 
    geonameid
    ,name
    ,asciiname
    ,latitude
    ,longitude
    ,fclass 
    ,cc2
    ,admin1 
    ,admin2 
    ,admin3 
    ,admin4 
    ,population
    ,elevation
    ,gtopo30 
    ,timezone 
    ,moddate 
    ,fcode
FROM 
    geonames.geoname
WHERE
    geonames.geoname.country = '';

-- copy alternatename

INSERT IGNORE INTO your_db_name.alternatename(
 alternatenameid
 ,isolanguage
 ,alternatename
 ,ispreferredname
 ,isshortname
 ,iscolloquial
 ,ishistoric
 ,geonameid
) SELECT 
 alternatenameid
 ,isolanguage
 ,alternatename
 ,ispreferredname
 ,isshortname
 ,iscolloquial
 ,ishistoric
 ,geonameid
FROM geonames.alternatename;

-- copy hierachy

INSERT IGNORE INTO your_db_name.hierarchy(
     parentId
   , childId
   , is_custom_entry
) SELECT DISTINCT
     parentId
   , childId
   , 0
FROM geonames.hierarchy;


-- RENAME DRC
INSERT INTO your_db_name.alternatename(alternatenameId) VALUES (11092987) ON DUPLICATE KEY UPDATE alternateName = 'Kongo (DRC)';

-- DEFINE REGIONS

INSERT INTO region(
      region_id
    , name
    , englishname
    , fcode
    , geonameid
)
SELECT DISTINCT
	  pkey
    , IF(alt2.alternateName IS NOT NULL, alt2.alternateName, pname) AS aname
    , pname
    , pfcode
    , pgid
FROM
(   SELECT
              parent.geonameid as pgid
            , parent.name as pname
            , concat(replace(lower(parent.name)," ","-"),"-",parent.geonameid) as pkey
            , parent.fcode as pfcode
            , child.geonameid as cgid
            , child.name as cname
            , child.country as ccountry
            , child.fcode as cfcode
    FROM
            geonames.hierarchy
    JOIN
            geonames.geoname AS parent
        ON parent.geonameid = geonames.hierarchy.parentid
    JOIN
            geonames.geoname AS child
        ON child.geonameid = geonames.hierarchy.childid

    WHERE
            child.fcode IN ('PCLI','TERR','PCLD','PCLX')
        AND parent.fcode IN ('CONT', 'RGN')
        AND child.fcode != parent.fcode
        AND child.country != ''
    ORDER BY
          parent.name
        , child.name
) as regions
LEFT JOIN
    ( SELECT
		*
	  FROM
            geonames.alternatename as alt
	  WHERE
			alt.isoLanguage = 'de'
	) as alt2
ON pgid = alt2.geonameid
;

-- POPULATE REGION MANY TO MANY

INSERT INTO your_db_name.region_laender(region_id, countryinfo_id)
SELECT DISTINCT pkey, ccountry FROM
(	SELECT
			  parent.geonameid as pgid
			, parent.name as pname
            , reg.id as pkey
            , parent.fcode as pfcode
            , child.geonameid as cgid
            , child.name as cname
            , child.country as ccountry
            , child.fcode as cfcode
	FROM
			geonames.hierarchy
	JOIN
			geonames.geoname AS parent
		ON parent.geonameid = geonames.hierarchy.parentid
	JOIN
			geonames.geoname AS child
	    ON child.geonameid = geonames.hierarchy.childid
    JOIN
            your_db_name.region as reg
        ON concat(replace(lower(parent.name) COLLATE utf8mb4_unicode_ci," ","-"),"-",parent.geonameid) = reg.region_id
	WHERE
			child.fcode IN ('RGN','PCLI','TERR','PCLD','PCLX')
        AND parent.fcode IN ('CONT', 'RGN')
        AND child.fcode != parent.fcode
        AND child.country != ''
	ORDER BY
		  parent.name
		, child.name
) as regions;

-- ADD GERMAN NAMES TO CONTINENTCODES, COUNTRYINFO, AND GEONAMES (Prefer short names) 

INSERT INTO
    your_db_name.continentCodes(
          code
        , name
    )
SELECT
    cont.code,
    alt1.alternateName as altname
FROM
    your_db_name.continentCodes AS cont
JOIN
    your_db_name.alternatename as alt1
ON
    alt1.geonameid = cont.geonameid
AND
    alt1.alternatenameId = (
        SELECT alternatenameId FROM
            your_db_name.alternatename as alt2
        Where
            cont.geonameid = alt2.geonameid
            AND isoLanguage = 'de'
        ORDER BY
                alt2.isShortName DESC
              , alt2.isPreferredName DESC
        LIMIT 1
    )
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO
    your_db_name.countryinfo(
          iso_alpha2
        , name
    )
SELECT
    country.iso_alpha2,
    alt1.alternateName as altname
FROM
    your_db_name.countryinfo AS country
JOIN
    your_db_name.alternatename as alt1
ON
    alt1.geonameid = country.geonameid
AND
    alt1.alternatenameId = (
        SELECT alternatenameId FROM
            your_db_name.alternatename as alt2
        Where
            country.geonameid = alt2.geonameid
            AND isoLanguage = 'de'
        ORDER BY
                alt2.isShortName DESC
              , alt2.isPreferredName DESC
        LIMIT 1
    )
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO
    your_db_name.countryinfo(
          iso_alpha2
        , name
    )
SELECT
          iso_alpha2
        , englishname
FROM
    your_db_name.countryinfo as c
WHERE
    c.name IS NULL
ON DUPLICATE KEY UPDATE name = VALUES(name)
    ;

INSERT INTO
    your_db_name.geoname(
          geonameid
        , name
    )
SELECT
    gname.geonameid,
    alt1.alternateName as altname
FROM
    your_db_name.geoname AS gname
JOIN
    your_db_name.alternatename as alt1
ON
    alt1.geonameid = gname.geonameid
AND
    alt1.alternatenameId = (
        SELECT alternatenameId FROM
            your_db_name.alternatename as alt2
        Where
            gname.geonameid = alt2.geonameid
            AND isoLanguage = 'de'
        ORDER BY
                alt2.isShortName DESC
              , alt2.isPreferredName DESC
        LIMIT 1
    )
ON DUPLICATE KEY UPDATE name = VALUES(name);
    ;


INSERT INTO
    your_db_name.geoname(
          geonameid
        , name
    )
SELECT
          geonameid
        , englishname
FROM
    your_db_name.geoname AS g
WHERE
    g.name IS NULL
ON DUPLICATE KEY UPDATE name = VALUES(name)
    ;

-- ADD EVERY COUNTRY AS A REGION FOR ITS OWN AND ADD "GLOBAL" AS A REGION

INSERT INTO your_db_name.region(
      region_id
    , name
    , fcode
    , englishname
)
VALUES (
    'global', 'Weltweit', 'GL', 'Global'
);

INSERT INTO your_db_name.region(
      region_id
    , name
    , englishname
    , fcode
    , geonameid
)
SELECT
      pkey
    , name
    , englishname
    , fcode
    , geonameid
FROM 
( SELECT
      concat(replace(lower(c.iso_alpha2)," ","-"),"-",c.geonameid) as pkey
    , c.name as name
    , c.englishname as englishname
    , g.fcode as fcode
    , g.geonameid as geonameid
 FROM 
    your_db_name.countryinfo as c
 LEFT JOIN
    your_db_name.geoname as g
 ON
    g.geonameid = c.geonameid
) as country;

INSERT INTO your_db_name.region_laender(region_id, countryinfo_id)
SELECT (SELECT id FROM your_db_name.region where region_id='global' LIMIT 1), iso_alpha2 FROM your_db_name.countryinfo ;

INSERT INTO your_db_name.region_laender(region_id, countryinfo_id)
SELECT 
     reg.id
   , iso_alpha2
  FROM
     your_db_name.countryinfo as country
  JOIN
     your_db_name.region as reg
  ON
     concat(replace(lower(country.iso_alpha2) COLLATE utf8mb4_unicode_ci," ","-"),"-",country.geonameid) = reg.region_id
;


