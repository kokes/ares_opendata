drop table if exists firmy;
drop table if exists posoby;
drop table if exists fosoby;

create table firmy (
	aktualizace_db date,
	datum_vypisu date,
	cas_vypisu time,
	typ_vypisu varchar,
	rejstrik varchar,
	ico int32,
	obchodni_firma varchar collate nocase,
	datum_zapisu date,
	datum_vymazu date,
	sidlo varchar
);

create table posoby (
	ico int32,
	nazev_organu varchar,
	datum_zapisu date,
	datum_vymazu date,
	nazev_funkce varchar,
	obchodni_firma varchar,
	ico_organu int32,
	adresa varchar
);

create table fosoby (
	ico int32,
	nazev_organu varchar,
	datum_zapisu date,
	datum_vymazu date,
	nazev_funkce varchar,
	jmeno varchar,
	prijmeni varchar,
	titul_pred varchar,
	titul_za varchar,
	adresa varchar,
	bydliste varchar
);
