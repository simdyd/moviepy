use moviepy;

truncate table film_genere;

insert into film_genere (id,nome)
select id,nome from movie.movie_categorie; 

truncate table film_formati;

insert into film_formati (id,nome)
select id_formato,nome from movie.movie_formati;

truncate table film_movie;

insert into film_movie(id,titolo,titolo_originale,trama,recensione,studio,durata,anno,data_ins,data_mod,genere_id,formato_id,old_supporto)
select id,titolo,titolo_originale,trama,recensione,studio,durata,anno,data_ins,data_mod,categorie,id_formato,supporto
from movie.movie;

truncate table film_supporti;

truncate table film_foto_old;

insert into film_foto_old (film_id,nome_file,descrizione,peso,old_id)
select id_film,nome_file,descrizione,peso,id
from movie.movie_img;

truncate table film_persone_old;

insert into film_persone_old (film_id,text,professione)
select id,attori,'ATT'
from movie.movie;

insert into film_persone_old (film_id,text,professione)
select id,cast,'ATT'
from movie.movie;

insert into film_persone_old (film_id,text,professione)
select id,regia,'REG'
from movie.movie;

insert into film_persone_old (film_id,text,professione)
select id,sceneggiatura,'SCE'
from movie.movie;

insert into film_persone_old (film_id,text,professione)
select id,fotografia,'FOT'
from movie.movie;

insert into film_persone_old (film_id,text,professione)
select id,musica,'MUS'
from movie.movie;

insert into film_persone_old (film_id,text,professione)
select id,produttore,'PRO'
from movie.movie;

update film_persone_old set text=replace(text,char(13,10),',');
update film_persone_old set text=replace(text,char(13),',');
update film_persone_old set text=replace(text,char(10),',');

truncate table persone_persona;
truncate table persone_persona_professione;